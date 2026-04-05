import os
from datetime import datetime

OUTPUT_FILE = "output/report.md"

def generate_report(cases, changes, search_query):
    """Generate a markdown report summarizing the results."""
    os.makedirs("output", exist_ok=True)
    
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    lines = []
    
    # Header
    lines.append(f"# AI Copyright Case Law Tracker")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Search Query:** `{search_query}`")
    lines.append(f"**Total Cases Found:** {len(cases)}")
    lines.append("")
    
    # Changes section
    lines.append("## Changes Since Last Run")
    if changes["total_previous"] == 0:
        lines.append("This is the first run. No previous data to compare.")
    else:
        lines.append(f"- Previous run had **{changes['total_previous']}** cases")
        lines.append(f"- Current run has **{changes['total_current']}** cases")
        
        if changes["new_cases"]:
            lines.append("")
            lines.append("### New Cases")
            for case in changes["new_cases"]:
                lines.append(f"- {case}")
        
        if changes["dropped_cases"]:
            lines.append("")
            lines.append("### Dropped Cases")
            for case in changes["dropped_cases"]:
                lines.append(f"- {case}")
        
        if not changes["new_cases"] and not changes["dropped_cases"]:
            lines.append("No changes since last run.")
    
    lines.append("")
    
    # Cases section
    lines.append("## Cases Found")
    lines.append("")
    
    for i, case in enumerate(cases, 1):
        case_name = case.get("caseName", "Unknown")
        date = case.get("dateFiled", "Unknown")
        court = case.get("court", "Unknown")
        case_id = case.get("cluster_id") or case.get("id")
        url = f"https://www.courtlistener.com/opinion/{case_id}/"
        snippet = case.get("snippet", "No preview available.")
        
        lines.append(f"### {i}. {case_name}")
        lines.append(f"- **Date Filed:** {date}")
        lines.append(f"- **Court:** {court}")
        lines.append(f"- **Link:** [View on CourtListener]({url})")
        lines.append(f"- **Preview:** {snippet}")
        lines.append("")
    
    # Write to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))
    
    print(f"Report saved to {OUTPUT_FILE}")