# app.py - Flask Web Interface for Cyber Threat Intelligence
from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)

class ThreatIntelligenceAPI:
    def __init__(self):
        self.data_path = 'data/processed/threat_intelligence.json'
    
    def load_data(self):
        """Load threat intelligence data"""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_statistics(self):
        """Get overall statistics"""
        data = self.load_data()
        
        if not data:
            return {}
        
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        targets = [inc['threat_intelligence']['target'] for inc in data]
        
        cves = []
        for inc in data:
            cve = inc['threat_intelligence'].get('vulnerability', 'N/A')
            if 'CVE-' in cve:
                cves.append(cve)
        
        return {
            'total_incidents': len(data),
            'critical_count': sum(1 for s in severities if s == 'critical'),
            'high_count': sum(1 for s in severities if s == 'high'),
            'unique_attack_types': len(set(attack_types)),
            'unique_cves': len(set(cves)),
            'most_common_attack': Counter(attack_types).most_common(1)[0] if attack_types else ('N/A', 0),
            'most_targeted_sector': Counter(targets).most_common(1)[0] if targets else ('N/A', 0)
        }
    
    def get_recent_incidents(self, limit=10):
        """Get recent incidents"""
        data = self.load_data()
        return data[:limit]
    
    def search_incidents(self, query):
        """Search incidents by keyword"""
        data = self.load_data()
        query_lower = query.lower()
        
        results = []
        for inc in data:
            if (query_lower in inc['title'].lower() or 
                query_lower in inc.get('cleaned_text', '').lower() or
                query_lower in inc['threat_intelligence']['attack_type'].lower()):
                results.append(inc)
        
        return results
    
    def get_by_severity(self, severity):
        """Get incidents by severity"""
        data = self.load_data()
        return [inc for inc in data if inc['threat_intelligence']['severity'] == severity.lower()]
    
    def get_chart_data(self):
        """Get data for charts"""
        data = self.load_data()
        
        if not data:
            return {}
        
        attack_types = [inc['threat_intelligence']['attack_type'] for inc in data]
        severities = [inc['threat_intelligence']['severity'] for inc in data]
        targets = [inc['threat_intelligence']['target'] for inc in data]
        
        attack_counts = Counter(attack_types)
        severity_counts = Counter(severities)
        target_counts = Counter(targets)
        
        return {
            'attack_types': dict(attack_counts.most_common(10)),
            'severities': dict(severity_counts),
            'targets': dict(target_counts.most_common(10))
        }

api = ThreatIntelligenceAPI()

@app.route('/')
def index():
    """Main dashboard page"""
    stats = api.get_statistics()
    recent = api.get_recent_incidents(5)
    return render_template('index.html', stats=stats, recent=recent)

@app.route('/api/statistics')
def get_statistics():
    """API endpoint for statistics"""
    return jsonify(api.get_statistics())

@app.route('/api/incidents')
def get_incidents():
    """API endpoint for all incidents"""
    data = api.load_data()
    return jsonify(data)

@app.route('/api/incidents/recent')
def get_recent():
    """API endpoint for recent incidents"""
    limit = request.args.get('limit', 10, type=int)
    incidents = api.get_recent_incidents(limit)
    return jsonify(incidents)

@app.route('/api/search')
def search():
    """API endpoint for search"""
    query = request.args.get('q', '')
    results = api.search_incidents(query)
    return jsonify(results)

@app.route('/api/severity/<severity>')
def get_by_severity(severity):
    """API endpoint for incidents by severity"""
    incidents = api.get_by_severity(severity)
    return jsonify(incidents)

@app.route('/api/charts')
def get_charts():
    """API endpoint for chart data"""
    return jsonify(api.get_chart_data())

@app.route('/dashboard')
def dashboard():
    """Interactive dashboard page"""
    return render_template('dashboard.html')

@app.route('/search')
def search_page():
    """Search page"""
    query = request.args.get('q', '')
    results = api.search_incidents(query) if query else []
    return render_template('search.html', query=query, results=results)

@app.route('/incident/<int:incident_id>')
def incident_detail(incident_id):
    """Incident detail page"""
    data = api.load_data()
    if 0 <= incident_id < len(data):
        incident = data[incident_id]
        return render_template('incident_detail.html', incident=incident, incident_id=incident_id)
    return "Incident not found", 404

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 CYBER THREAT INTELLIGENCE WEB INTERFACE")
    print("="*70)
    print("\n🚀 Starting Flask server...")
    print("📍 Access the dashboard at: http://127.0.0.1:5000")
    print("\n⚠️  Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)