import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_URL = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
VERIFY_URL = "file:///" + os.path.join(ROOT, "verify.html").replace("\\", "/").lstrip("/")
from playwright.sync_api import sync_playwright
SKIP_ONB = "try{var K='vkp.pals2025.v4';var r=localStorage.getItem(K);"\
    "var s=r?JSON.parse(r):{v:1,items:{},prefs:{pri:'all',lvl:'x',set:'both',fs:'m',theme:'system'},"\
    "placement:null,lastUnit:null,exam:{attempts:[],lockUntil:0},settings:null,started:null,"\
    "profile:null,plan:null,onboarded:false};"\
    "s.onboarded=true;localStorage.setItem(K,JSON.stringify(s));}catch(e){}"

U=MODULE_URL
fails=[]
def check(n,c,x=""):
    print(("  OK   " if c else "  FAIL ")+n+((" :: "+str(x)) if x and not c else ""))
    if not c: fails.append(n)

with sync_playwright() as pw:
    b=pw.chromium.launch()
    ctx=b.new_context(viewport={"width":1280,"height":900}); p=ctx.new_page()
    ctx.add_init_script(SKIP_ONB)
    errs=[]; p.on("pageerror",lambda e:errs.append(str(e)))
    p.goto(U); p.wait_for_timeout(700)

    print("\n== HINTS ARE ON DEMAND ==")
    p.evaluate("()=>document.querySelector('#u1 .unit-head').click()"); p.wait_for_timeout(250)
    check("all hints hidden on load",
          p.evaluate("()=>[...document.querySelectorAll('.hint')].every(h=>h.hidden)"))
    check("hint button enabled",
          p.evaluate("()=>!document.querySelector('.q[data-q=\"1.1\"] .hint-btn').disabled"))
    p.evaluate("()=>document.querySelector('.q[data-q=\"1.1\"] .hint-btn').click()"); p.wait_for_timeout(200)
    check("first hint revealed only",
          p.evaluate("()=>{const h=[...document.querySelectorAll('.q[data-q=\"1.1\"] .hint')];return !h[0].hidden && h[1].hidden;}"))
    p.evaluate("()=>document.querySelector('.q[data-q=\"1.1\"] .hint-btn').click()"); p.wait_for_timeout(200)
    check("second hint revealed, button disabled",
          p.evaluate("()=>{const h=[...document.querySelectorAll('.q[data-q=\"1.1\"] .hint')];return !h[1].hidden && document.querySelector('.q[data-q=\"1.1\"] .hint-btn').disabled;}"))
    check("other questions still hidden",
          p.evaluate("()=>[...document.querySelectorAll('.q[data-q=\"1.2\"] .hint')].every(h=>h.hidden)"))
    p.reload(); p.wait_for_timeout(700)
    check("hints stay hidden after reload",
          p.evaluate("()=>[...document.querySelectorAll('.hint')].every(h=>h.hidden)"))

    print("\n== PROGRESS RING / TOPBAR ==")
    check("progress starts at 0",
          p.evaluate("()=>document.getElementById('heroPct').textContent")=='0%')
    check("topbar pct present", "0%" in p.evaluate("()=>document.getElementById('tbPct').textContent"))
    for q in ["1.1","1.2","2.1","2.2","3.1","3.2"]:
        p.evaluate(f"""()=>{{const q=document.querySelector('.q[data-q="{q}"]');
            const b=q.querySelector('.opt[data-c="1"]'); if(b&&!b.disabled) b.click();}}""")
        p.wait_for_timeout(40)
    p.wait_for_timeout(500)
    v=p.evaluate("()=>({hero:document.getElementById('heroPct').textContent, prog:getComputedStyle(document.documentElement).getPropertyValue('--progress').trim(), parts:document.getElementById('statParts').textContent, bar:document.getElementById('dashBar').style.width})")
    print("   ",v)
    check("ring shows 15% after Part A", v['hero']=='15%', v)
    check("--progress custom property set", v['prog'] in ('15','15.0'), v)
    check("parts tile updated", v['parts'].startswith('A, B'), v)
    check("bar width matches", v['bar']=='15%', v)

    print("\n== TOPBAR / STICKY ==")
    st=p.evaluate("()=>{const t=document.querySelector('.topbar'); return {pos:getComputedStyle(t).position, top:t.getBoundingClientRect().top};}")
    p.evaluate("()=>window.scrollTo(0,3000)"); p.wait_for_timeout(300)
    st2=p.evaluate("()=>document.querySelector('.topbar').getBoundingClientRect().top")
    check("topbar sticky at top after scroll", st['pos']=='sticky' and abs(st2)<1, (st,st2))

    print("\n== DRAWER TOC STYLED ==")
    _c = b.new_context(viewport={"width":390,"height":844})
    _c.add_init_script(SKIP_ONB)
    m = _c.new_page()
    m.goto(U); m.wait_for_timeout(700)
    m.evaluate("()=>document.getElementById('drawerOpen').click()"); m.wait_for_timeout(300)
    d=m.evaluate("""()=>{const a=document.querySelector('#tocMobile a');
      const cs=getComputedStyle(a); return {display:cs.display, pad:cs.paddingLeft, radius:cs.borderRadius};}""")
    check("drawer links styled as blocks", d['display']=='block' and d['pad']!='0px', d)
    check("no horizontal scroll on mobile",
          m.evaluate("()=>document.documentElement.scrollWidth<=window.innerWidth"))

    print("\n== REDUCED MOTION ==")
    _c = b.new_context(viewport={"width":1280,"height":900},reduced_motion="reduce")
    _c.add_init_script(SKIP_ONB)
    r = _c.new_page()
    r.goto(U); r.wait_for_timeout(500)
    check("scroll-behavior auto under reduced motion",
          r.evaluate("()=>getComputedStyle(document.documentElement).scrollBehavior")=='auto')

    print("\nJS ERRORS:", errs or "none")
    print("FAILURES:", fails or "none")
    b.close()
