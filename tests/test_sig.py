import os, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = "file:///" + os.path.join(ROOT,"index.html").replace("\\","/").lstrip("/")
SKIP=("try{var K='vkp.pals2025.v4';var r=localStorage.getItem(K);"
 "var s=r?JSON.parse(r):{v:1,items:{},prefs:{},exam:{attempts:[],lockUntil:0},onboarded:false};"
 "s.onboarded=true;localStorage.setItem(K,JSON.stringify(s));}catch(e){}")
fails=[]
def check(n,c,x=""):
    print(("  OK   " if c else "  FAIL ")+n+((" :: "+str(x)) if x and not c else ""))
    if not c: fails.append(n)

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
    b=pw.chromium.launch(); ctx=b.new_context(viewport={"width":1280,"height":900},accept_downloads=True)
    ctx.add_init_script(SKIP); p=ctx.new_page()
    errs=[]; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(U); p.wait_for_timeout(700)
    # make all criteria met so the certificate gate opens
    seed_and_reload(p,
      """()=>{const K='vkp.pals2025.v4';const s=JSON.parse(localStorage.getItem(K));
        const past=Date.now()-3*86400000; s.items=s.items||{};
        document.querySelectorAll('.q').forEach(q=>{s.items[q.getAttribute('data-q')]=
          {box:3,due:Date.now()+7*86400000,ok:true,firstPass:past,longest:2*86400000,
           retained:true,hint:0,tries:2};});
        s.exam={attempts:[{at:Date.now(),n:50,right:48,pct:96}],lockUntil:0};
        localStorage.setItem(K,JSON.stringify(s));}""",
      "()=>!document.getElementById('certGate').hidden")

    print("\n== SIGNATURE UPLOAD ==")
    check("field present and default signature previewed", p.evaluate("()=>!!document.getElementById('fPhoto') && !document.getElementById('sigPrev').hidden && document.getElementById('sigImg').src.startsWith('data:image/png')"))
    p.set_input_files("#fPhoto", os.path.join(ROOT,"tests","sig-test.png")); p.wait_for_timeout(900)
    st=p.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('vkp.pals2025.v4'));
      const d=(s.settings&&s.settings.signPhoto)||'';
      return {len:d.length, isPng:d.slice(0,22), prevShown:!document.getElementById('sigPrev').hidden,
              meta:document.getElementById('sigMeta').textContent,
              imgSet:(document.getElementById('sigImg').getAttribute('src')||'').slice(0,15)};}""")
    print("   ", {k:v for k,v in st.items() if k!='isPng'})
    check("stored as a PNG data URI", st['isPng'].startswith("data:image/png;base64"), st['isPng'])
    check("downscaled and small", 0 < st['len'] < 220000, st['len'])
    check("preview shown with size", st['prevShown'] and "KB" in st['meta'], st['meta'])
    alpha=p.evaluate("""async()=>{const s=JSON.parse(localStorage.getItem('vkp.pals2025.v4'));
      const im=new Image(); im.src=s.settings.signPhoto; await im.decode();
      const c=document.createElement('canvas'); c.width=im.width;c.height=im.height;
      c.getContext('2d').drawImage(im,0,0);
      const d=c.getContext('2d').getImageData(0,0,im.width,im.height).data;
      let clear=0,ink=0; for(let i=3;i<d.length;i+=4){ if(d[i]===0) clear++; else if(d[i]>150) ink++; }
      return {w:im.width,h:im.height,clearPct:Math.round(100*clear/(d.length/4)),inkPct:Math.round(100*ink/(d.length/4))};}""")
    print("   matte:", alpha)
    check("downscaled to 600px wide", alpha['w']==600, alpha)
    check("paper matted to transparent", alpha['clearPct']>70, alpha)
    check("ink retained", alpha['inkPct']>0.5, alpha)

    print("\n== CERTIFICATE ==")
    p.wait_for_selector("#certGate", state="visible", timeout=15000)
    p.fill("#certName","Dr Ananya Raghavan")
    p.click("#makeCert"); p.wait_for_timeout(900)
    sig=p.evaluate("""()=>{const cv=document.getElementById('certCanvas');
      const x=cv.getContext('2d');
      // sample the band just above the signature rule (y 1080-1190)
      const d=x.getImageData(700,1080,1000,110).data;
      let dark=0; for(let i=0;i<d.length;i+=4){ if(d[i]<160&&d[i+1]<160) dark++; }
      return dark;}""")
    check("signature drawn on the canvas", sig>200, sig)
    check("print sheet carries the image", p.evaluate("()=>!!document.querySelector('#printRoot .cert-sheet img.sig')"))

    print("\n== REMOVE ==")
    p.click("#sigClear"); p.wait_for_timeout(400)
    check("cleared from storage", p.evaluate("()=>{const s=JSON.parse(localStorage.getItem('vkp.pals2025.v4'));return !(s.settings&&s.settings.signPhoto);}"))
    check("preview hidden again", p.evaluate("()=>document.getElementById('sigPrev').hidden"))
    p.click("#makeCert"); p.wait_for_timeout(700)
    check("print sheet has no image when cleared", p.evaluate("()=>!document.querySelector('#printRoot .cert-sheet img.sig')"))

    print("\n== EXPORT CARRIES IT, ONCE ==")
    p.set_input_files("#fPhoto", os.path.join(ROOT,"tests","sig-test.png")); p.wait_for_timeout(900)
    with p.expect_download() as dl:
        p.click("#exportCopy")
    out="/tmp/exported-sig.html"; dl.value.save_as(out); html=open(out,encoding='utf-8').read()
    check("seed carries the signature", "__VKP_SEED__" in html and "signPhoto" in html)
    # one copy is the engine's built-in default, one is the seed; the DOM itself must hold none
    check("image not duplicated in the DOM", html.count("data:image/png;base64") == 2 and 'id="sigImg" src=' not in html, html.count("data:image/png;base64"))
    ctx2=b.new_context(); ctx2.add_init_script(SKIP)
    e=ctx2.new_page(); eerrs=[]; e.on("pageerror", lambda x: eerrs.append(str(x)))
    e.goto("file:///tmp/exported-sig.html"); e.wait_for_timeout(900)
    check("exported copy shows the signature in settings", e.evaluate("()=>!document.getElementById('sigPrev').hidden"))
    check("exported copy starts fresh", e.evaluate("()=>document.querySelectorAll('.q .opt[data-state]').length===0"))
    check("exported copy has no JS errors", not eerrs, eerrs)

    print("\nJS ERRORS:", errs or "none")
    print("FAILURES:", fails or "none")
    b.close()
