# 🚨 Cyber OSINT GPT – Threat Intelligence System

Cyber OSINT GPT is an intelligent threat intelligence system designed to analyze **historical cyber incident reports** using **GPT-based Natural Language Processing (NLP)**.  
This project leverages Open-Source Intelligence (OSINT) to extract meaningful insights that aid in cybersecurity research and analysis.

---

## 📌 Features

- Automated scraping of cyber incident and threat data  
- GPT-powered NLP analysis of historical reports  
- Organized storage of raw and processed OSINT data  
- Jupyter notebooks for exploratory data analysis and insights  

---

## ⚙️ Setup Instructions

### 1️⃣ Create a Virtual Environment

```bash
python -m venv venv

```

## Activate the virtual environment:

### Linux / macOS
```bash

source venv/bin/activate

```

### Windows
```bash

venv\Scripts\activate

```

## Install Dependencies
```bash
pip install -r requirements.txt

```

## Configure Environment Variables
### Create a .env file in the project root directory and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here


## Run the Scraper
```bash

python src/scraper.py

```
## Project Structure
cyber-osint-gpt/
│
├── data/          # Raw and processed cyber incident data
├── src/           # Source code modules
├── notebooks/     # Jupyter notebooks for analysis
├── requirements.txt
├── README.md
└── .env

---
# Team Members
P. Venkata Sai Anish (22EG105A45)

D. Harshith Reddy (22EG105A21)

S. Varaprasad (22EG105A51)

T. Akshara (22EG105A65)
---
# 🎓 Project Guide
## Dr. G. Vishnu Murthy
---
# 📄 License
## This project is developed for academic and research purposes only.
---
# 🔮 Future Scope
Integration with real-time threat feeds

Advanced visualization dashboards

Multi-model threat correlation

Automated incident classification and tagging
---





