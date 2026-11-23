"""A field bound to a role the visual type does not own must abort the build."""
import json
import pathlib
import subprocess
import sys
import tempfile

spec = json.loads(pathlib.Path("examples/finance/spec.json").read_text(encoding="utf-8"))
spec["csv"] = str(pathlib.Path("examples/finance/data/fin.csv").resolve())
spec["visuals"] = [{"name": "bad", "type": "card", "category": "Fin[年份]"}]

with tempfile.TemporaryDirectory() as d:
    f = pathlib.Path(d) / "bad.json"
    f.write_text(json.dumps(spec), encoding="utf-8")
    r = subprocess.run([sys.executable, "pbipgen.py", str(f)], capture_output=True, text=True)
    if r.returncode == 0:
        raise SystemExit("expected a non-zero exit: 'card' has no Category role")
    print(r.stderr.strip().splitlines()[-1])
