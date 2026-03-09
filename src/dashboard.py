# src/dashboard.py - Interactive Dashboard with Plotly
import json
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from collections import Counter
from datetime import datetime

class InteractiveDashboard:
    def __init__(self):
        self.data_path = 'data/processed/threat_intelligence.json'
        self.output_dir = 'dashboard'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_data(self):
        """Load threat intelligence data"""
        if not os.path.exists(self.data_path):
            print(f"✗ Data file not found: {self.data_path}")
            print("  Run analyzer first: python src/gpt_analyzer.py")
            return None
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_attack_types_chart(self, data):
        """Interactive attack types bar chart"""
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        attack_counts = Counter(attack_types)
        
        sorted_attacks = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)
        attacks, counts = zip(*sorted_attacks) if sorted_attacks else ([], [])
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(attacks),
                y=list(counts),
                marker=dict(
                    color=list(counts),
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Count")
                ),
                text=list(counts),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Incidents: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🎯 Attack Types Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            xaxis_title='Attack Type',
            yaxis_title='Number of Incidents',
            template='plotly_white',
            height=500,
            hovermode='x'
        )
        
        return fig
    
    def create_severity_pie(self, data):
        """Interactive severity pie chart"""
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        severity_counts = Counter(severities)
        
        severity_order = ['critical', 'high', 'medium', 'low']
        colors = {'critical': '#e74c3c', 'high': '#f39c12', 'medium': '#3498db', 'low': '#2ecc71'}
        
        labels = [s.upper() for s in severity_order if severity_counts.get(s, 0) > 0]
        values = [severity_counts.get(s, 0) for s in severity_order if severity_counts.get(s, 0) > 0]
        colors_list = [colors[s] for s in severity_order if severity_counts.get(s, 0) > 0]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors_list),
                hole=0.4,
                textposition='inside',
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Incidents: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '⚠️ Threat Severity Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            template='plotly_white',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_timeline(self, data):
        """Interactive timeline chart"""
        dates = [inc.get('date', '') for inc in data]
        date_counts = Counter(dates)
        
        if not date_counts:
            return None
        
        sorted_dates = sorted(date_counts.items())
        dates_list, counts_list = zip(*sorted_dates)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(dates_list),
            y=list(counts_list),
            mode='lines+markers',
            name='Incidents',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=10, color='#c0392b'),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.2)',
            hovertemplate='<b>Date: %{x}</b><br>Incidents: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': '📈 Incident Timeline',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            xaxis_title='Date',
            yaxis_title='Number of Incidents',
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_target_sectors(self, data):
        """Interactive target sectors chart"""
        targets = [inc['threat_intelligence']['target'] for inc in data]
        target_counts = Counter(targets)
        
        sorted_targets = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)
        target_names, counts = zip(*sorted_targets) if sorted_targets else ([], [])
        
        fig = go.Figure(data=[
            go.Bar(
                y=list(target_names),
                x=list(counts),
                orientation='h',
                marker=dict(
                    color=list(counts),
                    colorscale='Viridis',
                    showscale=True
                ),
                text=list(counts),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Incidents: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🎯 Most Targeted Sectors',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            xaxis_title='Number of Incidents',
            yaxis_title='Sector',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def create_cve_analysis(self, data):
        """CVE vulnerability analysis"""
        cves = []
        for inc in data:
            cve = inc['threat_intelligence'].get('vulnerability', 'N/A')
            if 'CVE-' in cve:
                cves.append(cve)
        
        cve_counts = Counter(cves)
        
        if not cve_counts:
            return None
        
        sorted_cves = sorted(cve_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        cve_names, counts = zip(*sorted_cves)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(cve_names),
                y=list(counts),
                marker=dict(
                    color='#e67e22',
                    line=dict(color='#d35400', width=2)
                ),
                text=list(counts),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Occurrences: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🔍 Top CVE Vulnerabilities',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            xaxis_title='CVE Number',
            yaxis_title='Occurrences',
            template='plotly_white',
            height=500,
            xaxis={'tickangle': -45}
        )
        
        return fig
    
    def create_comprehensive_dashboard(self, data):
        """Create comprehensive multi-chart dashboard"""
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                '🎯 Attack Types', '⚠️ Severity Levels',
                '📈 Timeline Trend', '🎯 Target Sectors',
                '🔍 Top CVEs', '📊 Statistics Summary'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'pie'}],
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'table'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Attack Types
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        attack_counts = Counter(attack_types)
        sorted_attacks = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        attacks, counts = zip(*sorted_attacks) if sorted_attacks else ([], [])
        
        fig.add_trace(
            go.Bar(x=list(attacks), y=list(counts), marker_color='#3498db', name='Attacks'),
            row=1, col=1
        )
        
        # 2. Severity Pie
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        severity_counts = Counter(severities)
        severity_order = ['critical', 'high', 'medium', 'low']
        colors_map = {'critical': '#e74c3c', 'high': '#f39c12', 'medium': '#3498db', 'low': '#2ecc71'}
        
        sev_labels = [s.upper() for s in severity_order if severity_counts.get(s, 0) > 0]
        sev_values = [severity_counts.get(s, 0) for s in severity_order if severity_counts.get(s, 0) > 0]
        sev_colors = [colors_map[s] for s in severity_order if severity_counts.get(s, 0) > 0]
        
        fig.add_trace(
            go.Pie(labels=sev_labels, values=sev_values, marker=dict(colors=sev_colors)),
            row=1, col=2
        )
        
        # 3. Timeline
        dates = [inc.get('date', '') for inc in data]
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.items())
        if sorted_dates:
            dates_list, counts_list = zip(*sorted_dates)
            fig.add_trace(
                go.Scatter(x=list(dates_list), y=list(counts_list), mode='lines+markers', 
                          line=dict(color='#e74c3c', width=2), name='Incidents'),
                row=2, col=1
            )
        
        # 4. Targets
        targets = [inc['threat_intelligence']['target'] for inc in data]
        target_counts = Counter(targets)
        sorted_targets = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        target_names, target_cnts = zip(*sorted_targets) if sorted_targets else ([], [])
        
        fig.add_trace(
            go.Bar(y=list(target_names), x=list(target_cnts), orientation='h', marker_color='#2ecc71'),
            row=2, col=2
        )
        
        # 5. CVEs
        cves = []
        for inc in data:
            cve = inc['threat_intelligence'].get('vulnerability', 'N/A')
            if 'CVE-' in cve:
                cves.append(cve)
        
        cve_counts = Counter(cves)
        if cve_counts:
            sorted_cves = sorted(cve_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            cve_names, cve_cnts = zip(*sorted_cves)
            fig.add_trace(
                go.Bar(x=list(cve_names), y=list(cve_cnts), marker_color='#e67e22'),
                row=3, col=1
            )
        
        # 6. Statistics Table
        total = len(data)
        critical = sum(1 for inc in data if inc['threat_intelligence']['severity'] == 'critical')
        unique_attacks = len(set(attack_types))
        unique_cves = len(set(cves))
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Metric', 'Value'], fill_color='#3498db', font=dict(color='white', size=14)),
                cells=dict(values=[
                    ['Total Incidents', 'Critical Threats', 'Unique Attack Types', 'CVEs Identified'],
                    [total, critical, unique_attacks, unique_cves]
                ], fill_color='#ecf0f1', font=dict(size=12))
            ),
            row=3, col=2
        )
        
        fig.update_layout(
            title={
                'text': '🛡️ Cyber Threat Intelligence Dashboard',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 28, 'color': '#2c3e50', 'family': 'Arial Black'}
            },
            showlegend=False,
            height=1400,
            template='plotly_white'
        )
        
        return fig
    
    def generate_all_dashboards(self):
        """Generate all interactive dashboards"""
        print("\n" + "="*70)
        print("📊 GENERATING INTERACTIVE DASHBOARDS")
        print("="*70 + "\n")
        
        data = self.load_data()
        if not data:
            return
        
        print(f"Loaded {len(data)} incidents\n")
        
        # 1. Attack Types
        print("Creating attack types chart...")
        fig1 = self.create_attack_types_chart(data)
        fig1.write_html(f'{self.output_dir}/attack_types_interactive.html')
        print("  ✓ Saved: attack_types_interactive.html")
        
        # 2. Severity Pie
        print("Creating severity distribution...")
        fig2 = self.create_severity_pie(data)
        fig2.write_html(f'{self.output_dir}/severity_interactive.html')
        print("  ✓ Saved: severity_interactive.html")
        
        # 3. Timeline
        print("Creating timeline...")
        fig3 = self.create_timeline(data)
        if fig3:
            fig3.write_html(f'{self.output_dir}/timeline_interactive.html')
            print("  ✓ Saved: timeline_interactive.html")
        
        # 4. Target Sectors
        print("Creating target sectors chart...")
        fig4 = self.create_target_sectors(data)
        fig4.write_html(f'{self.output_dir}/targets_interactive.html')
        print("  ✓ Saved: targets_interactive.html")
        
        # 5. CVE Analysis
        print("Creating CVE analysis...")
        fig5 = self.create_cve_analysis(data)
        if fig5:
            fig5.write_html(f'{self.output_dir}/cve_analysis_interactive.html')
            print("  ✓ Saved: cve_analysis_interactive.html")
        
        # 6. Comprehensive Dashboard
        print("Creating comprehensive dashboard...")
        fig6 = self.create_comprehensive_dashboard(data)
        fig6.write_html(f'{self.output_dir}/comprehensive_dashboard.html')
        print("  ✓ Saved: comprehensive_dashboard.html")
        
        print(f"\n{'='*70}")
        print(f"✅ All dashboards created in: {self.output_dir}/")
        print(f"{'='*70}\n")
        print("🌐 Open in browser:")
        print(f"   {self.output_dir}/comprehensive_dashboard.html")
        print("="*70 + "\n")

def main():
    dashboard = InteractiveDashboard()
    dashboard.generate_all_dashboards()

if __name__ == "__main__":
    main()