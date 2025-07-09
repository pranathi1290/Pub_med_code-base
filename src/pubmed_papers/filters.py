from typing import List, Dict

ACADEMIC_KEYWORDS = [
    "university", "college", "school", "institute",
    "department", "hospital", "centre", "center",
    "faculty", "lab", "clinic"
]


def is_non_academic(affiliation: str) -> bool:
    return not any(keyword in affiliation.lower() for keyword in ACADEMIC_KEYWORDS)


def extract_company_authors(authors: List[Dict]) -> List[Dict]:
    non_acads = []
    for author in authors:
        company_affils = [aff for aff in author["affiliations"] if is_non_academic(aff)]
        if company_affils:
            non_acads.append({
                "name": author["name"],
                "companies": company_affils,
                "email": author["email"]
            })
    return non_acads
