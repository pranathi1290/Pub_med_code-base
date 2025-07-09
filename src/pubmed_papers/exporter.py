import csv
from typing import List, Dict


def export_csv(data: List[Dict], filename: str) -> None:
    with open(filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email"
        ])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    