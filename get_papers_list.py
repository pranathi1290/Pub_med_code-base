import typer     # type: ignore
from pubmed_papers import fetcher, parser, filters, exporter
from typing import Optional

app = typer.Typer()


@app.command()
def main(
    query: str,
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Filename to save results as CSV"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Print debug information")
):
    if debug:
        print(f"[DEBUG] Searching PubMed with query: {query}")

    # 1. Search PubMed
    ids = fetcher.search_pubmed(query)
    if debug:
        print(f"[DEBUG] Found {len(ids)} paper IDs")

    # 2. Fetch details
    xml_data = fetcher.fetch_details(ids)

    # 3. Parse articles
    articles = parser.parse_pubmed_xml(xml_data)

    # 4. Filter non-academic authors
    output_rows = []
    for article in articles:
        company_authors = filters.extract_company_authors(article["authors"])
        if company_authors:
            output_rows.append({
                "PubmedID": article["pmid"],
                "Title": article["title"],
                "Publication Date": article["publication_date"],
                "Non-academic Author(s)": "; ".join(a["name"] for a in company_authors),
                "Company Affiliation(s)": "; ".join(set(aff for a in company_authors for aff in a["companies"])),
                "Corresponding Author Email": next((a["email"] for a in company_authors if a["email"]), "")
            })

    # 5. Export or print
    if file:
        exporter.export_csv(output_rows, file)
        print(f"✅ Results saved to '{file}'")
    else:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title="PubMed Results")

        for col in ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]:
            table.add_column(col)

        for row in output_rows:
            table.add_row(*(row[col] for col in table.columns._keys))

        console.print(table)


if __name__ == "__main__":
    app()
