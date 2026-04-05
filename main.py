import sys
from fetch import search_cases, download_pdf
from search import build_index, search_index
from tracker import compare_results, save_current
from report import generate_report

SEARCH_QUERY = "artificial intelligence copyright"

def main():
    print("=== AI Copyright Case Law Tracker ===")
    print("")

    # Step 1: Search for cases
    cases = search_cases(query=SEARCH_QUERY, max_results=10)
    
    if not cases:
        print("No cases found. Exiting.")
        return

    # Step 2: Download PDFs
    print("\nDownloading PDFs...")
    for case in cases:
        download_pdf(case)

    # Step 3: Build search index
    print("\nBuilding index...")
    build_index(cases)

    # Step 4: Compare with previous run
    print("\nChecking for changes...")
    changes = compare_results(cases)

    # Step 5: Save current results
    save_current(cases)

    # Step 6: Generate report
    print("\nGenerating report...")
    generate_report(cases, changes, SEARCH_QUERY)

    print("\n=== Done! ===")
    print("Report saved to output/report.md")

    # Step 7: Optional keyword search
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
        print(f"\nSearching index for: '{keyword}'")
        matches = search_index(keyword)
        if matches:
            for match in matches:
                print(f"\nCase: {match['case_name']}")
                print(f"Court: {match['court']}")
                print(f"Snippet: ...{match['snippet']}...")
        else:
            print("No matches found.")

if __name__ == "__main__":
    main()