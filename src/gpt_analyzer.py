# src/gpt_analyzer_enhanced.py - Enhanced with REAL LLM Integration
import json
import os
import re
from typing import Dict, List, Optional
import time

class EnhancedGPTAnalyzer:
    """
    Enhanced analyzer with multiple LLM integration options:
    1. OpenAI GPT (requires API key - paid)
    2. Hugging Face Models (free alternatives)
    3. Ollama (local open-source models)
    4. Fallback to pattern matching
    """
    
    def __init__(self, mode='huggingface'):
        """
        Initialize analyzer with specified mode
        
        Args:
            mode: 'openai', 'huggingface', 'ollama', or 'pattern'
        """
        self.mode = mode
        os.makedirs('data/processed', exist_ok=True)
        
        if mode == 'openai':
            self._init_openai()
        elif mode == 'huggingface':
            self._init_huggingface()
        elif mode == 'ollama':
            self._init_ollama()
        else:
            print("🆓 Running in PATTERN MATCHING mode")
            print("   For better results, use 'huggingface' or 'ollama' mode\n")
    
    def _init_openai(self):
        """Initialize OpenAI API (requires API key)"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            openai.api_key = api_key
            self.client = openai
            print("✅ OpenAI GPT initialized")
        except Exception as e:
            print(f"⚠️  OpenAI init failed: {e}")
            print("   Falling back to pattern matching")
            self.mode = 'pattern'
    
    def _init_huggingface(self):
        """Initialize Hugging Face transformers (FREE)"""
        try:
            from transformers import pipeline
            print("🤗 Initializing Hugging Face model...")
            print("   This may take a few minutes on first run...\n")
            
            # Use a lightweight model for cyber security text classification
            # Options: 'distilbert-base-uncased', 'bert-base-uncased', etc.
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU, use 0 for GPU
            )
            
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1
            )
            
            print("✅ Hugging Face models loaded successfully!\n")
            
        except Exception as e:
            print(f"⚠️  Hugging Face init failed: {e}")
            print("   Install with: pip install transformers torch --break-system-packages")
            print("   Falling back to pattern matching")
            self.mode = 'pattern'
    
    def _init_ollama(self):
        """Initialize Ollama (local LLM)"""
        try:
            import requests
            # Check if Ollama is running
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                self.ollama_url = 'http://localhost:11434/api/generate'
                print("✅ Ollama connected successfully")
            else:
                raise ConnectionError("Ollama not responding")
        except Exception as e:
            print(f"⚠️  Ollama init failed: {e}")
            print("   Install Ollama from: https://ollama.ai")
            print("   Then run: ollama pull llama2")
            print("   Falling back to pattern matching")
            self.mode = 'pattern'
    
    def extract_threat_intelligence(self, incident_text: str, incident_title: str) -> Dict:
        """
        Extract threat intelligence using configured LLM
        """
        if self.mode == 'openai':
            return self._extract_with_openai(incident_text, incident_title)
        elif self.mode == 'huggingface':
            return self._extract_with_huggingface(incident_text, incident_title)
        elif self.mode == 'ollama':
            return self._extract_with_ollama(incident_text, incident_title)
        else:
            return self._extract_with_patterns(incident_text, incident_title)
    
    def _extract_with_openai(self, text: str, title: str) -> Dict:
        """Extract using OpenAI GPT"""
        prompt = f"""
        Analyze this cyber security incident and extract structured threat intelligence:
        
        Title: {title}
        Description: {text[:1500]}
        
        Extract and return in JSON format:
        - attack_type: (e.g., Ransomware, Phishing, DDoS)
        - threat_actor: (APT group or actor type)
        - target: (affected sector/organization type)
        - vulnerability: (CVE or vulnerability type)
        - impact: (brief description of impact)
        - severity: (critical/high/medium/low)
        - mitigation: (recommended actions)
        """
        
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cyber security analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            # Parse JSON from response
            threat_intel = json.loads(result)
            threat_intel['iocs'] = self._extract_iocs(text)
            return threat_intel
            
        except Exception as e:
            print(f"    ⚠️  OpenAI API error: {e}")
            return self._extract_with_patterns(text, title)
    
    def _extract_with_huggingface(self, text: str, title: str) -> Dict:
        """Extract using Hugging Face models"""
        combined_text = (title + " " + text)[:1024]  # Model token limit
        
        try:
            # 1. Classify attack type
            attack_labels = [
                "ransomware attack", "phishing campaign", "DDoS attack",
                "SQL injection", "zero-day exploit", "malware distribution",
                "APT campaign", "data breach", "vulnerability exploit"
            ]
            attack_result = self.classifier(
                combined_text,
                candidate_labels=attack_labels,
                multi_label=False
            )
            attack_type = attack_result['labels'][0].title()
            
            # 2. Classify severity
            severity_labels = ["critical", "high", "medium", "low"]
            severity_result = self.classifier(
                combined_text,
                candidate_labels=severity_labels,
                multi_label=False
            )
            severity = severity_result['labels'][0]
            
            # 3. Classify target
            target_labels = [
                "healthcare sector", "financial institutions", "government agencies",
                "technology companies", "critical infrastructure", "education sector"
            ]
            target_result = self.classifier(
                combined_text,
                candidate_labels=target_labels,
                multi_label=False
            )
            target = target_result['labels'][0].title()
            
            # 4. Generate summary for impact
            if len(text) > 100:
                summary = self.summarizer(
                    text[:1024],
                    max_length=100,
                    min_length=30,
                    do_sample=False
                )
                impact = summary[0]['summary_text']
            else:
                impact = text[:200]
            
            # 5. Use pattern matching for technical details
            vulnerability = self._extract_vulnerability(text)
            threat_actor = self._detect_threat_actor(text)
            mitigation = self._generate_mitigation(attack_type, vulnerability)
            iocs = self._extract_iocs(text)
            
            return {
                'attack_type': attack_type,
                'threat_actor': threat_actor,
                'target': target,
                'vulnerability': vulnerability,
                'impact': impact,
                'severity': severity,
                'mitigation': mitigation,
                'iocs': iocs,
                'confidence_score': attack_result['scores'][0]
            }
            
        except Exception as e:
            print(f"    ⚠️  Hugging Face error: {e}")
            return self._extract_with_patterns(text, title)
    
    def _extract_with_ollama(self, text: str, title: str) -> Dict:
        """Extract using Ollama local LLM"""
        prompt = f"""Analyze this cyber incident and extract: attack_type, threat_actor, target, vulnerability, severity, impact, and mitigation recommendations.

Title: {title}
Text: {text[:1000]}

Respond in JSON format."""
        
        try:
            import requests
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()['response']
                threat_intel = json.loads(result)
                threat_intel['iocs'] = self._extract_iocs(text)
                return threat_intel
            else:
                raise Exception("Ollama request failed")
                
        except Exception as e:
            print(f"    ⚠️  Ollama error: {e}")
            return self._extract_with_patterns(text, title)
    
    def _extract_with_patterns(self, text: str, title: str) -> Dict:
        """Fallback pattern-based extraction (your original method)"""
        combined_text = (title + ' ' + text).lower()
        
        return {
            'attack_type': self._detect_attack_type(combined_text),
            'threat_actor': self._detect_threat_actor(text),
            'target': self._detect_target(combined_text),
            'vulnerability': self._extract_vulnerability(text),
            'impact': self._assess_impact(combined_text, self._detect_attack_type(combined_text)),
            'severity': self._determine_severity(combined_text, self._extract_vulnerability(text), 
                                                 self._detect_attack_type(combined_text)),
            'mitigation': self._generate_mitigation(self._detect_attack_type(combined_text), 
                                                    self._extract_vulnerability(text)),
            'iocs': self._extract_iocs(text)
        }
    
    # Keep all your original helper methods
    def _detect_attack_type(self, text):
        attack_patterns = {
            'Ransomware Attack': ['ransomware', 'encrypted', 'ransom', 'lockbit', 'blackcat'],
            'Phishing Campaign': ['phishing', 'spear phishing', 'credential', 'fake email'],
            'DDoS Attack': ['ddos', 'denial of service', 'botnet attack'],
            'SQL Injection': ['sql injection', 'sqli'],
            'Zero-Day Exploit': ['zero-day', 'zero day'],
            'Malware Distribution': ['malware', 'trojan', 'backdoor'],
            'APT Campaign': ['apt', 'advanced persistent threat'],
            'Data Breach': ['data breach', 'leaked', 'exposed database'],
        }
        
        for attack_type, keywords in attack_patterns.items():
            if any(kw in text for kw in keywords):
                return attack_type
        return 'Unknown Attack Type'
    
    def _detect_threat_actor(self, text):
        apt_groups = ['apt28', 'apt29', 'apt41', 'lazarus', 'blackcat', 'lockbit']
        for group in apt_groups:
            if group in text.lower():
                return group.upper()
        
        if 'state-sponsored' in text.lower():
            return 'State-Sponsored Actor'
        elif 'ransomware' in text.lower():
            return 'Ransomware Group'
        return 'Unknown Actor'
    
    def _detect_target(self, text):
        sectors = {
            'Healthcare Sector': ['hospital', 'healthcare', 'medical'],
            'Financial Institutions': ['bank', 'financial', 'fintech'],
            'Government Agencies': ['government', 'agency', 'federal'],
            'Technology Companies': ['tech company', 'software', 'cloud'],
        }
        
        for sector, keywords in sectors.items():
            if any(kw in text for kw in keywords):
                return sector
        return 'Multiple Sectors'
    
    def _extract_vulnerability(self, text):
        cve_match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
        if cve_match:
            return cve_match.group(0).upper()
        
        vuln_keywords = ['zero-day', 'remote code execution', 'authentication bypass']
        for kw in vuln_keywords:
            if kw in text.lower():
                return f"{kw.title()} Vulnerability"
        return 'N/A'
    
    def _assess_impact(self, text, attack_type):
        impacts = []
        if any(w in text for w in ['encrypted', 'locked']):
            impacts.append('data encryption')
        if any(w in text for w in ['stolen', 'leaked']):
            impacts.append('data theft')
        if any(w in text for w in ['disrupted', 'outage']):
            impacts.append('service disruption')
        
        if impacts:
            return 'Incident resulted in ' + ', '.join(impacts)
        return f'{attack_type} with potential system compromise'
    
    def _extract_iocs(self, text):
        iocs = []
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        iocs.extend([f"IP: {ip}" for ip in ips[:3]])
        
        hashes = re.findall(r'\b[a-f0-9]{64}\b', text.lower())
        iocs.extend([f"Hash: {h[:16]}..." for h in hashes[:2]])
        
        return iocs if iocs else ['No specific IOCs extracted']
    
    def _determine_severity(self, text, vuln, attack):
        score = 0
        if any(w in text for w in ['critical', 'widespread', 'zero-day']):
            score += 3
        if any(w in text for w in ['ransomware', 'data breach']):
            score += 2
        if 'CVE-' in vuln:
            score += 2
        
        if score >= 5:
            return 'critical'
        elif score >= 3:
            return 'high'
        elif score >= 1:
            return 'medium'
        return 'low'
    
    def _generate_mitigation(self, attack_type, vuln):
        mitigations = {
            'Ransomware Attack': 'Isolate systems, restore from backups, deploy anti-ransomware tools.',
            'Phishing Campaign': 'Enhance email filtering, conduct security training, implement MFA.',
            'DDoS Attack': 'Deploy DDoS mitigation, implement rate limiting, use CDN protection.',
            'SQL Injection': 'Apply input validation, use parameterized queries, implement WAF.',
        }
        
        base = mitigations.get(attack_type, 'Apply security patches and follow best practices.')
        if 'CVE-' in vuln:
            base = f"Patch {vuln} immediately. " + base
        return base
    
    def analyze_dataset(self, input_file='processed_incidents.json', 
                       output_file='threat_intelligence.json'):
        """Analyze all incidents"""
        input_path = os.path.join('data/processed', input_file)
        output_path = os.path.join('data/processed', output_file)
        
        print("\n" + "="*70)
        print(f"🤖 THREAT INTELLIGENCE ANALYZER ({self.mode.upper()} mode)")
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
                'threat_intelligence': threat_intel,
                'analysis_method': self.mode
            }
            
            analyzed_incidents.append(analyzed)
            
            print(f"    ✓ Type: {threat_intel['attack_type']}")
            print(f"    ✓ Severity: {threat_intel['severity'].upper()}")
            
            if self.mode == 'huggingface' and 'confidence_score' in threat_intel:
                print(f"    ✓ Confidence: {threat_intel['confidence_score']:.2%}")
            
            print()
            
            # Rate limiting for API calls
            if self.mode == 'openai':
                time.sleep(1)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_incidents, f, indent=2, ensure_ascii=False)
        
        print(f"{'='*70}")
        print(f"✅ Analysis complete! Saved to: {output_path}")
        print(f"{'='*70}\n")
        
        return analyzed_incidents


def main():
    print("\n🚀 Select Analysis Mode:")
    print("  1. Hugging Face (FREE, best quality)")
    print("  2. Ollama (FREE, requires local install)")
    print("  3. OpenAI GPT (requires API key)")
    print("  4. Pattern Matching (fallback)\n")
    
    choice = input("Enter choice (1-4) [default: 1]: ").strip() or "1"
    
    mode_map = {
        '1': 'huggingface',
        '2': 'ollama',
        '3': 'openai',
        '4': 'pattern'
    }
    
    mode = mode_map.get(choice, 'huggingface')
    
    analyzer = EnhancedGPTAnalyzer(mode=mode)
    analyzer.analyze_dataset()
    
    print("\n💡 Next step: python src/visualizer.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()