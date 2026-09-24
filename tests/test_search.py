import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_URL = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
from playwright.sync_api import sync_playwright
SKIP_ONB = ("try{var K='vkp.pals2025.v4';var r=localStorage.getItem(K);"
    "var s=r?JSON.parse(r):{v:1,items:{},prefs:{pri:'all',lvl:'x',set:'both',fs:'m',theme:'system'},"
    "placement:null,lastUnit:null,exam:{attempts:[],lockUntil:0},settings:null,started:null,"
    "profile:null,plan:null,onboarded:false};"
    "s.onboarded=true;localStorage.setItem(K,JSON.stringify(s));}catch(e){}")
fails=[]
def check(n,c,x=""):
    print(("  OK   " if c else "  FAIL ")+n+((" :: "+str(x)) if x and not c else ""))
    if not c: fails.append(n)

with sync_playwright() as pw:
    b=pw.chromium.launch(); ctx=b.new_context(viewport={"width":1280,"height":900},reduced_motion="reduce")
    ctx.add_init_script(SKIP_ONB); p=ctx.new_page()
    errs=[]; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(MODULE_URL); p.wait_for_timeout(800)

    print("\n== OPENING ==")
    check("palette hidden at rest", p.evaluate("()=>document.getElementById('srch').hidden"))
    p.keyboard.press("Control+k"); p.wait_for_timeout(300)
    check("Ctrl+K opens it", p.evaluate("()=>!document.getElementById('srch').hidden"))
    check("input is focused", p.evaluate("()=>document.activeElement.id")=='srchInput')
    p.keyboard.press("Escape"); p.wait_for_timeout(250)
    check("Escape closes it", p.evaluate("()=>document.getElementById('srch').hidden"))
    p.keyboard.press("/"); p.wait_for_timeout(300)
    check("slash opens it", p.evaluate("()=>!document.getElementById('srch').hidden"))
    check("slash did not land in the box", p.evaluate("()=>document.getElementById('srchInput').value")=="")

    print("\n== RESULTS ==")
    p.fill("#srchInput","epinephrine"); p.wait_for_timeout(400)
    r=p.evaluate("()=>({n:document.querySelectorAll('.sr').length,count:document.getElementById('srchCount').textContent,marks:document.querySelectorAll('.sr-txt mark').length})")
    print("   ", r)
    check("finds epinephrine", r['n']>3, r)
    check("highlights the term", r['marks']>0, r)
    p.fill("#srchInput","adrenaline dose"); p.wait_for_timeout(400)
    check("multi-word requires all terms",
      p.evaluate("""()=>[...document.querySelectorAll('.sr')].every(e=>{const t=e.textContent.toLowerCase();
        return t.includes('adrenaline')||e.querySelector('.sr-note');})"""))
    p.fill("#srchInput","zzzqqq"); p.wait_for_timeout(400)
    check("empty state shown", p.evaluate("()=>!!document.querySelector('.srch-empty')"))

    print("\n== ANSWERS ARE NOT LEAKED ==")
    rat = p.evaluate("""()=>{const r=document.querySelector('.rationale');
      return r? r.textContent.replace(/\\s+/g,' ').trim().slice(40,90):'';}""")
    p.fill("#srchInput", rat[:34]); p.wait_for_timeout(450)
    check("rationale text is not indexed", p.evaluate("()=>!!document.querySelector('.srch-empty')"),
          p.evaluate("()=>document.getElementById('srchCount').textContent"))
    hint = p.evaluate("""()=>{const h=document.querySelector('.hint p');
      return h? h.textContent.replace(/\\s+/g,' ').trim().slice(0,34):'';}""")
    p.fill("#srchInput", hint); p.wait_for_timeout(450)
    check("hint text is not indexed", p.evaluate("()=>!!document.querySelector('.srch-empty')"))

    print("\n== LOCKED UNITS ==")
    p.fill("#srchInput","sotalol"); p.wait_for_timeout(450)
    lk=p.evaluate("""()=>{const rs=[...document.querySelectorAll('.sr')];
      const locked=rs.filter(e=>e.querySelector('.sr-lock'));
      return {total:rs.length, locked:locked.length,
              leaks:locked.filter(e=>e.querySelector('.sr-txt')).length};}""")
    print("   ", lk)
    check("locked units appear in results", lk['locked']>0, lk)
    check("locked results show no content", lk['leaks']==0, lk)

    print("\n== NAVIGATION ==")
    p.fill("#srchInput","closed-loop"); p.wait_for_timeout(450)
    p.keyboard.press("ArrowDown"); p.wait_for_timeout(150)
    check("arrow moves the selection", p.evaluate("()=>document.querySelectorAll('.sr')[1].getAttribute('aria-selected')")=='true')
    p.keyboard.press("ArrowUp"); p.wait_for_timeout(150)
    p.fill("#srchInput","two roads to arrest"); p.wait_for_timeout(450)
    p.keyboard.press("Enter"); p.wait_for_timeout(1200)
    check("enter closes the palette", p.evaluate("()=>document.getElementById('srch').hidden"))
    check("body scroll restored", p.evaluate("()=>getComputedStyle(document.body).overflow")!='hidden')
    check("target unit is open", p.evaluate("()=>document.querySelector('#u1').getAttribute('data-open')")=='1')

    print("\n== APPENDICES ARE REACHABLE ==")
    p.keyboard.press("Control+k"); p.wait_for_timeout(250)
    p.fill("#srchInput","Angoff"); p.wait_for_timeout(450)
    check("finds appendix content", p.evaluate("()=>document.querySelectorAll('.sr').length")>0)
    p.keyboard.press("Enter"); p.wait_for_timeout(1000)
    check("appendix opened", p.evaluate("()=>[...document.querySelectorAll('.appendix')].some(a=>a.getAttribute('data-open')==='1')"))

    print("\n== FIGURES ==")
    figs=p.evaluate("""()=>[...document.querySelectorAll('.fig-svg')].map(h=>({
      key:h.getAttribute('data-figspec'), svg:h.querySelectorAll('svg').length,
      nodes:h.querySelectorAll('.fn').length, label:!!h.querySelector('svg[aria-label]')}))""")
    check("every figure rendered once", all(f['svg']==1 and f['nodes']>3 for f in figs), figs)
    check("figures are labelled for screen readers", all(f['label'] for f in figs), figs)
    check("text version still present", p.evaluate("()=>document.querySelectorAll('.fig-alt pre').length")==len(figs))
    p.evaluate("()=>document.querySelector('.fig-svg').click()"); p.wait_for_timeout(400)
    check("clicking opens the full-screen viewer", p.evaluate("()=>!document.getElementById('figZoom').hidden"))
    check("viewer has the diagram", p.evaluate("()=>!!document.querySelector('#figZoomBody svg')"))
    p.keyboard.press("Escape"); p.wait_for_timeout(300)
    check("escape closes the viewer", p.evaluate("()=>document.getElementById('figZoom').hidden"))
    check("viewer emptied", p.evaluate("()=>document.getElementById('figZoomBody').innerHTML")=="")

    print("\nJS ERRORS:", errs or "none")
    print("FAILURES:", fails or "none")
    b.close()
