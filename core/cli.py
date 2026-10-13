import argparse, json
from pathlib import Path
from core.scoring import recommend_assortment

def main():
    p=argparse.ArgumentParser(description="Retail assortment planning")
    p.add_argument("input"); p.add_argument("--limit",type=int,default=5); a=p.parse_args()
    try:
        data=json.loads(Path(a.input).read_text(encoding="utf-8"))
        print(json.dumps(recommend_assortment(data,a.limit),indent=2)); return 0
    except (OSError,ValueError,json.JSONDecodeError) as e: p.exit(1,f"Error: {e}\n")
if __name__=="__main__": raise SystemExit(main())
