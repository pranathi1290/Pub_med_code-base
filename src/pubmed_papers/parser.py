import xml.etree.ElementTree as ET
from typing import List, Dict


def parse_pubmed_xml(xml_str: str) -> List[Dict]:
    root = ET.fromstring(xml_str)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"

        authors = []
        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName") or ""
            fore_name = author.findtext("ForeName") or ""
            full_name = f"{fore_name} {last_name}".strip()

            affils = [
                aff.text.strip()
                for aff in author.findall(".//AffiliationInfo/Affiliation")
                if aff is not None and aff.text
            ]

            email = next((a for a in affils if "@" in a), "")

            authors.append({
                "name": full_name,
                "affiliations": affils,
                "email": email
            })

        articles.append({
            "pmid": pmid,
            "title": title,
            "publication_date": pub_date,
            "authors": authors
        })

    return articles
