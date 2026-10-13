from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
FILES=['agent.yaml','SOUL.md','README.md','RULES.md','DUTIES.md','AGENTS.md','EXPLAINABILITY.md','requirements.txt','.env.example','.gitignore','pytest.ini','core/__init__.py','core/scoring.py','core/cli.py','tools/score-assortment-candidates.yaml','tools/recommend-assortment.yaml','tools/explain-assortment-plan.yaml','skills/assortment-analysis/SKILL.md','skills/demand-aware-planning/SKILL.md','skills/assortment-explanation/SKILL.md','tests/test_scoring.py','examples/products.json']
missing=[f for f in FILES if not (R/f).is_file()]
if missing: print('FAIL: missing files: '+', '.join(missing)); sys.exit(1)
print(f'PASS: all {len(FILES)}/{len(FILES)} required files present')
