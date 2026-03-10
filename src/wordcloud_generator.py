"""
Generate word cloud from paper abstracts.
"""
from pathlib import Path
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# TEI namespace used by Grobid
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def extract_abstract(xml_path: str) -> str:
    """
    Extract abstract text from a Grobid XML file.

    Args:
        xml_path: Path to the XML file

    Returns:
        Abstract text or empty string if not found
    """
    tree = etree.parse(xml_path)

    # Try to find abstract in TEI format
    abstract_elements = tree.xpath("//tei:abstract//text()", namespaces=TEI_NS)

    if abstract_elements:
        return " ".join(abstract_elements).strip()

    return ""


def extract_all_abstracts(xml_dir: str) -> dict:
    """
    Extract abstracts from all XML files in a directory.

    Args:
        xml_dir: Directory containing XML files

    Returns:
        Dictionary mapping filename to abstract text
    """
    xml_dir = Path(xml_dir)
    abstracts = {}

    for xml_path in xml_dir.glob("*.xml"):
        abstract = extract_abstract(str(xml_path))
        if abstract:
            abstracts[xml_path.stem] = abstract
            print(f"Extracted abstract from: {xml_path.name} ({len(abstract)} chars)")
        else:
            print(f"No abstract found in: {xml_path.name}")

    return abstracts


def generate_wordcloud(abstracts: dict, output_path: str) -> None:
    """
    Generate and save a word cloud from abstracts.

    Args:
        abstracts: Dictionary of abstracts
        output_path: Path to save the word cloud image
    """
    # Combine all abstracts
    all_text = " ".join(abstracts.values())

    if not all_text.strip():
        print("No text found to generate word cloud")
        return

    # Generate word cloud
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="viridis",
        max_words=100
    ).generate(all_text)

    # Save the image
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud from Paper Abstracts")
    plt.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Word cloud saved to: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    xml_dir = base_dir / "outputs" / "xml"
    output_path = base_dir / "outputs" / "wordcloud.png"

    abstracts = extract_all_abstracts(xml_dir)
    generate_wordcloud(abstracts, output_path)
