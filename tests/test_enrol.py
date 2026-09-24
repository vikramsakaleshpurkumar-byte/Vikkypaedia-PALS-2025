import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_URL = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/").lstrip("/")
VERIFY_URL = "file:///" + os.path.join(ROOT, "verify.html").replace("\\", "/").lstrip("/")
import json, os, glob
from playwright.sync_api import sync_playwright
U=MODULE_URL
V=VERIFY_URL
fails=[]
def check(n,c,x=""):
    print(("  OK   " if c else "  FAIL ")+n+((" :: "+str(x)) if x and not c else ""))
    if not c: fails.append(n)

with sync_playwright() as pw:
    b=pw.chromium.launch()
    ctx=b.new_context(viewport={"width":1280,"height":900},accept_downloads=True,reduced_motion="reduce")
    p=ctx.new_page(); errs=[]; p.on("pageerror",lambda e:errs.append(str(e)))
    p.goto(U); p.wait_for_timeout(700)

    print("\n== FIRST RUN ==")
    check("onboarding opens on first visit", p.evaluate("()=>!document.getElementById('onb').hidden"))
    check("page behind is not scrollable", p.evaluate("()=>getComputedStyle(document.body).overflow")=='hidden')
    check("profile bar hidden before onboarding", p.evaluate("()=>document.getElementById('profileBar').hidden"))
    p.click("#onbNext"); p.wait_for_timeout(200)
    p.click("#onbNext"); p.wait_for_timeout(200)
    check("name is required", p.evaluate("()=>!document.getElementById('enErr').hidden"))
    p.fill("#enName","Dr Ananya Raghavan"); p.fill("#enInst","District Hospital, Hassan")
    p.fill("#enReg","KMC 123456"); p.fill("#enEmail","ananya@example.org")
    p.click("#onbNext"); p.wait_for_timeout(200)
    check("reached placement step", p.evaluate("()=>document.querySelector('.onb-step[data-step=\"3\"]').hidden")==False)
    p.click("#onbNext"); p.wait_for_timeout(200)
    check("placement is required", "Three taps" in p.evaluate("()=>document.getElementById('placeResult').textContent"))
    for k,v in [("role","a"),("setting","rc"),("exp","some")]:
        p.evaluate(f"()=>document.querySelector('.place-q[data-pq=\"{k}\"] button[data-v=\"{v}\"]').click()")
        p.wait_for_timeout(60)
    p.click("#onbNext"); p.wait_for_timeout(300)
    pl=p.evaluate("()=>({s:planScope.textContent,h:planHours.textContent,w:planWeeks.textContent})")
    check("plan reflects Advanced + some experience", pl['s'].startswith("Parts A") and pl['h']=="≈19 h", pl)
    p.select_option("#planMins","90"); p.select_option("#planDays","7"); p.wait_for_timeout(250)
    pl2=p.evaluate("()=>planWeeks.textContent")
    check("plan recomputes when pace changes", pl2=="≈2 weeks", pl2)
    p.click("#onbNext"); p.wait_for_timeout(700)

    print("\n== AFTER ONBOARDING ==")
    check("overlay closed", p.evaluate("()=>document.getElementById('onb').hidden"))
    check("scroll restored", p.evaluate("()=>getComputedStyle(document.body).overflow")!='hidden')
    check("profile bar shows name", "Ananya" in p.evaluate("()=>pbName.textContent"))
    check("profile bar shows track + institution",
          "Advanced" in p.evaluate("()=>pbMeta.textContent") and "Hassan" in p.evaluate("()=>pbMeta.textContent"))
    check("target date shown", "Target" in p.evaluate("()=>pbPlan.textContent"))
    check("placement applied to prefs", p.evaluate("()=>document.documentElement.getAttribute('data-set')")=='rc')
    check("landed inside a unit", p.evaluate("()=>document.querySelector('#u1').getAttribute('data-open')")=='1')
    p.reload(); p.wait_for_timeout(700)
    check("does not re-onboard after reload", p.evaluate("()=>document.getElementById('onb').hidden"))
    check("profile persists", "Ananya" in p.evaluate("()=>pbName.textContent"))
    p.evaluate("()=>pbEdit.click()"); p.wait_for_timeout(300)
    check("edit reopens at step 2", p.evaluate("()=>document.querySelector('.onb-step[data-step=\"2\"]').hidden")==False)
    check("edit prefills the form", p.evaluate("()=>document.getElementById('enName').value")=="Dr Ananya Raghavan")
    p.keyboard.press("Escape"); p.wait_for_timeout(300)
    check("escape closes", p.evaluate("()=>document.getElementById('onb').hidden"))

    print("\n== COMPLETION RECORD ==")
    p.evaluate("""()=>{const K='vkp.pals2025.v4';const s=JSON.parse(localStorage.getItem(K));
      const past=Date.now()-3*86400000;
      Object.keys(s.items).forEach(id=>{s.items[id]={box:3,due:Date.now()+7*86400000,ok:true,
        firstPass:past,longest:2*86400000,retained:true,hint:0,tries:2};});
      s.exam={attempts:[{at:Date.now(),n:50,right:48,pct:96}],lockUntil:0};
      localStorage.setItem(K,JSON.stringify(s));}""")
    p.reload(); p.wait_for_timeout(900)
    check("cert gate open", p.evaluate("()=>!document.getElementById('certGate').hidden"))
    check("certName prefilled from profile", p.evaluate("()=>document.getElementById('certName').value")=="Dr Ananya Raghavan")
    with p.expect_download() as dl:
        p.click("#dlRecord")
    down = dl.value
    saved = json.load(open(down.path()))
    r = saved
    check("downloaded file parses", saved['format']=="vikkypaedia-completion-record")
    check("filename carries the learner name", "ananya" in down.suggested_filename, down.suggested_filename)
    check("record names the learner", r['learner']['name']=="Dr Ananya Raghavan", r['learner'])
    check("record keeps institution and registration", r['learner']['institution']=="District Hospital, Hassan" and r['learner']['registration']=="KMC 123456")
    check("record reports certified", r['result']['certified'] is True, r['result'])
    check("record carries a checksum", bool(r.get('checksum')), r.get('checksum'))
    check("record states it is self-attested", "Self-attested" in r['attestation'])
    open(os.path.join(ROOT,"sample-record.json"),"w").write(json.dumps(saved,indent=2))

    print("\n== VERIFIER PAGE ==")
    v=ctx.new_page(); verrs=[]; v.on("pageerror",lambda e:verrs.append(str(e)))
    v.goto(V); v.wait_for_timeout(400)
    v.fill("#src", json.dumps(saved)); v.click("#go"); v.wait_for_timeout(300)
    cls=v.evaluate("()=>document.getElementById('verdict').className")
    check("genuine record verifies", "v-ok" in cls, cls)
    check("verifier shows the name", "Ananya" in v.evaluate("()=>document.getElementById('rows').textContent"))
    tampered = dict(saved); tampered['result']=dict(saved['result']); tampered['result']['bestScore']=100
    v.fill("#src", json.dumps(tampered)); v.click("#go"); v.wait_for_timeout(300)
    check("tampered record is rejected", "v-bad" in v.evaluate("()=>document.getElementById('verdict').className"))
    v.fill("#src", "{not json"); v.click("#go"); v.wait_for_timeout(300)
    check("malformed input handled", "v-bad" in v.evaluate("()=>document.getElementById('verdict').className"))
    check("verifier has no JS errors", not verrs, verrs)

    print("\n== SKIP PATH ==")
    s2=ctx.new_page(); s2.goto(U); s2.wait_for_timeout(700)
    s2.evaluate("()=>localStorage.clear()"); s2.reload(); s2.wait_for_timeout(700)
    s2.click("#onbSkip"); s2.wait_for_timeout(400)
    check("skip closes and marks onboarded", s2.evaluate("()=>document.getElementById('onb').hidden"))
    check("skip still shows a profile bar", s2.evaluate("()=>!document.getElementById('profileBar').hidden"))
    check("skip labels the learner anonymous", "Anonymous" in s2.evaluate("()=>pbName.textContent"))
    s2.reload(); s2.wait_for_timeout(700)
    check("skip persists", s2.evaluate("()=>document.getElementById('onb').hidden"))

    print("\nJS ERRORS:", errs or "none")
    print("FAILURES:", fails or "none")
    b.close()
