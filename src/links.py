"""
Extract links from papers.
"""
import re
from pathlib import Path
from lxml import etree

# TEI namespace used by Grobid
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# URL regex pattern
URL_PATTERN = re.compile(
    r'https?://[^\s<>"{}|\\^`\[\]]+'
)


def extract_links(xml_path: str) -> list:
    """
    Extract all URLs from a Grobid XML file.

    Args:
        xml_path: Path to the XML file

    Returns:
        List of unique URLs found
    """
    tree = etree.parse(xml_path)

    # Get all text content
    all_text = etree.tostring(tree, encoding="unicode", method="text")

    # Also check ptr and ref elements with target attribute
    targets = tree.xpath("//*/@target")

    # Find URLs in text
    urls = set(URL_PATTERN.findall(all_text))

    # Add URLs from target attributes
    for target in targets:
        if target.startswith("http"):
            urls.add(target)

    # Clean URLs (remove trailing punctuation)
    cleaned_urls = []
    for url in urls:
        url = url.rstrip(".,;:)")
        if url:
            cleaned_urls.append(url)

    return sorted(set(cleaned_urls))


def extract_all_links(xml_dir: str) -> dict:
    """
    Extract links from all XML files in a directory.

    Args:
        xml_dir: Directory containing XML files

    Returns:
        Dictionary mapping filename to list of links
    """
    xml_dir = Path(xml_dir)
    all_links = {}

    for xml_path in xml_dir.glob("*.xml"):
        links = extract_links(str(xml_path))
        all_links[xml_path.stem] = links
        print(f"{xml_path.name}: {len(links)} links found")

    return all_links


def save_links_report(all_links: dict, output_path: str) -> None:
    """
    Save a report of all links found.

    Args:
        all_links: Dictionary of links per paper
        output_path: Path to save the report
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Links Found in Papers\n\n")

        total_links = 0
        for paper, links in sorted(all_links.items()):
            f.write(f"## {paper}\n\n")
            if links:
                for link in links:
                    f.write(f"- {link}\n")
                total_links += len(links)
            else:
                f.write("No links found.\n")
            f.write("\n")

        f.write(f"---\n**Total links found: {total_links}**\n")

    print(f"Links report saved to: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    xml_dir = base_dir / "outputs" / "xml"
    output_path = base_dir / "outputs" / "links_report.md"

    all_links = extract_all_links(xml_dir)
    save_links_report(all_links, output_path)
