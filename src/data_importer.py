# src/data_importer.py - Import External Unstructured Data
import json
import os
from datetime import datetime
from pathlib import Path
import re

class DataImporter:
    """
    Import external cyber incident data from various formats:
    - Text files (.txt)
    - JSON files
    - CSV files
    - Direct text input
    """
    
    def __init__(self):
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/imported', exist_ok=True)
        self.supported_formats = ['.txt', '.json', '.csv', '.md']
    
    def import_from_file(self, filepath: str) -> list:
        """
        Import incidents from a file
        
        Args:
            filepath: Path to the file to import
            
        Returns:
            List of incident dictionaries
        """
        path = Path(filepath)
        
        if not path.exists():
            print(f"✗ File not found: {filepath}")
            return []
        
        if path.suffix not in self.supported_formats:
            print(f"✗ Unsupported format: {path.suffix}")
            print(f"  Supported: {', '.join(self.supported_formats)}")
            return []
        
        print(f"\n📥 Importing from: {path.name}")
        print(f"   Format: {path.suffix}")
        
        if path.suffix == '.json':
            return self._import_json(path)
        elif path.suffix == '.csv':
            return self._import_csv(path)
        elif path.suffix in ['.txt', '.md']:
            return self._import_text(path)
        
        return []
    
    def _import_json(self, path: Path) -> list:
        """Import from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                incidents = data
            elif isinstance(data, dict):
                if 'incidents' in data:
                    incidents = data['incidents']
                else:
                    incidents = [data]
            else:
                print("✗ Invalid JSON structure")
                return []
            
            # Normalize format
            normalized = []
            for i, inc in enumerate(incidents):
                normalized.append(self._normalize_incident(inc, i, path.name))
            
            print(f"✓ Imported {len(normalized)} incidents from JSON")
            return normalized
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON parse error: {e}")
            return []
        except Exception as e:
            print(f"✗ Error: {e}")
            return []
    
    def _import_csv(self, path: Path) -> list:
        """Import from CSV file"""
        try:
            import csv
            incidents = []
            
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    inc = self._normalize_incident(row, i, path.name)
                    incidents.append(inc)
            
            print(f"✓ Imported {len(incidents)} incidents from CSV")
            return incidents
            
        except Exception as e:
            print(f"✗ Error reading CSV: {e}")
            return []
    
    def _import_text(self, path: Path) -> list:
        """
        Import from plain text file
        Expects format:
        
        TITLE: [title]
        URL: [url] (optional)
        DATE: [date] (optional)
        ---
        [incident description]
        ===
        [next incident]
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by separator
            sections = re.split(r'={3,}', content)
            incidents = []
            
            for i, section in enumerate(sections):
                if len(section.strip()) < 50:
                    continue
                
                # Extract title if present
                title_match = re.search(r'TITLE:\s*(.+)', section, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    # Remove the title line from text
                    text = re.sub(r'TITLE:.+\n', '', section, flags=re.IGNORECASE)
                else:
                    # Use first line or generate title
                    lines = section.strip().split('\n')
                    title = lines[0][:100] if lines else f"Incident {i+1}"
                    text = '\n'.join(lines[1:]) if len(lines) > 1 else section
                
                # Extract URL if present
                url_match = re.search(r'URL:\s*(.+)', text, re.IGNORECASE)
                url = url_match.group(1).strip() if url_match else f"file://{path.name}"
                text = re.sub(r'URL:.+\n', '', text, flags=re.IGNORECASE)
                
                # Extract date if present
                date_match = re.search(r'DATE:\s*(.+)', text, re.IGNORECASE)
                date = date_match.group(1).strip() if date_match else datetime.now().strftime('%Y-%m-%d')
                text = re.sub(r'DATE:.+\n', '', text, flags=re.IGNORECASE)
                
                # Clean separator
                text = re.sub(r'-{3,}', '', text).strip()
                
                if len(text) < 50:
                    continue
                
                incident = {
                    'id': f'import_{i+1}_{int(datetime.now().timestamp())}',
                    'source': f'Imported from {path.name}',
                    'title': title.strip(),
                    'url': url,
                    'text': text,
                    'date': date,
                    'scraped_at': datetime.now().isoformat()
                }
                
                incidents.append(incident)
            
            print(f"✓ Imported {len(incidents)} incidents from text file")
            return incidents
            
        except Exception as e:
            print(f"✗ Error reading text file: {e}")
            return []
    
    def _normalize_incident(self, data: dict, index: int, source: str) -> dict:
        """Normalize incident data to standard format"""
        
        # Try to extract standard fields
        title = (data.get('title') or 
                data.get('Title') or 
                data.get('headline') or 
                data.get('subject') or 
                f"Imported Incident {index+1}")
        
        text = (data.get('text') or 
               data.get('description') or 
               data.get('content') or 
               data.get('body') or 
               data.get('snippet') or 
               str(data))
        
        url = (data.get('url') or 
              data.get('link') or 
              data.get('source_url') or 
              f"imported://#{index+1}")
        
        date = (data.get('date') or 
               data.get('published') or 
               data.get('timestamp') or 
               datetime.now().strftime('%Y-%m-%d'))
        
        return {
            'id': f'import_{index}_{int(datetime.now().timestamp())}',
            'source': f'Imported from {source}',
            'title': str(title)[:200],
            'url': str(url),
            'text': str(text),
            'date': str(date)[:10],
            'scraped_at': datetime.now().isoformat()
        }
    
    def import_from_text(self, text: str, title: str = None) -> list:
        """
        Import from direct text input
        
        Args:
            text: The incident description
            title: Optional title
            
        Returns:
            List with single incident
        """
        if len(text.strip()) < 50:
            print("✗ Text too short (minimum 50 characters)")
            return []
        
        incident = {
            'id': f'manual_{int(datetime.now().timestamp())}',
            'source': 'Manual Input',
            'title': title or text[:100],
            'url': 'manual://input',
            'text': text,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"✓ Created incident from manual input")
        return [incident]
    
    def merge_with_existing(self, new_incidents: list, 
                           existing_file: str = 'cyber_incidents.json') -> list:
        """
        Merge new incidents with existing dataset
        
        Args:
            new_incidents: List of new incidents to add
            existing_file: Existing incidents file
            
        Returns:
            Combined list of incidents
        """
        existing_path = os.path.join('data/raw', existing_file)
        
        existing_incidents = []
        if os.path.exists(existing_path):
            try:
                with open(existing_path, 'r', encoding='utf-8') as f:
                    existing_incidents = json.load(f)
                print(f"📂 Found {len(existing_incidents)} existing incidents")
            except:
                pass
        
        # Combine
        combined = existing_incidents + new_incidents
        
        # Remove duplicates based on title similarity
        unique = []
        titles_seen = set()
        
        for inc in combined:
            title_key = inc['title'].lower()[:50]
            if title_key not in titles_seen:
                titles_seen.add(title_key)
                unique.append(inc)
        
        removed = len(combined) - len(unique)
        if removed > 0:
            print(f"🔄 Removed {removed} duplicate(s)")
        
        return unique
    
    def save_imported(self, incidents: list, filename: str = 'cyber_incidents.json'):
        """Save imported incidents"""
        if not incidents:
            print("⚠️  No incidents to save")
            return None
        
        output_path = os.path.join('data/raw', filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(incidents, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*70}")
        print(f"✅ Saved {len(incidents)} incidents to: {output_path}")
        print(f"{'='*70}\n")
        
        return output_path
    
    def create_sample_import_file(self):
        """Create a sample file showing import format"""
        sample_text = """TITLE: Sample Ransomware Attack on Hospital Network
URL: https://example.com/incident1
DATE: 2025-01-15
---
A major hospital network was hit by a ransomware attack that encrypted critical patient data and disrupted operations. The attackers demanded $2 million in Bitcoin. Security researchers identified the attack as being carried out by the BlackCat ransomware group, exploiting a known vulnerability CVE-2024-1234 in the hospital's VPN gateway. The incident affected over 50,000 patient records and caused a 48-hour service disruption.
===
TITLE: SQL Injection Vulnerability in E-commerce Platform
URL: https://example.com/incident2
DATE: 2025-01-20
---
Security researchers discovered a critical SQL injection vulnerability (CVE-2024-5678) in a popular e-commerce platform used by thousands of online retailers. The vulnerability allows attackers to bypass authentication and access customer databases containing credit card information and personal data. Several websites have already been compromised, with stolen data appearing on dark web marketplaces. The platform vendor has released an emergency patch.
===
TITLE: State-Sponsored APT Targets Financial Sector
---
An advanced persistent threat (APT) group believed to be state-sponsored has been conducting espionage campaigns against major banks and financial institutions. The attackers used sophisticated spear-phishing emails and zero-day exploits to gain access to internal networks. Once inside, they established persistence and exfiltrated sensitive financial data over several months before being detected."""
        
        sample_path = 'data/imported/sample_import.txt'
        os.makedirs('data/imported', exist_ok=True)
        
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        print(f"📝 Created sample import file: {sample_path}")
        print(f"   Use this as a template for importing your own data\n")
        
        return sample_path


def interactive_import():
    """Interactive data import interface"""
    importer = DataImporter()
    
    print("\n" + "="*70)
    print("📥 DATA IMPORTER - Import External Cyber Incident Data")
    print("="*70 + "\n")
    
    print("Import Options:")
    print("  1. Import from file (TXT, JSON, CSV)")
    print("  2. Import from manual text input")
    print("  3. Create sample import file")
    print("  4. Exit\n")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == '1':
        filepath = input("\nEnter file path: ").strip()
        incidents = importer.import_from_file(filepath)
        
        if incidents:
            merge = input("\nMerge with existing data? (y/n) [y]: ").strip().lower()
            if merge != 'n':
                incidents = importer.merge_with_existing(incidents)
            
            importer.save_imported(incidents)
            
            print("\n💡 Next steps:")
            print("  1. python src/preprocessor.py")
            print("  2. python src/gpt_analyzer_enhanced.py")
            print("  3. python src/visualizer.py\n")
    
    elif choice == '2':
        print("\nEnter incident details:")
        title = input("Title: ").strip()
        print("Description (press Ctrl+D or Ctrl+Z when done):")
        print("-" * 50)
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        text = '\n'.join(lines)
        
        incidents = importer.import_from_text(text, title)
        
        if incidents:
            merge = input("\nMerge with existing data? (y/n) [y]: ").strip().lower()
            if merge != 'n':
                incidents = importer.merge_with_existing(incidents)
            
            importer.save_imported(incidents)
    
    elif choice == '3':
        sample_path = importer.create_sample_import_file()
        print(f"\n✓ View the sample file to see the format")
        print(f"✓ Edit it with your own data, then import using option 1\n")
    
    print("="*70 + "\n")


def main():
    interactive_import()


if __name__ == "__main__":
    main()