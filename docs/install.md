# Installation

## Requirements

- Python 3.11+
- Docker (for Grobid)

## Steps

### 1. Clone the repository

```bash
git clone https://github.com/albertob1412/grobid-paper-analysis.git
cd grobid-paper-analysis
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
.\venv\Scripts\Activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Grobid

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

Grobid will be available at http://localhost:8070
