# update_templates.py - Update templates with embedded visualizations
import os

def update_dashboard_template():
    """Update dashboard.html with embedded charts"""
    
    dashboard_content = """{% extends "base.html" %}
{% block title %}Analytics Dashboard - Cyber Threat Intelligence{% endblock %}

{% block content %}
<h1 class="mb-4"><i class="fas fa-chart-line"></i> Interactive Analytics Dashboard</h1>

<div class="alert alert-info">
    <i class="fas fa-info-circle"></i> <strong>Tip:</strong> All charts are interactive! Zoom, pan, and hover for details.
</div>

<!-- Statistics Cards Row -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-danger">
            <div class="card-body text-center">
                <h2 id="total-incidents">0</h2>
                <p><i class="fas fa-exclamation-triangle"></i> Total Incidents</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body text-center">
                <h2 id="critical-count">0</h2>
                <p><i class="fas fa-fire"></i> Critical Threats</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body text-center">
                <h2 id="attack-types-count">0</h2>
                <p><i class="fas fa-bug"></i> Attack Types</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body text-center">
                <h2 id="cve-count">0</h2>
                <p><i class="fas fa-shield-virus"></i> CVEs Found</p>
            </div>
        </div>
    </div>
</div>

<!-- Charts Container -->
<div class="row">
    <!-- Attack Types Chart -->
    <div class="col-md-6 mb-4">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h5><i class="fas fa-chart-bar"></i> Attack Types Distribution</h5>
            </div>
            <div class="card-body">
                <div id="attack-types-chart" style="height: 400px;"></div>
            </div>
        </div>
    </div>

    <!-- Severity Chart -->
    <div class="col-md-6 mb-4">
        <div class="card shadow">
            <div class="card-header bg-danger text-white">
                <h5><i class="fas fa-chart-pie"></i> Severity Distribution</h5>
            </div>
            <div class="card-body">
                <div id="severity-chart" style="height: 400px;"></div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- Target Sectors Chart -->
    <div class="col-md-6 mb-4">
        <div class="card shadow">
            <div class="card-header bg-success text-white">
                <h5><i class="fas fa-bullseye"></i> Most Targeted Sectors</h5>
            </div>
            <div class="card-body">
                <div id="targets-chart" style="height: 400px;"></div>
            </div>
        </div>
    </div>

    <!-- Timeline Chart -->
    <div class="col-md-6 mb-4">
        <div class="card shadow">
            <div class="card-header bg-warning text-white">
                <h5><i class="fas fa-calendar-alt"></i> Incident Timeline</h5>
            </div>
            <div class="card-body">
                <div id="timeline-chart" style="height: 400px;"></div>
            </div>
        </div>
    </div>
</div>

<!-- CVE Analysis -->
<div class="row">
    <div class="col-12 mb-4">
        <div class="card shadow">
            <div class="card-header bg-dark text-white">
                <h5><i class="fas fa-bug"></i> Top CVE Vulnerabilities</h5>
            </div>
            <div class="card-body">
                <div id="cve-chart" style="height: 400px;"></div>
            </div>
        </div>
    </div>
</div>

<!-- Action Buttons -->
<div class="text-center mt-4 mb-4">
    <a href="/" class="btn btn-primary btn-lg"><i class="fas fa-home"></i> Back to Dashboard</a>
    <a href="/search" class="btn btn-success btn-lg"><i class="fas fa-search"></i> Search Incidents</a>
</div>

{% endblock %}

{% block scripts %}
<script>
fetch('/api/charts')
    .then(response => response.json())
    .then(data => {
        createAllCharts(data);
        loadStatistics();
    });

function loadStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(stats => {
            document.getElementById('total-incidents').textContent = stats.total_incidents || 0;
            document.getElementById('critical-count').textContent = stats.critical_count || 0;
            document.getElementById('attack-types-count').textContent = stats.unique_attack_types || 0;
            document.getElementById('cve-count').textContent = stats.unique_cves || 0;
        });
}

function createAllCharts(data) {
    // 1. Attack Types
    Plotly.newPlot('attack-types-chart', [{
        x: Object.keys(data.attack_types),
        y: Object.values(data.attack_types),
        type: 'bar',
        marker: {
            color: Object.values(data.attack_types),
            colorscale: 'Reds'
        }
    }], {
        xaxis: { tickangle: -45 },
        margin: { b: 100 }
    }, {responsive: true});

    // 2. Severity
    const sevColors = {'critical': '#e74c3c', 'high': '#f39c12', 'medium': '#3498db', 'low': '#2ecc71'};
    const sevOrder = ['critical', 'high', 'medium', 'low'];
    
    Plotly.newPlot('severity-chart', [{
        labels: sevOrder.filter(s => data.severities[s]).map(s => s.toUpperCase()),
        values: sevOrder.filter(s => data.severities[s]).map(s => data.severities[s]),
        type: 'pie',
        marker: { colors: sevOrder.filter(s => data.severities[s]).map(s => sevColors[s]) },
        hole: 0.4
    }], {margin: { t: 20 }}, {responsive: true});

    // 3. Targets
    Plotly.newPlot('targets-chart', [{
        y: Object.keys(data.targets),
        x: Object.values(data.targets),
        type: 'bar',
        orientation: 'h',
        marker: { color: '#2ecc71' }
    }], {margin: { l: 150 }}, {responsive: true});

    // 4. Timeline
    fetch('/api/incidents')
        .then(response => response.json())
        .then(incidents => {
            const dates = {};
            incidents.forEach(inc => dates[inc.date] = (dates[inc.date] || 0) + 1);
            const sorted = Object.keys(dates).sort();
            
            Plotly.newPlot('timeline-chart', [{
                x: sorted,
                y: sorted.map(d => dates[d]),
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#e74c3c', width: 3 },
                fill: 'tozeroy'
            }], {}, {responsive: true});

            // 5. CVEs
            const cves = {};
            incidents.forEach(inc => {
                const cve = inc.threat_intelligence?.vulnerability;
                if (cve && cve.includes('CVE-')) cves[cve] = (cves[cve] || 0) + 1;
            });
            
            const topCVEs = Object.entries(cves).sort((a,b) => b[1]-a[1]).slice(0, 10);
            
            if (topCVEs.length > 0) {
                Plotly.newPlot('cve-chart', [{
                    x: topCVEs.map(c => c[0]),
                    y: topCVEs.map(c => c[1]),
                    type: 'bar',
                    marker: { color: '#e67e22' }
                }], { xaxis: { tickangle: -45 }, margin: { b: 100 }}, {responsive: true});
            } else {
                document.getElementById('cve-chart').innerHTML = 
                    '<div class="alert alert-info">No CVEs in dataset</div>';
            }
        });
}
</script>
{% endblock %}
"""
    
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print("✅ Updated templates/dashboard.html")

def main():
    print("\n" + "="*70)
    print("🔄 UPDATING TEMPLATES WITH EMBEDDED VISUALIZATIONS")
    print("="*70 + "\n")
    
    if not os.path.exists('templates'):
        print("❌ templates/ folder not found!")
        print("   Run: python setup_enhancements.py first")
        return
    
    # Backup old file if exists
    if os.path.exists('templates/dashboard.html'):
        os.rename('templates/dashboard.html', 'templates/dashboard.html.backup')
        print("📦 Backed up old dashboard.html")
    
    update_dashboard_template()
    
    print("\n" + "="*70)
    print("✅ TEMPLATES UPDATED SUCCESSFULLY!")
    print("="*70)
    print("\nNext steps:")
    print("1. Restart Flask server:")
    print("   python app.py")
    print("\n2. Visit:")
    print("   http://127.0.0.1:5000/dashboard")
    print("\n3. You'll see 5 interactive charts embedded!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()