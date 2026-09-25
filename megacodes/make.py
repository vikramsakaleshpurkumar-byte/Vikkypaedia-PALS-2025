#!/usr/bin/env python3
"""Compile megacodes/cases.py into build/86_megacodes.html, after validating every case.

A case is a directed graph of decision nodes. Checks that fail the build:
  - every `to` points at an existing node, and every node is reachable from `start`;
  - every decision node has 3-4 options, at least one correct, every correct option moves on;
  - every option has feedback; every critical option is also incorrect;
  - following correct options only can never loop, and always reaches an end node;
  - from every node some end node is reachable (no dead ends after a wrong turn);
  - case.part is a real Part, case.units are real units of this module, timer marks exist.
Run:  python megacodes/make.py      (build.py then picks up build/86_megacodes.html)
"""
import html, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("cases", os.path.join(ROOT, "megacodes", "cases.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)

mod = open(os.path.join(ROOT, "build", "05_module.html"), encoding="utf-8").read()
parts = {k: [int(u) for u in us.split(",")] for k, us in re.findall(r'key:"([A-E])",\s*units:\[([\d,\s]+)\]', mod)}
all_units = {u for us in parts.values() for u in us}

errs = []
def err(case, msg): errs.append("%s: %s" % (case, msg))

seen_ids = set()
for c in C.CASES:
    cid = c["id"]
    if cid in seen_ids: err(cid, "duplicate case id")
    seen_ids.add(cid)
    for k in ("title", "patient", "part", "units", "minutes", "brief", "start", "nodes", "debrief"):
        if k not in c: err(cid, "missing " + k)
    if c.get("part") not in parts: err(cid, "unknown Part %r" % c.get("part"))
    for u in c.get("units", []):
        if u not in all_units: err(cid, "unknown unit %r" % u)
    N = c["nodes"]
    if c["start"] not in N: err(cid, "start node missing")
    marks = set()
    for nid, n in N.items():
        if n.get("end"):
            if n["end"] not in ("good", "partial", "bad"): err(cid, "%s: end must be good/partial/bad" % nid)
            continue
        opts = n.get("opts", [])
        if not 3 <= len(opts) <= 4: err(cid, "%s has %d options" % (nid, len(opts)))
        if not any(o.get("ok") for o in opts): err(cid, "%s has no correct option" % nid)
        for i, o in enumerate(opts):
            if not o.get("fb"): err(cid, "%s option %d has no feedback" % (nid, i))
            for fld in ("t", "fb"):
                bad = set(re.findall(r"</?([a-zA-Z0-9]+)", o.get(fld, ""))) - {"b", "i"}
                if bad: err(cid, "%s option %d %s uses markup other than <b>/<i>: %s" % (nid, i, fld, sorted(bad)))
            if o.get("ok") and not o.get("to"): err(cid, "%s option %d is correct but does not move on" % (nid, i))
            if o.get("ok") and o.get("crit"): err(cid, "%s option %d is both correct and critical" % (nid, i))
            if o.get("to") and o["to"] not in N: err(cid, "%s option %d -> missing node %r" % (nid, i, o["to"]))
            if o.get("mark"): marks.add(o["mark"])
    # reachability
    reach, stack = set(), [c["start"]]
    while stack:
        x = stack.pop()
        if x in reach or x not in N: continue
        reach.add(x)
        for o in N[x].get("opts", []):
            if o.get("to"): stack.append(o["to"])
    for nid in N:
        if nid not in reach: err(cid, "node %s is unreachable" % nid)
    # an end is reachable from every node
    def can_end(start):
        seen, st = set(), [start]
        while st:
            x = st.pop()
            if x in seen or x not in N: continue
            if N[x].get("end"): return True
            seen.add(x)
            for o in N[x].get("opts", []):
                if o.get("to"): st.append(o["to"])
        return False
    for nid in reach:
        if not can_end(nid): err(cid, "no end is reachable from %s" % nid)
    # correct-only path: acyclic and ends well
    def ok_walk(x, path):
        if x in path: err(cid, "correct options loop: %s" % " > ".join(path + [x])); return
        if N[x].get("end"):
            if N[x]["end"] != "good": err(cid, "correct path ends in %s at %s" % (N[x]["end"], x))
            return
        for o in N[x]["opts"]:
            if o.get("ok"): ok_walk(o["to"], path + [x])
    if c["start"] in N: ok_walk(c["start"], [])
    for t in c.get("timers", []):
        if t["mark"] not in marks: err(cid, "timer mark %r is never set" % t["mark"])

if errs:
    for e in errs: print("  ERROR:", e)
    sys.exit(1)

data = {"intro": C.INTRO, "cases": C.CASES}
js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = '''<section class="part" id="megacodes" aria-labelledby="mcH">
  <div class="part-head">
    <div>
      <span class="pk">Practice</span>
      <h2 id="mcH">Interactive megacodes</h2>
    </div>
    <span class="part-meta" id="mcSum"></span>
  </div>
  <div id="mcIntro"><p class="part-lede" id="mcIntroText"></p></div>
  <div class="mg-list" id="mcList" role="list" aria-label="Megacode cases"></div>
  <div class="card mg-runner" id="mcRunner" hidden></div>
</section>
<script>window.VKP_MEGACODES = %s;</script>
''' % js
open(os.path.join(ROOT, "build", "86_megacodes.html"), "w", encoding="utf-8").write(out)
nd = sum(len([n for n in c["nodes"].values() if not n.get("end")]) for c in C.CASES)
print("wrote build/86_megacodes.html: %d cases, %d decision points" % (len(C.CASES), nd))
for c in C.CASES:
    path, x = [], c["start"]
    while not c["nodes"][x].get("end"):
        o = [o for o in c["nodes"][x]["opts"] if o.get("ok")][0]; path.append(x); x = o["to"]
    print("  %-4s %-48s Part %s  %d decisions on the correct path" % (c["id"], c["title"][:48], c["part"], len(path)))
