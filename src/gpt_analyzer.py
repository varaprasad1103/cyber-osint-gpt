# src/gpt_analyzer.py - Working version with multiple LLM options
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
        """
        Initialize with mode: 'ollama', 'pattern', or 'openai'
        """
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
        """Check Ollama connection"""
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
            print("   Start Ollama with: ollama serve")
            print("   Then download model: ollama pull llama3.2")
            print("   Falling back to pattern matching\n")
            self.ollama_available = False
            self.mode = 'pattern'
    
    def _init_openai(self):
        """Check OpenAI API key"""
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("No API key found")
            self.openai_client = OpenAI(api_key=api_key)
            print("✅ OpenAI API initialized\n")
        except Exception as e:
            print(f"⚠️  OpenAI not available: {e}")
            print("   Add OPENAI_API_KEY to .env file")
            print("   Falling back to pattern matching\n")
            self.mode = 'pattern'
    
    def extract_with_ollama(self, text, title):
        """Use Ollama for extraction"""
        prompt = f"""You are a cybersecurity analyst. Analyze this incident and respond with ONLY these fields (one per line):

ATTACK_TYPE: [ransomware/phishing/ddos/malware/zero-day/vulnerability]
SEVERITY: [critical/high/medium/low]
TARGET: [affected sector]
VULNERABILITY: [CVE number or N/A]
IMPACT: [brief impact description]

Incident: {title}
Details: {text[:1000]}

Respond with ONLY the fields above, nothing else."""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2',
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.3,
                        'num_predict': 150
                    }
                },
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json().get('response', '')
                return self._parse_llm_response(result, text, title)
            
        except requests.exceptions.Timeout:
            print(f"    ⚠️  Ollama timeout (slow model)")
        except Exception as e:
            print(f"    ⚠️  Ollama error: {str(e)[:40]}")
        
        return None
    
    def extract_with_openai(self, text, title):
        """Use OpenAI GPT for extraction"""
        prompt = f"""Analyze this cybersecurity incident. Extract:
- Attack type
- Severity (critical/high/medium/low)  
- Target sector
- CVE/Vulnerability
- Impact (1 sentence)

Title: {title}
Text: {text[:1500]}

Respond in format:
ATTACK_TYPE: [value]
SEVERITY: [value]
TARGET: [value]
VULNERABILITY: [value]
IMPACT: [value]"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity threat analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content
            return self._parse_llm_response(result, text, title)
            
        except Exception as e:
            print(f"    ⚠️  OpenAI error: {str(e)[:40]}")
        
        return None
    
    def _parse_llm_response(self, response_text, original_text, title):
        """Parse LLM response into structured format"""
        
        # Extract fields using regex
        attack = re.search(r'ATTACK[_\s]*TYPE:\s*(.+)', response_text, re.IGNORECASE)
        severity = re.search(r'SEVERITY:\s*(.+)', response_text, re.IGNORECASE)
        target = re.search(r'TARGET:\s*(.+)', response_text, re.IGNORECASE)
        vuln = re.search(r'VULNERABILITY:\s*(.+)', response_text, re.IGNORECASE)
        impact = re.search(r'IMPACT:\s*(.+)', response_text, re.IGNORECASE)
        
        # If parsing fails, use pattern matching
        if not attack or not severity:
            return None
        
        attack_type = attack.group(1).strip()
        
        return {
            'attack_type': self._normalize_attack_type(attack_type),
            'severity': severity.group(1).strip().lower() if severity else 'medium',
            'target': target.group(1).strip() if target else self._detect_target(original_text),
            'vulnerability': vuln.group(1).strip() if vuln else self._extract_cve(original_text),
            'impact': impact.group(1).strip() if impact else f'{attack_type} detected',
            'threat_actor': self._detect_threat_actor(original_text),
            'iocs': self._extract_iocs(original_text),
            'mitigation': self._generate_mitigation(attack_type)
        }
    
    def _normalize_attack_type(self, attack_str):
        """Normalize attack type from LLM"""
        attack_map = {
            'ransomware': 'Ransomware Attack',
            'phishing': 'Phishing Campaign',
            'ddos': 'DDoS Attack',
            'malware': 'Malware Distribution',
            'zero-day': 'Zero-Day Exploit',
            'zero day': 'Zero-Day Exploit',
            'vulnerability': 'Vulnerability Exploit',
            'sql injection': 'SQL Injection',
            'apt': 'APT Campaign',
        }
        
        attack_lower = attack_str.lower()
        for key, value in attack_map.items():
            if key in attack_lower:
                return value
        
        return attack_str.title()
    
    def _pattern_extraction(self, text, title):
        """Enhanced pattern-based extraction"""
        combined = (title + ' ' + text).lower()
        
        attack_patterns = {
            'Ransomware Attack': ['ransomware', 'encrypted', 'ransom', 'lockbit'],
            'Phishing Campaign': ['phishing', 'credential', 'fake email'],
            'DDoS Attack': ['ddos', 'denial of service', 'botnet'],
            'Zero-Day Exploit': ['zero-day', 'zero day', 'unpatched'],
            'Malware Distribution': ['malware', 'trojan', 'backdoor', 'stealer'],
            'SQL Injection': ['sql injection', 'sqli'],
            'Vulnerability Exploit': ['exploit', 'vulnerability', 'cve'],
        }
        
        attack_type = 'Unknown Attack'
        for attack, keywords in attack_patterns.items():
            if any(kw in combined for kw in keywords):
                attack_type = attack
                break
        
        # Severity scoring
        severity_score = 0
        if any(w in combined for w in ['critical', 'actively exploited', 'zero-day', 'widespread']):
            severity_score += 3
        if any(w in combined for w in ['ransomware', 'data breach', 'rce']):
            severity_score += 2
        if 'cve-' in combined:
            severity_score += 2
        
        if severity_score >= 5:
            severity = 'critical'
        elif severity_score >= 3:
            severity = 'high'
        elif severity_score >= 1:
            severity = 'medium'
        else:
            severity = 'low'
        
        impact_parts = []
        if any(w in combined for w in ['encrypted', 'locked']):
            impact_parts.append('data encryption')
        if any(w in combined for w in ['stolen', 'leaked', 'exposed']):
            impact_parts.append('data exposure')
        if any(w in combined for w in ['disrupted', 'offline', 'outage']):
            impact_parts.append('service disruption')
        
        impact = f"Incident involved {', '.join(impact_parts)}" if impact_parts else f"{attack_type} detected"
        
        return {
            'attack_type': attack_type,
            'threat_actor': self._detect_threat_actor(text),
            'target': self._detect_target(combined),
            'vulnerability': self._extract_cve(text),
            'impact': impact,
            'severity': severity,
            'mitigation': self._generate_mitigation(attack_type),
            'iocs': self._extract_iocs(text)
        }
    
    def _detect_threat_actor(self, text):
        """Detect threat actor from text"""
        apt_groups = ['apt28', 'apt29', 'apt41', 'lazarus', 'blackcat', 'lockbit', 'alphv']
        text_lower = text.lower()
        
        for group in apt_groups:
            if group in text_lower:
                return group.upper()
        
        if 'state-sponsored' in text_lower or 'nation-state' in text_lower:
            return 'State-Sponsored Actor'
        if 'ransomware' in text_lower:
            return 'Ransomware Group'
        
        return 'Unknown Actor'
    
    def _detect_target(self, text):
        """Detect target sector"""
        sectors = {
            'Healthcare Sector': ['hospital', 'healthcare', 'medical', 'patient'],
            'Financial Sector': ['bank', 'financial', 'payment', 'fintech'],
            'Government': ['government', 'agency', 'federal', 'public sector'],
            'Technology': ['tech', 'software', 'cloud', 'saas'],
            'Retail': ['retail', 'e-commerce', 'shopping'],
        }
        
        for sector, keywords in sectors.items():
            if any(kw in text for kw in keywords):
                return sector
        
        return 'Multiple Sectors'
    
    def _extract_cve(self, text):
        """Extract CVE number"""
        match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
        return match.group(0).upper() if match else 'N/A'
    
    def _extract_iocs(self, text):
        """Extract indicators of compromise"""
        iocs = []
        
        # IPs
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        iocs.extend([f"IP: {ip}" for ip in ips[:2]])
        
        # File hashes
        hashes = re.findall(r'\b[a-f0-9]{64}\b', text.lower())
        iocs.extend([f"Hash: {h[:16]}..." for h in hashes[:2]])
        
        return iocs if iocs else ['No specific IOCs extracted']
    
    def _generate_mitigation(self, attack_type):
        """Generate mitigation recommendations"""
        mitigations = {
            'Ransomware Attack': 'Isolate systems, restore from backups, deploy anti-ransomware tools',
            'Phishing Campaign': 'Enhance email filtering, conduct security training, implement MFA',
            'DDoS Attack': 'Deploy DDoS mitigation, implement rate limiting, use CDN',
            'Zero-Day Exploit': 'Apply patches immediately, implement compensating controls',
            'Malware Distribution': 'Update antivirus, block malicious domains, scan systems',
            'Vulnerability Exploit': 'Apply security patches, conduct vulnerability assessment',
            'SQL Injection': 'Use parameterized queries, apply input validation, deploy WAF',
        }
        
        return mitigations.get(attack_type, 'Apply security patches and monitor systems')
    
    def extract_threat_intelligence(self, text, title):
        """Main extraction method"""
        
        # Try LLM if available
        if self.mode == 'ollama' and self.ollama_available:
            result = self.extract_with_ollama(text, title)
            if result:
                return result
        
        elif self.mode == 'openai':
            result = self.extract_with_openai(text, title)
            if result:
                return result
        
        # Fallback to pattern matching
        return self._pattern_extraction(text, title)
    
    def analyze_dataset(self, input_file='processed_incidents.json', 
                        output_file='threat_intelligence.json'):
        """Analyze all incidents"""
        
        input_path = os.path.join('data/processed', input_file)
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
                incident['title']
            )
            
            analyzed = {
                **incident,
                'threat_intelligence': threat_intel,
                'analysis_method': self.mode
            }
            
            analyzed_incidents.append(analyzed)
            
            print(f"    ✓ Type: {threat_intel['attack_type']}")
            print(f"    ✓ Severity: {threat_intel['severity'].upper()}")
            print(f"    ✓ CVE: {threat_intel['vulnerability']}\n")
            
            # Rate limiting for APIs
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
        """Display summary statistics"""
        print("\n📊 THREAT INTELLIGENCE SUMMARY\n")
        
        attack_counts = Counter(inc['threat_intelligence']['attack_type'] for inc in incidents)
        severity_counts = Counter(inc['threat_intelligence']['severity'] for inc in incidents)
        
        print("🎯 Attack Types:")
        for attack, count in attack_counts.most_common():
            print(f"   • {attack}: {count}")
        
        print("\n⚠️  Severity Distribution:")
        for sev in ['critical', 'high', 'medium', 'low']:
            count = severity_counts.get(sev, 0)
            if count > 0:
                print(f"   • {sev.upper()}: {count}")
        
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