# src/preprocessor.py
import re
import json
import nltk
import os

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        os.makedirs('data/processed', exist_ok=True)
    
    def clean_text(self, text):
        if not text:
            return ""
        
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def preprocess_incident(self, incident):
        full_text = incident.get('text', '') or incident.get('snippet', '')
        cleaned = self.clean_text(full_text)
        
        processed = {
            'id': incident.get('id', ''),
            'source': incident.get('source', ''),
            'title': incident.get('title', ''),
            'url': incident.get('url', ''),
            'cleaned_text': cleaned,
            'sentences': sent_tokenize(cleaned) if cleaned else [],
            'word_count': len(cleaned.split())
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
            print(f"[{i}/{len(incidents)}] {p['title'][:50]}... ({p['word_count']} words)")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved to: {output_path}")
        print("="*70 + "\n")

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    preprocessor.preprocess_dataset()