"""
Main script to run the complete analysis pipeline.
"""
from pathlib import Path

from extract import process_all_pdfs
from wordcloud_generator import extract_all_abstracts, generate_wordcloud
from figures import count_all_figures, visualize_figures
from links import extract_all_links, save_links_report


def main():
    """Run the complete analysis pipeline."""
    base_dir = Path(__file__).parent.parent
    papers_dir = base_dir / "papers"
    outputs_dir = base_dir / "outputs"
    xml_dir = outputs_dir / "xml"

    print("=" * 60)
    print("OPEN SCIENCE AND AI - TEXT ANALYSIS PIPELINE")
    print("=" * 60)

    # Step 1: Process PDFs with Grobid
    print("\n[1/4] Processing PDFs with Grobid...")
    print("-" * 40)
    xml_files = process_all_pdfs(papers_dir, xml_dir)
    print(f"Processed {len(xml_files)} files")

    # Step 2: Generate word cloud from abstracts
    print("\n[2/4] Generating word cloud from abstracts...")
    print("-" * 40)
    abstracts = extract_all_abstracts(xml_dir)
    generate_wordcloud(abstracts, outputs_dir / "wordcloud.png")

    # Step 3: Count and visualize figures
    print("\n[3/4] Counting figures per article...")
    print("-" * 40)
    figure_counts = count_all_figures(xml_dir)
    visualize_figures(figure_counts, outputs_dir / "figures_chart.png")

    # Step 4: Extract links
    print("\n[4/4] Extracting links from papers...")
    print("-" * 40)
    all_links = extract_all_links(xml_dir)
    save_links_report(all_links, outputs_dir / "links_report.md")

    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs saved to: {outputs_dir}")
    print("  - xml/           : Grobid XML files")
    print("  - wordcloud.png  : Word cloud from abstracts")
    print("  - figures_chart.png : Figures per article")
    print("  - links_report.md   : Links found in papers")


if __name__ == "__main__":
    main()
