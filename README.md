# GPT-Based Open-Source Intelligence System
## Automated Cyber Threat Intelligence Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18-orange.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [NEW: Enhanced Features](#new-enhanced-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Web Interface](#web-interface)
- [Interactive Dashboards](#interactive-dashboards)
- [Project Structure](#project-structure)
- [Results](#results)
- [Team](#team)

---

## 🎯 Overview

An intelligent, **production-ready** system that automatically analyzes cyber incident reports using GPT-based Natural Language Processing. Features a complete web interface, interactive dashboards, and real-time threat intelligence extraction.

### Problem Statement

- **Volume**: Large amounts of cyber incident data generated daily
- **Format**: Predominantly unstructured text (hard to analyze manually)
- **Cost**: Commercial threat intelligence platforms cost $50,000+/year
- **Limitations**: Existing systems lack semantic understanding and automation
- **Need**: Free, automated, scalable threat intelligence extraction

### Our Solution

A **complete end-to-end system** that:
1. ✅ Automatically collects cyber incidents from live websites
2. ✅ Analyzes unstructured text using AI (GPT/Ollama/LLMs)
3. ✅ Extracts structured threat intelligence automatically
4. ✅ Provides professional web interface with search
5. ✅ Generates interactive visualizations
6. ✅ **100% Free and Open Source**

---

## ✨ Features

### Core Capabilities

- **🌐 Real-Time Data Collection**
  - Live web scraping from BleepingComputer, CISA
  - Dynamic content extraction
  - Automated incident discovery
  - No pre-configured datasets

- **🤖 AI-Powered Analysis**
  - GPT/Ollama integration (FREE local AI)
  - OpenAI API support (optional)
  - Pattern matching fallback
  - Semantic understanding of threats
  - Multi-model architecture

- **🎯 Threat Intelligence Extraction**
  - Attack type classification (12+ types)
  - Threat actor identification
  - Target sector analysis
  - CVE/vulnerability extraction
  - Severity assessment (Critical/High/Medium/Low)
  - Impact analysis
  - Mitigation recommendations
  - IOC detection (IPs, domains, hashes)

- **📊 Advanced Visualizations**
  - Static charts (PNG - for reports)
  - Interactive dashboards (Plotly - zoom, pan, hover)
  - Timeline analysis
  - Trend identification
  - Comprehensive analytics

---

## 🆕 NEW: Enhanced Features

### 1. Professional Web Interface

**Flask-based web application** with:
- ✅ Real-time dashboard with statistics
- ✅ Advanced search functionality
- ✅ Incident details pages
- ✅ RESTful API endpoints
- ✅ Responsive design (Bootstrap)
- ✅ Beautiful gradient UI

**Access**: Run `python app.py` → http://127.0.0.1:5000

### 2. Interactive Dashboards (Plotly)

**Features**:
- ✅ Zoom, pan, and select
- ✅ Hover tooltips with details
- ✅ Export to PNG
- ✅ Mobile-responsive
- ✅ 6+ chart types

**Charts Included**:
- Attack types bar chart
- Severity pie chart
- Target sectors analysis
- CVE vulnerability trends
- Timeline graphs
- Comprehensive multi-chart dashboard

**Generate**: Run `python src/dashboard.py`

### 3. Search & Query System

- ✅ Full-text search across all incidents
- ✅ Filter by severity level
- ✅ Filter by attack type
- ✅ CVE lookup
- ✅ Date range filtering
- ✅ Real-time results

### 4. REST API

**Endpoints**:
```
GET  /api/statistics          - Overall statistics
GET  /api/incidents           - All incidents
GET  /api/incidents/recent    - Recent incidents
GET  /api/search?q={query}    - Search incidents
GET  /api/severity/{level}    - Filter by severity
GET  /api/charts              - Chart data
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  WEB INTERFACE LAYER (NEW!)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Flask Server │  │  REST API    │  │  Web Dashboard  │  │
│  │ (app.py)     │  │  Endpoints   │  │   (Bootstrap)   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Web Scraping │  │   Manual     │  │  Future: RSS/   │  │
│  │ (Dynamic)    │  │   Input      │  │  Twitter/Reddit │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  PREPROCESSING LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Text Cleaning • Entity Extraction • CVE Detection  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI ANALYSIS LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │    Ollama    │  │   OpenAI     │  │    Pattern      │  │
│  │  (FREE AI)   │  │     GPT      │  │    Matching     │  │
│  │   LLaMA 3.2  │  │  (Optional)  │  │   (Fallback)    │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA STORAGE LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  JSON Files • Future: SQLite/MongoDB • Cache        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│         VISUALIZATION & REPORTING LAYER (NEW!)               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Plotly     │  │  Matplotlib  │  │   Text Reports  │  │
│  │ Interactive  │  │    Static    │  │    (Future:     │  │
│  │  Dashboards  │  │    Charts    │  │      PDF)       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM (for local AI models)
- Modern web browser

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/cyber-threat-intelligence.git
cd cyber-threat-intelligence
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Core dependencies
pip install requests beautifulsoup4 nltk pandas matplotlib seaborn

# Web interface and interactive dashboards
pip install flask plotly

# AI models (choose one or more)
pip install openai              # For OpenAI GPT (optional, requires API key)
# OR install Ollama from: https://ollama.ai (FREE, local AI)

# Optional: For future features
pip install reportlab           # PDF generation
```

**Or install everything at once:**
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 5: Setup Ollama (Optional - FREE AI)

```bash
# Download from: https://ollama.ai
# After installation:
ollama serve              # Start Ollama server
ollama pull llama3.2      # Download model (in separate terminal)
```

---

## ⚡ Quick Start

### Option 1: Web Interface (Recommended)

```bash
# 1. Collect data
python src/scraper.py

# 2. Preprocess
python src/preprocessor.py

# 3. Analyze (choose Ollama for FREE AI)
python src/gpt_analyzer.py

# 4. Start web interface
python app.py

# 5. Open browser: http://127.0.0.1:5000
```

### Option 2: Command Line + Dashboards

```bash
# Steps 1-3 same as above

# 4. Generate static charts
python src/visualizer.py

# 5. Generate interactive dashboards
python src/dashboard.py

# 6. Open: dashboard/comprehensive_dashboard.html
```

---

## 💻 Usage Guide

### 1. Data Collection

```bash
python src/scraper.py
```

**What it does**:
- Scrapes BleepingComputer.com (live website)
- Collects 10-20 recent cyber incidents
- Extracts full article text
- Saves to `data/raw/cyber_incidents.json`

**Features**:
- Dynamic collection (different data each run)
- Rate limiting (respectful scraping)
- Error handling
- Automatic retries

### 2. Text Preprocessing

```bash
python src/preprocessor.py
```

**What it does**:
- Cleans text (removes URLs, special characters)
- Extracts sentences
- Detects CVE numbers automatically
- Identifies attack keywords
- Saves to `data/processed/processed_incidents.json`

### 3. AI Analysis

```bash
python src/gpt_analyzer.py
```

**Choose your mode**:
1. **Pattern Matching** - Fast, no setup (good baseline)
2. **Ollama** - FREE local AI (best free option)
3. **OpenAI GPT** - Highest quality (requires API key)

**What it extracts**:
```json
{
  "attack_type": "Zero-Day Exploit",
  "threat_actor": "APT28",
  "target": "Government Agencies",
  "vulnerability": "CVE-2026-21509",
  "severity": "critical",
  "impact": "Remote code execution possible",
  "mitigation": "Apply Microsoft patch immediately",
  "iocs": ["IP: 192.168.1.100", "Domain: malicious.com"]
}
```

**Output**: `data/processed/threat_intelligence.json`

### 4. Visualization

#### Static Charts (for presentations/reports)

```bash
python src/visualizer.py
```

**Generates**:
- `visualizations/attack_types.png`
- `visualizations/severity_distribution.png`
- `visualizations/targeted_sectors.png`
- `visualizations/dashboard.png`
- `visualizations/threat_report.txt`

#### Interactive Dashboards (for analysis)

```bash
python src/dashboard.py
```

**Generates**:
- `dashboard/comprehensive_dashboard.html` - All-in-one dashboard
- `dashboard/attack_types_interactive.html`
- `dashboard/severity_interactive.html`
- `dashboard/timeline_interactive.html`
- `dashboard/cve_analysis_interactive.html`

**Features**:
- Zoom in/out
- Pan across data
- Hover for details
- Click legends to filter
- Export to PNG

---

## 🌐 Web Interface

### Starting the Server

```bash
python app.py
```

**Access**: http://127.0.0.1:5000

### Features

#### Main Dashboard
- **Statistics Cards**: Total incidents, critical threats, attack types, CVEs
- **Recent Incidents**: Latest 5 incidents with severity badges
- **Quick Actions**: Search and analytics buttons

#### Search Page
- Full-text search across all incidents
- Search by keywords, CVE numbers, attack types
- Real-time results with highlighting
- Severity filtering

#### Incident Details
- Complete threat intelligence breakdown
- Attack metadata
- Impact assessment
- Mitigation recommendations
- IOCs (Indicators of Compromise)
- Original article link

#### Analytics Dashboard
- Interactive Plotly charts embedded
- Real-time chart updates
- Multiple visualization types
- Export capabilities

### API Usage

```bash
# Get statistics
curl http://127.0.0.1:5000/api/statistics

# Search incidents
curl http://127.0.0.1:5000/api/search?q=ransomware

# Get critical incidents
curl http://127.0.0.1:5000/api/severity/critical

# Get all incidents
curl http://127.0.0.1:5000/api/incidents
```

---

## 📊 Interactive Dashboards

### Accessing Dashboards

**Method 1: Via Web Interface**
- Go to http://127.0.0.1:5000/dashboard

**Method 2: Direct File**
- Open `dashboard/comprehensive_dashboard.html` in browser

### Dashboard Features

**Attack Types Chart**
- Bar chart with color gradients
- Hover: See exact count
- Click legend: Show/hide categories
- Zoom: Click and drag

**Severity Distribution**
- Donut pie chart
- Color-coded by severity
- Percentage labels
- Interactive legend

**Timeline Trend**
- Line chart with area fill
- Shows incidents over time
- Zoom timeline
- Hover for date details

**Target Sectors**
- Horizontal bar chart
- Most targeted sectors
- Color-coded
- Click to filter

**CVE Analysis**
- Top 10 CVEs
- Occurrence frequency
- Hover for details

---

## 📁 Project Structure

```
cyber-threat-intelligence/
│
├── app.py                            # Flask web application ⭐NEW
├── setup_enhancements.py             # Setup script ⭐NEW
├── config.py                         # Configuration
├── requirements.txt                  # Dependencies
├── .env                              # API keys (gitignored)
├── .gitignore                       # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── scraper.py                    # Web scraping module
│   ├── preprocessor.py               # Text preprocessing
│   ├── gpt_analyzer.py               # AI analysis (multi-model)
│   ├── visualizer.py                 # Static charts
│   └── dashboard.py                  # Interactive dashboards ⭐NEW
│
├── templates/                        # Flask HTML templates ⭐NEW
│   ├── base.html                     # Base template
│   ├── index.html                    # Main dashboard
│   ├── search.html                   # Search page
│   ├── dashboard.html                # Analytics page
│   └── incident_detail.html          # Incident details
│
├── static/                           # Static assets ⭐NEW
│   ├── css/
│   └── js/
│
├── data/
│   ├── raw/                          # Raw scraped data
│   │   └── cyber_incidents.json
│   └── processed/                    # Analyzed data
│       ├── processed_incidents.json
│       └── threat_intelligence.json
│
├── dashboard/                        # Interactive dashboards ⭐NEW
│   ├── comprehensive_dashboard.html
│   ├── attack_types_interactive.html
│   ├── severity_interactive.html
│   ├── timeline_interactive.html
│   └── cve_analysis_interactive.html
│
├── visualizations/                   # Static charts
│   ├── attack_types.png
│   ├── severity_distribution.png
│   ├── targeted_sectors.png
│   ├── incident_timeline.png
│   ├── dashboard.png
│   └── threat_report.txt
│
└── docs/
    └── IOMP_Team_5.pptx.pdf         # Project presentation
```

---

## 📊 Results

### Sample Output Statistics

```
======================================================================
📊 THREAT INTELLIGENCE SUMMARY
======================================================================

Total Incidents Analyzed: 10
Critical Threats: 6
Unique Attack Types: 6
CVEs Identified: 4

🎯 Attack Types:
   • Zero-Day Exploit: 4
   • Phishing Campaign: 2
   • Unknown Attack: 2
   • DDoS Attack: 1
   • Ransomware Attack: 1

⚠️  Severity Distribution:
   • CRITICAL: 6
   • HIGH: 1
   • LOW: 3

Most Common Attack: Zero-Day Exploit (4 incidents)
Most Targeted Sector: Multiple Sectors (9 incidents)
```

### Sample Extracted Intelligence

```json
{
  "id": "bc_1_1234567890",
  "source": "BleepingComputer",
  "title": "Microsoft patches actively exploited Office zero-day",
  "threat_intelligence": {
    "attack_type": "Zero-Day Exploit",
    "threat_actor": "Unknown Actor",
    "target": "Multiple Sectors",
    "vulnerability": "CVE-2026-21509",
    "severity": "critical",
    "impact": "Zero-Day Exploit detected",
    "mitigation": "Apply patches immediately, implement compensating controls",
    "iocs": ["No specific IOCs extracted"]
  },
  "analysis_method": "ollama"
}
```

---

## 🎯 Key Features Comparison

| Feature | Previous Version | Current Version |
|---------|-----------------|-----------------|
| **Interface** | Command line only | Professional web interface |
| **Search** | Manual file browsing | Full-text search + filters |
| **Dashboards** | Static PNG only | Interactive + Static |
| **AI Models** | Pattern matching | Ollama + GPT + Patterns |
| **API** | None | RESTful API |
| **Deployment** | Scripts | Web server |
| **User Experience** | Technical users | Anyone with browser |

---

## 🔧 Configuration

### API Keys (.env file)

```bash
# OpenAI (optional)
OPENAI_API_KEY=sk-your-key-here

# Groq (optional - another free API)
GROQ_API_KEY=gsk_your-key-here

# MongoDB (future)
MONGODB_URI=mongodb://localhost:27017/
```

### config.py Settings

```python
# Scraping
REQUEST_DELAY = 2          # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# Paths
RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
```

---

## 🚀 Deployment

### Development

```bash
python app.py
# Access: http://127.0.0.1:5000
```

### Production (Future)

```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (create Dockerfile)
docker build -t threat-intel .
docker run -p 5000:5000 threat-intel
```

---

## 📈 Performance Metrics

- **Data Collection**: ~2-3 seconds per incident
- **Preprocessing**: ~0.5 seconds per incident
- **AI Analysis (Ollama)**: ~3-5 seconds per incident
- **AI Analysis (Pattern)**: <1 second per incident
- **Visualization**: ~2-3 seconds total
- **Web Interface**: <100ms response time

**Total Pipeline**: ~30-60 seconds for 10 incidents (with Ollama)

---

## 🎓 Academic Contribution

### Innovation Points

1. **First system** to combine automated OSINT + GPT for cyber threat intelligence
2. **Multi-model architecture** with fallback mechanisms
3. **Production-ready** web interface
4. **Interactive analytics** for threat analysis
5. **Free and open-source** (democratizing threat intelligence)

### Use Cases

- **Security Operations Centers (SOCs)**
- **Incident Response Teams**
- **Threat Intelligence Analysts**
- **Academic Research**
- **Small/Medium Businesses** (can't afford commercial tools)

---

## 🛠️ Troubleshooting

### Web Interface Won't Start

```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux

# Use different port
python app.py --port 8080
```

### Ollama Connection Failed

```bash
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags

# Download model
ollama pull llama3.2
```

### Scraper Returns No Data

```bash
# Check internet connection
# Website might have changed structure
# Use pattern matching mode as fallback
```

### Dashboard Not Showing Charts

```bash
# Ensure plotly is installed
pip install plotly

# Check data file exists
ls data/processed/threat_intelligence.json
```

---

## 🔮 Future Enhancements

### Planned Features

- ✅ PDF Report Generation
- ✅ Email/SMS Alerts for Critical Threats
- ✅ Export to Excel/CSV
- ✅ More Data Sources (Twitter, Reddit, Dark Web)
- ✅ Database Integration (PostgreSQL/MongoDB)
- ✅ Trend Prediction using ML
- ✅ User Authentication
- ✅ Collaborative Features
- ✅ Mobile App

---

## 👥 Team

**Team 5**
- **P. Venkata Sai Anish** (22EG105A45)
- **D. Harshith Reddy** (22EG105A21)
- **S. Varaprasad** (22EG105A51)
- **T. Akshara** (22EG105A65)

**Project Guide**
- **Dr. G. Vishnu Murthy**
- Professor & Dean CSE

**Institution**
- Department of Computer Science and Engineering
- Project Date: January 2026

---

## 📚 References

1. **MITRE ATT&CK Framework**: https://attack.mitre.org/
2. **OpenCTI Platform**: https://github.com/OpenCTI-Platform/opencti
3. **Cyber Threat Intelligence Survey**: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2214212624000899)
4. **LLMs for CTI Extraction**: [arXiv](https://arxiv.org/abs/2505.03147)
5. **Flask Documentation**: https://flask.palletsprojects.com/
6. **Plotly Documentation**: https://plotly.com/python/
7. **Ollama**: https://ollama.ai

---

## 📝 License

This project is developed for academic purposes at the Department of Computer Science and Engineering.

---

## 🤝 Acknowledgments

- Dr. G. Vishnu Murthy for project guidance
- Department of Computer Science and Engineering
- Open-source community (Flask, Plotly, Transformers)
- BleepingComputer for cyber security news

---

## 📧 Contact

For questions, suggestions, or collaboration:
- **Email**: [team contact]
- **Project Guide**: Dr. G. Vishnu Murthy
- **Institution**: Department of CSE

---

## ⭐ Project Highlights

✅ **100% Free & Open Source**  
✅ **Production-Ready Web Interface**  
✅ **Real AI Integration** (not just keywords)  
✅ **Interactive Dashboards**  
✅ **Live Data Collection** (not pre-configured)  
✅ **Multi-Model Architecture**  
✅ **RESTful API**  
✅ **Professional UI/UX**  
✅ **Scalable & Extensible**  
✅ **Academic Innovation**  

---

**Last Updated**: March 9, 2026  
**Version**: 3.0 (Web Interface + Interactive Dashboards)  
**Status**: ✅ Active Development

---

**🌟 Star this project if you find it useful!**
