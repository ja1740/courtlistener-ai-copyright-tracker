import os
import json
import fitz  # PyMuPDF

INDEX_FILE = "data/index.json"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Could not extract text from {pdf_path}: {e}")
        return ""

def build_index(cases, pdf_dir="data/pdfs"):
    """Extract text from all downloaded PDFs and save to index."""
    print("Building search index...")
    index = {}

    for case in cases:
        case_id = str(case.get("cluster_id") or case.get("id"))
        pdf_path = f"{pdf_dir}/case_{case_id}.pdf"

        if os.path.exists(pdf_path):
            text = extract_text_from_pdf(pdf_path)
            index[case_id] = {
                "case_name": case.get("caseName", "Unknown"),
                "date": case.get("dateFiled", "Unknown"),
                "court": case.get("court", "Unknown"),
                "text": text
            }
            print(f"Indexed: {case.get('caseName', case_id)}")
        else:
            index[case_id] = {
                "case_name": case.get("caseName", "Unknown"),
                "date": case.get("dateFiled", "Unknown"),
                "court": case.get("court", "Unknown"),
                "text": case.get("snippet", "")
            }

    os.makedirs("data", exist_ok=True)
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

    print(f"Index saved with {len(index)} cases")
    return index

def search_index(keyword):
    """Search the index for a keyword and return matching cases."""
    if not os.path.exists(INDEX_FILE):
        print("No index found. Run the program first to build the index.")
        return []

    with open(INDEX_FILE, "r") as f:
        index = json.load(f)

    keyword_lower = keyword.lower()
    matches = []

    for case_id, data in index.items():
        text = data.get("text", "").lower()
        if keyword_lower in text:
            position = text.find(keyword_lower)
            snippet = data["text"][max(0, position-100):position+200]
            matches.append({
                "case_name": data["case_name"],
                "date": data["date"],
                "court": data["court"],
                "snippet": snippet
            })

    print(f"Found {len(matches)} cases matching '{keyword}'")
    return matches