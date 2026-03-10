# Open Science and AI - Text Analysis Pipeline

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python pipeline for analyzing scientific papers using Grobid. This project extracts and analyzes information from PDF articles, generating word clouds, figure statistics, and link reports.

## Features

- **PDF Processing**: Extract structured information from PDFs using Grobid
- **Word Cloud Generation**: Create a word cloud from paper abstracts
- **Figure Analysis**: Count and visualize the number of figures per article
- **Link Extraction**: Extract and list all URLs found in papers

## Requirements

- Python 3.11+
- Docker (for running Grobid)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/albertob1412/Open_science_and_AI.git
cd Open_science_and_AI
```

### 2. Create and activate virtual environment

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

### 4. Start Grobid service

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

## Usage

### Running the complete pipeline

1. Place your PDF files in the `papers/` directory
2. Make sure Grobid is running (see step 4 above)
3. Run the main script:

```bash
cd src
python main.py
```

### Running individual modules

```bash
# Extract PDFs to XML
python src/extract.py

# Generate word cloud
python src/wordcloud_generator.py

# Count figures
python src/figures.py

# Extract links
python src/links.py
```

### Running with Docker

```bash
# Build the image
docker build -t os-ai-analysis .

# Run with Grobid on host
docker run --rm -v $(pwd)/outputs:/app/outputs os-ai-analysis
```

## Output

The pipeline generates the following outputs in the `outputs/` directory:

| File | Description |
|------|-------------|
| `xml/` | Grobid XML files for each paper |
| `wordcloud.png` | Word cloud generated from abstracts |
| `figures_chart.png` | Bar chart showing figures per article |
| `links_report.md` | Markdown report of all links found |

## Project Structure

```
Open_science_and_AI/
├── papers/              # Input PDF files
├── outputs/             # Generated outputs
├── src/
│   ├── __init__.py
│   ├── main.py          # Main pipeline script
│   ├── extract.py       # PDF processing with Grobid
│   ├── wordcloud_generator.py  # Word cloud generation
│   ├── figures.py       # Figure counting and visualization
│   └── links.py         # Link extraction
├── tests/
│   └── test_analysis.py # Unit tests
├── Dockerfile
├── requirements.txt
├── codemeta.json
├── CITATION.cff
├── LICENSE
└── README.md
```

## Testing

Run the tests with pytest:

```bash
pytest tests/ -v
```

## Validation

### Word Cloud Validation
The word cloud is generated from abstracts extracted by Grobid. We validated this by:
1. Manually checking that extracted abstracts match the original PDFs
2. Verifying that frequent terms in the word cloud correspond to paper topics

### Figure Count Validation
Figure counts were validated by:
1. Manually counting figures in a sample of papers
2. Comparing with Grobid's extracted `<figure>` elements

### Link Extraction Validation
Links were validated by:
1. Manually checking a sample of extracted URLs
2. Verifying that URLs are properly formatted and resolve

## Limitations

- Grobid may not correctly parse all PDF formats, especially scanned documents
- Some figures may be missed if they are not properly tagged in the PDF
- Link extraction depends on URL patterns and may miss some non-standard URLs
- The word cloud excludes common stop words but may include some domain-specific common terms

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Author

Alberto Barrachina - Universidad Politecnica de Madrid

## Acknowledgements

- [Grobid](https://github.com/kermitt2/grobid) for PDF processing
- Course: Open Science and AI in Research Software Engineering (UPM)
