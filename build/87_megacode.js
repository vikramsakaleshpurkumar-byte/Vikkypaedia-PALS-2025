/* ================= Vikkypaedia Standard v2.2 · interactive megacodes =================
   Branching cases, played one decision at a time against a patient monitor.
   Spliced into the engine at the MEGA marker by build.py. Case data lives in
   window.VKP_MEGACODES (build/86_megacodes.html); a module without it gets nothing.
   Formative only: results are stored and reported, never used for certification. */

var MCD = window.VKP_MEGACODES || null;
var MG = null;                       // the run in progress
function mgOn(){ return !!(MCD && MCD.cases && MCD.cases.length); }
function mgNode(id){ return document.getElementById("mc" + id); }
function mgCase(id){ for (var i=0;i<MCD.cases.length;i++) if (MCD.cases[i].id === id) return MCD.cases[i]; return null; }
function mgOpen(c){ return partUnlocked(c.part); }
function mgStore(){ S.mega = S.mega || {}; return S.mega; }
function mgClock(s){ s = Math.max(0, Math.round(s)); return Math.floor(s/60) + ":" + ("0" + (s%60)).slice(-2); }

/* ---- rhythm strips: drawn, not pictured, so they cost no bytes and scale crisply ---- */
var MG_DESC = {
  sinus:"Regular rhythm. Every QRS is narrow and preceded by a P wave.",
  stach:"Fast, regular rhythm. Narrow QRS complexes, each preceded by a P wave; the rate varies slightly.",
  brady:"Slow, regular rhythm. Narrow QRS complexes with P waves, widely spaced.",
  svt:"Very fast, regular, narrow-complex rhythm. No visible P waves; the rate does not vary at all.",
  vt:"Fast, regular, wide and bizarre complexes. No P waves.",
  vf:"Chaotic, irregular baseline of varying amplitude. No identifiable QRS complexes.",
  asys:"Almost flat line with slight baseline wander. No complexes.",
  pea:"Organised complexes on the monitor. Interpret this with the pulse check, not the screen.",
  cpr:"Large regular deflections at the compression rate. Compression artefact: no rhythm can be read during CPR.",
  none:"No monitor attached yet."
};
function mgWave(type, hr){
  var W = 600, H = 90, mid = 52, pts = [], seed = 7;
  function rnd(){ seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var secs = 4, pxs = W / secs;
  function beat(t, wide){        // one complex centred at t (seconds); returns y offset at time x
    return function(x){
      var d = (x - t) * 1000, y = 0;
      if (!wide){
        y += 6 * Math.exp(-Math.pow((d + 160) / 28, 2));      // P
        y -= 4 * Math.exp(-Math.pow((d + 25) / 9, 2));        // Q
        y += 38 * Math.exp(-Math.pow(d / 11, 2));             // R
        y -= 9 * Math.exp(-Math.pow((d - 30) / 12, 2));       // S
        y += 10 * Math.exp(-Math.pow((d - 230) / 55, 2));     // T
      } else {
        y += 34 * Math.exp(-Math.pow(d / 45, 2));
        y -= 22 * Math.exp(-Math.pow((d - 120) / 60, 2));
      }
      return y;
    };
  }
  var fns = [], rate = hr || 0;
  if (type === "sinus" || type === "stach" || type === "brady" || type === "pea" || type === "svt"){
    var noP = type === "svt", step = 60 / Math.max(rate, 20), jitter = type === "stach" ? 0.03 : 0;
    for (var t = 0.25; t < secs + step; t += step * (1 + (rnd() - .5) * jitter)){
      var f = beat(t, false);
      if (noP){ (function(g, tt){ fns.push(function(x){ var d=(x-tt)*1000; return g(x) - 6*Math.exp(-Math.pow((d+160)/28,2)); }); })(f, t); }
      else fns.push(f);
    }
  } else if (type === "vt"){
    var st = 60 / Math.max(rate, 150);
    for (var t2 = 0.1; t2 < secs + st; t2 += st) fns.push(beat(t2, true));
  }
  var ph = [rnd()*6, rnd()*6, rnd()*6];
  for (var x = 0; x <= W; x += 2){
    var s = x / pxs, y = 0;
    if (type === "vf") y = 14*Math.sin(s*2*Math.PI*5.1+ph[0]) + 9*Math.sin(s*2*Math.PI*7.3+ph[1]) + 6*Math.sin(s*2*Math.PI*3.2+ph[2]) + (rnd()-.5)*6;
    else if (type === "asys") y = 1.5*Math.sin(s*1.3) + (rnd()-.5)*1.2;
    else if (type === "cpr") y = 26*Math.pow(Math.max(0, Math.sin(s*2*Math.PI*1.85)), 3) - 6 + (rnd()-.5)*3;
    else if (type === "none") y = 0;
    else for (var i=0;i<fns.length;i++) y += fns[i](s);
    pts.push(x + "," + (mid - y).toFixed(1));
  }
  return '<svg class="mg-ecg" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true" focusable="false">' +
    '<polyline points="' + pts.join(" ") + '"/></svg>';
}

/* ---- the monitor ---- */
function mgMonitor(c, n){
  var m = n.mon || {}, show = c.monitor || ["rhythm","hr","spo2","bp"];
  var lab = { hr:"HR", spo2:"SpO₂", bp:"BP", etco2:"EtCO₂", temp:"Temp", fio2:"FiO₂" };
  var unit = { hr:"/min", spo2:"%", bp:"mmHg", etco2:"mmHg", temp:"°C", fio2:"%" };
  var h = '<div class="mg-mon" role="group" aria-label="Patient monitor">';
  h += '<div class="mg-top"><span class="mg-clock" aria-label="Elapsed time">' + (c.clockLabel || "Time") + ' <b>' + mgClock(MG.clock) + '</b></span>' +
       (m.flag ? '<span class="mg-flag">' + esc(m.flag) + '</span>' : "") + '</div>';
  if (show.indexOf("rhythm") >= 0){
    var r = m.rhythm || "none";
    // no leads is not a flat line: a flat line would read as asystole
    if (r === "none") h += '<div class="mg-strip mg-noleads"><span>No monitor leads attached</span></div>';
    else h += '<div class="mg-strip">' + mgWave(r, m.hr) + '</div>' +
         '<button type="button" class="mg-desc-btn" aria-expanded="false">Describe the strip</button>' +
         '<p class="mg-desc" hidden>' + esc(MG_DESC[r] || "") + '</p>';
  }
  h += '<div class="mg-vals">';
  show.forEach(function(k){
    if (k === "rhythm") return;
    var v = m[k];
    var txt = (v == null || v === "") ? "—" : esc(String(v));
    h += '<div class="mg-v mg-' + k + '"><span>' + lab[k] + '</span><b>' + txt + '</b><i>' + (v == null || typeof v === "string" && !/^\d/.test(v) ? "" : unit[k]) + '</i></div>';
  });
  h += '</div>';
  if (m.target) h += '<p class="mg-target">' + esc(m.target) + '</p>';
  return h + '</div>';
}

/* ---- list of cases ---- */
function renderMega(){
  if (!mgOn()) return;
  var list = mgNode("List"); if (!list) return;
  if (MG && !mgNode("Runner").hidden) return;
  var st = mgStore(), done = 0;
  list.innerHTML = "";
  MCD.cases.forEach(function(c, i){
    var r = st[c.id], open = mgOpen(c);
    if (r && r.runs) done++;
    var card = el("div", "mg-card" + (open ? "" : " locked"));
    card.setAttribute("role", "listitem");
    var status = !open ? '<span class="pill">Opens with Part ' + esc(c.part) + '</span>' :
      (r && r.runs ? '<span class="pill ok">Best: ' + r.best.pct + '% right decisions' + (r.best.crit ? ' · ' + r.best.crit + ' critical' : ' · no critical errors') + '</span><span class="mg-runs">' + r.runs + (r.runs === 1 ? " run" : " runs") + '</span>'
                   : '<span class="pill">Not tried yet</span>');
    card.innerHTML = '<span class="mg-no">' + (i+1) + '</span><div class="mg-cbody"><b>' + esc(c.title) + '</b>' +
      '<span class="mg-pt">' + esc(c.patient) + '</span>' +
      '<span class="mg-units">Practises Units ' + c.units.join(", ") + ' · about ' + c.minutes + ' min</span>' +
      '<span class="mg-st">' + status + '</span></div>';
    var b = el("button", "btn sm" + (r && r.runs ? " ghost" : ""), open ? (r && r.runs ? "Run again" : "Start") : "Locked");
    b.type = "button"; b.disabled = !open;
    b.setAttribute("aria-label", (open ? (r && r.runs ? "Run again: " : "Start: ") : "Locked: ") + c.title);
    b.addEventListener("click", function(){ mgStart(c.id); });
    card.appendChild(b);
    list.appendChild(card);
  });
  var sum = mgNode("Sum");
  if (sum) sum.textContent = done + " of " + MCD.cases.length + " practised";
}

/* ---- a run ---- */
function mgStart(id){
  var c = mgCase(id); if (!c || !mgOpen(c)) return;
  MG = { c:c, node:c.start, clock:c.clock0 || 0, path:[], tried:{}, ord:{}, marks:{}, crit:[], decisions:0, right:0, fb:null };
  mgNode("List").hidden = true; mgNode("Intro").hidden = true;
  var R = mgNode("Runner"); R.hidden = false;
  mgDraw(true);
  R.scrollIntoView({ behavior:"smooth", block:"start" });
}
function mgQuit(){
  MG = null;
  var R = mgNode("Runner"); R.hidden = true; R.innerHTML = "";
  mgNode("List").hidden = false; mgNode("Intro").hidden = false;
  renderMega();
  var sec = mgNode("List").closest("section"); if (sec) sec.scrollIntoView({ behavior:"smooth", block:"start" });
}
function mgDraw(first){
  var c = MG.c, n = c.nodes[MG.node], R = mgNode("Runner");
  if (n.end){ mgFinish(n); return; }
  var tried = MG.tried[MG.node] || [];
  var h = '<div class="mg-head"><div><span class="pk">Megacode · practice</span><h3 tabindex="-1" id="mcTitle">' + esc(c.title) + '</h3>' +
          '<p class="mg-pt">' + esc(c.patient) + '</p></div>' +
          '<button type="button" class="btn ghost sm" id="mcQuit">Leave case</button></div>';
  if (first) h += '<div class="mg-brief"><b>Scenario.</b> ' + c.brief + '</div>';
  h += '<div class="mg-grid">' + mgMonitor(c, n) + '<div class="mg-play">';
  h += '<div class="mg-scene">' + n.text + '</div>';
  if (MG.fb){
    h += '<div class="mg-fb ' + (MG.fb.ok ? "ok" : (MG.fb.crit ? "crit" : "no")) + '" role="status">' +
         '<b>' + (MG.fb.ok ? "✓ Right call." : (MG.fb.crit ? "✖ Critical error." : "✖ Not the best call.")) + '</b> ' + MG.fb.text + '</div>';
  }
  h += '<p class="mg-ask"><b>' + esc(n.ask || "What do you do next?") + '</b></p><div class="mg-opts">';
  // options are shuffled once per node per run, so a repeat run tests reasoning, not letter memory
  var ord = MG.ord[MG.node];
  if (!ord){ ord = n.opts.map(function(_, i){ return i; }); for (var j = ord.length - 1; j > 0; j--){ var r = Math.floor(Math.random() * (j + 1)), t = ord[j]; ord[j] = ord[r]; ord[r] = t; } MG.ord[MG.node] = ord; }
  ord.forEach(function(i, pos){
    var o = n.opts[i], off = tried.indexOf(i) >= 0;
    h += '<button type="button" class="mg-opt" data-i="' + i + '" data-pos="' + pos + '"' + (off ? ' disabled aria-disabled="true"' : "") + '><span class="k">' + String.fromCharCode(65 + pos) + '</span><span class="t">' + o.t + '</span>' + (off ? '<span class="mg-tried">already tried</span>' : "") + '</button>';
  });
  h += '</div></div></div>';
  R.innerHTML = h;
  $$(".mg-opt", R).forEach(function(b){ b.addEventListener("click", function(){ mgChoose(parseInt(b.getAttribute("data-i"), 10)); }); });
  $("#mcQuit", R).addEventListener("click", mgQuit);
  var db = $(".mg-desc-btn", R);
  if (db) db.addEventListener("click", function(){ var p = $(".mg-desc", R); p.hidden = !p.hidden; db.setAttribute("aria-expanded", p.hidden ? "false" : "true"); });
  var focus = MG.fb ? $(".mg-fb", R) : $("#mcTitle", R);
  if (focus){ focus.setAttribute("tabindex", "-1"); focus.focus({ preventScroll: !!first }); }
}
function mgChoose(i){
  var c = MG.c, id = MG.node, n = c.nodes[id], o = n.opts[i];
  MG.decisions++;
  if (o.ok) MG.right++;
  if (o.crit) MG.crit.push(o.fb);
  // a timed action happens at the start of the step it belongs to (mt), not after the step's full duration
  if (o.mark && MG.marks[o.mark] == null) MG.marks[o.mark] = MG.clock + (o.mt != null ? o.mt : Math.min(o.dt || 0, 15));
  MG.clock += (o.dt || 0);
  MG.path.push({ n:id, i:i, ok:!!o.ok });
  MG.fb = { ok:!!o.ok, crit:!!o.crit, text:o.fb };
  announce((o.ok ? "Right call. " : (o.crit ? "Critical error. " : "Not the best call. ")) + String(o.fb).replace(/<[^>]+>/g, ""));
  if (o.to){ MG.node = o.to; }
  else { MG.tried[id] = (MG.tried[id] || []).concat([i]); }
  mgDraw(false);
}
function mgFinish(n){
  var c = MG.c, R = mgNode("Runner"), pct = MG.decisions ? Math.round(MG.right * 100 / MG.decisions) : 0;
  var run = { pct:pct, crit:MG.crit.length, secs:MG.clock - (c.clock0 || 0), at:now(), outcome:n.end, decisions:MG.decisions };
  var st = mgStore(), rec = st[c.id] || { runs:0, best:null };
  var prev = rec.best;
  rec.runs++; rec.last = run;
  var better = !prev || run.crit < prev.crit || (run.crit === prev.crit && (run.pct > prev.pct || (run.pct === prev.pct && run.secs < prev.secs)));
  if (better) rec.best = run;
  st[c.id] = rec; save();
  var h = '<div class="mg-head"><div><span class="pk">Megacode · debrief</span><h3 tabindex="-1" id="mcTitle">' + esc(c.title) + '</h3></div></div>';
  h += '<div class="mg-grid">' + mgMonitor(c, n) + '<div class="mg-play">';
  if (MG.fb) h += '<div class="mg-fb ' + (MG.fb.ok ? "ok" : (MG.fb.crit ? "crit" : "no")) + '"><b>' + (MG.fb.ok ? "✓ Right call." : "✖ Last call.") + '</b> ' + MG.fb.text + '</div>';
  h += '<div class="mg-scene">' + n.text + '</div>';
  h += '<div class="mg-score"><div class="stat"><span class="sl">Right decisions</span><span class="sv">' + MG.right + '/' + MG.decisions + '</span><span class="sn">' + pct + '%</span></div>' +
       '<div class="stat"><span class="sl">Critical errors</span><span class="sv">' + MG.crit.length + '</span><span class="sn">' + (MG.crit.length ? "see below" : "none") + '</span></div>' +
       '<div class="stat"><span class="sl">Case clock</span><span class="sv">' + mgClock(MG.clock) + '</span><span class="sn">' + (better && prev ? "new personal best" : (prev ? "best: " + prev.pct + "%" : "first run")) + '</span></div></div>';
  if (c.timers && c.timers.length){
    h += '<h4>Key times</h4><ul class="mg-timers">';
    c.timers.forEach(function(t){
      var v = MG.marks[t.mark], okT = v != null && (t.max == null || v <= t.max);
      h += '<li class="' + (okT ? "ok" : "no") + '"><span>' + (okT ? "✓" : "✖") + '</span> ' + esc(t.label) + ': <b>' + (v == null ? "not done" : mgClock(v)) + '</b> <i>' + esc(t.target) + '</i></li>';
    });
    h += '</ul>';
  }
  if (MG.crit.length){
    h += '<h4>Critical errors to fix</h4><ul class="mg-crits">' + MG.crit.map(function(f){ return "<li>" + f + "</li>"; }).join("") + '</ul>';
  }
  h += '<h4>Debrief: take these away</h4><ul class="mg-deb">' + c.debrief.map(function(d){ return "<li>" + d + "</li>"; }).join("") + '</ul>';
  h += '<p class="mg-units">Revisit: ' + c.units.map(function(u){ return '<a href="#u' + u + '" data-u="' + u + '">Unit ' + u + (UNITS[u] ? " · " + esc(UNITS[u].title) : "") + '</a>'; }).join(" · ") + '</p>';
  h += '<p class="note-sm">Practice only. Megacode results are recorded for you and your faculty, but they are not part of the certificate. Hands-on megacodes on a manikin (Appendix B) remain essential.</p>';
  h += '<div class="btnrow"><button type="button" class="btn" id="mcAgain">Run this case again</button><button type="button" class="btn ghost" id="mcBack">All megacodes</button></div>';
  h += '</div></div>';
  R.innerHTML = h;
  $("#mcAgain", R).addEventListener("click", function(){ mgStart(c.id); });
  $("#mcBack", R).addEventListener("click", mgQuit);
  $$(".mg-units a", R).forEach(function(a){ a.addEventListener("click", function(e){ e.preventDefault(); var u = parseInt(a.getAttribute("data-u"), 10); mgQuit(); goUnit(u); }); });
  var t = $("#mcTitle", R); if (t) t.focus({ preventScroll:true });
  announce("Case finished. " + MG.right + " of " + MG.decisions + " right decisions, " + MG.crit.length + " critical errors.");
  if (better && prev) toast("Personal best", c.title + ": " + pct + "% right decisions" + (run.crit ? "" : ", no critical errors") + ".");
  MG = null;
  refresh();
}

/* ---- the record: one line per case practised ---- */
function mgRecord(){
  if (!mgOn()) return null;
  var st = S.mega || {};
  return MCD.cases.filter(function(c){ return st[c.id] && st[c.id].runs; }).map(function(c){
    var r = st[c.id];
    return { id:c.id, title:c.title, runs:r.runs, best:r.best.pct, crit:r.best.crit, secs:r.best.secs };
  });
}

function wireMega(){
  if (!mgOn()) return;
  var intro = mgNode("IntroText"); if (intro && MCD.intro) intro.innerHTML = MCD.intro;
  document.addEventListener("keydown", function(e){
    var R = mgNode("Runner");
    if (!R || R.hidden || !MG) return;
    var tag = (e.target && e.target.tagName) || "";
    if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    var k = (e.key || "").toUpperCase();
    if (/^[A-F]$/.test(k)){ var b = $('.mg-opt[data-pos="' + (k.charCodeAt(0) - 65) + '"]', R); if (b && !b.disabled){ e.preventDefault(); b.click(); } }
  });
}
