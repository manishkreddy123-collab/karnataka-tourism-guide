"""Run CSV behavior checks against a running local server and save results to SQLite."""
import csv,json,sqlite3,time,urllib.error,urllib.request,uuid
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE="http://127.0.0.1:8000"
def main() -> int:
    results=[]; session_id=f"eval-{uuid.uuid4()}"
    with (ROOT/"test_set.csv").open(encoding="utf-8",newline="") as f: cases=list(csv.DictReader(f))
    for case in cases:
        started=time.perf_counter(); payload=json.dumps({"session_id":session_id,"message":case["query"]}).encode()
        request=urllib.request.Request(f"{BASE}/api/chat",data=payload,headers={"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(request,timeout=30) as response: data=json.loads(response.read())
            actual=data["reply"]; latency=round((time.perf_counter()-started)*1000); answer=actual.casefold()
            required=case["must_contain"].casefold(); forbidden=case["must_not_contain"].casefold()
            correct=(not required or required in answer) and (not forbidden or forbidden not in answer)
        except (urllib.error.URLError,TimeoutError,KeyError,json.JSONDecodeError) as exc:
            actual=f"EVALUATION ERROR: {exc}"; latency=round((time.perf_counter()-started)*1000); correct=False
        results.append((case,actual,latency,correct)); print(f"{'PASS' if correct else 'REVIEW'} {case['case_id']} {case['category']} ({latency} ms)")
    db_path=Path(__import__("os").getenv("DATABASE_PATH",str(ROOT/"chatbot.db")))
    with sqlite3.connect(db_path) as db:
        for case,actual,latency,correct in results:
            db.execute("INSERT INTO test_results VALUES (?,?,?,?,?,?,?)",(str(uuid.uuid4()),case["query"],f"must_contain={case['must_contain']}; must_not_contain={case['must_not_contain']}",actual,int(correct),latency,datetime.now(timezone.utc).isoformat(timespec="milliseconds")))
    passed=sum(int(item[3]) for item in results); print(f"\n{passed}/{len(results)} checks met their simple text criteria. Review every reply; this is not a substitute for human evaluation.")
    return 0 if passed==len(results) else 1
if __name__=="__main__": raise SystemExit(main())
