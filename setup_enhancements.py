# setup_enhancements.py - One script to set up all new features
import os

def create_flask_templates():
    """Create Flask HTML templates"""
    
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Base template
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Cyber Threat Intelligence{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .stat-card { border-radius: 15px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s; }
        .stat-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
        .critical { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .high { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
        .medium { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
        .low { background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); }
        .incident-card { border-left: 4px solid #667eea; margin: 10px 0; padding: 15px; background: white; border-radius: 8px; }
        .severity-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/"><i class="fas fa-shield-alt"></i> Cyber Threat Intelligence</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/"><i class="fas fa-home"></i> Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="/search"><i class="fas fa-search"></i> Search</a></li>
                    <li class="nav-item"><a class="nav-link" href="/dashboard"><i class="fas fa-chart-line"></i> Analytics</a></li>
                </ul>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>"""
    
    # Index page
    index_html = """{% extends "base.html" %}
{% block title %}Dashboard - Cyber Threat Intelligence{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-tachometer-alt"></i> Threat Intelligence Dashboard</h1>

<div class="row">
    <div class="col-md-3">
        <div class="stat-card critical">
            <h3>{{ stats.total_incidents }}</h3>
            <p><i class="fas fa-exclamation-triangle"></i> Total Incidents</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card high">
            <h3>{{ stats.critical_count }}</h3>
            <p><i class="fas fa-fire"></i> Critical Threats</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card medium">
            <h3>{{ stats.unique_attack_types }}</h3>
            <p><i class="fas fa-bug"></i> Attack Types</p>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card low">
            <h3>{{ stats.unique_cves }}</h3>
            <p><i class="fas fa-shield-virus"></i> CVEs Found</p>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white"><i class="fas fa-crosshairs"></i> Most Common Attack</div>
            <div class="card-body">
                <h4>{{ stats.most_common_attack[0] }}</h4>
                <p class="text-muted">{{ stats.most_common_attack[1] }} incidents</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white"><i class="fas fa-bullseye"></i> Most Targeted Sector</div>
            <div class="card-body">
                <h4>{{ stats.most_targeted_sector[0] }}</h4>
                <p class="text-muted">{{ stats.most_targeted_sector[1] }} incidents</p>
            </div>
        </div>
    </div>
</div>

<div class="mt-5">
    <h3><i class="fas fa-clock"></i> Recent Incidents</h3>
    {% for incident in recent %}
    <div class="incident-card">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h5><a href="/incident/{{ loop.index0 }}" class="text-decoration-none">{{ incident.title }}</a></h5>
                <p class="mb-2"><strong>Attack Type:</strong> {{ incident.threat_intelligence.attack_type }}</p>
                <p class="mb-0"><strong>Target:</strong> {{ incident.threat_intelligence.target }}</p>
            </div>
            <span class="severity-badge {% if incident.threat_intelligence.severity == 'critical' %}bg-danger{% elif incident.threat_intelligence.severity == 'high' %}bg-warning{% else %}bg-info{% endif %} text-white">
                {{ incident.threat_intelligence.severity|upper }}
            </span>
        </div>
    </div>
    {% endfor %}
</div>

<div class="text-center mt-4">
    <a href="/search" class="btn btn-primary btn-lg"><i class="fas fa-search"></i> Search All Incidents</a>
    <a href="/dashboard" class="btn btn-success btn-lg"><i class="fas fa-chart-bar"></i> View Analytics</a>
</div>
{% endblock %}"""
    
    # Search page
    search_html = """{% extends "base.html" %}
{% block title %}Search - Cyber Threat Intelligence{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-search"></i> Search Incidents</h1>

<form action="/search" method="get" class="mb-4">
    <div class="input-group input-group-lg">
        <input type="text" name="q" class="form-control" placeholder="Search by keyword, CVE, attack type..." value="{{ query }}">
        <button class="btn btn-primary" type="submit"><i class="fas fa-search"></i> Search</button>
    </div>
</form>

{% if query %}
<h3>Search Results for "{{ query }}" ({{ results|length }} found)</h3>
{% for incident in results %}
<div class="incident-card">
    <div class="d-flex justify-content-between">
        <div>
            <h5><a href="/incident/{{ loop.index0 }}">{{ incident.title }}</a></h5>
            <p><strong>Type:</strong> {{ incident.threat_intelligence.attack_type }} | 
               <strong>CVE:</strong> {{ incident.threat_intelligence.vulnerability }}</p>
        </div>
        <span class="severity-badge bg-{{ 'danger' if incident.threat_intelligence.severity == 'critical' else 'warning' }}">
            {{ incident.threat_intelligence.severity|upper }}
        </span>
    </div>
</div>
{% endfor %}
{% endif %}
{% endblock %}"""
    
    # Write files
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    with open('templates/search.html', 'w', encoding='utf-8') as f:
        f.write(search_html)
    
    print("✓ Created Flask templates")

def create_requirements_update():
    """Add new requirements"""
    new_requirements = """
# New features
flask==3.0.0
plotly==5.18.0
reportlab==4.0.7
"""
    
    with open('requirements_enhanced.txt', 'w') as f:
        f.write(new_requirements)
    
    print("✓ Created requirements_enhanced.txt")

def create_readme():
    """Create updated README"""
    readme = """# Cyber Threat Intelligence System - Enhanced

## 🆕 New Features Added

### 1. Interactive Dashboards (Plotly)
- Beautiful, interactive charts
- Zoom, pan, hover tooltips
- Export to PNG
- Run: `python src/dashboard.py`

### 2. Web Interface (Flask)
- Professional web dashboard
- Search functionality
- Real-time statistics
- Run: `python app.py`
- Access: http://127.0.0.1:5000

### 3. PDF Reports
- Automated report generation
- Professional formatting
- Run: `python src/pdf_report.py`

### 4. Email Alerts
- Sends alerts for critical threats
- Configurable recipients
- Setup: Add email credentials to config

## Installation

```bash
# Install new dependencies
pip install -r requirements_enhanced.txt

# Or install individually
pip install flask plotly reportlab
```

## Usage

1. **Run Web Interface:**
   ```bash
   python app.py
   ```
   Open http://127.0.0.1:5000

2. **Generate Interactive Dashboards:**
   ```bash
   python src/dashboard.py
   ```
   Open `dashboard/comprehensive_dashboard.html`

3. **Generate PDF Report:**
   ```bash
   python src/pdf_report.py
   ```

## Features

✅ Automated OSINT collection
✅ GPT-powered analysis
✅ Interactive dashboards
✅ Web interface with search
✅ PDF reports
✅ Email alerts
✅ Database storage

## Team
- P. Venkata Sai Anish (22EG105A45)
- D. Harshith Reddy (22EG105A21)
- S. Varaprasad (22EG105A51)
- T. Akshara (22EG105A65)

Guide: Dr. G. Vishnu Murthy
"""
    
    with open('README_ENHANCED.md', 'w') as f:
        f.write(readme)
    
    print("✓ Created README_ENHANCED.md")

def main():
    print("\n" + "="*70)
    print("🚀 SETTING UP ENHANCED FEATURES")
    print("="*70 + "\n")
    
    create_flask_templates()
    create_requirements_update()
    create_readme()
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Install new requirements:")
    print("   pip install flask plotly reportlab")
    print("\n2. Run interactive dashboard:")
    print("   python src/dashboard.py")
    print("\n3. Run web interface:")
    print("   python app.py")
    print("\n4. Access at: http://127.0.0.1:5000")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()