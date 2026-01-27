# src/database_manager.py - Database Storage for Threat Intelligence
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ThreatIntelligenceDB:
    """
    SQLite database manager for cyber threat intelligence
    Implements the structured storage layer from your methodology
    """
    
    def __init__(self, db_path='data/threat_intelligence.db'):
        """Initialize database connection"""
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.create_tables()
        print(f"✅ Database initialized: {db_path}")
    
    def create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()
        
        # Main incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                source TEXT,
                title TEXT NOT NULL,
                url TEXT,
                date TEXT,
                scraped_at TEXT,
                cleaned_text TEXT,
                word_count INTEGER,
                sentence_count INTEGER
            )
        """)
        
        # Threat intelligence table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threat_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                attack_type TEXT,
                threat_actor TEXT,
                target TEXT,
                vulnerability TEXT,
                impact TEXT,
                severity TEXT CHECK(severity IN ('critical', 'high', 'medium', 'low')),
                mitigation TEXT,
                confidence_score REAL,
                analysis_method TEXT,
                FOREIGN KEY (incident_id) REFERENCES incidents(id)
            )
        """)
        
        # CVEs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                cve_id TEXT NOT NULL,
                FOREIGN KEY (incident_id) REFERENCES incidents(id)
            )
        """)
        
        # IOCs (Indicators of Compromise) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iocs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                ioc_type TEXT,
                ioc_value TEXT,
                FOREIGN KEY (incident_id) REFERENCES incidents(id)
            )
        """)
        
        # Attack types reference table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attack_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                attack_type TEXT,
                FOREIGN KEY (incident_id) REFERENCES incidents(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_severity ON threat_intelligence(severity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attack_type ON threat_intelligence(attack_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON incidents(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cve ON cves(cve_id)")
        
        self.conn.commit()
    
    def insert_incident(self, incident: Dict) -> bool:
        """Insert a single incident into database"""
        try:
            cursor = self.conn.cursor()
            
            # Insert main incident
            cursor.execute("""
                INSERT OR REPLACE INTO incidents 
                (id, source, title, url, date, scraped_at, cleaned_text, word_count, sentence_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident['id'],
                incident.get('source', ''),
                incident['title'],
                incident.get('url', ''),
                incident.get('date', ''),
                incident.get('scraped_at', ''),
                incident.get('cleaned_text', ''),
                incident.get('word_count', 0),
                incident.get('sentence_count', 0)
            ))
            
            # Insert threat intelligence if available
            if 'threat_intelligence' in incident:
                ti = incident['threat_intelligence']
                cursor.execute("""
                    INSERT INTO threat_intelligence 
                    (incident_id, attack_type, threat_actor, target, vulnerability, 
                     impact, severity, mitigation, confidence_score, analysis_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    incident['id'],
                    ti.get('attack_type', ''),
                    ti.get('threat_actor', ''),
                    ti.get('target', ''),
                    ti.get('vulnerability', ''),
                    ti.get('impact', ''),
                    ti.get('severity', 'medium'),
                    ti.get('mitigation', ''),
                    ti.get('confidence_score'),
                    incident.get('analysis_method', 'unknown')
                ))
                
                # Insert CVEs
                if 'entities' in incident and 'cves' in incident['entities']:
                    for cve in incident['entities']['cves']:
                        cursor.execute("""
                            INSERT INTO cves (incident_id, cve_id)
                            VALUES (?, ?)
                        """, (incident['id'], cve))
                
                # Insert IOCs
                if 'iocs' in ti:
                    for ioc in ti['iocs']:
                        if isinstance(ioc, str) and ':' in ioc:
                            ioc_type, ioc_value = ioc.split(':', 1)
                            cursor.execute("""
                                INSERT INTO iocs (incident_id, ioc_type, ioc_value)
                                VALUES (?, ?, ?)
                            """, (incident['id'], ioc_type.strip(), ioc_value.strip()))
                
                # Insert attack types
                if 'entities' in incident and 'attack_types' in incident['entities']:
                    for attack_type in incident['entities']['attack_types']:
                        cursor.execute("""
                            INSERT INTO attack_types (incident_id, attack_type)
                            VALUES (?, ?)
                        """, (incident['id'], attack_type))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error inserting incident: {e}")
            self.conn.rollback()
            return False
    
    def import_from_json(self, json_path: str) -> int:
        """Import incidents from JSON file"""
        print(f"\n📥 Importing from: {json_path}")
        
        if not os.path.exists(json_path):
            print(f"✗ File not found: {json_path}")
            return 0
        
        with open(json_path, 'r', encoding='utf-8') as f:
            incidents = json.load(f)
        
        count = 0
        for incident in incidents:
            if self.insert_incident(incident):
                count += 1
        
        print(f"✓ Imported {count}/{len(incidents)} incidents")
        return count
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total incidents
        cursor.execute("SELECT COUNT(*) FROM incidents")
        stats['total_incidents'] = cursor.fetchone()[0]
        
        # Severity distribution
        cursor.execute("""
            SELECT severity, COUNT(*) as count 
            FROM threat_intelligence 
            GROUP BY severity
            ORDER BY 
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                END
        """)
        stats['severity_distribution'] = dict(cursor.fetchall())
        
        # Top attack types
        cursor.execute("""
            SELECT attack_type, COUNT(*) as count 
            FROM threat_intelligence 
            WHERE attack_type != '' AND attack_type IS NOT NULL
            GROUP BY attack_type 
            ORDER BY count DESC 
            LIMIT 5
        """)
        stats['top_attack_types'] = dict(cursor.fetchall())
        
        # Top targets
        cursor.execute("""
            SELECT target, COUNT(*) as count 
            FROM threat_intelligence 
            WHERE target != '' AND target IS NOT NULL
            GROUP BY target 
            ORDER BY count DESC 
            LIMIT 5
        """)
        stats['top_targets'] = dict(cursor.fetchall())
        
        # Total CVEs
        cursor.execute("SELECT COUNT(DISTINCT cve_id) FROM cves")
        stats['unique_cves'] = cursor.fetchone()[0]
        
        # Recent incidents
        cursor.execute("""
            SELECT date, COUNT(*) as count 
            FROM incidents 
            WHERE date != '' AND date IS NOT NULL
            GROUP BY date 
            ORDER BY date DESC 
            LIMIT 7
        """)
        stats['recent_activity'] = dict(cursor.fetchall())
        
        return stats
    
    def query_by_severity(self, severity: str) -> List[Dict]:
        """Query incidents by severity level"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT i.*, ti.* 
            FROM incidents i
            JOIN threat_intelligence ti ON i.id = ti.incident_id
            WHERE ti.severity = ?
            ORDER BY i.date DESC
        """, (severity,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def query_by_attack_type(self, attack_type: str) -> List[Dict]:
        """Query incidents by attack type"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT i.*, ti.* 
            FROM incidents i
            JOIN threat_intelligence ti ON i.id = ti.incident_id
            WHERE ti.attack_type LIKE ?
            ORDER BY i.date DESC
        """, (f'%{attack_type}%',))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def query_by_cve(self, cve_id: str) -> List[Dict]:
        """Query incidents by CVE ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT i.*, ti.*, c.cve_id
            FROM incidents i
            JOIN threat_intelligence ti ON i.id = ti.incident_id
            JOIN cves c ON i.id = c.incident_id
            WHERE c.cve_id = ?
        """, (cve_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def search_incidents(self, keyword: str) -> List[Dict]:
        """Full-text search in incidents"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT i.*, ti.*
            FROM incidents i
            LEFT JOIN threat_intelligence ti ON i.id = ti.incident_id
            WHERE i.title LIKE ? OR i.cleaned_text LIKE ?
            ORDER BY i.date DESC
        """, (f'%{keyword}%', f'%{keyword}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_trend_analysis(self, days: int = 30) -> Dict:
        """Analyze trends over specified period"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                date,
                COUNT(*) as incidents,
                SUM(CASE WHEN ti.severity = 'critical' THEN 1 ELSE 0 END) as critical,
                SUM(CASE WHEN ti.severity = 'high' THEN 1 ELSE 0 END) as high
            FROM incidents i
            LEFT JOIN threat_intelligence ti ON i.id = ti.incident_id
            WHERE date != '' AND date IS NOT NULL
            GROUP BY date
            ORDER BY date DESC
            LIMIT ?
        """, (days,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def export_to_json(self, output_path: str):
        """Export database contents to JSON"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                i.*,
                ti.attack_type, ti.threat_actor, ti.target, ti.vulnerability,
                ti.impact, ti.severity, ti.mitigation, ti.confidence_score
            FROM incidents i
            LEFT JOIN threat_intelligence ti ON i.id = ti.incident_id
        """)
        
        incidents = []
        for row in cursor.fetchall():
            incident = dict(row)
            
            # Get CVEs
            cursor.execute("SELECT cve_id FROM cves WHERE incident_id = ?", (incident['id'],))
            incident['cves'] = [row[0] for row in cursor.fetchall()]
            
            # Get IOCs
            cursor.execute("SELECT ioc_type, ioc_value FROM iocs WHERE incident_id = ?", (incident['id'],))
            incident['iocs'] = [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]
            
            incidents.append(incident)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(incidents, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {len(incidents)} incidents to: {output_path}")
    
    def print_statistics(self):
        """Print formatted statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("📊 DATABASE STATISTICS")
        print("="*70 + "\n")
        
        print(f"Total Incidents: {stats['total_incidents']}")
        print(f"Unique CVEs: {stats['unique_cves']}\n")
        
        print("Severity Distribution:")
        for severity, count in stats['severity_distribution'].items():
            print(f"  • {severity.upper()}: {count}")
        
        print("\nTop Attack Types:")
        for attack, count in stats['top_attack_types'].items():
            print(f"  • {attack}: {count}")
        
        print("\nTop Targets:")
        for target, count in stats['top_targets'].items():
            print(f"  • {target}: {count}")
        
        if stats['recent_activity']:
            print("\nRecent Activity:")
            for date, count in list(stats['recent_activity'].items())[:5]:
                print(f"  • {date}: {count} incidents")
        
        print("\n" + "="*70 + "\n")
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Main function to demonstrate database usage"""
    print("\n" + "="*70)
    print("🗄️  THREAT INTELLIGENCE DATABASE MANAGER")
    print("="*70 + "\n")
    
    db = ThreatIntelligenceDB()
    
    print("\nOptions:")
    print("  1. Import from processed data")
    print("  2. View statistics")
    print("  3. Query by severity")
    print("  4. Search incidents")
    print("  5. Export to JSON")
    print("  6. Exit\n")
    
    choice = input("Select option (1-6): ").strip()
    
    if choice == '1':
        # Import from threat intelligence JSON
        json_path = 'data/processed/threat_intelligence.json'
        if os.path.exists(json_path):
            db.import_from_json(json_path)
            db.print_statistics()
        else:
            print(f"✗ File not found: {json_path}")
            print("  Run the analysis pipeline first")
    
    elif choice == '2':
        db.print_statistics()
    
    elif choice == '3':
        severity = input("Enter severity (critical/high/medium/low): ").strip().lower()
        results = db.query_by_severity(severity)
        print(f"\nFound {len(results)} {severity} severity incidents:")
        for i, inc in enumerate(results[:5], 1):
            print(f"  {i}. {inc['title'][:60]}...")
    
    elif choice == '4':
        keyword = input("Enter search keyword: ").strip()
        results = db.search_incidents(keyword)
        print(f"\nFound {len(results)} incidents matching '{keyword}':")
        for i, inc in enumerate(results[:5], 1):
            print(f"  {i}. {inc['title'][:60]}...")
    
    elif choice == '5':
        output_path = input("Enter output path [export.json]: ").strip() or "export.json"
        db.export_to_json(output_path)
    
    db.close()
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()