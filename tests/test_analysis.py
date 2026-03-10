"""
Tests for the analysis modules.
"""
import os
import tempfile
from pathlib import Path

import pytest

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wordcloud_generator import extract_abstract
from figures import count_figures
from links import extract_links


# Sample Grobid XML for testing
SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Test Paper</title>
      </titleStmt>
    </fileDesc>
    <profileDesc>
      <abstract>
        <p>This is a test abstract about machine learning and artificial intelligence.</p>
      </abstract>
    </profileDesc>
  </teiHeader>
  <text>
    <body>
      <figure xml:id="fig1">
        <head>Figure 1</head>
      </figure>
      <figure xml:id="fig2">
        <head>Figure 2</head>
      </figure>
      <p>Visit https://example.com for more information.</p>
      <p>Also check https://github.com/test/repo for the code.</p>
    </body>
  </text>
</TEI>
"""


@pytest.fixture
def sample_xml_file():
    """Create a temporary XML file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False, encoding="utf-8") as f:
        f.write(SAMPLE_XML)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


def test_extract_abstract(sample_xml_file):
    """Test that abstracts are correctly extracted."""
    abstract = extract_abstract(sample_xml_file)
    assert "machine learning" in abstract.lower()
    assert "artificial intelligence" in abstract.lower()


def test_count_figures(sample_xml_file):
    """Test that figures are correctly counted."""
    count = count_figures(sample_xml_file)
    assert count == 2


def test_extract_links(sample_xml_file):
    """Test that links are correctly extracted."""
    links = extract_links(sample_xml_file)
    assert "https://example.com" in links
    assert "https://github.com/test/repo" in links
    assert len(links) == 2


def test_extract_abstract_empty():
    """Test handling of XML without abstract."""
    xml_no_abstract = """<?xml version="1.0" encoding="UTF-8"?>
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
      <teiHeader><fileDesc><titleStmt><title>Test</title></titleStmt></fileDesc></teiHeader>
    </TEI>
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False, encoding="utf-8") as f:
        f.write(xml_no_abstract)
        temp_path = f.name

    abstract = extract_abstract(temp_path)
    assert abstract == ""
    os.unlink(temp_path)
