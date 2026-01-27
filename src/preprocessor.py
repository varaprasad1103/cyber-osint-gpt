# src/preprocessor.py
import re
import json
import os

class TextPreprocessor:
    def __init__(self):
        os.makedirs('data/processed', exist_ok=True)
    
    def clean_text(self, text):
        if not text:
            return ""
        
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_sentences(self, text):
        """Simple sentence extraction without NLTK"""
        if not text:
            return []
        
        # Split on periods, question marks, exclamation marks
        sentences = re.split(r'[.!?]+', text)
        # Filter out short fragments
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def extract_cyber_entities(self, text):
        """Extract cyber security entities"""
        entities = {
            'cves': [],
            'malware': [],
            'attack_types': []
        }
        
        # Extract CVEs
        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        entities['cves'] = list(set(re.findall(cve_pattern, text)))
        
        # Common attack types
        attack_keywords = ['ransomware', 'phishing', 'ddos', 'malware', 
                          'sql injection', 'zero-day', 'vulnerability',
                          'exploit', 'botnet', 'trojan']
        
        text_lower = text.lower()
        for attack in attack_keywords:
            if attack in text_lower:
                entities['attack_types'].append(attack)
        
        return entities
    
    def preprocess_incident(self, incident):
        full_text = incident.get('text', '') or incident.get('snippet', '')
        cleaned = self.clean_text(full_text)
        
        sentences = self.extract_sentences(cleaned)
        entities = self.extract_cyber_entities(cleaned)
        
        processed = {
            'id': incident.get('id', ''),
            'source': incident.get('source', ''),
            'title': incident.get('title', ''),
            'url': incident.get('url', ''),
            'date': incident.get('date', ''),
            'cleaned_text': cleaned,
            'sentences': sentences,
            'word_count': len(cleaned.split()),
            'sentence_count': len(sentences),
            'entities': entities
        }
        
        return processed
    
    def preprocess_dataset(self):
        input_path = 'data/raw/cyber_incidents.json'
        output_path = 'data/processed/processed_incidents.json'
        
        print("\n" + "="*70)
        print("🧹 TEXT PREPROCESSOR")
        print("="*70 + "\n")
        
        if not os.path.exists(input_path):
            print(f"✗ File not found: {input_path}")
            print("  Run scraper first: python src/scraper.py")
            return
        
        with open(input_path, 'r', encoding='utf-8') as f:
            incidents = json.load(f)
        
        print(f"Processing {len(incidents)} incidents...\n")
        
        processed = []
        for i, inc in enumerate(incidents, 1):
            p = self.preprocess_incident(inc)
            processed.append(p)
            print(f"[{i}/{len(incidents)}] {p['title'][:60]}...")
            print(f"    Words: {p['word_count']}, Sentences: {p['sentence_count']}")
            if p['entities']['cves']:
                print(f"    CVEs found: {', '.join(p['entities']['cves'])}")
            if p['entities']['attack_types']:
                print(f"    Attack types: {', '.join(p['entities']['attack_types'][:3])}")
            print()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
        
        print(f"{'='*70}")
        print(f"✅ Saved to: {output_path}")
        
        # Statistics
        total_words = sum(p['word_count'] for p in processed)
        total_cves = sum(len(p['entities']['cves']) for p in processed)
        
        print(f"\n📊 Statistics:")
        print(f"  Total incidents: {len(processed)}")
        print(f"  Total words: {total_words:,}")
        print(f"  CVEs detected: {total_cves}")
        print(f"  Average words per incident: {total_words // len(processed)}")
        print("="*70 + "\n")
        
        print("💡 Next step: python src/gpt_analyzer.py")

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    preprocessor.preprocess_dataset()