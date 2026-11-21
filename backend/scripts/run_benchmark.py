import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import json
from app.services.legal_benchmark import run_full_benchmark_evaluation

if __name__ == "__main__":
    report = run_full_benchmark_evaluation()
    print(f"Total Scenarios : {report['total_scenarios']}")
    print(f"Passed Scenarios: {report['passed_scenarios']}")
    print(f"Pass Rate       : {report['pass_rate']}")
    print("=" * 60)
    for res in report["results"]:
        status = "PASS" if res["passed"] else "FAIL"
        print(f"[{status}] {res['scenario_id']} - Score: {res['score']}%")
        print(f"       Found: {res['found_provisions']}")
        if res['missing_provisions']:
            print(f"       Missing: {res['missing_provisions']}")
        if res['prohibited_violations']:
            print(f"       VIOLATIONS: {res['prohibited_violations']}")
