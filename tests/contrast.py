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

import re as _re
def lum(c):
    c=c.strip()
    if c.startswith('color('):
        nums=[float(x) for x in _re.findall(r'[\d.]+', c[c.find('srgb')+4:])][:3]
        r,g,b=nums
    else:
        r,g,b=[int(x)/255 for x in c[c.find('(')+1:c.find(')')].split(',')[:3]]
    f=lambda v:v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return (l1+0.05)/(l2+0.05)
sel = ['#continueBtn','#expandAll','#collapseAll','.toggle[aria-pressed="true"]','.toggle[aria-pressed="false"]',
       '.place-opts button','.opt','.unit-head','.mast-tag','.dash-status','.side a','.chip','.part-lede',
       '.tb-pct','.nb-title','.stat .sv','.stat .sl','.ring-val b','.arc-step b','.arc-step span',
       '.part-head .pk','.part-meta','.unit-head .un','.ubadge[data-s="not"]','.q .qh','.q .stem',
       '.hint h6','.lede','.hc-note','.side .part-label','.lk','footer p','.crit .cnote','.legend','.pb-id > .pb-avatar','.pb-id > div > b','.pb-id > div > span','.pb-plan','.onb-step h2','.onb-kicker','.onb-list li','.onb-note','.plan-tile .pv','.plan-tile .pl','.onb-skip','.sigfield > label','.sigmeta','.fig-t','.fig-alt > summary','.srch-foot','.srch-keys kbd','.nextstep .ns-k','#nsTitle','#nsDesc','.stat .sn','#dayWeek','.conf .conf-l','.conf button[aria-pressed="false"]','.conf button[aria-pressed="true"]','.cw-flag','.cw-flag b','#dueBtn','.printbtn','.box.roles h5','.box.roles li','.box.roles .roles-note','.box.deeper h5','.box.deeper a','.box.deeper .roles-note']
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for scheme in ("light","dark"):
        _c = b.new_context(viewport={"width":1280,"height":900}, color_scheme=scheme)
        _c.add_init_script(SKIP_ONB)
        p = _c.new_page()
        p.goto(MODULE_URL); p.wait_for_timeout(600)
        p.evaluate("()=>document.querySelector('#u1 .unit-head').click()"); p.wait_for_timeout(250)
        p.evaluate("()=>{const q=document.querySelector('.q[data-q=\"1.1\"]');q.querySelector('.conf button[data-cf=\"s\"]').click();q.querySelector('.opt:not([data-c=\"1\"])').click();document.querySelector('.q[data-q=\"1.2\"] .conf button[data-cf=\"f\"]').click();document.getElementById('dueBtn').hidden=false;document.querySelector('#appE h3').click();}"); p.wait_for_timeout(300)
        p.evaluate("()=>{var b=document.getElementById('pbEdit'); if(b) b.click();}"); p.wait_for_timeout(350)
        p.evaluate("()=>{for(var i=0;i<2;i++){document.getElementById('onbNext').click();}}"); p.wait_for_timeout(300)
        p.evaluate("()=>{document.getElementById('onbSkip').click(); document.getElementById('searchBtn').click();}"); p.wait_for_timeout(350)
        print(f"\n--- {scheme.upper()} ---")
        for s_ in sel:
            r=p.evaluate("""(s)=>{const e=document.querySelector(s); if(!e) return null;
              let bg='rgba(0, 0, 0, 0)', n=e;
              while(n && (bg==='rgba(0, 0, 0, 0)'||bg==='transparent')){bg=getComputedStyle(n).backgroundColor;n=n.parentElement;}
              return {fg:getComputedStyle(e).color, bg:bg, txt:(e.textContent||'').trim().slice(0,22)};}""", s_)
            if not r: print(f"  {s_:34s} MISSING"); continue
            cr=ratio(r['fg'],r['bg'])
            mark = "ok " if cr>=4.5 else ("AA-lg" if cr>=3 else "LOW")
            print(f"  {s_:34s} {cr:5.2f}:1  {mark:5s}  \"{r['txt']}\"")
        p.close()
    b.close()
