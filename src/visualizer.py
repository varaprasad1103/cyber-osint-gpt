# src/visualizer.py
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime

class ThreatVisualizer:
    def __init__(self):
        self.output_dir = 'visualizations'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def load_data(self, filename='threat_intelligence.json'):
        """Load threat intelligence data"""
        filepath = os.path.join('data/processed', filename)
        
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            print("  Run analyzer first: python src/gpt_analyzer.py")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def visualize_all(self, data):
        """Create all visualizations"""
        print("\n" + "="*70)
        print("📊 CREATING VISUALIZATIONS")
        print("="*70 + "\n")
        
        # 1. Attack Types Distribution
        print("Creating attack types chart...")
        self.plot_attack_types(data)
        
        # 2. Severity Distribution
        print("Creating severity distribution chart...")
        self.plot_severity(data)
        
        # 3. Target Sectors
        print("Creating target sectors chart...")
        self.plot_targets(data)
        
        # 4. Threat Timeline (if dates available)
        print("Creating threat timeline...")
        self.plot_timeline(data)
        
        # 5. Combined Dashboard
        print("Creating dashboard overview...")
        self.create_dashboard(data)
        
        print(f"\n✅ All visualizations saved to: {self.output_dir}/")
        print("="*70 + "\n")
    
    def plot_attack_types(self, data):
        """Plot attack types distribution"""
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        attack_counts = Counter(attack_types)
        
        plt.figure(figsize=(12, 6))
        
        # Sort by count
        sorted_attacks = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)
        attacks, counts = zip(*sorted_attacks) if sorted_attacks else ([], [])
        
        colors = plt.cm.Set3(range(len(attacks)))
        bars = plt.bar(range(len(attacks)), counts, color=colors, edgecolor='black', linewidth=1.5)
        
        plt.xlabel('Attack Type', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Incidents', fontsize=12, fontweight='bold')
        plt.title('Cyber Attack Types Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.xticks(range(len(attacks)), attacks, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/attack_types.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: attack_types.png")
    
    def plot_severity(self, data):
        """Plot severity distribution"""
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        severity_counts = Counter(severities)
        
        # Define order and colors
        severity_order = ['critical', 'high', 'medium', 'low']
        severity_colors = {'critical': '#d9534f', 'high': '#f0ad4e', 
                          'medium': '#5bc0de', 'low': '#5cb85c'}
        
        # Get counts in order
        ordered_counts = [severity_counts.get(s, 0) for s in severity_order]
        ordered_labels = [s.upper() for s in severity_order]
        colors = [severity_colors[s] for s in severity_order]
        
        plt.figure(figsize=(10, 6))
        
        # Create pie chart
        explode = [0.1 if c == max(ordered_counts) else 0 for c in ordered_counts]
        
        plt.pie(ordered_counts, labels=ordered_labels, autopct='%1.1f%%',
                startangle=90, colors=colors, explode=explode,
                shadow=True, textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        plt.title('Threat Severity Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/severity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: severity_distribution.png")
    
    def plot_targets(self, data):
        """Plot targeted sectors"""
        targets = [inc['threat_intelligence']['target'] for inc in data]
        target_counts = Counter(targets)
        
        plt.figure(figsize=(12, 6))
        
        sorted_targets = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)
        target_names, counts = zip(*sorted_targets) if sorted_targets else ([], [])
        
        colors = plt.cm.Pastel1(range(len(target_names)))
        bars = plt.barh(range(len(target_names)), counts, color=colors, 
                       edgecolor='black', linewidth=1.5)
        
        plt.ylabel('Target Sector', fontsize=12, fontweight='bold')
        plt.xlabel('Number of Incidents', fontsize=12, fontweight='bold')
        plt.title('Most Targeted Sectors', fontsize=14, fontweight='bold', pad=20)
        plt.yticks(range(len(target_names)), target_names)
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            plt.text(count, i, f' {int(count)}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/targeted_sectors.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: targeted_sectors.png")
    
    def plot_timeline(self, data):
        """Plot threat timeline"""
        dates = [inc.get('date', '') for inc in data]
        
        if not any(dates):
            print(f"  ⚠️  Skipped: timeline (no date data)")
            return
        
        # Count incidents by date
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.items())
        
        if not sorted_dates:
            return
        
        dates, counts = zip(*sorted_dates)
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(range(len(dates)), counts, marker='o', linewidth=2, 
                markersize=8, color='#e74c3c', markerfacecolor='white', 
                markeredgewidth=2)
        
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Incidents', fontsize=12, fontweight='bold')
        plt.title('Cyber Incident Timeline', fontsize=14, fontweight='bold', pad=20)
        plt.xticks(range(len(dates)), dates, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        # Fill area under curve
        plt.fill_between(range(len(dates)), counts, alpha=0.3, color='#e74c3c')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/incident_timeline.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: incident_timeline.png")
    
    def create_dashboard(self, data):
        """Create comprehensive dashboard"""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('Cyber Threat Intelligence Dashboard', 
                     fontsize=18, fontweight='bold', y=0.98)
        
        # Create grid
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Attack Types (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        attack_counts = Counter(attack_types)
        sorted_attacks = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_attacks:
            attacks, counts = zip(*sorted_attacks)
            ax1.barh(range(len(attacks)), counts, color=plt.cm.Set3(range(len(attacks))))
            ax1.set_yticks(range(len(attacks)))
            ax1.set_yticklabels(attacks)
            ax1.set_xlabel('Count')
            ax1.set_title('Top Attack Types', fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
        
        # 2. Severity (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        severity_counts = Counter(severities)
        severity_order = ['critical', 'high', 'medium', 'low']
        counts = [severity_counts.get(s, 0) for s in severity_order]
        colors = ['#d9534f', '#f0ad4e', '#5bc0de', '#5cb85c']
        ax2.pie(counts, labels=[s.upper() for s in severity_order], 
               autopct='%1.0f%%', colors=colors, startangle=90)
        ax2.set_title('Severity Distribution', fontweight='bold')
        
        # 3. Targets (middle left)
        ax3 = fig.add_subplot(gs[1, 0])
        targets = [inc['threat_intelligence']['target'] for inc in data]
        target_counts = Counter(targets)
        sorted_targets = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_targets:
            tgt_names, tgt_counts = zip(*sorted_targets)
            ax3.barh(range(len(tgt_names)), tgt_counts, color=plt.cm.Pastel1(range(len(tgt_names))))
            ax3.set_yticks(range(len(tgt_names)))
            ax3.set_yticklabels(tgt_names)
            ax3.set_xlabel('Count')
            ax3.set_title('Targeted Sectors', fontweight='bold')
            ax3.grid(axis='x', alpha=0.3)
        
        # 4. Vulnerabilities (middle right)
        ax4 = fig.add_subplot(gs[1, 1])
        vulns = [inc['threat_intelligence']['vulnerability'] for inc in data]
        vuln_counts = Counter(vulns)
        sorted_vulns = sorted(vuln_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        if sorted_vulns:
            vuln_names, vuln_cnts = zip(*sorted_vulns)
            ax4.bar(range(len(vuln_names)), vuln_cnts, color=plt.cm.Set2(range(len(vuln_names))))
            ax4.set_xticks(range(len(vuln_names)))
            ax4.set_xticklabels([v[:15] for v in vuln_names], rotation=45, ha='right', fontsize=8)
            ax4.set_ylabel('Count')
            ax4.set_title('Vulnerabilities Detected', fontweight='bold')
            ax4.grid(axis='y', alpha=0.3)
        
        # 5. Statistics (bottom - full width)
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        # Calculate statistics
        total_incidents = len(data)
        critical_count = sum(1 for inc in data if inc['threat_intelligence']['severity'] == 'critical')
        unique_attacks = len(set(attack_types))
        unique_cves = len(set(v for v in vulns if 'CVE-' in v))
        
        stats_text = f"""
        📊 KEY STATISTICS
        
        Total Incidents Analyzed: {total_incidents}
        Critical Threats: {critical_count}
        Unique Attack Types: {unique_attacks}
        CVEs Identified: {unique_cves}
        
        Data Sources: {', '.join(set(inc['source'] for inc in data))}
        Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        ax5.text(0.5, 0.5, stats_text, transform=ax5.transAxes,
                fontsize=12, verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                family='monospace')
        
        plt.savefig(f'{self.output_dir}/dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: dashboard.png")
    
    def generate_report(self, data):
        """Generate text report"""
        print("\n" + "="*70)
        print("📄 GENERATING THREAT INTELLIGENCE REPORT")
        print("="*70 + "\n")
        
        report_path = os.path.join(self.output_dir, 'threat_report.txt')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("CYBER THREAT INTELLIGENCE REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Incidents Analyzed: {len(data)}\n\n")
            
            # Attack types summary
            f.write("ATTACK TYPES:\n")
            f.write("-" * 40 + "\n")
            attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
            for attack, count in Counter(attack_types).most_common():
                f.write(f"  • {attack}: {count}\n")
            f.write("\n")
            
            # Severity summary
            f.write("SEVERITY DISTRIBUTION:\n")
            f.write("-" * 40 + "\n")
            severities = [inc['threat_intelligence']['severity'] for inc in data]
            for severity in ['critical', 'high', 'medium', 'low']:
                count = severities.count(severity)
                if count > 0:
                    f.write(f"  • {severity.upper()}: {count}\n")
            f.write("\n")
            
            # Detailed incidents
            f.write("DETAILED INCIDENT ANALYSIS:\n")
            f.write("="*70 + "\n\n")
            
            for i, inc in enumerate(data, 1):
                ti = inc['threat_intelligence']
                f.write(f"[{i}] {inc['title']}\n")
                f.write(f"    Source: {inc['source']}\n")
                f.write(f"    URL: {inc['url']}\n")
                f.write(f"    Attack Type: {ti['attack_type']}\n")
                f.write(f"    Severity: {ti['severity'].upper()}\n")
                f.write(f"    Target: {ti['target']}\n")
                f.write(f"    Vulnerability: {ti['vulnerability']}\n")
                f.write(f"    Impact: {ti['impact']}\n")
                f.write(f"    Mitigation: {ti['mitigation']}\n")
                f.write("\n" + "-"*70 + "\n\n")
        
        print(f"✅ Report saved to: {report_path}\n")

def main():
    visualizer = ThreatVisualizer()
    
    # Load data
    data = visualizer.load_data()
    
    if not data:
        return
    
    # Create visualizations
    visualizer.visualize_all(data)
    
    # Generate report
    visualizer.generate_report(data)
    
    print("="*70)
    print("✅ ALL DONE! Your project is complete!")
    print("="*70)
    print("\nGenerated files:")
    print(f"  📊 Visualizations: {visualizer.output_dir}/")
    print(f"  📄 Detailed report: {visualizer.output_dir}/threat_report.txt")
    print(f"  💾 Data files: data/processed/")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()