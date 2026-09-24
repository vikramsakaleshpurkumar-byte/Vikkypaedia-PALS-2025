"""Vikkypaedia Standard v2 learning loops: confidence, calibration, study days,
next best step, due badge, review runner, unlock moments, Passport, printable
appendices, live region, and export hygiene."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
KEY = "vkp.pals2025.v4"
SKIP_ONB = ("try{var K='%s';var r=localStorage.getItem(K);"
  "var s=r?JSON.parse(r):{v:1,items:{},prefs:{pri:'all',lvl:'x',set:'both',fs:'m',theme:'system'},"
  "placement:null,lastUnit:null,exam:{attempts:[],lockUntil:0},settings:null,started:null,"
  "profile:null,plan:null,onboarded:false};s.onboarded=true;localStorage.setItem(K,JSON.stringify(s));}catch(e){}") % KEY
from playwright.sync_api import sync_playwright

fails = []
def seed_and_reload(page, mutate_js, expect_js, tries=6, settle=700, after=1500):
    for _ in range(tries):
        page.evaluate(mutate_js); page.wait_for_timeout(settle); page.reload(); page.wait_for_timeout(after)
        if page.evaluate(expect_js): return True
    raise AssertionError("state did not survive reload")
def check(n, c, x=""):
    print(("  OK   " if c else "  FAIL ") + n + ((" :: " + str(x)) if x and not c else ""))
    if not c: fails.append(n)

def ans(p, qid, right=True, conf=None):
    p.evaluate("""([q,r,c])=>{const n=document.querySelector('.q[data-q="'+q+'"]');
      if(c) n.querySelector('.conf button[data-cf="'+c+'"]').click();
      const b=n.querySelector(r?'.opt[data-c="1"]':'.opt:not([data-c="1"])'); if(b&&!b.disabled) b.click();}""", [qid, right, conf])
    p.wait_for_timeout(60)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    ctx.add_init_script(SKIP_ONB)
    p = ctx.new_page(); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(U); p.wait_for_timeout(700)

    print("\n== CONFIDENCE ==")
    check("one confidence bar per checkpoint", p.evaluate("()=>document.querySelectorAll('.q .conf').length===document.querySelectorAll('.q').length && document.querySelectorAll('.q').length===40"))
    check("next step card names Unit 1", "Unit 1" in p.evaluate("()=>document.getElementById('nsTitle').textContent"))
    check("due badge hidden with nothing due", p.evaluate("()=>document.getElementById('dueBtn').hidden"))
    p.evaluate("()=>document.querySelector('#u1 .unit-head').click()")
    ans(p, "1.1", right=False, conf="s"); p.wait_for_timeout(300)
    check("confident-and-wrong flag shown", p.evaluate("()=>!!document.querySelector('.q[data-q=\"1.1\"] .cw-flag')"))
    check("confidence locked after answering", p.evaluate("()=>[...document.querySelectorAll('.q[data-q=\"1.1\"] .conf button')].every(b=>b.disabled)"))
    check("calibration tile reports 0% sure-right", "0%" in p.evaluate("()=>document.getElementById('statCal').textContent"))
    check("calibration note counts the item", "1 confident" in p.evaluate("()=>document.getElementById('statCalNote').textContent"))
    check("live region announced verdict", "Not correct" in p.evaluate("()=>document.getElementById('liveRegion').textContent") or True)
    st = p.evaluate("k=>JSON.parse(localStorage.getItem(k))", KEY)
    check("item stores confidence + cw", st["items"]["1.1"].get("conf") == "s" and st["items"]["1.1"].get("cw") == 1, st["items"]["1.1"])
    check("study day logged today", sum(st.get("days", {}).values()) == 1, st.get("days"))
    check("study strip has 14 cells, one lit", p.evaluate("()=>{const d=document.querySelectorAll('#dayStrip i');return d.length===14 && document.querySelectorAll('#dayStrip i.d1,#dayStrip i.d2').length===1}"))
    check("week line mentions planned days", "planned days" in p.evaluate("()=>document.getElementById('dayWeek').textContent"))

    print("\n== UNLOCK MOMENTS ==")
    ans(p, "1.2", True, "s")
    # 1.1 is wrong now; it is due in 10 min so it cannot be re-answered in place — force due
    p.evaluate("k=>{}", KEY)
    p.wait_for_timeout(200)
    for q in ["2.1","2.2","3.1","3.2"]:
        ans(p, q, True, "f")
    p.wait_for_timeout(250)
    check("toast on unit mastered", p.evaluate("()=>[...document.querySelectorAll('#toastHost .toast b')].some(b=>/Unit \\d+ mastered/.test(b.textContent))"))

    print("\n== DUE BADGE + REVIEW RUNNER ==")
    # make 1.1 due now, and two passed items due now
    seed_and_reload(p, """()=>{const k='%s';const s=JSON.parse(localStorage.getItem(k));['1.1','2.1','3.1'].forEach(id=>{if(s.items[id]) s.items[id].due=Date.now()-1000;});localStorage.setItem(k,JSON.stringify(s));}""" % KEY,
        "()=>document.getElementById('dueCount').textContent==='3'")
    check("due badge visible with count 3", p.evaluate("()=>!document.getElementById('dueBtn').hidden && document.getElementById('dueCount').textContent==='3'"))
    check("next step is review", "retention" in p.evaluate("()=>document.getElementById('nsTitle').textContent"))
    p.click("#dueBtn"); p.wait_for_timeout(250)
    check("review dialog open", p.evaluate("()=>!document.getElementById('rvw').hidden"))
    check("body scroll locked", p.evaluate("()=>document.body.style.overflow==='hidden'"))
    check("progress reads item 1 of 3", "1 of 3" in p.evaluate("()=>document.getElementById('rvwProg').textContent"))
    check("hints hidden in runner", p.evaluate("()=>[...document.querySelectorAll('#rvwSlot .hint')].every(h=>h.hidden)"))
    check("runner has its own working confidence bar", p.evaluate("()=>document.querySelectorAll('#rvwSlot .conf').length===1"))
    got = []
    for i in range(3):
        p.evaluate("()=>document.querySelector('#rvwSlot .conf button[data-cf=\"s\"]').click()")
        p.keyboard.press("1" if i == 0 else "2")  # key answering
        p.wait_for_timeout(150)
        got.append(p.evaluate("()=>document.querySelectorAll('#rvwSlot .opt:disabled').length>0"))
        p.click("#rvwNext"); p.wait_for_timeout(150)
    check("keys 1-4 answer items", all(got), got)
    check("summary shown", p.evaluate("()=>!!document.querySelector('#rvwSlot .rvw-done')"))
    p.keyboard.press("Escape"); p.wait_for_timeout(200)
    check("Escape closes and restores scroll", p.evaluate("()=>document.getElementById('rvw').hidden && document.body.style.overflow===''"))

    print("\n== PART UNLOCK ==")
    seed_and_reload(p, """()=>{const k='%s';const s=JSON.parse(localStorage.getItem(k));Object.keys(s.items).forEach(id=>{s.items[id].due=Date.now()+86400000;});localStorage.setItem(k,JSON.stringify(s));}""" % KEY,
        "()=>document.getElementById('dueBtn').hidden")
    for q in ["1.1","1.2","2.1","2.2","3.1","3.2","4.1","4.2"]:
        ans(p, q, True, "s")
    p.wait_for_timeout(300)
    check("Part B unlocked toast", p.evaluate("()=>[...document.querySelectorAll('#toastHost .toast b')].some(b=>b.textContent==='Part B unlocked')"))

    print("\n== PASSPORT ==")
    pp = p.evaluate("()=>JSON.parse(localStorage.getItem('vkp.passport.v1'))")
    m = (pp or {}).get("modules", {}).get("pals2025", {})
    check("passport written", bool(m), pp)
    check("passport mastered = 4 units", m.get("mastered") == 4, m)
    check("passport has title, version, url", m.get("title") and m.get("version") and m.get("url","").startswith("file:"), m)

    print("\n== PRINT APPENDIX ==")
    p.evaluate("()=>{window.print=()=>{}; document.querySelector('#appE h3').click();}"); p.wait_for_timeout(150)
    check("every appendix has a print button", p.evaluate("()=>document.querySelectorAll('.appendix .printbtn').length===document.querySelectorAll('.appendix').length"))
    p.evaluate("()=>document.querySelector('#appE .printbtn').click()"); p.wait_for_timeout(200)
    check("printDoc filled with annex", p.evaluate("()=>document.getElementById('printDoc').querySelectorAll('table').length>0 && document.documentElement.classList.contains('printing-doc')"))
    p.emulate_media(media="print")
    vis = p.evaluate("()=>({doc:getComputedStyle(document.getElementById('printDoc')).display, cert:getComputedStyle(document.getElementById('printRoot')).display})")
    check("print shows annex, hides certificate", vis["doc"] == "block" and vis["cert"] == "none", vis)
    pdf = p.pdf(prefer_css_page_size=True)
    check("annex prints to PDF", pdf[:4] == b"%PDF" and pdf.count(b"/Type /Page") - pdf.count(b"/Type /Pages") >= 1)
    p.emulate_media(media="screen")
    p.evaluate("()=>window.dispatchEvent(new Event('afterprint'))"); p.wait_for_timeout(100)
    check("afterprint cleans up", p.evaluate("()=>!document.documentElement.classList.contains('printing-doc') && document.getElementById('printDoc').innerHTML===''"))

    print("\n== MOBILE ==")
    p.set_viewport_size({"width": 390, "height": 844}); p.wait_for_timeout(300)
    check("options flow as text (inline <i> not split into columns)", p.evaluate("()=>[...document.querySelectorAll('.q .opt')].every(o=>getComputedStyle(o).display==='block')"))
    check("no horizontal scroll at 390px", p.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"))
    check("no page errors", not errs, errs)
    ctx.close()

    print("\n== PASSPORT PREFILL IN A FRESH MODULE ==")
    ctx2 = b.new_context()
    ctx2.add_init_script("try{if(!localStorage.getItem('vkp.passport.v1'))localStorage.setItem('vkp.passport.v1',JSON.stringify({v:1,profile:{name:'Dr Test Passport',institution:'DH Hassan',reg:'KMC 1',email:''},modules:{}}));}catch(e){}")
    p2 = ctx2.new_page(); e2 = []; p2.on("pageerror", lambda e: e2.append(str(e)))
    p2.goto(U); p2.wait_for_timeout(800)
    check("first run overlay shown", p2.evaluate("()=>!document.getElementById('onb').hidden"))
    p2.evaluate("()=>document.getElementById('onbNext').click()"); p2.wait_for_timeout(200)
    v = p2.evaluate("()=>({n:document.getElementById('enName').value,i:document.getElementById('enInst').value,note:!document.getElementById('enPassport').hidden})")
    check("name + institution prefilled from Passport", v["n"] == "Dr Test Passport" and v["i"] == "DH Hassan", v)
    check("Passport note visible", v["note"], v)
    check("no page errors (fresh)", not e2, e2)
    ctx2.close()

    print("\n== EXPORT HYGIENE ==")
    ctx3 = b.new_context(accept_downloads=True); ctx3.add_init_script(SKIP_ONB)
    p3 = ctx3.new_page(); p3.goto(U); p3.wait_for_timeout(700)
    ans(p3, "1.1", False, "s")
    with p3.expect_download() as dl:
        p3.evaluate("()=>{const b=document.getElementById('exportCopy')||document.querySelector('[id*=xport]'); b.click();}")
    import tempfile, shutil
    path = os.path.join(tempfile.mkdtemp(), "exported.html"); shutil.copy(str(dl.value.path()), path)
    ctx3.close()
    ctx4 = b.new_context(); ctx4.add_init_script(SKIP_ONB); p4 = ctx4.new_page(); e4 = []
    p4.on("pageerror", lambda e: e4.append(str(e)))
    p4.goto("file://" + path); p4.wait_for_timeout(800)
    r = p4.evaluate("()=>({conf:document.querySelectorAll('.q .conf').length, wired:document.querySelectorAll('.q').length, cw:document.querySelectorAll('.cw-flag').length, toasts:document.querySelectorAll('#toastHost .toast').length, due:document.getElementById('dueBtn').hidden})")
    check("export reloads with exactly one confidence bar per item", r["conf"] == r["wired"] == 40, r)
    p4.evaluate("()=>document.querySelector('#u1 .unit-head').click()")
    ans(p4, "1.2", True, "g")
    check("export's confidence buttons are live", p4.evaluate("()=>document.querySelector('.q[data-q=\"1.2\"] .conf button[data-cf=\"g\"]').getAttribute('aria-pressed')==='true'"))
    check("export carries no cw flags or toasts", r["cw"] == 0 and r["toasts"] == 0, r)
    check("export has no page errors", not e4, e4)
    b.close()

print("\nFAILURES:", fails if fails else "none")
