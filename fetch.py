import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("COURTLISTENER_API_TOKEN")
HEADERS = {"Authorization": f"Token {TOKEN}"}
BASE_URL = "https://www.courtlistener.com/api/rest/v4/"

def search_cases(query="artificial intelligence copyright", max_results=10):
    """Search CourtListener for AI copyright cases."""
    print(f"Searching for: {query}")
    
    params = {
        "q": query,
        "type": "o",
        "order_by": "score desc",
        "page_size": max_results
    }
    
    response = requests.get(
        BASE_URL + "search/",
        headers=HEADERS,
        params=params
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    
    data = response.json()
    results = data.get("results", [])
    print(f"Found {len(results)} cases")
    return results

def download_pdf(case, save_dir="data/pdfs"):
    """Download the PDF for a case if available."""
    os.makedirs(save_dir, exist_ok=True)
    
    case_id = case.get("cluster_id") or case.get("id")
    filename = f"{save_dir}/case_{case_id}.pdf"
    
    if os.path.exists(filename):
        print(f"PDF already exists for case {case_id}, skipping")
        return filename
    
    pdf_url = case.get("download_url")
    if not pdf_url:
        print(f"No PDF available for case {case_id}")
        return None
    
    try:
        response = requests.get(pdf_url, timeout=30)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded PDF for case {case_id}")
            return filename
    except Exception as e:
        print(f"Failed to download PDF for case {case_id}: {e}")
    
    return None