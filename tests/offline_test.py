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

with sync_playwright() as pw:
    b=pw.chromium.launch(); ctx=b.new_context(); ctx.add_init_script(SKIP_ONB); p=ctx.new_page()
    reqs=[]
    p.on("request", lambda r: reqs.append(r.url) if not r.url.startswith("file://") else None)
    p.goto(MODULE_URL); p.wait_for_timeout(1200)
    p.evaluate("()=>document.querySelector('#u1 .unit-head').click()"); p.wait_for_timeout(400)
    p.evaluate("()=>document.querySelector('.toggle[data-set=\"theme\"][data-v=\"dark\"]').click()"); p.wait_for_timeout(300)
    print("non-file requests:", reqs or "none")
    b.close()
