"""
Count and visualize figures per article.
"""
from pathlib import Path
from lxml import etree
import matplotlib.pyplot as plt

# TEI namespace used by Grobid
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def count_figures(xml_path: str) -> int:
    """
    Count the number of figures in a Grobid XML file.

    Args:
        xml_path: Path to the XML file

    Returns:
        Number of figures found
    """
    tree = etree.parse(xml_path)

    # Count figure elements in TEI format
    figures = tree.xpath("//tei:figure", namespaces=TEI_NS)

    return len(figures)


def count_all_figures(xml_dir: str) -> dict:
    """
    Count figures in all XML files in a directory.

    Args:
        xml_dir: Directory containing XML files

    Returns:
        Dictionary mapping filename to figure count
    """
    xml_dir = Path(xml_dir)
    figure_counts = {}

    for xml_path in xml_dir.glob("*.xml"):
        count = count_figures(str(xml_path))
        figure_counts[xml_path.stem] = count
        print(f"{xml_path.name}: {count} figures")

    return figure_counts


def visualize_figures(figure_counts: dict, output_path: str) -> None:
    """
    Create a bar chart showing figures per article.

    Args:
        figure_counts: Dictionary of figure counts
        output_path: Path to save the chart
    """
    if not figure_counts:
        print("No data to visualize")
        return

    # Prepare data
    papers = list(figure_counts.keys())
    counts = list(figure_counts.values())

    # Shorten paper names for display
    short_names = [name[:15] + "..." if len(name) > 15 else name for name in papers]

    # Create bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(papers)), counts, color="steelblue")

    plt.xlabel("Paper")
    plt.ylabel("Number of Figures")
    plt.title("Number of Figures per Article")
    plt.xticks(range(len(papers)), short_names, rotation=45, ha="right")

    # Add value labels on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha="center", va="bottom")

    plt.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Figure chart saved to: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    xml_dir = base_dir / "outputs" / "xml"
    output_path = base_dir / "outputs" / "figures_chart.png"

    figure_counts = count_all_figures(xml_dir)
    visualize_figures(figure_counts, output_path)
