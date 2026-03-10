# src/gpt_analyzer.py - Fixed version with improved CVE, Target, and Attack extraction
import json
import os
import re
import requests
from collections import Counter
import time
from dotenv import load_dotenv
load_dotenv()

class GPTThreatAnalyzer:
    def __init__(self, mode='pattern'):
        self.mode = mode
        os.makedirs('data/processed', exist_ok=True)
        
        print("\n" + "="*70)
        print("🤖 INITIALIZING THREAT ANALYZER")
        print("="*70 + "\n")
        
        if mode == 'ollama':
            self._init_ollama()
        elif mode == 'openai':
            self._init_openai()
        else:
            print("🆓 Using PATTERN MATCHING mode")
            print("   Fast and reliable, no dependencies needed\n")
    
    def _init_ollama(self):
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    print(f"✅ Ollama connected! Available models: {len(models)}")
                    print(f"   Using model: llama3.2\n")
                    self.ollama_available = True
                else:
                    print("⚠️  Ollama running but no models found")
                    print("   Run: ollama pull llama3.2")
                    print("   Falling back to pattern matching\n")
                    self.ollama_available = False
                    self.mode = 'pattern'
            else:
                raise Exception("Connection failed")
        except Exception as e:
            print(f"⚠️  Ollama not available: {str(e)[:50]}")
            print("   Falling back to pattern matching\n")
            self.ollama_available = False
            self.mode = 'pattern'
    
    def _init_openai(self):
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("No API key found")
            self.openai_client = OpenAI(api_key=api_key)
            print("✅ OpenAI API initialized\n")
        except Exception as e:
            print(f"⚠️  OpenAI not available: {e}")
            print("   Falling back to pattern matching\n")
            self.mode = 'pattern'

    # ── CVE helpers ──────────────────────────────────────────────────────────

    def _extract_cve_best(self, text, title='', entities=None):
        """
        Priority-order CVE extraction:
        1. preprocessor entities.cves  (already validated)
        2. regex on article text
        3. regex on title
        """
        if entities and entities.get('cves'):
            return entities['cves'][0].upper()
        match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
        if match:
            return match.group(0).upper()
        if title:
            match = re.search(r'CVE-\d{4}-\d{4,7}', title, re.IGNORECASE)
            if match:
                return match.group(0).upper()
        return 'N/A'

    def _patch_cve(self, threat_intel, incident):
        """After LLM analysis, replace N/A vulnerability with real CVE if found."""
        current = threat_intel.get('vulnerability', 'N/A')
        if current and current != 'N/A' and 'CVE-' in current.upper():
            return threat_intel
        entities = incident.get('entities', {})
        text     = incident.get('cleaned_text', incident.get('text', ''))
        title    = incident.get('title', '')
        threat_intel['vulnerability'] = self._extract_cve_best(text, title, entities)
        return threat_intel

    # ── LLM methods ──────────────────────────────────────────────────────────

    def extract_with_ollama(self, text, title):
        prompt = f"""You are a cybersecurity analyst. Analyze this incident and respond with ONLY these 5 fields, one per line, no extra text:

ATTACK_TYPE: one of [Ransomware Attack, Phishing Campaign, DDoS Attack, Malware Distribution, Zero-Day Exploit, Vulnerability Exploit, Data Breach, APT Campaign, Credential Theft, Supply Chain Attack, Security Incident]
SEVERITY: one of [critical, high, medium, low]
TARGET: one specific sector name like [Technology, Finance, Healthcare, Government, Education, Energy, Retail, Telecom, Enterprise, Developers, End Users]
VULNERABILITY: exact CVE ID like CVE-2024-1234 if mentioned in text, otherwise N/A
IMPACT: one sentence description

Incident Title: {title}
Article Text: {text[:800]}

Rules:
- TARGET must be a single clean sector name, NOT phrases like "affected sector: X"
- VULNERABILITY must be an exact CVE-YYYY-NNNNN from the text only, not guessed
- Reply with ONLY the 5 fields above"""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2',
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': 0.1, 'num_predict': 120}
                },
                timeout=90  # FIX: increased from 45 to 90 seconds
            )
            if response.status_code == 200:
                result = response.json().get('response', '')
                return self._parse_llm_response(result, text, title)
        except requests.exceptions.Timeout:
            print(f"    ⚠️  Ollama timeout")
        except Exception as e:
            print(f"    ⚠️  Ollama error: {str(e)[:40]}")
        return None
    
    def extract_with_openai(self, text, title):
        prompt = f"""Analyze this cybersecurity incident. Extract:
ATTACK_TYPE: [value]
SEVERITY: [critical/high/medium/low]
TARGET: [value]
VULNERABILITY: [CVE number or N/A]
IMPACT: [value]

Title: {title}
Text: {text[:1500]}"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity threat analyst."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            result = response.choices[0].message.content
            return self._parse_llm_response(result, text, title)
        except Exception as e:
            print(f"    ⚠️  OpenAI error: {str(e)[:40]}")
        return None
    
    def _clean_llm_target(self, raw_target):
        """Strip LLM noise like 'affected sector: X' and normalize to clean sector name."""
        if not raw_target:
            return None
        t = raw_target.strip()
        # Strip common LLM prefixes
        t = re.sub(r'^(affected\s+sector[s]?[:\/]?\s*|sector[:\/]?\s*|industry[:\/]?\s*|target[:\/]?\s*)', '', t, flags=re.IGNORECASE).strip()
        # Strip brackets
        t = re.sub(r'[\[\]()]', '', t).strip()
        # If multiple sectors joined by / or , take the first meaningful one
        parts = re.split(r'[\/,]', t)
        t = parts[0].strip().title()
        # Map common LLM outputs to clean labels
        mapping = {
            'Finance':        ['finance', 'financial', 'banking', 'fintech', 'bank'],
            'Technology':     ['technology', 'tech', 'software', 'cloud', 'it '],
            'Healthcare':     ['healthcare', 'health', 'medical', 'hospital'],
            'Government':     ['government', 'federal', 'public sector', 'gov'],
            'Enterprise':     ['enterprise', 'corporate', 'business', 'industry', 'organization'],
            'Developers':     ['developer', 'developers', 'open source', 'github'],
            'Education':      ['education', 'university', 'school', 'academic'],
            'Energy':         ['energy', 'power', 'utility', 'oil', 'gas'],
            'Retail':         ['retail', 'e-commerce', 'ecommerce'],
            'Telecom':        ['telecom', 'isp', 'carrier'],
            'End Users':      ['end user', 'consumer', 'individual', 'user'],
        }
        t_lower = t.lower()
        for clean_name, keywords in mapping.items():
            if any(kw in t_lower for kw in keywords):
                return clean_name
        if len(t) < 2 or t.lower() in ('n/a', 'na', 'none', 'unknown', 'not specified', 'multiple', ''):
            return None
        return t

    def _parse_llm_response(self, response_text, original_text, title):
        attack   = re.search(r'ATTACK[_\s]*TYPE:\s*(.+)', response_text, re.IGNORECASE)
        severity = re.search(r'SEVERITY:\s*(.+)',          response_text, re.IGNORECASE)
        target   = re.search(r'TARGET:\s*(.+)',            response_text, re.IGNORECASE)
        vuln     = re.search(r'VULNERABILITY:\s*(.+)',     response_text, re.IGNORECASE)
        impact   = re.search(r'IMPACT:\s*(.+)',            response_text, re.IGNORECASE)
        
        if not attack or not severity:
            return None

        def clean(val):
            return re.sub(r'[\[\]]', '', val).strip() if val else ''

        attack_type  = clean(attack.group(1))
        severity_raw = clean(severity.group(1)).lower().split('/')[0].strip()
        vuln_raw     = clean(vuln.group(1)) if vuln else ''

        if severity_raw not in ('critical', 'high', 'medium', 'low'):
            severity_raw = 'medium'

        if not vuln_raw or vuln_raw.lower() in ('n/a', 'na', 'none', 'unknown'):
            vuln_val = self._extract_cve_best(original_text, title)
        else:
            vuln_val = vuln_raw

        normalized_attack = self._normalize_attack_type(attack_type)

        # Strategy: Pattern detection is authoritative for specific sectors.
        # LLM only contributes when pattern falls back to "Multiple Sectors".
        pattern_target = self._detect_target(original_text + ' ' + title, title)
        llm_target = self._clean_llm_target(clean(target.group(1)) if target else '')

        if pattern_target != 'Multiple Sectors':
            final_target = pattern_target
        elif llm_target:
            final_target = llm_target
        else:
            final_target = 'Multiple Sectors'

        return {
            'attack_type':   normalized_attack,
            'severity':      severity_raw,
            'target':        final_target,
            'vulnerability': vuln_val,
            'impact':        clean(impact.group(1)) if impact else f'{normalized_attack} detected',
            'threat_actor':  self._detect_threat_actor(original_text),
            'iocs':          self._extract_iocs(original_text),
            'mitigation':    self._generate_mitigation(normalized_attack)
        }
    
    def _normalize_attack_type(self, attack_str):
        cleaned = re.sub(r'[\[\]]', '', attack_str).strip().lower()
        if cleaned in ('n/a', 'na', 'none', 'unknown', 'other', ''):
            return 'Security Incident'
        attack_map = {
            'ransomware':         'Ransomware Attack',
            'phishing':           'Phishing Campaign',
            'ddos':               'DDoS Attack',
            'denial of service':  'DDoS Attack',
            'malware':            'Malware Distribution',
            'infostealer':        'Malware Distribution',
            'stealer':            'Malware Distribution',
            'spyware':            'Malware Distribution',
            'backdoor':           'Malware Distribution',
            'trojan':             'Malware Distribution',
            'zero-day':           'Zero-Day Exploit',
            'zero day':           'Zero-Day Exploit',
            'vulnerability':      'Vulnerability Exploit',
            'exploit':            'Vulnerability Exploit',
            'sql injection':      'SQL Injection',
            'sqli':               'SQL Injection',
            'apt':                'APT Campaign',
            'supply chain':       'Supply Chain Attack',
            'credential':         'Credential Theft',
            'data breach':        'Data Breach',
            'data leak':          'Data Breach',
            'brute force':        'Brute Force Attack',
            'man in the middle':  'MitM Attack',
            'mitm':               'MitM Attack',
            'cryptojacking':      'Cryptojacking',
            'social engineering': 'Social Engineering',
        }
        for key, value in attack_map.items():
            if key in cleaned:
                return value
        return attack_str.title()
    
    # ── Pattern matching ──────────────────────────────────────────────────────

    def _pattern_extraction(self, text, title):
        combined = (title + ' ' + text).lower()
        
        # FIX: Greatly expanded attack patterns
        attack_patterns = {
            'Ransomware Attack':     ['ransomware', 'encrypted files', 'ransom demand', 'lockbit', 'blackcat', 'alphv', 'clop', 'revil', 'ryuk', 'conti', 'maze', 'decryption key'],
            'Phishing Campaign':     ['phishing', 'credential harvesting', 'fake login', 'spear phishing', 'smishing', 'vishing', 'fake email', 'email lure', 'malicious link', 'arpa dns', 'ipv6', 'evade phishing'],
            'Malware Distribution':  ['malware', 'trojan', 'backdoor', 'infostealer', 'spyware', 'stealer', 'worm', 'keylogger', 'rat ', 'remote access trojan', 'infostealers', 'installfix', 'fake install'],
            'DDoS Attack':           ['ddos', 'denial of service', 'botnet flood', 'amplification attack', 'traffic flood', 'service disruption'],
            'Zero-Day Exploit':      ['zero-day', 'zero day', 'unpatched vulnerability', '0-day', 'actively exploited', 'in the wild'],
            'Vulnerability Exploit': ['exploit', 'cve-', 'vulnerability', 'patch', 'rce', 'remote code execution', 'privilege escalation', 'buffer overflow', 'arbitrary code'],
            'Data Breach':           ['data breach', 'data leak', 'exposed data', 'stolen data', 'leaked database', 'unauthorized access', 'data exposure', 'personal data', 'pii'],
            'Supply Chain Attack':   ['supply chain', 'third-party', 'software update', 'compromised package', 'npm package', 'pypi', 'open source'],
            'APT Campaign':          ['apt', 'apt28', 'apt29', 'apt41', 'advanced persistent', 'state-sponsored', 'nation-state', 'espionage', 'nation state', 'fancy bear', 'cozy bear', 'lazarus'],
            'Credential Theft':      ['credential theft', 'password theft', 'account takeover', 'brute force', 'credential stuffing', 'stolen credentials', 'account hijacking', 'hijacking attack'],
            'SQL Injection':         ['sql injection', 'sqli', 'database injection'],
            'Cryptojacking':         ['cryptojacking', 'cryptominer', 'crypto miner', 'mining malware'],
        }
        
        attack_type = 'Security Incident'  # FIX: better default than "Unknown Attack"
        for attack, keywords in attack_patterns.items():
            if any(kw in combined for kw in keywords):
                attack_type = attack
                break
        
        severity_score = 0
        if any(w in combined for w in ['critical', 'actively exploited', 'zero-day', 'widespread', 'emergency patch']):
            severity_score += 3
        if any(w in combined for w in ['ransomware', 'data breach', 'rce', 'remote code execution', 'apt', 'apt28']):
            severity_score += 2
        if 'cve-' in combined:
            severity_score += 2
        if any(w in combined for w in ['phishing', 'malware', 'backdoor', 'infostealer']):
            severity_score += 1
        if any(w in combined for w in ['high', 'severe', 'dangerous', 'warning', 'alert']):
            severity_score += 1
        
        if severity_score >= 5:   severity = 'critical'
        elif severity_score >= 3: severity = 'high'
        elif severity_score >= 1: severity = 'medium'
        else:                     severity = 'low'
        
        impact_parts = []
        if any(w in combined for w in ['encrypted', 'locked']):             impact_parts.append('data encryption')
        if any(w in combined for w in ['stolen', 'leaked', 'exposed']):     impact_parts.append('data exposure')
        if any(w in combined for w in ['disrupted', 'offline', 'outage']):  impact_parts.append('service disruption')
        if any(w in combined for w in ['rce', 'remote code execution']):    impact_parts.append('remote code execution')
        impact = f"Incident involved {', '.join(impact_parts)}" if impact_parts else f"{attack_type} detected"
        
        return {
            'attack_type':   attack_type,
            'threat_actor':  self._detect_threat_actor(text),
            'target':        self._detect_target(combined, title),
            'vulnerability': self._extract_cve_best(text, title),
            'impact':        impact,
            'severity':      severity,
            'mitigation':    self._generate_mitigation(attack_type),
            'iocs':          self._extract_iocs(text)
        }
    
    def _detect_threat_actor(self, text):
        apt_groups = ['apt28', 'apt29', 'apt41', 'apt42', 'lazarus', 'blackcat',
                      'lockbit', 'alphv', 'clop', 'revil', 'conti', 'maze',
                      'scattered spider', 'sandworm', 'cozy bear', 'fancy bear']
        text_lower = text.lower()
        for group in apt_groups:
            if group in text_lower:
                return group.upper()
        if 'state-sponsored' in text_lower or 'nation-state' in text_lower:
            return 'State-Sponsored Actor'
        if 'ransomware' in text_lower:
            return 'Ransomware Group'
        if 'hacktivist' in text_lower:
            return 'Hacktivist Group'
        return 'Unknown Actor'
    
    def _detect_target(self, text, title=''):
        """
        Sector detection — ordered from most-specific to least-specific.
        Checks title separately first for high-confidence matches.
        """
        text_lower = text.lower()
        title_lower = title.lower() if title else ''

        # Title-based overrides (highest confidence — checked before body)
        title_sector_map = [
            ('Technology',   ['microsoft 365', 'windows hotpatch', 'windows update', 'm365', 'backup to add', 'file-level restore']),
            ('Government',   ['dutch govt', 'cisa:', 'apt28', 'APT28', 'government warns', 'govt warns']),
            ('Developers',   ['claude code', 'installfix', 'install guides']),
            ('Enterprise',   ['microsoft teams phishing', 'employees with']),
            ('Telecom',      ['signal, whatsapp', 'whatsapp account']),
        ]
        for sector, keywords in title_sector_map:
            if any(kw.lower() in title_lower for kw in keywords):
                return sector

        # Body-based detection — most-specific first
        sector_map = [
            ('Developers',    ['developer', 'developers', 'github', 'npm', 'pypi', 'vscode']),
            ('Government',    ['government', 'parliament', 'federal', 'agency', 'ministry', 'military', 'defense', 'pentagon', 'senate', 'cisa', 'national security', 'state-sponsored']),
            ('Finance',       ['bank', 'financial', 'payment', 'fintech', 'credit card', 'trading', 'insurance', 'investment', 'cryptocurrency', 'wallet']),
            ('Healthcare',    ['hospital', 'healthcare', 'medical', 'patient', 'clinic', 'pharmacy', 'nhs', 'ehr']),
            ('Education',     ['university', 'school', 'college', 'education', 'student', 'academic', 'campus']),
            ('Retail',        ['retail', 'e-commerce', 'shopping', 'store', 'merchant']),
            ('Energy',        ['energy', 'power grid', 'utility', 'oil', 'gas', 'pipeline', 'electricity', 'nuclear']),
            ('Telecom',       ['telecom', 'isp', 'carrier', 'mobile network', 'broadband', 'telco']),
            ('Manufacturing', ['manufacturing', 'factory', 'industrial', 'ics', 'scada', 'ot network']),
            ('Enterprise',    ['enterprise', 'corporate', 'employees', 'workplace', 'organization', 'firm']),
            ('Technology',    ['sharepoint', 'onedrive', 'exchange', 'software', 'cloud', 'saas', 'microsoft', 'google cloud', 'aws', 'azure', 'windows', 'ivanti', 'backup', 'hotpatch', 'restore']),
        ]

        for sector, keywords in sector_map:
            if any(kw in text_lower for kw in keywords):
                return sector

        if 'phishing' in text_lower:
            return 'Enterprise'
        if 'android' in text_lower or 'ios' in text_lower or 'mobile' in text_lower:
            return 'End Users'

        return 'Multiple Sectors'
    
    def _extract_cve(self, text):
        """Legacy — use _extract_cve_best() instead"""
        match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
        return match.group(0).upper() if match else 'N/A'
    
    def _extract_iocs(self, text):
        iocs = []
        ips    = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        hashes = re.findall(r'\b[a-f0-9]{64}\b', text.lower())
        domains = re.findall(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:com|net|org|io|ru|cn|xyz)\b', text.lower())
        iocs.extend([f"IP: {ip}"           for ip  in ips[:2]])
        iocs.extend([f"Hash: {h[:16]}..."  for h   in hashes[:2]])
        iocs.extend([f"Domain: {d}"        for d   in domains[:2] if len(d) > 6])
        return iocs if iocs else ['No specific IOCs extracted']
    
    def _generate_mitigation(self, attack_type):
        mitigations = {
            'Ransomware Attack':     'Isolate systems, restore from backups, deploy anti-ransomware tools',
            'Phishing Campaign':     'Enhance email filtering, conduct security training, implement MFA',
            'DDoS Attack':           'Deploy DDoS mitigation, implement rate limiting, use CDN',
            'Zero-Day Exploit':      'Apply patches immediately, implement compensating controls',
            'Malware Distribution':  'Update antivirus, block malicious domains, scan systems',
            'Vulnerability Exploit': 'Apply security patches, conduct vulnerability assessment',
            'SQL Injection':         'Use parameterized queries, apply input validation, deploy WAF',
            'Data Breach':           'Reset credentials, notify affected users, audit access logs',
            'Supply Chain Attack':   'Audit third-party dependencies, verify software integrity',
            'APT Campaign':          'Threat hunt across environment, isolate compromised systems',
            'Credential Theft':      'Enable MFA, reset compromised passwords, audit login logs',
            'Cryptojacking':         'Monitor CPU usage, remove miner, patch entry point',
            'Security Incident':     'Apply security patches, monitor systems, review access logs',
        }
        return mitigations.get(attack_type, 'Apply security patches and monitor systems')
    
    # ── Main methods ──────────────────────────────────────────────────────────

    def extract_threat_intelligence(self, text, title, incident=None):
        """Main extraction — pass full incident dict to enable CVE patching."""
        result = None

        if self.mode == 'ollama' and self.ollama_available:
            result = self.extract_with_ollama(text, title)
        elif self.mode == 'openai':
            result = self.extract_with_openai(text, title)
        
        if not result:
            result = self._pattern_extraction(text, title)
        
        # Always run CVE patch — uses preprocessor entities if available
        if incident:
            result = self._patch_cve(result, incident)
        
        return result
    
    def analyze_dataset(self, input_file='processed_incidents.json',
                        output_file='threat_intelligence.json'):
        input_path  = os.path.join('data/processed', input_file)
        output_path = os.path.join('data/processed', output_file)
        
        if not os.path.exists(input_path):
            print(f"✗ File not found: {input_path}")
            print("  Run preprocessor first: python src/preprocessor.py")
            return
        
        with open(input_path, 'r', encoding='utf-8') as f:
            incidents = json.load(f)
        
        print(f"📊 Analyzing {len(incidents)} incidents using {self.mode.upper()} mode...\n")
        
        analyzed_incidents = []
        
        for i, incident in enumerate(incidents, 1):
            print(f"[{i}/{len(incidents)}] {incident['title'][:55]}...")
            
            threat_intel = self.extract_threat_intelligence(
                incident['cleaned_text'],
                incident['title'],
                incident=incident
            )
            
            analyzed = {
                **incident,
                'threat_intelligence': threat_intel,
                'analysis_method':     self.mode
            }
            analyzed_incidents.append(analyzed)
            
            print(f"    ✓ Type: {threat_intel['attack_type']}")
            print(f"    ✓ Target: {threat_intel['target']}")
            print(f"    ✓ Severity: {threat_intel['severity'].upper()}")
            print(f"    ✓ CVE: {threat_intel['vulnerability']}\n")
            
            if self.mode in ['ollama', 'openai']:
                time.sleep(1)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_incidents, f, indent=2, ensure_ascii=False)
        
        print(f"{'='*70}")
        print(f"✅ Analysis complete! Saved to: {output_path}")
        print(f"{'='*70}\n")
        self._display_summary(analyzed_incidents)
        return analyzed_incidents
    
    def _display_summary(self, incidents):
        print("\n📊 THREAT INTELLIGENCE SUMMARY\n")
        attack_counts   = Counter(inc['threat_intelligence']['attack_type'] for inc in incidents)
        severity_counts = Counter(inc['threat_intelligence']['severity']    for inc in incidents)
        target_counts   = Counter(inc['threat_intelligence']['target']      for inc in incidents)
        cve_count       = sum(1 for inc in incidents
                              if inc['threat_intelligence'].get('vulnerability', 'N/A') != 'N/A')
        print("🎯 Attack Types:")
        for attack, count in attack_counts.most_common():
            print(f"   • {attack}: {count}")
        print("\n⚠️  Severity Distribution:")
        for sev in ['critical', 'high', 'medium', 'low']:
            count = severity_counts.get(sev, 0)
            if count > 0:
                print(f"   • {sev.upper()}: {count}")
        print("\n🎯 Top Targeted Sectors:")
        for target, count in target_counts.most_common(5):
            print(f"   • {target}: {count}")
        print(f"\n🔍 CVEs Identified: {cve_count}")
        print("\n" + "="*70)

def main():
    print("\n🚀 SELECT ANALYSIS MODE:")
    print("  1. Pattern Matching (Fast, no setup needed)")
    print("  2. Ollama (FREE AI, requires ollama serve)")
    print("  3. OpenAI GPT (Requires API key)\n")
    
    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"
    mode_map = {'1': 'pattern', '2': 'ollama', '3': 'openai'}
    mode = mode_map.get(choice, 'pattern')
    
    analyzer = GPTThreatAnalyzer(mode=mode)
    analyzer.analyze_dataset()
    
    print("\n💡 Next step: python src/visualizer.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()