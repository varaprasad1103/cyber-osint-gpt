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
- [Enhanced Features](#new-enhanced-features)
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
  - Live web scraping from BleepingComputer
  - Dynamic content extraction with deduplication
  - Automated incident discovery
  - No pre-configured datasets

- **🤖 AI-Powered Analysis**
  - GPT/Ollama integration (FREE local AI)
  - OpenAI API support (optional)
  - Pattern matching fallback
  - Semantic understanding of threats
  - Multi-model architecture with cross-validation

- **🎯 Threat Intelligence Extraction**
  - Attack type classification (12+ types)
  - Threat actor identification
  - Target sector analysis (11 sectors)
  - CVE/vulnerability extraction via regex
  - Severity assessment (Critical/High/Medium/Low)
  - Impact analysis
  - Mitigation recommendations
  - IOC detection (IPs, domains, hashes)

- **📊 Advanced Visualizations**
  - Interactive dashboards (Plotly - zoom, pan, hover)
  - Timeline analysis
  - Trend identification
  - Comprehensive analytics

---

## 🆕 Enhanced Features

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
│                  WEB INTERFACE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Flask Server │  │  REST API    │  │  Web Dashboard  │  │
│  │ (app.py)     │  │  Endpoints   │  │   (Bootstrap)   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Web Scraping │  │ Deduplication│  │  Future: RSS/   │  │
│  │ (Dynamic)    │  │   Filter     │  │  Twitter/Reddit │  │
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
│              VISUALIZATION & REPORTING LAYER                 │
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
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests beautifulsoup4 flask plotly python-dotenv openai
```

### Step 4: Setup Ollama (Optional - FREE AI)

```bash
# Download from: https://ollama.ai
ollama serve              # Start Ollama server
ollama pull llama3.2      # Download model (separate terminal)
```

---

## ⚡ Quick Start

```bash
# 1. Collect data
python src/scraper.py

# 2. Preprocess
python src/preprocessor.py

# 3. Analyze
python src/gpt_analyzer.py    # Choose mode: 1=Pattern, 2=Ollama, 3=OpenAI

# 4. Start web interface
python app.py

# 5. Open browser
# http://127.0.0.1:5000
```

---

## 💻 Usage Guide

### 1. Data Collection

```bash
python src/scraper.py
```

- Scrapes BleepingComputer.com live
- Deduplicates articles automatically
- Detects and logs CVEs found in articles
- Saves to `data/raw/cyber_incidents.json`

### 2. Text Preprocessing

```bash
python src/preprocessor.py
```

- Cleans text (removes URLs, special characters)
- Extracts sentences and word counts
- Detects CVE numbers via regex (`CVE-YYYY-NNNNN`)
- Identifies attack keywords
- Saves to `data/processed/processed_incidents.json`

### 3. AI Analysis

```bash
python src/gpt_analyzer.py
```

**Choose your mode**:
1. **Pattern Matching** — Fast, no setup, deterministic results
2. **Ollama** — FREE local AI using LLaMA 3.2
3. **OpenAI GPT** — Highest quality (requires API key)

**What it extracts**:
```json
{
  "attack_type": "APT Campaign",
  "threat_actor": "APT28",
  "target": "Government",
  "vulnerability": "CVE-2026-21509",
  "severity": "critical",
  "impact": "Long-term espionage operations detected",
  "mitigation": "Threat hunt across environment, isolate compromised systems",
  "iocs": ["No specific IOCs extracted"]
}
```

**Note on CVE**: CVE shows `N/A` when an article does not mention a specific software vulnerability ID. This is correct behavior — phishing and AI-abuse articles have no CVE because they exploit human behavior, not software flaws.

**Output**: `data/processed/threat_intelligence.json`

---

## 🌐 Web Interface

```bash
python app.py
# Access: http://127.0.0.1:5000
```

### Pages

- **/** — Main dashboard with statistics, recent incidents, quick charts
- **/search** — Full-text search across all incidents
- **/incident/<id>** — Full threat intelligence detail page
- **/dashboard** — Interactive Plotly analytics

### API Endpoints

```bash
curl http://127.0.0.1:5000/api/statistics
curl http://127.0.0.1:5000/api/search?q=ransomware
curl http://127.0.0.1:5000/api/severity/critical
curl http://127.0.0.1:5000/api/incidents
```

---

## 📁 Project Structure

```
cyber-osint-gpt/
│
├── app.py                        # Flask web application
├── config.py                     # Configuration settings
├── requirements.txt              # Dependencies
├── .env                          # API keys (gitignored)
│
├── src/
│   ├── scraper.py                # Web scraping + deduplication
│   ├── preprocessor.py           # Text cleaning + CVE extraction
│   ├── gpt_analyzer.py           # AI analysis (multi-model)
│   ├── visualizer.py             # Text reports
│   └── dashboard.py              # Interactive Plotly dashboards
│
├── templates/
│   ├── base.html
│   ├── index.html                # Main dashboard
│   ├── search.html
│   ├── dashboard.html
│   └── incident_detail.html
│
├── data/
│   ├── raw/
│   │   └── cyber_incidents.json
│   └── processed/
│       ├── processed_incidents.json
│       └── threat_intelligence.json
│
└── dashboard/
    ├── comprehensive_dashboard.html
    ├── attack_types_interactive.html
    ├── severity_interactive.html
    ├── timeline_interactive.html
    └── cve_analysis_interactive.html
```

---

## 📊 Results

### Actual Pipeline Output (March 10, 2026)

```
======================================================================
🧹 TEXT PREPROCESSOR
======================================================================

Total incidents: 10
Total words: 6,705
CVEs detected: 8
Average words per incident: 670
```

```
======================================================================
📊 THREAT INTELLIGENCE SUMMARY (Ollama Mode)
======================================================================

Total Incidents Analyzed: 10

🎯 Attack Types:
   • Phishing Campaign: 4
   • APT Campaign: 2
   • Security Incident: 2
   • Vulnerability Exploit: 2

⚠️  Severity Distribution:
   • CRITICAL: 3
   • HIGH: 4
   • MEDIUM: 2
   • LOW: 1

🎯 Top Targeted Sectors:
   • Government: 4
   • Enterprise: 2
   • Developers: 2
   • Technology: 2

🔍 CVEs Identified: 3
```

### Sample Extracted Intelligence

```json
{
  "id": "bc_7_1741608000",
  "source": "BleepingComputer",
  "title": "APT28 hackers deploy customized variant of Covenant open-source tool",
  "threat_intelligence": {
    "attack_type": "APT Campaign",
    "threat_actor": "APT28",
    "target": "Government",
    "vulnerability": "CVE-2026-21509",
    "severity": "critical",
    "impact": "Long-term espionage operations using custom C2 framework",
    "mitigation": "Threat hunt across environment, isolate compromised systems",
    "iocs": ["No specific IOCs extracted"]
  },
  "analysis_method": "ollama"
}
```

### Articles Analyzed (March 10, 2026)

| # | Title | Attack Type | Target | CVE |
|---|-------|-------------|--------|-----|
| 1 | Hackers abuse .arpa DNS and ipv6 to evade phishing | Phishing Campaign | Government | N/A |
| 2 | Microsoft: Hackers abusing AI at every stage | APT Campaign | Enterprise | N/A |
| 3 | Fake Claude Code install guides push infostealers | Phishing Campaign | Developers | N/A |
| 4 | Microsoft 365 Backup file-level restore | Security Incident | Technology | N/A |
| 5 | CISA: Ivanti EPM flaw actively exploited | Vulnerability Exploit | Government | CVE-2026-1603 |
| 6 | Microsoft Windows hotpatch security updates | Security Incident | Technology | N/A |
| 7 | APT28 deploy Covenant open-source tool | APT Campaign | Government | CVE-2026-21509 |
| 8 | Microsoft Teams phishing with A0Backdoor | Phishing Campaign | Enterprise | N/A |
| 9 | Google: Cloud attacks exploit flaws | Vulnerability Exploit | Developers | CVE-2025-55182 |
| 10 | Dutch govt warns Signal/WhatsApp hijacking | Phishing Campaign | Government | N/A |

---

## 🎯 Key Features Comparison

| Feature | Previous Version | Current Version |
|---------|-----------------|-----------------|
| **Interface** | Command line only | Professional web interface |
| **Search** | Manual file browsing | Full-text search + filters |
| **Dashboards** | Static PNG only | Interactive Plotly |
| **AI Models** | Pattern matching only | Ollama + GPT + Patterns |
| **Target Detection** | Often incorrect | Title-first + body cross-validation |
| **Deduplication** | None | URL + title dedup |
| **API** | None | RESTful API |
| **Attack Labels** | "Unknown Attack" | 12 specific attack types |
| **Sector Labels** | "Multiple Sectors" | 11 named sectors |

---

## 🔧 Configuration

### .env file

```bash
# OpenAI (optional)
OPENAI_API_KEY=sk-your-key-here
```

### config.py

```python
REQUEST_DELAY = 2       # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30
RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
```

---

## 🛠️ Troubleshooting

### Ollama Timeout

```bash
# Reduce article text sent to Ollama (already set to 800 chars in analyzer)
# Or switch to pattern matching mode (choice 1) for consistent fast results
```

### Web Interface Won't Start

```bash
netstat -ano | findstr :5000   # Check if port is in use (Windows)
```

### UnicodeDecodeError on Windows

```python
# Always open JSON files with encoding='utf-8'
open('file.json', encoding='utf-8')
```

### Scraper Returns No Data

```bash
# Website structure may have changed
# System automatically falls back to sample data
```

---

## 🔮 Future Enhancements

- PDF Report Generation
- Email/SMS Alerts for Critical Threats
- Export to Excel/CSV
- More Data Sources (Twitter, Reddit, CISA feeds)
- Database Integration (PostgreSQL/MongoDB)
- Trend Prediction using ML
- User Authentication

---

## 👥 Team

**Team 5**
- **P. Venkata Sai Anish** (22EG105A45)
- **D. Harshith Reddy** (22EG105A21)
- **S. Varaprasad** (22EG105A51)
- **T. Akshara** (22EG105A65)

**Project Guide**: Dr. G. Vishnu Murthy — Professor & Dean CSE

**Institution**: Department of Computer Science and Engineering

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

Developed for academic purposes — Department of Computer Science and Engineering.

---

**Last Updated**: March 10, 2026
**Version**: 4.0 (Improved AI Analysis + Cross-Validation + Deduplication)
**Status**: ✅ Active Development
