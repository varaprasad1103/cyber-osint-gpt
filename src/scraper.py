# src/scraper.py - Simple version for testing
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        os.makedirs('data/raw', exist_ok=True)
    
    def scrape_hacker_news(self, max_articles=20):
        """Scrape recent cyber security news from TheHackerNews"""
        base_url = "https://thehackernews.com"
        incidents = []
        
        print(f"\n🔍 Scraping TheHackerNews for cyber incidents...")
        print(f"Target: {max_articles} articles\n")
        
        try:
            response = self.session.get(base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article containers
            articles = soup.find_all('div', class_='body-post')[:max_articles]
            
            print(f"✓ Found {len(articles)} articles on the page\n")
            
            for idx, article in enumerate(articles, 1):
                try:
                    # Extract title and link
                    title_elem = article.find('h2', class_='home-title')
                    if not title_elem:
                        continue
                    
                    link_elem = title_elem.find('a')
                    if not link_elem:
                        continue
                    
                    title = link_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    
                    # Extract snippet
                    snippet_elem = article.find('div', class_='home-desc')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    print(f"[{idx}/{len(articles)}] Fetching: {title[:60]}...")
                    
                    # Get full article
                    full_text = self.scrape_article_content(url)
                    
                    incident = {
                        'id': f'thn_{idx}_{int(time.time())}',
                        'source': 'TheHackerNews',
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'text': full_text,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    incidents.append(incident)
                    print(f"    ✓ Success! ({len(full_text)} characters)\n")
                    
                    time.sleep(2)  # Be respectful
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}\n")
                    continue
            
        except Exception as e:
            print(f"✗ Error accessing website: {e}")
        
        return incidents
    
    def scrape_article_content(self, url):
        """Fetch full content of article"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'aside', 'iframe']):
                tag.decompose()
            
            # Find article body
            article_body = soup.find('div', class_='articlebody') or \
                          soup.find('article') or \
                          soup.find('div', class_='post-body')
            
            if article_body:
                paragraphs = article_body.find_all('p')
                text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                return text
            
            return ""
            
        except Exception as e:
            return f"Error fetching content: {e}"
    
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
        
        # Show sample
        if incidents:
            print("Sample incident:")
            print(f"  Title: {incidents[0]['title']}")
            print(f"  URL: {incidents[0]['url']}")
            print(f"  Text length: {len(incidents[0]['text'])} chars\n")
        
        return filepath

def main():
    print("\n" + "="*70)
    print("🚀 CYBER INCIDENT SCRAPER")
    print("="*70)
    
    scraper = CyberIncidentScraper()
    
    # Scrape 15 articles (faster for testing)
    incidents = scraper.scrape_hacker_news(max_articles=15)
    
    if incidents:
        scraper.save_incidents(incidents)
        print(f"✅ Done! Collected {len(incidents)} cyber incidents")
        print(f"\n💡 Next step: python src/preprocessor.py")
    else:
        print("⚠️  No incidents collected. Check your internet connection.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()