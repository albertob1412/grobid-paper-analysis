"""
Extract information from PDFs using Grobid.
"""
import os
import json
import time
import requests
from pathlib import Path


def load_config():
    """Load configuration from config.json file."""
    config_path = Path(__file__).parent.parent / "config.json"

    default_config = {
        "grobid_server": "http://localhost:8070",
        "batch_size": 1000,
        "sleep_time": 5,
        "timeout": 180,
        "coordinates": ["persName", "figure", "ref", "biblStruct", "formula", "s"]
    }

    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return default_config


CONFIG = load_config()
GROBID_URL = f"{CONFIG['grobid_server']}/api/processFulltextDocument"


def process_pdf(pdf_path: str, output_dir: str) -> str:
    """
    Send a PDF to Grobid and save the resulting XML.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the XML output

    Returns:
        Path to the saved XML file
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(pdf_path, "rb") as f:
        files = {"input": (pdf_path.name, f, "application/pdf")}
        response = requests.post(
            GROBID_URL,
            files=files,
            timeout=CONFIG['timeout']
        )

    if response.status_code != 200:
        raise Exception(f"Grobid error for {pdf_path.name}: {response.status_code}")

    xml_filename = pdf_path.stem + ".xml"
    xml_path = output_dir / xml_filename

    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return str(xml_path)


def process_all_pdfs(papers_dir: str, output_dir: str) -> list:
    """
    Process all PDFs in a directory.

    Args:
        papers_dir: Directory containing PDF files
        output_dir: Directory to save XML outputs

    Returns:
        List of paths to saved XML files
    """
    papers_dir = Path(papers_dir)
    xml_files = []

    pdf_files = list(papers_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")

    for i, pdf_path in enumerate(pdf_files):
        print(f"Processing: {pdf_path.name}")
        try:
            xml_path = process_pdf(pdf_path, output_dir)
            xml_files.append(xml_path)
            print(f"  -> Saved: {xml_path}")

            # Sleep between requests to avoid overloading the server
            if i < len(pdf_files) - 1:
                time.sleep(CONFIG['sleep_time'])

        except Exception as e:
            print(f"  -> Error: {e}")

    return xml_files


if __name__ == "__main__":
    # Default paths
    base_dir = Path(__file__).parent.parent
    papers_dir = base_dir / "papers"
    output_dir = base_dir / "outputs" / "xml"

    process_all_pdfs(papers_dir, output_dir)
