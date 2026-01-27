# src/scraper.py - Improved with better error handling
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime

class CyberIncidentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        os.makedirs('data/raw', exist_ok=True)
    
    def scrape_bleeping_computer(self, max_articles=15):
        """Scrape from BleepingComputer - more reliable structure"""
        base_url = "https://www.bleepingcomputer.com"
        incidents = []
        
        print(f"\n🔍 Scraping BleepingComputer for cyber incidents...")
        print(f"Target: {max_articles} articles\n")
        
        try:
            response = self.session.get(base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links
            articles = soup.find_all('h4', class_='bc_latest_news_text')[:max_articles]
            
            if not articles:
                # Try alternative selector
                articles = soup.find_all('a', href=True)
                articles = [a for a in articles if '/news/' in a.get('href', '')][:max_articles]
            
            print(f"✓ Found {len(articles)} articles\n")
            
            for idx, article in enumerate(articles, 1):
                try:
                    if article.name == 'h4':
                        link = article.find('a')
                        if not link:
                            continue
                        title = link.get_text(strip=True)
                        url = link.get('href', '')
                    else:
                        title = article.get_text(strip=True)
                        url = article.get('href', '')
                    
                    if not url.startswith('http'):
                        url = base_url + url
                    
                    if not title or len(title) < 10:
                        continue
                    
                    print(f"[{idx}/{len(articles)}] {title[:60]}...")
                    
                    # Get article content
                    try:
                        full_text = self.scrape_article_content(url)
                    except KeyboardInterrupt:
                        print(f"    ⚠️  Interrupted by user\n")
                        break
                    except:
                        print(f"    ⚠️  Timeout/Error fetching content\n")
                        continue
                    
                    if len(full_text) < 100:
                        print(f"    ⚠️  Skipping (insufficient content)\n")
                        continue
                    
                    incident = {
                        'id': f'bc_{idx}_{int(time.time())}',
                        'source': 'BleepingComputer',
                        'title': title,
                        'url': url,
                        'text': full_text,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    incidents.append(incident)
                    print(f"    ✓ Success! ({len(full_text)} chars)\n")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:50]}\n")
                    continue
            
        except Exception as e:
            print(f"✗ Error accessing website: {e}")
        
        return incidents
    
    def scrape_sample_data(self):
        """Create sample data if scraping fails - for testing"""
        print("\n📝 Creating sample cyber incident data for testing...\n")
        
        sample_incidents = [
            {
                'id': 'sample_1',
                'source': 'Sample Data',
                'title': 'Major Ransomware Attack Targets Healthcare Sector',
                'url': 'https://example.com/ransomware-healthcare',
                'text': '''A sophisticated ransomware group known as BlackCat has launched a series of coordinated attacks against healthcare institutions across North America. The attack encrypted critical patient data and disrupted hospital operations. Security researchers identified the vulnerability as CVE-2024-1234, a zero-day exploit in commonly used hospital management software. The attackers demanded a ransom of $5 million in Bitcoin. Hospitals are working with cybersecurity firms to restore operations and prevent data loss. The FBI has issued an alert warning other healthcare providers to patch their systems immediately.''',
                'date': '2025-01-27',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_2',
                'source': 'Sample Data',
                'title': 'Critical SQL Injection Vulnerability Discovered in Popular CMS',
                'url': 'https://example.com/sql-injection-cms',
                'text': '''Security researchers have discovered a critical SQL injection vulnerability (CVE-2024-5678) in WordPress plugins used by over 2 million websites. The vulnerability allows attackers to bypass authentication and gain unauthorized access to databases containing sensitive user information. The flaw was introduced in version 3.2 of the plugin and affects all subsequent versions. Attackers have already exploited this vulnerability in targeted attacks against e-commerce sites. Website administrators are urged to update to the patched version immediately. The vulnerability has a CVSS score of 9.8, indicating critical severity.''',
                'date': '2025-01-26',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_3',
                'source': 'Sample Data',
                'title': 'State-Sponsored APT Group Targets Financial Institutions',
                'url': 'https://example.com/apt-financial',
                'text': '''A state-sponsored Advanced Persistent Threat (APT) group identified as APT42 has been conducting espionage campaigns against major financial institutions in Europe and Asia. The attackers used sophisticated phishing emails containing malicious attachments to deliver custom malware. The campaign leveraged social engineering tactics targeting executive-level employees. Once inside the network, the attackers established persistence using Living-off-the-Land techniques and exfiltrated sensitive financial data over encrypted channels. The operation is believed to have been ongoing for at least six months before detection.''',
                'date': '2025-01-25',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_4',
                'source': 'Sample Data',
                'title': 'DDoS Attack Disrupts Major Cloud Service Provider',
                'url': 'https://example.com/ddos-cloud',
                'text': '''A massive Distributed Denial of Service (DDoS) attack peaking at 2.3 Tbps disrupted services for a major cloud provider affecting thousands of businesses worldwide. The attack utilized a botnet of compromised IoT devices including routers, cameras, and smart home devices. Service outages lasted approximately 4 hours before mitigation measures were fully effective. The attack vector combined multiple techniques including UDP amplification and HTTP floods. This incident highlights the growing threat of IoT-based botnets and the importance of securing internet-connected devices.''',
                'date': '2025-01-24',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_5',
                'source': 'Sample Data',
                'title': 'Zero-Day Exploit in Enterprise VPN Allows Remote Code Execution',
                'url': 'https://example.com/vpn-zero-day',
                'text': '''Cybersecurity firm discovered a critical zero-day vulnerability (CVE-2024-9012) in enterprise VPN software that allows remote code execution without authentication. The vulnerability affects version 5.x through 7.2 of the software used by thousands of organizations worldwide. Attackers can exploit this flaw to gain complete control of VPN servers and pivot into internal networks. Evidence suggests the vulnerability has been actively exploited in the wild for at least two weeks. The vendor has released an emergency patch and is urging all customers to update immediately. Organizations using affected versions should assume their networks may be compromised.''',
                'date': '2025-01-23',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        for inc in sample_incidents:
            print(f"✓ Created: {inc['title']}")
        
        return sample_incidents
    
    def scrape_article_content(self, url):
        """Fetch article content with better error handling"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'aside', 'iframe', 'header']):
                tag.decompose()
            
            # Try multiple selectors
            selectors = [
                {'name': 'div', 'class_': 'articleBody'},
                {'name': 'article'},
                {'name': 'div', 'class_': 'article-content'},
                {'name': 'div', 'class_': 'post-content'},
                {'name': 'div', 'class_': 'entry-content'},
            ]
            
            article_body = None
            for selector in selectors:
                article_body = soup.find(**selector)
                if article_body:
                    break
            
            if article_body:
                paragraphs = article_body.find_all('p')
                text = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
                return text
            
            return ""
            
        except Exception as e:
            return ""
    
    def save_incidents(self, incidents, filename='cyber_incidents.json'):
        """Save to JSON"""
        if not incidents:
            print("⚠️  No incidents to save!")
            return None
        
        filepath = os.path.join('data/raw', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(incidents, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*70}")
        print(f"✅ SUCCESS! Saved {len(incidents)} incidents")
        print(f"📁 File: {filepath}")
        print(f"{'='*70}\n")
        
        # Show statistics
        total_words = sum(len(inc['text'].split()) for inc in incidents)
        avg_words = total_words // len(incidents) if incidents else 0
        
        print(f"📊 Statistics:")
        print(f"  Total incidents: {len(incidents)}")
        print(f"  Total words: {total_words:,}")
        print(f"  Average words per incident: {avg_words}")
        print(f"\n  Sample: {incidents[0]['title'][:60]}...")
        
        return filepath

def main():
    print("\n" + "="*70)
    print("🚀 CYBER INCIDENT SCRAPER")
    print("="*70)
    
    scraper = CyberIncidentScraper()
    incidents = []
    
    # Try BleepingComputer first
    print("\n[Option 1] Trying BleepingComputer...")
    try:
        incidents = scraper.scrape_bleeping_computer(max_articles=10)
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n⚠️  Error during scraping: {e}")
    
    # If scraping fails, use sample data
    if len(incidents) < 3:
        print("\n⚠️  Live scraping yielded few results")
        print("[Option 2] Using sample data for testing...\n")
        incidents = scraper.scrape_sample_data()
    
    if incidents:
        scraper.save_incidents(incidents)
        print(f"\n✅ Done! Collected {len(incidents)} cyber incidents")
        print(f"\n💡 Next step: python src/preprocessor.py")
    else:
        print("✗ Failed to collect data")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()