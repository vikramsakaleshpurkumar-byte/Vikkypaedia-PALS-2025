"""Interactive megacodes: locking, every case along its correct path, wrong and critical calls,
personal bests, keyboard play, the completion record and verify.html, contrast and phone width.

    python tests/test_mega.py
"""
import json, os, re, tempfile
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = lambda f: "file:///" + os.path.join(ROOT, f).replace("\\", "/").lstrip("/")
KEY = re.search(r'storeKey:\s*"([^"]+)"', open(os.path.join(ROOT, "build", "05_module.html"), encoding="utf-8").read()).group(1)
fails = []
def check(n, c, x=""):
    print(("  OK   " if c else "  FAIL ") + n + ((" :: " + str(x)) if x and not c else ""))
    if not c: fails.append(n)

BLANK = "{v:1,items:{},prefs:{pri:'all',lvl:'x',set:'both',fs:'m',theme:'system'},placement:null,lastUnit:null,exam:{attempts:[],lockUntil:0},settings:null,started:Date.now(),profile:{name:'Mega Tester',institution:'Test',reg:'MT-1',email:'',enrolledAt:Date.now()},plan:null,onboarded:true}"
ONB = "try{var K='%s';if(!localStorage.getItem(K))localStorage.setItem(K,JSON.stringify(%s));}catch(e){}" % (KEY, BLANK)
MASTER_ALL = """k=>{const s=JSON.parse(localStorage.getItem(k)); document.querySelectorAll('.q').forEach(q=>{const id=q.getAttribute('data-q');
  s.items[id]=Object.assign(s.items[id]||{}, {ok:true,tries:1,box:1,due:Date.now()+86400000,hint:0,first:1});}); localStorage.setItem(k,JSON.stringify(s));}"""
CUR = """()=>{const t=document.getElementById('mcTitle').textContent; const c=VKP_MEGACODES.cases.find(c=>c.title===t);
  const txt=[...document.querySelectorAll('.mg-opt .t')].map(b=>b.textContent);
  for (const [k,n] of Object.entries(c.nodes)){ if(n.opts && n.opts.length===txt.length && n.opts.every(o=>txt.some(x=>x.includes(o.t.replace(/<[^>]+>/g,''))))) return {c:c.id,node:k}; }
  return null;}"""
CONTRAST = r"""(sel)=>{
 function rgb(s){const m=s.match(/[\d.]+/g); return m?m.map(Number):[0,0,0,0];}
 function L(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2];}
 function bg(el){while(el){const c=rgb(getComputedStyle(el).backgroundColor); if(c.length<4||c[3]>0.5) return c; el=el.parentElement;} return [255,255,255];}
 const bad=[]; document.querySelectorAll(sel+' *').forEach(el=>{
  if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) return;
  const r=el.getBoundingClientRect(); if(!r.width||!r.height||el.closest('[hidden]')) return;
  const cs=getComputedStyle(el), f=rgb(cs.color), b=bg(el), l1=L(f), l2=L(b), cr=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
  if(cs.opacity!=='1') return;
  if(cr<4.5) bad.push(el.className+' '+cr.toFixed(2)+' "'+el.textContent.trim().slice(0,24)+'"');}); return bad;}"""

with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, accept_downloads=True, reduced_motion="reduce")
    ctx.add_init_script(ONB)
    p = ctx.new_page(); errs = []; net = []
    p.on("pageerror", lambda e: errs.append(str(e)))
    ctx.on("request", lambda r: net.append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
    p.goto(url("index.html")); p.wait_for_timeout(700)
    data = p.evaluate("()=>VKP_MEGACODES")
    cases = data["cases"]

    print("\n== STRUCTURE AND LOCKING ==")
    check("6 cases shipped", len(cases) == 6, len(cases))
    check("section and TOC link present", p.evaluate("()=>!!document.getElementById('megacodes') && !!document.querySelector('#tocDesk a[href=\"#megacodes\"]')"))
    check("section sits before the final assessment", p.evaluate("()=>document.getElementById('megacodes').compareDocumentPosition(document.getElementById('assessment')) & 4") > 0)
    locked = p.evaluate("()=>[...document.querySelectorAll('#mcList .mg-card')].map(c=>c.classList.contains('locked'))")
    check("fresh learner: every case beyond Part A is locked", all(locked[i] for i, c in enumerate(cases) if c["part"] != "A"), locked)
    check("locked cards say which Part opens them", "Opens with Part" in p.evaluate("()=>document.getElementById('mcList').textContent"))
    p.evaluate(MASTER_ALL, KEY); p.wait_for_timeout(800); p.reload(); p.wait_for_timeout(900)
    check("all cases open once every Part is unlocked", p.evaluate("()=>document.querySelectorAll('#mcList .mg-card.locked').length") == 0)

    print("\n== EVERY CASE, CORRECT PATH ==")
    for i, c in enumerate(cases):
        p.evaluate("i=>document.querySelectorAll('#mcList .mg-card button')[i].click()", i); p.wait_for_timeout(150)
        steps = 0
        while steps < 25 and not p.evaluate("()=>!!document.getElementById('mcAgain')"):
            cur = p.evaluate(CUR)
            if not cur: break
            n = c["nodes"][cur["node"]]; ok = [k for k, o in enumerate(n["opts"]) if o.get("ok")][0]
            p.click('.mg-opt[data-i="%d"]' % ok); p.wait_for_timeout(60); steps += 1
        sc = p.evaluate("()=>[...document.querySelectorAll('.mg-score .sv')].map(x=>x.textContent)")
        tm = p.evaluate("()=>[...document.querySelectorAll('.mg-timers li')].every(li=>li.classList.contains('ok'))")
        check("%s: finishes 100%%, no critical errors, all key times met" % c["id"], sc[:2] == ["%d/%d" % (steps, steps), "0"] and tm, (sc, tm))
        p.click("#mcBack"); p.wait_for_timeout(120)
    check("list shows 6 of 6 practised", "6 of 6" in p.evaluate("()=>document.getElementById('mcSum').textContent"))

    print("\n== WRONG AND CRITICAL CALLS ==")
    c0 = cases[0]
    p.evaluate("()=>document.querySelectorAll('#mcList .mg-card button')[0].click()"); p.wait_for_timeout(150)
    n = c0["nodes"][c0["start"]]
    wrong = [k for k, o in enumerate(n["opts"]) if not o.get("ok") and not o.get("to")]
    crit = [k for k, o in enumerate(n["opts"]) if o.get("crit")]
    if wrong:
        p.click('.mg-opt[data-i="%d"]' % wrong[0]); p.wait_for_timeout(120)
        check("a wrong call shows feedback and disables that option", p.evaluate("i=>document.querySelector('.mg-opt[data-i=\"'+i+'\"]').disabled && !!document.querySelector('.mg-fb.no, .mg-fb.crit')", wrong[0]))
        check("the clock moves on after a wrong call", p.evaluate("()=>document.querySelector('.mg-clock b').textContent") != "0:00")
    order1 = p.evaluate("()=>[...document.querySelectorAll('.mg-opt')].map(b=>b.getAttribute('data-i')).join()")
    # play to the end choosing correctly, but with one critical error somewhere if available
    steps = 0; took_crit = False
    while steps < 25 and not p.evaluate("()=>!!document.getElementById('mcAgain')"):
        cur = p.evaluate(CUR); nn = c0["nodes"][cur["node"]]
        cr = [k for k, o in enumerate(nn["opts"]) if o.get("crit") and not o.get("to") and not p.evaluate("i=>document.querySelector('.mg-opt[data-i=\"'+i+'\"]').disabled", k)]
        if cr and not took_crit:
            p.click('.mg-opt[data-i="%d"]' % cr[0]); took_crit = True
            check("a critical call is labelled as critical", p.evaluate("()=>!!document.querySelector('.mg-fb.crit')"))
        else:
            p.click('.mg-opt[data-i="%d"]' % [k for k, o in enumerate(nn["opts"]) if o.get("ok")][0])
        p.wait_for_timeout(60); steps += 1
    if took_crit:
        check("debrief lists the critical error", p.evaluate("()=>document.querySelectorAll('.mg-crits li').length") >= 1)
    st = p.evaluate("k=>JSON.parse(localStorage.getItem(k)).mega", KEY)
    check("a worse run does not replace the personal best", st[c0["id"]]["best"]["pct"] == 100 and st[c0["id"]]["best"]["crit"] == 0 and st[c0["id"]]["runs"] == 2, st[c0["id"]])
    check("the last run is stored separately", st[c0["id"]]["last"]["pct"] < 100 or st[c0["id"]]["last"]["crit"] > 0, st[c0["id"]]["last"])
    p.click("#mcAgain"); p.wait_for_timeout(120)
    orders = set([order1])
    for _ in range(6):
        p.click("#mcQuit"); p.wait_for_timeout(60)
        p.evaluate("()=>document.querySelectorAll('#mcList .mg-card button')[0].click()"); p.wait_for_timeout(60)
        orders.add(p.evaluate("()=>[...document.querySelectorAll('.mg-opt')].map(b=>b.getAttribute('data-i')).join()"))
    check("option order is shuffled between runs", len(orders) > 1, orders)
    p.keyboard.press("A"); p.wait_for_timeout(120)
    check("keyboard letters choose options", p.evaluate("()=>!!document.querySelector('.mg-fb')"))
    check("feedback is announced to screen readers", len(p.evaluate("()=>document.getElementById('liveRegion').textContent")) > 10)
    check("'Describe the strip' reveals a text description", p.evaluate("()=>{const b=document.querySelector('.mg-desc-btn'); if(!b) return true; b.click(); return !document.querySelector('.mg-desc').hidden && b.getAttribute('aria-expanded')==='true';}"))

    print("\n== CONTRAST ==")
    for th in ("light", "dark"):
        p.evaluate("t=>document.documentElement.setAttribute('data-theme',t)", th); p.wait_for_timeout(150)
        bad = p.evaluate(CONTRAST, "#megacodes")
        check("megacode text >= 4.5:1 (%s)" % th, not bad, bad[:5])
    p.evaluate("()=>document.documentElement.removeAttribute('data-theme')")
    p.click("#mcQuit"); p.wait_for_timeout(100)

    print("\n== RECORD AND VERIFY ==")
    with p.expect_download() as d:
        p.evaluate("()=>document.getElementById('dlRecord').click()")
    rp = os.path.join(tmp, "rec.json"); d.value.save_as(rp); rec = json.load(open(rp))
    mc = rec["detail"]["megacodes"]
    check("record lists 6 practised cases", len(mc) == 6, len(mc))
    check("record keeps the best run (100%, 0 critical)", all(m["best"] == 100 and m["crit"] == 0 for m in mc))
    v = ctx.new_page(); v.on("pageerror", lambda e: errs.append("verify: " + str(e)))
    v.goto(url("verify.html")); v.wait_for_timeout(300)
    v.fill("#src", json.dumps(rec)) if v.query_selector("#src") else v.set_input_files("input[type=file]", rp)
    v.click("#go"); v.wait_for_timeout(300)
    vt = v.evaluate("()=>document.getElementById('rows').textContent")
    check("verify.html: detail checksum matches", "detail checksum matches" in vt, vt[:200])
    check("verify.html: megacodes row shown", "Megacodes practised" in vt)
    rec["detail"]["megacodes"][0]["best"] = 55
    v.fill("#src", json.dumps(rec)) if v.query_selector("#src") else None
    if v.query_selector("#src"):
        v.click("#go"); v.wait_for_timeout(300)
        check("verify.html: an altered megacode score breaks the detail checksum", "does NOT match" in v.evaluate("()=>document.getElementById('rows').textContent"))

    print("\n== PHONE WIDTH ==")
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 800})
    m.goto(url("index.html")); m.wait_for_timeout(700)
    m.evaluate("()=>document.querySelectorAll('#mcList .mg-card button')[%d].click()" % (len(cases) - 1)); m.wait_for_timeout(300)
    check("no horizontal scroll at 390 px during a case", m.evaluate("()=>document.documentElement.scrollWidth") <= 390, m.evaluate("()=>document.documentElement.scrollWidth"))
    check("monitor is not sticky on phones", m.evaluate("()=>getComputedStyle(document.querySelector('.mg-mon')).position") == "static")

    check("no page errors", not errs, errs)
    check("no network requests", not net, net[:4])
    b.close()

print("\nFAILURES:", ", ".join(fails) if fails else "none")
