# Open Science and AI - Text Analysis Pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18965657.svg)](https://doi.org/10.5281/zenodo.18965657)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python pipeline for analyzing scientific papers using Grobid. This project extracts information from PDF articles and generates word clouds, figure statistics, and link reports.

## Features

- PDF processing with Grobid to extract structured text
- Word cloud generation from paper abstracts
- Figure counting and visualization per article
- Link extraction from papers

## Requirements

- Python 3.11+
- Docker (for Grobid)

## Installation

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

## Usage

### Running the complete pipeline

1. Place PDF files in the `papers/` directory
2. Make sure Grobid is running
3. Run:

```bash
cd src
python main.py
```

### Running individual modules

```bash
python src/extract.py              # Extract PDFs to XML
python src/wordcloud_generator.py  # Generate word cloud
python src/figures.py              # Count figures
python src/links.py                # Extract links
```

### Running with Docker

```bash
docker build -t os-ai-analysis .
docker run --rm -v $(pwd)/outputs:/app/outputs os-ai-analysis
```

## Outputs

The pipeline generates these files in `outputs/`:

| File | Description |
|------|-------------|
| `xml/` | Grobid XML files |
| `wordcloud.png` | Word cloud from abstracts |
| `figures_chart.png` | Figure count per article |
| `links_report.md` | List of links found |

## Project Structure

```
Open_science_and_AI/
├── papers/              # Input PDFs
├── outputs/             # Generated results
├── src/
│   ├── main.py          # Main script
│   ├── extract.py       # Grobid processing
│   ├── wordcloud_generator.py
│   ├── figures.py
│   └── links.py
├── tests/
│   └── test_analysis.py
├── Dockerfile
├── requirements.txt
├── codemeta.json
├── CITATION.cff
└── LICENSE
```

## Tests

```bash
pytest tests/ -v
```

## Validation

### Word Cloud
I validated the word cloud by manually checking that extracted abstracts match the original PDFs, and verifying that the most frequent terms correspond to the paper topics.

### Figure Count
I validated the figure count by manually comparing figures in some papers with the `<figure>` elements extracted by Grobid.

### Link Extraction
I validated the links by checking a sample of extracted URLs and verifying they have the correct format.

## Limitations

- Grobid may fail with some PDF formats, especially scanned documents
- Some figures may not be detected if they are not properly tagged in the PDF
- Link extraction depends on URL patterns and may miss some non-standard links
- The word cloud excludes stopwords but may include common domain terms

## License

Apache License 2.0 - see [LICENSE](LICENSE)

## Author

Alberto Barranquero - Universidad Politecnica de Madrid

## Acknowledgements

- [Grobid](https://github.com/kermitt2/grobid) for PDF processing
- Course: Open Science and AI in Research Software Engineering (UPM)
