# src/visualizer.py - Text reports only, no visualizations folder
import json
import os
from collections import Counter
from datetime import datetime

class ThreatVisualizer:
    def __init__(self):
        self.data_path = 'data/processed/threat_intelligence.json'
    
    def load_data(self):
        if not os.path.exists(self.data_path):
            print(f"✗ Data file not found: {self.data_path}")
            return None
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_text_report(self, data):
        os.makedirs('reports', exist_ok=True)
        report_path = 'reports/threat_summary.txt'
        
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("CYBER THREAT INTELLIGENCE SUMMARY\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Total Incidents: {len(data)}\n")
            f.write(f"Critical: {sum(1 for s in severities if s == 'critical')}\n\n")
            
            f.write("ATTACK TYPES:\n")
            for attack, count in Counter(attack_types).most_common():
                f.write(f"  • {attack}: {count}\n")
        
        print(f"✅ Text report: {report_path}")

def main():
    print("\n" + "="*70)
    print("📊 THREAT INTELLIGENCE VISUALIZATION")
    print("="*70 + "\n")
    
    visualizer = ThreatVisualizer()
    data = visualizer.load_data()
    
    if data:
        visualizer.generate_text_report(data)
        
        print("\n🌐 All visualizations are in the web dashboard!")
        print("   Run: python app.py")
        print("   Open: http://127.0.0.1:5000/dashboard")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()