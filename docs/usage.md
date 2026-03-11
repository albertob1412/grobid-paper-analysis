# Usage

## Running the complete pipeline

1. Place PDF files in the `papers/` directory
2. Make sure Grobid is running
3. Run:

```bash
cd src
python main.py
```

## Outputs

The pipeline generates these files in `outputs/`:

| File | Description |
|------|-------------|
| `xml/` | Grobid XML files |
| `wordcloud.png` | Word cloud from abstracts |
| `figures_chart.png` | Figure count per article |
| `links_report.md` | List of links found |

## Running with Docker

```bash
docker build -t os-ai-analysis .
docker run --rm -v $(pwd)/outputs:/app/outputs os-ai-analysis
```

## Configuration

Edit `config.json` to change Grobid settings:

```json
{
    "grobid_server": "http://localhost:8070",
    "timeout": 180,
    "sleep_time": 3
}
```
