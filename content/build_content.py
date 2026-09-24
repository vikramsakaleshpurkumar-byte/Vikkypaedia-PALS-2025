"""Generate build/20_partA.html … 60_partE.html from the content modules."""
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
FILES = {"A": "20_partA.html", "B": "30_partB.html", "C": "40_partC.html", "D": "50_partD.html", "E": "60_partE.html"}
for mod in ["partA", "partB", "partC", "partD", "partE"]:
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), mod + ".py")):
        importlib.import_module(mod)
importlib.import_module("balance")
for k, f in FILES.items():
    if k in gen.PARTS_META:
        open(os.path.join(OUT, f), "w", encoding="utf-8").write(gen.part_html(k))
        print("wrote", f, [u for u in gen.PARTS_META[k]["units"]])
