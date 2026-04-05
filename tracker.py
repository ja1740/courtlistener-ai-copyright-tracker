import os
import json
from datetime import datetime

PREVIOUS_FILE = "data/previous.json"

def load_previous():
    """Load the results from the last run."""
    if not os.path.exists(PREVIOUS_FILE):
        return {}
    
    with open(PREVIOUS_FILE, "r") as f:
        return json.load(f)

def save_current(cases):
    """Save the current results for comparison next run."""
    os.makedirs("data", exist_ok=True)
    
    current = {}
    for case in cases:
        case_id = str(case.get("cluster_id") or case.get("id"))
        current[case_id] = {
            "case_name": case.get("caseName", "Unknown"),
            "date": case.get("dateFiled", "Unknown"),
            "court": case.get("court", "Unknown"),
            "timestamp": datetime.now().isoformat()
        }
    
    with open(PREVIOUS_FILE, "w") as f:
        json.dump(current, f, indent=2)
    
    print(f"Saved {len(current)} cases for future comparison")
    return current

def compare_results(current_cases):
    """Compare current results to previous run and flag changes."""
    previous = load_previous()
    
    current = {}
    for case in current_cases:
        case_id = str(case.get("cluster_id") or case.get("id"))
        current[case_id] = case.get("caseName", "Unknown")
    
    new_cases = []
    for case_id, case_name in current.items():
        if case_id not in previous:
            new_cases.append(case_name)
    
    dropped_cases = []
    for case_id, data in previous.items():
        if case_id not in current:
            dropped_cases.append(data["case_name"])
    
    changes = {
        "new_cases": new_cases,
        "dropped_cases": dropped_cases,
        "total_current": len(current),
        "total_previous": len(previous)
    }
    
    print(f"Changes since last run:")
    print(f"  New cases: {len(new_cases)}")
    print(f"  Dropped cases: {len(dropped_cases)}")
    
    return changes