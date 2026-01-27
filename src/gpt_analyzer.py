# src/gpt_analyzer.py - FREE VERSION (No API key needed)
import json
import os
import re

class GPTThreatAnalyzer:
    def __init__(self):
        os.makedirs('data/processed', exist_ok=True)
        print("🆓 Running in FREE MODE - Using intelligent pattern matching")
        print("   (No API key required!)\n")
    
    def extract_threat_intelligence(self, incident_text, incident_title):
        """Extract threat intelligence using advanced pattern matching"""
        
        combined_text = (incident_title + ' ' + incident_text).lower()
        
        # 1. Detect Attack Type
        attack_type = self._detect_attack_type(combined_text)
        
        # 2. Detect Threat Actor
        threat_actor = self._detect_threat_actor(incident_text)
        
        # 3. Detect Target
        target = self._detect_target(combined_text)
        
        # 4. Extract Vulnerability/CVE
        vulnerability = self._extract_vulnerability(incident_text)
        
        # 5. Assess Impact
        impact = self._assess_impact(combined_text, attack_type)
        
        # 6. Extract IOCs (Indicators of Compromise)
        iocs = self._extract_iocs(incident_text)
        
        # 7. Determine Severity
        severity = self._determine_severity(combined_text, vulnerability, attack_type)
        
        # 8. Generate Mitigation
        mitigation = self._generate_mitigation(attack_type, vulnerability)
        
        return {
            'attack_type': attack_type,
            'threat_actor': threat_actor,
            'target': target,
            'vulnerability': vulnerability,
            'impact': impact,
            'iocs': iocs,
            'severity': severity,
            'mitigation': mitigation
        }
    
    def _detect_attack_type(self, text):
        """Detect the primary attack type"""
        attack_patterns = {
            'Ransomware Attack': ['ransomware', 'encrypted', 'ransom', 'lockbit', 'blackcat'],
            'Phishing Campaign': ['phishing', 'spear phishing', 'credential', 'fake email'],
            'DDoS Attack': ['ddos', 'denial of service', 'botnet attack', 'amplification'],
            'SQL Injection': ['sql injection', 'sqli', 'database injection'],
            'Zero-Day Exploit': ['zero-day', 'zero day', 'unknown vulnerability', 'unpatched'],
            'Malware Distribution': ['malware', 'trojan', 'backdoor', 'stealer', 'infostealer'],
            'APT Campaign': ['apt', 'advanced persistent threat', 'state-sponsored', 'targeted attack'],
            'Data Breach': ['data breach', 'leaked', 'exposed database', 'stolen data'],
            'Vulnerability Exploit': ['exploit', 'vulnerability', 'cve', 'security flaw'],
            'Credential Stuffing': ['credential stuffing', 'password spray', 'brute force'],
            'Supply Chain Attack': ['supply chain', 'third-party', 'dependency'],
            'Cryptojacking': ['cryptomining', 'cryptojacking', 'cryptocurrency'],
        }
        
        for attack_type, keywords in attack_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    return attack_type
        
        return 'Unknown Attack Type'
    
    def _detect_threat_actor(self, text):
        """Detect threat actor or group"""
        # Known APT groups
        apt_groups = ['apt28', 'apt29', 'apt41', 'lazarus', 'fancy bear', 'cozy bear', 
                     'sandworm', 'apt42', 'kimsuky', 'blackcat', 'lockbit', 'alphv']
        
        for group in apt_groups:
            if group in text.lower():
                return group.upper()
        
        # Generic actor types
        if 'state-sponsored' in text.lower() or 'nation-state' in text.lower():
            return 'State-Sponsored Actor'
        elif 'ransomware' in text.lower():
            return 'Ransomware Group'
        elif 'organized' in text.lower() and 'crime' in text.lower():
            return 'Organized Cybercrime'
        
        return 'Unknown Actor'
    
    def _detect_target(self, text):
        """Detect the target sector or entity"""
        sectors = {
            'Healthcare Sector': ['hospital', 'healthcare', 'medical', 'patient'],
            'Financial Institutions': ['bank', 'financial', 'fintech', 'payment'],
            'Government Agencies': ['government', 'agency', 'federal', 'municipal'],
            'Education Sector': ['university', 'school', 'education', 'academic'],
            'Technology Companies': ['tech company', 'software', 'cloud provider', 'saas'],
            'Critical Infrastructure': ['infrastructure', 'utility', 'power grid', 'water'],
            'Retail & E-commerce': ['retail', 'e-commerce', 'shopping', 'store'],
            'Manufacturing': ['manufacturing', 'industrial', 'factory', 'production'],
        }
        
        for sector, keywords in sectors.items():
            for keyword in keywords:
                if keyword in text:
                    return sector
        
        return 'Multiple Sectors'
    
    def _extract_vulnerability(self, text):
        """Extract CVE or vulnerability information"""
        # Look for CVE
        cve_match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
        if cve_match:
            return cve_match.group(0).upper()
        
        # Look for vulnerability types
        vuln_keywords = ['zero-day', 'remote code execution', 'rce', 'authentication bypass', 
                        'privilege escalation', 'buffer overflow', 'xss', 'csrf']
        
        for keyword in vuln_keywords:
            if keyword in text.lower():
                return f"{keyword.title()} Vulnerability"
        
        return 'N/A'
    
    def _assess_impact(self, text, attack_type):
        """Assess the impact of the incident"""
        impacts = []
        
        if any(word in text for word in ['encrypted', 'locked', 'inaccessible']):
            impacts.append('data encryption and system lockout')
        
        if any(word in text for word in ['stolen', 'exfiltrated', 'leaked', 'exposed']):
            impacts.append('data theft and potential exposure')
        
        if any(word in text for word in ['disrupted', 'outage', 'unavailable', 'offline']):
            impacts.append('service disruption and downtime')
        
        if any(word in text for word in ['financial loss', 'monetary', 'ransom']):
            impacts.append('financial losses')
        
        if any(word in text for word in ['credential', 'password', 'authentication']):
            impacts.append('compromised credentials')
        
        if impacts:
            return 'Incident resulted in ' + ', '.join(impacts) + '.'
        
        return f'{attack_type} detected with potential system and data compromise.'
    
    def _extract_iocs(self, text):
        """Extract Indicators of Compromise"""
        iocs = []
        
        # IP addresses
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        iocs.extend([f"IP: {ip}" for ip in ips[:3]])
        
        # Domain patterns
        domains = re.findall(r'\b[a-z0-9-]+\.[a-z]{2,}\b', text.lower())
        suspicious_domains = [d for d in domains if len(d) > 8 and '.' in d][:2]
        iocs.extend([f"Domain: {d}" for d in suspicious_domains])
        
        # File hashes (SHA256 pattern)
        hashes = re.findall(r'\b[a-f0-9]{64}\b', text.lower())
        iocs.extend([f"Hash: {h[:16]}..." for h in hashes[:2]])
        
        return iocs if iocs else ['No specific IOCs extracted from report']
    
    def _determine_severity(self, text, vulnerability, attack_type):
        """Determine severity level"""
        score = 0
        
        # Critical keywords
        if any(word in text for word in ['critical', 'actively exploited', 'widespread', 'zero-day']):
            score += 3
        
        # High severity indicators
        if any(word in text for word in ['ransomware', 'data breach', 'remote code execution']):
            score += 2
        
        # CVE present
        if 'CVE-' in vulnerability:
            score += 2
        
        # Impact indicators
        if any(word in text for word in ['million', 'thousand', 'major']):
            score += 1
        
        # Determine level
        if score >= 5:
            return 'critical'
        elif score >= 3:
            return 'high'
        elif score >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _generate_mitigation(self, attack_type, vulnerability):
        """Generate mitigation recommendations"""
        mitigations = {
            'Ransomware Attack': 'Isolate affected systems, restore from backups, deploy anti-ransomware tools, and implement network segmentation.',
            'Phishing Campaign': 'Enhance email filtering, conduct security awareness training, implement MFA, and monitor for credential compromise.',
            'DDoS Attack': 'Deploy DDoS mitigation services, implement rate limiting, use CDN protection, and have incident response plan ready.',
            'SQL Injection': 'Apply input validation, use parameterized queries, conduct code review, and implement WAF protection.',
            'Zero-Day Exploit': 'Apply vendor patches immediately, implement compensating controls, monitor for suspicious activity, and isolate vulnerable systems.',
            'Malware Distribution': 'Update antivirus signatures, block malicious domains, scan all systems, and review security logs for compromise indicators.',
            'Data Breach': 'Contain the breach, notify affected parties, conduct forensic analysis, and strengthen access controls.',
            'Vulnerability Exploit': 'Apply security patches immediately, conduct vulnerability assessment, and implement defense-in-depth strategies.',
        }
        
        mitigation = mitigations.get(attack_type, 'Apply latest security patches, monitor systems closely, and follow security best practices.')
        
        if 'CVE-' in vulnerability:
            mitigation = f"Patch {vulnerability} immediately. " + mitigation
        
        return mitigation
    
    def analyze_dataset(self, input_file='processed_incidents.json', 
                        output_file='threat_intelligence.json'):
        """Analyze all incidents"""
        
        input_path = os.path.join('data/processed', input_file)
        output_path = os.path.join('data/processed', output_file)
        
        print("\n" + "="*70)
        print("🤖 THREAT INTELLIGENCE ANALYZER (FREE VERSION)")
        print("="*70 + "\n")
        
        if not os.path.exists(input_path):
            print(f"✗ File not found: {input_path}")
            return
        
        with open(input_path, 'r', encoding='utf-8') as f:
            incidents = json.load(f)
        
        print(f"📊 Analyzing {len(incidents)} incidents...\n")
        
        analyzed_incidents = []
        
        for i, incident in enumerate(incidents, 1):
            print(f"[{i}/{len(incidents)}] {incident['title'][:55]}...")
            
            threat_intel = self.extract_threat_intelligence(
                incident['cleaned_text'], 
                incident['title']
            )
            
            analyzed = {
                **incident,
                'threat_intelligence': threat_intel
            }
            
            analyzed_incidents.append(analyzed)
            
            print(f"    ✓ Type: {threat_intel['attack_type']}")
            print(f"    ✓ Severity: {threat_intel['severity'].upper()}")
            print(f"    ✓ Target: {threat_intel['target']}")
            print(f"    ✓ CVE: {threat_intel['vulnerability']}\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_incidents, f, indent=2, ensure_ascii=False)
        
        print(f"{'='*70}")
        print(f"✅ Analysis complete! Saved to: {output_path}")
        print(f"{'='*70}\n")
        
        self._display_summary(analyzed_incidents)
        
        return analyzed_incidents
    
    def _display_summary(self, incidents):
        """Display analysis summary"""
        print("\n📊 THREAT INTELLIGENCE SUMMARY\n")
        
        attack_counts = {}
        severity_counts = {}
        targets = {}
        
        for inc in incidents:
            ti = inc['threat_intelligence']
            attack_type = ti['attack_type']
            severity = ti['severity']
            target = ti['target']
            
            attack_counts[attack_type] = attack_counts.get(attack_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            targets[target] = targets.get(target, 0) + 1
        
        print("🎯 Attack Types:")
        for attack, count in sorted(attack_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {attack}: {count}")
        
        print("\n⚠️  Severity Distribution:")
        for sev in ['critical', 'high', 'medium', 'low']:
            count = severity_counts.get(sev, 0)
            if count > 0:
                print(f"   • {sev.upper()}: {count}")
        
        print("\n🎪 Targeted Sectors:")
        for target, count in sorted(targets.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {target}: {count}")
        
        print("\n" + "="*70)

def main():
    analyzer = GPTThreatAnalyzer()
    analyzer.analyze_dataset()
    
    print("\n💡 Next step: python src/visualizer.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()