#!/usr/bin/env python3
"""Assemble a single-file Vikkypaedia module (Standard engine v2.2)."""
EXPECT_UNITS, EXPECT_ITEMS = 20, 40
import os, re, sys

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

def read(name):
    p = os.path.join(B, name)
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as f:
        return f.read()

UNIT_FILES = ["20_partA.html", "30_partB.html", "40_partC.html",
              "50_partD.html", "60_partE.html"]

head   = read("00_head.html")
shell  = read("10_shell.html")
units  = "\n".join(read(f) for f in UNIT_FILES)
assess = read("70_assessment.html")
apps   = read("80_appendices.html")
examjs = read("85_examitems.html")
figjs  = read("88_figs.html")
script = read("90_script.html")
modjs  = read("05_module.html")
assert "window.VKP_MODULE" in modjs, "05_module.html missing"
loops_css = read("06_loops.css")
loops_js  = read("89_loops.js")

# Vikkypaedia Standard v2: learning loops are shared across modules
import base64
_sig = os.path.join(B, "signature.png")
if os.path.exists(_sig) and "@@SIGNATURE@@" in script:
    script = script.replace("@@SIGNATURE@@", "data:image/png;base64," + base64.b64encode(open(_sig, "rb").read()).decode())
assert "/*@@LOOPS@@*/" in script, "engine is missing the LOOPS marker"
script = script.replace("/*@@LOOPS@@*/", loops_js)
# v2.2: interactive megacodes. The player is shared; case data (86) exists only where a module has cases.
mega_js = read("87_megacode.js")
assert "/*@@MEGA@@*/" in script, "engine is missing the MEGA marker"
script = script.replace("/*@@MEGA@@*/", mega_js)
mega_html = read("86_megacodes.html")
if mega_html:
    assert "window.VKP_MEGACODES" in mega_html and 'id="megacodes"' in mega_html, "86_megacodes.html is malformed"
assert head.count("</style>") >= 1
head = head.replace("</style>", loops_css + "\n</style>", 1)

shell = shell.replace("<!--UNITS-->", units)
shell = shell.replace("<!--ASSESSMENT-->", (mega_html + "\n" if mega_html else "") + assess)
shell = shell.replace("<!--APPENDICES-->", apps)

html = head + shell + modjs + examjs + figjs + script

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

# ---- structural checks -------------------------------------------------
errs, warns = [], []

n_units = len(re.findall(r'<section class="unit"', html))
if n_units != EXPECT_UNITS:
    errs.append("unit count is %d, expected %d" % (n_units, EXPECT_UNITS))

qs = re.findall(r'<div class="q" data-q="([^"]+)"', html)
if len(qs) != len(set(qs)):
    dup = [q for q in set(qs) if qs.count(q) > 1]
    errs.append("duplicate question ids: %s" % dup)
if len(qs) != EXPECT_ITEMS:
    errs.append("checkpoint count is %d, expected %d" % (len(qs), EXPECT_ITEMS))

# one data-c="1" per question block
for block in re.findall(r'<div class="q" data-q="([^"]+)".*?(?=<div class="q" data-q="|</section>)', html, re.S):
    pass
blocks = re.split(r'(?=<div class="q" data-q=")', html)
for b in blocks[1:]:
    qid = re.search(r'data-q="([^"]+)"', b).group(1)
    body = b.split("</div><!--/q-->")[0]
    n = body.count('data-c="1"')
    if n != 1:
        errs.append("question %s has %d correct options (expected 1)" % (qid, n))

for marker in ["@@SIGNATURE@@", "/*@@LOOPS@@*/", "/*@@MEGA@@*/", "<!--UNITS-->", "<!--ASSESSMENT-->", "<!--APPENDICES-->", "PLACEHOLDER", "TODO", "TKTK"]:
    if marker in html:
        errs.append("leftover marker: %s" % marker)

# every getElementById / $("#id") has a matching id
ids = set(re.findall(r'\sid="([^"]+)"', html))
refs = set(re.findall(r'\$\("#([A-Za-z][\w-]*)"\)', script)) | set(re.findall(r'getElementById\("([^"]+)"\)', script))
refs -= {"part" , "u"}
missing = sorted(r for r in refs if r not in ids and not r.startswith("part"))
if missing:
    warns.append("script references ids not in HTML: %s" % missing)

# every unit's data-part must match the Part map in 05_module.html
_pm = {}
for k, us in re.findall(r'key:"([A-E])",\s*units:\[([\d,\s]+)\]', modjs):
    for u in us.split(","): _pm[int(u)] = k
for u, part in re.findall(r'<section class="unit" id="u\d+" data-unit="(\d+)" data-part="([A-E])"', html):
    if _pm.get(int(u)) != part:
        errs.append("unit %s is in Part %s in the HTML but Part %s in 05_module.html" % (u, part, _pm.get(int(u))))
opens = len(re.findall(r"<section", html)); closes = len(re.findall(r"</section>", html))
if opens != closes:
    errs.append("section tags unbalanced: %d open, %d close" % (opens, closes))

size = os.path.getsize(OUT)
print("wrote %s  (%.1f KB)" % (OUT, size/1024))
print("units: %d   checkpoints: %d" % (n_units, len(qs)))
for w in warns: print("  warn: %s" % w)
for e in errs:  print("  ERROR: %s" % e)
sys.exit(1 if errs else 0)
