# PubMed Papers Analyzer

A Python-based tool for searching and analyzing PubMed scientific papers, specifically designed to identify research papers with non-academic authors (industry/company affiliations).

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides a comprehensive solution for searching PubMed databases and identifying scientific papers that have authors with non-academic affiliations (e.g., pharmaceutical companies, biotech firms, etc.). The tool is particularly useful for:

- **Research Analysis**: Identifying industry-sponsored research
- **Conflict of Interest Studies**: Finding papers with corporate affiliations
- **Academic Research**: Analyzing publication patterns between academic and industry authors
- **Systematic Reviews**: Screening papers based on author affiliations

## ✨ Features

- **PubMed Integration**: Direct access to PubMed's E-utilities API
- **Smart Filtering**: Automatic detection of non-academic affiliations
- **Flexible Output**: Export to CSV or display in rich terminal tables
- **Debug Mode**: Detailed logging for troubleshooting
- **Batch Processing**: Handle multiple papers efficiently
- **Email Extraction**: Automatically extract corresponding author emails

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- pip or Poetry package manager

### Method 1: Using Poetry (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pub-med
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

### Method 2: Using pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pub-med
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Direct Installation

```bash
pip install requests typer rich
```

## 📖 Usage

### Basic Usage

Search for papers with a specific query:

```bash
python get_papers_list.py "breast cancer treatment"
```

### Advanced Usage

#### Export to CSV file:
```bash
python get_papers_list.py "diabetes research" --file results.csv
```

#### Enable debug mode:
```bash
python get_papers_list.py "cancer immunotherapy" --debug
```

#### Combine options:
```bash
python get_papers_list.py "vaccine development" --file vaccine_papers.csv --debug
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--file` | `-f` | Save results to CSV file |
| `--debug` | `-d` | Enable debug mode for detailed logging |

## 📁 Project Structure

```
pub-med/
├── README.md                 # This documentation file
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Locked dependencies
├── get_papers_list.py       # Main CLI entry point
├── src/
│   └── pubmed_papers/
│       ├── __init__.py      # Package initialization
│       ├── fetcher.py       # PubMed API interaction
│       ├── parser.py        # XML parsing utilities
│       ├── filters.py       # Affiliation filtering logic
│       └── exporter.py      # CSV export functionality
├── tests/                   # Test files
├── output.csv              # Sample output file
└── breast_cancer_results.csv # Sample results
```

## 🔧 API Documentation

### Core Modules

#### `fetcher.py`
Handles all PubMed API interactions.

**Functions:**
- `search_pubmed(query: str, max_results: int = 100) -> List[str]`
  - Searches PubMed for papers matching the query
  - Returns list of PubMed IDs (PMIDs)
  - Default limit: 100 results

- `fetch_details(pmid_list: List[str]) -> str`
  - Fetches detailed XML data for given PMIDs
  - Returns XML string with article metadata

#### `parser.py`
Parses PubMed XML data into structured Python objects.

**Functions:**
- `parse_pubmed_xml(xml_str: str) -> List[Dict]`
  - Converts PubMed XML to structured data
  - Extracts: PMID, title, publication date, authors, affiliations, emails

#### `filters.py`
Identifies non-academic authors based on affiliation keywords.

**Functions:**
- `is_non_academic(affiliation: str) -> bool`
  - Checks if affiliation contains non-academic keywords
  - Academic keywords: university, college, school, institute, etc.

- `extract_company_authors(authors: List[Dict]) -> List[Dict]`
  - Filters authors with non-academic affiliations
  - Returns authors with company/industry affiliations

#### `exporter.py`
Handles CSV export functionality.

**Functions:**
- `export_csv(data: List[Dict], filename: str) -> None`
  - Exports results to CSV file
  - Includes: PubmedID, Title, Publication Date, Non-academic Author(s), Company Affiliation(s), Corresponding Author Email

### Data Structures

#### Article Object
```python
{
    "pmid": "12345678",
    "title": "Research Paper Title",
    "publication_date": "2023",
    "authors": [
        {
            "name": "John Doe",
            "affiliations": ["Company Name", "Department"],
            "email": "john.doe@company.com"
        }
    ]
}
```

#### Output Row
```python
{
    "PubmedID": "12345678",
    "Title": "Research Paper Title",
    "Publication Date": "2023",
    "Non-academic Author(s)": "John Doe",
    "Company Affiliation(s)": "Company Name",
    "Corresponding Author Email": "john.doe@company.com"
}
```

## ⚙️ Configuration

### Academic Keywords
The system identifies academic institutions using predefined keywords in `filters.py`:

```python
ACADEMIC_KEYWORDS = [
    "university", "college", "school", "institute",
    "department", "hospital", "centre", "center",
    "faculty", "lab", "clinic"
]
```

### PubMed API Limits
- Default search results: 100 papers
- Rate limiting: Follows NCBI E-utilities guidelines
- No API key required for basic usage

## 📊 Examples

### Example 1: Basic Search
```bash
python get_papers_list.py "cancer immunotherapy"
```

**Output:**
```
PubMed Results
┌──────────┬──────────────────────┬──────────────────┬─────────────────────┬─────────────────────┬─────────────────────────────┐
│ PubmedID │ Title               │ Publication Date │ Non-academic Author │ Company Affiliation │ Corresponding Author Email  │
├──────────┼──────────────────────┼──────────────────┼─────────────────────┼─────────────────────┼─────────────────────────────┤
│ 12345678 │ Immunotherapy Study │ 2023             │ Dr. Smith           │ PharmaCorp Inc.     │ dr.smith@pharmacorp.com    │
└──────────┴──────────────────────┴──────────────────┴─────────────────────┴─────────────────────┴─────────────────────────────┘
```

### Example 2: Export to CSV
```bash
python get_papers_list.py "diabetes treatment" --file diabetes_papers.csv
```

**Output:**
```
✅ Results saved to 'diabetes_papers.csv'
```

### Example 3: Debug Mode
```bash
python get_papers_list.py "vaccine research" --debug
```

**Output:**
```
[DEBUG] Searching PubMed with query: vaccine research
[DEBUG] Found 45 paper IDs
✅ Results saved to 'output.csv'
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Network Connection Errors
**Problem:** `requests.exceptions.ConnectionError`
**Solution:** Check internet connection and firewall settings

#### 2. No Results Found
**Problem:** Query returns no papers
**Solution:** 
- Try broader search terms
- Check spelling
- Use PubMed's search syntax

#### 3. Permission Errors
**Problem:** Cannot write to output file
**Solution:** Check file permissions and directory access

#### 4. Import Errors
**Problem:** Module not found
**Solution:** Ensure virtual environment is activated and dependencies are installed

### Debug Mode
Enable debug mode to see detailed execution information:
```bash
python get_papers_list.py "your query" --debug
```

### Logging
The application provides detailed logging when debug mode is enabled, showing:
- Search queries
- Number of papers found
- Processing steps
- Error details

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup
```bash
# Clone and setup
git clone <repository-url>
cd pub-med
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black src/ tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NCBI PubMed**: For providing the E-utilities API
- **Rich**: For beautiful terminal output
- **Typer**: For elegant CLI interface
- **Requests**: For HTTP library

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [Issues](../../issues)
3. Create a new issue with detailed information

## 🔄 Version History

- **v0.1.0**: Initial release with basic PubMed search and filtering functionality

---

**Note:** This tool is designed for research and educational purposes. Please respect PubMed's terms of service and rate limiting guidelines when using this application.
