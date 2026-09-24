import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_URL = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
VERIFY_URL = "file:///" + os.path.join(ROOT, "verify.html").replace("\\", "/").lstrip("/")
import json, os, re
from playwright.sync_api import sync_playwright
SKIP_ONB = "try{var K='vkp.pals2025.v4';var r=localStorage.getItem(K);"\
    "var s=r?JSON.parse(r):{v:1,items:{},prefs:{pri:'all',lvl:'x',set:'both',fs:'m',theme:'system'},"\
    "placement:null,lastUnit:null,exam:{attempts:[],lockUntil:0},settings:null,started:null,"\
    "profile:null,plan:null,onboarded:false};"\
    "s.onboarded=true;localStorage.setItem(K,JSON.stringify(s));}catch(e){}"

PATH = MODULE_URL
errs=[]; fails=[]
def check(name, cond, extra=""):
    print(("  OK   " if cond else "  FAIL ")+name+((" :: "+str(extra)) if extra and not cond else ""))
    if not cond: fails.append(name)


def seed_and_reload(page, mutate_js, expect_js, tries=4, settle=350, after=1000):
    """Write state, then reload and confirm it survived.

    Chromium commits file:// localStorage asynchronously: a reload issued
    immediately after a write can start the next document before the write
    lands, and the page then boots from an empty store. Write, let it settle,
    reload, and verify -- retrying rather than assuming.
    """
    for _ in range(tries):
        page.evaluate(mutate_js)
        page.wait_for_timeout(settle)
        page.reload()
        page.wait_for_timeout(after)
        if page.evaluate(expect_js):
            return True
    raise AssertionError("state did not survive the reload after %d attempts" % tries)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width":1280,"height":1000}, accept_downloads=True)
    ctx.add_init_script(SKIP_ONB)
    p = ctx.new_page()
    p.on("pageerror", lambda e: errs.append("PAGEERROR:"+str(e)))
    p.on("console", lambda m: errs.append("CONSOLE:"+m.text) if m.type=="error" else None)
    p.goto(PATH); p.wait_for_timeout(700)

    print("\n== 1. PART GATING ==")
    check("Part B locked at start", p.evaluate("()=>document.querySelector('#u5').getAttribute('data-locked')==='1'"))
    check("Part B status says Locked", "Locked" in p.evaluate("()=>document.querySelector('#partB .part-status').textContent"))
    p.click('#u5 .unit-head'); p.wait_for_timeout(200)
    check("locked unit will not open by click", p.evaluate("()=>document.querySelector('#u5 .unit-body').hidden"))
    check("lock note shown", p.evaluate("()=>!!document.querySelector('#u5 .lock-note')"))
    p.click('#expandAll'); p.wait_for_timeout(300)
    check("expand-all does not open locked units", p.evaluate("()=>document.querySelector('#u5 .unit-body').hidden"))
    check("expand-all opens unlocked units", p.evaluate("()=>!document.querySelector('#u1 .unit-body').hidden"))

    # master Part A
    for q in ["1.1","1.2","2.1","2.2","3.1","3.2"]:
        p.evaluate(f"""()=>{{const q=document.querySelector('.q[data-q="{q}"]');
            const b=q.querySelector('.opt[data-c="1"]'); if(b&&!b.disabled) b.click();}}""")
        p.wait_for_timeout(50)
    p.wait_for_timeout(600)
    check("Part A complete -> Part B unlocked", p.evaluate("()=>document.querySelector('#u5').getAttribute('data-locked')==='0'"))
    check("Part C still locked", p.evaluate("()=>document.querySelector('#u10').getAttribute('data-locked')==='1'"))
    check("dashboard 3/20", "3 of 20" in p.evaluate("()=>document.querySelector('#dashLeft').textContent"))

    print("\n== 2. MASTERY REVERSAL ==")
    seed_and_reload(p,
      """()=>{const s=JSON.parse(localStorage.getItem('vkp.pals2025.v4'));
        s.items['1.1'].ok=false; s.items['1.1'].box=0;
        localStorage.setItem('vkp.pals2025.v4',JSON.stringify(s));}""",
      "()=>document.querySelector('#u5').getAttribute('data-locked')==='1'")
    check("losing an item re-locks Part B", p.evaluate("()=>document.querySelector('#u5').getAttribute('data-locked')==='1'"))

    print("\n== 3. FILTERS ==")
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"pri\"][data-v=\"must\"]').click()"); p.wait_for_timeout(200)
    r = p.evaluate("""()=>{const g=document.querySelectorAll('.tier-good'),n=document.querySelectorAll('.tier-nice');
      const hid=x=>getComputedStyle(x).display==='none';
      return {good:[...g].every(hid), nice:[...n].every(hid), qsVisible:[...document.querySelectorAll('.q')].every(x=>getComputedStyle(x).display!=='none')};}""")
    check("must-only hides good-to-know", r['good'])
    check("must-only hides nice-to-know", r['nice'])
    check("checkpoints never hidden by filter", r['qsVisible'])
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"pri\"][data-v=\"all\"]').click()")
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"set\"][data-v=\"rc\"]').click()"); p.wait_for_timeout(200)
    check("rc track hides ideal panels", p.evaluate("()=>[...document.querySelectorAll('.track-id')].every(x=>getComputedStyle(x).display==='none')"))
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"set\"][data-v=\"both\"]').click()")

    print("\n== 4. THEME ==")
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"theme\"][data-v=\"dark\"]').click()"); p.wait_for_timeout(200)
    bg = p.evaluate("()=>getComputedStyle(document.body).backgroundColor")
    check("dark theme applies", bg.replace(' ','') in ("rgb(10,13,18)",), bg)
    p.screenshot(path="shot-dark.png", full_page=False)
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"theme\"][data-v=\"light\"]').click()"); p.wait_for_timeout(200)

    print("\n== 5. EXAM ENGINE ==")
    # force full coverage + retention so the criteria panel is meaningful
    seed_and_reload(p,
      """()=>{const K='vkp.pals2025.v4';const s=JSON.parse(localStorage.getItem(K));
        const past=Date.now()-3*86400000; s.items=s.items||{};
        document.querySelectorAll('.q').forEach(q=>{s.items[q.getAttribute('data-q')]=
          {box:3,due:Date.now()+7*86400000,ok:true,firstPass:past,longest:2*86400000,
           retained:true,hint:0,tries:2};});
        localStorage.setItem(K,JSON.stringify(s));}""",
      "()=>[...document.querySelectorAll('.crit')].every(c=>c.getAttribute('data-met')==='1'||c.querySelector('.cval').textContent==='\u2014')")
    crit = p.evaluate("()=>[...document.querySelectorAll('.crit')].map(c=>({met:c.getAttribute('data-met'),v:c.querySelector('.cval').textContent}))")
    print("   criteria:", json.dumps(crit))
    check("coverage criterion met", crit[0]['met']=='1' and crit[0]['v']=='40/40')
    check("retention criterion met", crit[1]['met']=='1' and crit[1]['v']=='20/20')
    check("applied criterion not yet met", crit[2]['met']=='0')
    check("all 20 units mastered", "20 of 20" in p.evaluate("()=>document.querySelector('#dashLeft').textContent"))
    check("no unit locked now", p.evaluate("()=>[...document.querySelectorAll('.unit')].every(u=>u.getAttribute('data-locked')==='0')"))

    p.click('#startExam'); p.wait_for_timeout(600)
    n = p.evaluate("()=>document.querySelector('#examRunner .exam-topbar').textContent")
    check("exam started with 50 items", "of 50" in n, n)
    check("timer running", p.evaluate("()=>/^\\d+:\\d\\d$/.test(document.querySelector('#examTimer').textContent)"), p.evaluate("()=>document.querySelector('#examTimer').textContent"))
    # answer all correctly via the underlying data
    total = p.evaluate("()=>window.__E ? 0 : 0")
    p.evaluate("""()=>{ // click the correct option on every item
      const go=()=>{const opts=[...document.querySelectorAll('#examOpts .opt')];
        return opts;};
      window.__answer=()=>{};}""")
    for i in range(50):
        done = p.evaluate("""()=>{
          const ol=document.querySelector('#examOpts'); if(!ol) return 'noopts';
          const btns=[...ol.querySelectorAll('.opt')];
          // find the correct one by matching against EXAM state is not exposed; use text heuristics is unsafe.
          return btns.length; }""")
        # click first option, then Next
        p.evaluate("()=>{const b=document.querySelector('#examOpts .opt'); if(b) b.click();}")
        p.wait_for_timeout(30)
        p.evaluate("()=>{const n=document.querySelector('#exNext'); if(n && !n.disabled) n.click();}")
        p.wait_for_timeout(30)
    p.evaluate("()=>{const s=document.querySelector('#exSubmit'); if(s) s.click();}")
    p.wait_for_timeout(800)
    res = p.evaluate("()=>document.querySelector('#examRunner').textContent.slice(0,200)")
    check("exam scored and remediation plan shown", "Attempt 1" in res and ("%" in res), res[:90])
    check("attempt recorded", p.evaluate("()=>JSON.parse(localStorage.getItem('vkp.pals2025.v4')).exam.attempts.length===1"))
    check("24h lock applied", p.evaluate("()=>JSON.parse(localStorage.getItem('vkp.pals2025.v4')).exam.lockUntil>Date.now()"))
    p.evaluate("()=>{const r=document.querySelector('#exReview'); if(r) r.click();}"); p.wait_for_timeout(500)
    check("item review renders rationales", p.evaluate("()=>document.querySelectorAll('#examRunner .rationale').length>=40"))

    print("\n== 6. CERTIFICATE ==")
    seed_and_reload(p,
      """()=>{const K='vkp.pals2025.v4';const s=JSON.parse(localStorage.getItem(K));
        s.exam.attempts=[{at:Date.now(),n:50,right:48,pct:96}]; s.exam.lockUntil=0;
        localStorage.setItem(K,JSON.stringify(s));}""",
      "()=>!document.querySelector('#certGate').hidden")
    check("cert gate opens when all 3 criteria met", p.evaluate("()=>!document.querySelector('#certGate').hidden"))
    check("not-ready card hidden", p.evaluate("()=>document.querySelector('#certNotReady').hidden"))
    p.fill('#certName','Dr Ananya Raghavan')
    p.click('#makeCert'); p.wait_for_timeout(700)
    cv = p.evaluate("""()=>{const c=document.getElementById('certCanvas');
      const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
      let nonwhite=0; for(let i=0;i<d.length;i+=4000){ if(d[i]<240) nonwhite++; }
      return {w:c.width,h:c.height,ink:nonwhite, printLen:document.getElementById('printRoot').innerHTML.length};}""")
    check("certificate canvas 2400x1697 with content", cv['w']==2400 and cv['h']==1697 and cv['ink']>50, cv)
    check("print sheet built", cv['printLen']>800)
    check("verification code present", "PA26-" in p.evaluate("()=>document.getElementById('printRoot').textContent"))
    check("scope statement in print sheet", "does not attest" in p.evaluate("()=>document.getElementById('printRoot').textContent"))

    print("\n== 7. EXPORT CONFIGURED COPY ==")
    p.fill('#fName','Dr Vikram Sakaleshpur Kumar')
    p.fill('#fCut','85'); p.dispatch_event('#fCut','change'); p.wait_for_timeout(300)
    check("cut score setting applied", "85%" in p.evaluate("()=>document.querySelector('#criteria').textContent"))
    with p.expect_download(timeout=15000) as dl:
        p.click('#exportCopy')
    d = dl.value
    out = "/tmp/exported.html"; d.save_as(out)
    exp = open(out,encoding='utf-8').read()
    check("export produced a file", os.path.getsize(out)>400000, os.path.getsize(out))
    check("export has seed script", "__VKP_SEED__" in exp)
    # parse the exported DOM: no .opt may carry data-state or disabled
    ctxq = b.new_context(); pq = ctxq.new_page(); pq.goto("file:///tmp/exported.html"); pq.wait_for_timeout(400)
    residue = pq.evaluate("()=>({state:document.querySelectorAll('.q .opt[data-state]').length, hints:[...document.querySelectorAll('.hint')].filter(h=>!h.hidden).length, rats:[...document.querySelectorAll('.rationale')].filter(r=>!r.hidden).length})")
    ctxq.close()
    check("export reset all questions (DOM)", residue['state']==0 and residue['hints']==0 and residue['rats']==0, residue)
    check("export removed runtime nodes", 'class="verdict' not in exp and 'class="remed"' not in exp and 'class="part-status"' not in exp)
    check("export emptied ugrid/toc", re.search(r'id="ugrid"[^>]*>\s*</div>', exp) is not None)
    check("export units collapsed", exp.count('data-open="0"')>=20)
    check("export keeps all 20 units", exp.count('<section class="unit"')==20)
    ctx.close()

    print("\n== 8. EXPORTED FILE LOADS CLEAN ==")
    ctx2 = b.new_context(viewport={"width":400,"height":900})
    p2 = ctx2.new_page(); e2=[]
    p2.on("pageerror", lambda e: e2.append(str(e)))
    p2.goto("file:///tmp/exported.html"); p2.wait_for_timeout(800)
    check("exported file renders 20 units", p2.evaluate("()=>document.querySelectorAll('.unit').length")==20)
    check("exported file starts fresh (0 mastered)", "0 of 20" in p2.evaluate("()=>document.querySelector('#dashLeft').textContent"))
    check("exported file inherits cut score 85", "85%" in p2.evaluate("()=>document.querySelector('#criteria').textContent"))
    check("exported file no JS errors", not e2, e2)
    check("exported file no horizontal scroll", p2.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")<=0)
    p2.screenshot(path="shot-mobile-final.png")
    b.close()

print("\nJS ERRORS:", errs if errs else "none")
print("FAILURES:", fails if fails else "none")
