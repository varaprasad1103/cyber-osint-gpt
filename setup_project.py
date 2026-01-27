# setup_project.py - Run this once to create all files and folders
import os

def create_project_structure():
    """Create all folders and files for the project"""
    
    # Create directories
    directories = [
        'data/raw',
        'data/processed',
        'src',
        'notebooks'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create __init__.py in src
    with open('src/__init__.py', 'w') as f:
        f.write('# Cyber OSINT GPT Package\n')
    print("✓ Created src/__init__.py")
    
    # Create requirements.txt
    requirements_content = """# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2

# NLP Processing
nltk==3.8.1
spacy==3.7.2
pandas==2.1.3

# GPT Integration
openai==1.3.5
# anthropic==0.7.1  # Alternative

# Data Storage
pymongo==4.6.0

# Visualization
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0
numpy==1.26.2

# Utilities
python-dotenv==1.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("✓ Created requirements.txt")
    
    # Create config.py
    config_content = """# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Database Configuration
DB_TYPE = 'sqlite'  # or 'mongodb'
SQLITE_DB_PATH = 'data/cyber_intelligence.db'
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')

# Scraping Configuration
REQUEST_DELAY = 2  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# Data Paths
RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
"""
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("✓ Created config.py")
    
    # Create .env template
    env_content = """# .env file - Add your API keys here
# DO NOT COMMIT THIS FILE TO GIT!

OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
MONGODB_URI=mongodb://localhost:27017/
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✓ Created .env")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env

# Data files
data/raw/*.json
data/processed/*.json
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")
    
    # Create README.md
    readme_content = """# Cyber OSINT GPT - Threat Intelligence System

An intelligent system for analyzing historical cyber incident reports using GPT-based NLP.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to `.env` file

4. Run the scraper:
```bash
python src/scraper.py
```

## Project Structure

- `data/` - Raw and processed data
- `src/` - Source code modules
- `notebooks/` - Jupyter notebooks for analysis

## Team

- P. Venkata Sai Anish (22EG105A45)
- D. Harshith Reddy (22EG105A21)
- S. Varaprasad (22EG105A51)
- T. Akshara (22EG105A65)

**Guide:** Dr. G. Vishnu Murthy
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✓ Created README.md")
    
    print("\n" + "="*50)
    print("✓ PROJECT SETUP COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Add your OpenAI API key to .env file")
    print("3. Run scraper: python src/scraper.py")
    print("\n")

if __name__ == "__main__":
    print("Setting up Cyber OSINT GPT Project...\n")
    create_project_structure()