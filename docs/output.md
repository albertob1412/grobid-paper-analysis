# Output

The pipeline generates the following outputs in the `outputs/` directory:

## XML Files

Grobid extracts structured information from PDFs and saves them as XML files in `outputs/xml/`.

Each XML contains:
- Title
- Authors
- Abstract
- Sections
- Figures
- References
- Links

## Word Cloud

`outputs/wordcloud.png`

A word cloud generated from all paper abstracts. The most frequent terms appear larger.

![Word Cloud Example](https://via.placeholder.com/400x300?text=Word+Cloud)

## Figures Chart

`outputs/figures_chart.png`

A bar chart showing the number of figures per article.

## Links Report

`outputs/links_report.md`

A markdown file listing all URLs found in each paper:

```markdown
# Links Report

## paper1.pdf
- https://example.com/dataset
- https://github.com/example/repo

## paper2.pdf
- https://doi.org/10.1234/example
```
