/* ==========================================================================
   Vikkypaedia Standard · learning loops (engine v2)
   Spliced into the engine at the LOOPS marker by build.py.
   Mastery-linked loops only: no points, badges, leaderboards or streaks that
   punish. Every signal here maps to something that predicts retention.
   ======================================================================== */

var PASSPORT_KEY = "vkp.passport.v1";
var CONF_LABELS  = { s:"Sure", f:"Fairly sure", g:"Guessing" };

/* ---- live region: every verdict is announced to screen readers ---- */
function announce(msg){
  var lr = $("#liveRegion"); if (!lr) return;
  lr.textContent = "";
  setTimeout(function(){ lr.textContent = msg; }, 40);
}

/* ---- toasts: brief, dismissable, never block the page ---- */
function toast(title, body, kind){
  var host = $("#toastHost"); if (!host) return;
  var t = el("div", "toast" + (kind ? " " + kind : ""),
    "<b>" + esc(title) + "</b>" + (body ? "<span>" + esc(body) + "</span>" : ""));
  t.setAttribute("role", "status");
  host.appendChild(t);
  announce(title + (body ? ". " + body : ""));
  setTimeout(function(){ t.setAttribute("data-out","1"); }, 4200);
  setTimeout(function(){ if (t.parentNode) t.remove(); }, 4700);
}

/* ---- study days: counted, never punished ---- */
function dayKey(ms){
  var d = new Date(ms || now());
  return d.getFullYear() + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" + ("0"+d.getDate()).slice(-2);
}
function logStudy(){
  S.days = S.days || {};
  var k = dayKey();
  S.days[k] = (S.days[k] || 0) + 1;
}
function bestRun(){
  var keys = Object.keys(S.days || {}).sort(), best = 0, run = 0, prev = null;
  keys.forEach(function(k){
    var t = new Date(k + "T12:00:00").getTime();
    run = (prev && Math.round((t - prev) / DAY) === 1) ? run + 1 : 1;
    if (run > best) best = run;
    prev = t;
  });
  return best;
}
function daysThisWeek(){
  var d = new Date(), dow = (d.getDay() + 6) % 7, n = 0;   // Monday-based week
  for (var i = 0; i <= dow; i++){
    if ((S.days || {})[dayKey(now() - i * DAY)]) n++;
  }
  return n;
}
function renderStudyDays(){
  var strip = $("#dayStrip"); if (!strip) return;
  strip.innerHTML = "";
  for (var i = 13; i >= 0; i--){
    var k = dayKey(now() - i * DAY), c = (S.days || {})[k] || 0;
    var dot = el("i", c ? (c >= 5 ? "d2" : "d1") : "");
    dot.title = new Date(now() - i * DAY).toDateString() + (c ? " · " + c + " answers" : " · no study");
    strip.appendChild(dot);
  }
  var planned = (S.plan && S.plan.days) || 4;
  var wk = daysThisWeek();
  $("#dayWeek").textContent = wk + " of " + planned + " planned days this week";
  var b = bestRun();
  $("#dayBest").textContent = b ? ("Best run: " + b + (b === 1 ? " day" : " days in a row")) : "Your first study day starts the record";
}

/* ---- confidence-weighted answering ---- */
function wireConfidence(q){
  if ($(".conf", q)) return;
  var opts = $(".opts", q); if (!opts) return;
  var bar = el("div", "conf",
    '<span class="conf-l">How sure are you?</span>' +
    '<button type="button" data-cf="s" aria-pressed="false">Sure</button>' +
    '<button type="button" data-cf="f" aria-pressed="false">Fairly sure</button>' +
    '<button type="button" data-cf="g" aria-pressed="false">Guessing</button>');
  bar.setAttribute("role", "group");
  bar.setAttribute("aria-label", "Confidence before answering");
  opts.parentNode.insertBefore(bar, opts);
  $$("button", bar).forEach(function(b){
    b.addEventListener("click", function(){
      if (b.disabled) return;
      $$("button", bar).forEach(function(x){ x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      q.setAttribute("data-conf", b.getAttribute("data-cf"));
    });
  });
}
function resetConfidence(q){
  q.removeAttribute("data-conf");
  $$(".conf button", q).forEach(function(b){ b.setAttribute("aria-pressed","false"); b.disabled = false; });
  var f = $(".cw-flag", q); if (f) f.remove();
}
function lockConfidence(q){ $$(".conf button", q).forEach(function(b){ b.disabled = true; }); }

/* called by answer() after scoring */
function afterAnswer(q, id, correct){
  var st = S.items[id], c = q.getAttribute("data-conf") || "";
  S.cal = S.cal || { s:[0,0], f:[0,0], g:[0,0] };
  if (c && S.cal[c]) S.cal[c][correct ? 0 : 1]++;
  st.conf = c || null;
  if (!correct && c === "s"){
    st.cw = (st.cw || 0) + 1;
    if (!$(".cw-flag", q)){
      var f = el("div", "cw-flag",
        "<b>Confident and wrong.</b> This is the error pattern that matters most at the bedside — " +
        "and the one feedback corrects best. Read the rationale slowly, then say the right answer aloud once.");
      var rat = $(".rationale", q);
      if (rat) rat.parentNode.insertBefore(f, rat); else q.appendChild(f);
    }
  } else if (correct && c === "s" && st.cw){
    st.cw = 0;   // corrected with confidence: flag cleared
  }
  lockConfidence(q);
  logStudy();
  announce(correct ? "Correct." : "Not correct. The rationale is now shown and the item is re-queued.");
}

function calibration(){
  var c = S.cal || { s:[0,0] }, n = c.s[0] + c.s[1];
  return n ? { pct: Math.round(c.s[0] / n * 100), n: n } : null;
}
function confidentWrong(){
  return ORDER.filter(function(n){ return !isLocked(n); }).reduce(function(acc, n){
    return acc.concat(UNITS[n].items.filter(function(id){ return S.items[id].cw && !S.items[id].ok; }));
  }, []);
}
function renderCalibration(){
  var sv = $("#statCal"); if (!sv) return;
  var c = calibration(), cw = confidentWrong().length;
  sv.textContent = c ? (c.pct + "% of “sure” answers right") : "Rate your confidence to see this";
  var note = $("#statCalNote");
  if (note) note.textContent = cw ? (cw + " confident-and-wrong item" + (cw === 1 ? "" : "s") + " to revisit") : "";
}

/* ---- next best step: one clear action, always ---- */
function nextStep(){
  var due = dueItems();
  if (due.length) return { t:"Clear " + due.length + " retention check" + (due.length===1?"":"s"),
    d:"About " + Math.max(1, Math.round(due.length * 1.2)) + " min. Answering from memory is what makes a pass last.",
    b:"Start review", act:openReview };
  var cw = confidentWrong();
  if (cw.length){ var u = ITEMS[cw[0]].unit;
    return { t:"Revisit a confident-and-wrong answer", d:"Unit " + u + " · " + UNITS[u].title,
      b:"Open Unit " + u, act:function(){ goUnit(u); } }; }
  if (S.lastUnit){ var k = parseInt(S.lastUnit.replace("u",""), 10);
    if (UNITS[k] && !isLocked(k) && unitStatus(k) === "attempted")
      return { t:"Finish Unit " + k, d:UNITS[k].title, b:"Continue", act:function(){ goUnit(k); } }; }
  var nx = ORDER.filter(function(n){ return !isLocked(n) && !unitMastered(n); })[0];
  if (nx != null){
    var p = PARTS.filter(function(x){ return x.key === partOf(nx); })[0];
    var left = p.units.filter(function(u){ return !unitMastered(u); }).length;
    return { t:(unitStatus(nx) === "not" ? "Start" : "Continue") + " Unit " + nx, d:UNITS[nx].title +
      " · " + left + " unit" + (left===1?"":"s") + " to go before " + (PARTS[PARTS.indexOf(p)+1] ? "Part " + PARTS[PARTS.indexOf(p)+1].key + " unlocks" : "the final assessment"),
      b:"Open Unit " + nx, act:function(){ goUnit(nx); } };
  }
  if (!certReady()){
    var nd = nextDue();
    return { t:"Let retention build", d:"Every unit is mastered. Retention is evidenced only after 24 hours" +
      (nd ? " — your next check returns " + fmtDue(nd) + "." : "."), b:"Go to assessment",
      act:function(){ var a = $("#assessment"); if (a) a.scrollIntoView({behavior:"smooth"}); } };
  }
  return { t:"Take the final assessment", d:"Coverage and retention are met.", b:"Go to assessment",
    act:function(){ var a = $("#assessment"); if (a) a.scrollIntoView({behavior:"smooth"}); } };
}
function nextDue(){
  var m = 0;
  Object.keys(ITEMS).forEach(function(id){ var st = S.items[id];
    if (st && st.tries && st.due && st.due > now() && (!m || st.due < m)) m = st.due; });
  return m;
}
var NS_ACT = null;
function renderNextStep(){
  var c = $("#nextStep"); if (!c) return;
  var s = nextStep();
  $("#nsTitle").textContent = s.t;
  $("#nsDesc").textContent = s.d;
  $("#nsGo").textContent = s.b;
  NS_ACT = s.act;
  var nd = nextDue(), ret = $("#nsReturn");
  if (ret){ ret.hidden = !(nd && !dueItems().length); if (nd) ret.textContent = "Next retention check returns " + fmtDue(nd) + "."; }
}

/* ---- due badge + review runner ---- */
function renderDueBadge(){
  var b = $("#dueBtn"); if (!b) return;
  var n = dueItems().length;
  b.hidden = n === 0;
  $("#dueCount").textContent = n;
  b.setAttribute("aria-label", n + " retention check" + (n===1?"":"s") + " due — start review");
}
var RV = null;
function openReview(){
  var q = dueItems(); if (!q.length) return;
  RV = { queue:q, i:0, right:0, done:0 };
  var m = $("#rvw"); m.hidden = false;
  document.body.style.overflow = "hidden";
  drawReview();
}
function closeReview(){
  var m = $("#rvw"); if (!m || m.hidden) return;
  m.hidden = true; document.body.style.overflow = "";
  $("#rvwSlot").innerHTML = ""; RV = null; refresh();
}
function drawReview(){
  var slot = $("#rvwSlot"); slot.innerHTML = "";
  $("#rvwNext").hidden = true;
  if (RV.i >= RV.queue.length){
    var nd = nextDue();
    $("#rvwProg").textContent = "Review complete";
    $("#rvwBar").style.width = "100%";
    slot.appendChild(el("div", "rvw-done",
      "<h3>" + RV.right + " of " + RV.done + " answered correctly from memory</h3>" +
      "<p>" + (RV.right === RV.done ? "Every item moved up a box and will return later — that is durable learning, measured."
        : "The items you missed come back in 10 minutes. That is the system working, not a failure.") + "</p>" +
      (nd ? "<p class=\"rvw-nd\">Next check returns " + esc(fmtDue(nd)) + ".</p>" : "")));
    var c = el("button", "btn", "Back to the module"); c.type = "button";
    c.addEventListener("click", closeReview); slot.appendChild(c); c.focus();
    return;
  }
  var id = RV.queue[RV.i];
  $("#rvwProg").textContent = "Item " + (RV.i + 1) + " of " + RV.queue.length + " · Unit " + ITEMS[id].unit;
  $("#rvwBar").style.width = Math.round(RV.i / RV.queue.length * 100) + "%";
  var clone = ITEMS[id].node.cloneNode(true);
  $$(".conf", clone).forEach(function(n){ n.remove(); });
  resetQuestionUI(clone); resetConfidence(clone);
  var h = $(".qh", clone); if (h) h.innerHTML = 'Unit ' + ITEMS[id].unit + ' · ' + esc(UNITS[ITEMS[id].unit].title) + ' <span class="retag">from memory</span>';
  slot.appendChild(clone);
  wireConfidence(clone);
  $$(".opt", clone).forEach(function(b, i){
    if (!$(".k", b)) b.insertBefore(el("span","k", letter(i)), b.firstChild);
    b.setAttribute("type","button");
    b.addEventListener("click", function(){
      if (b.disabled) return;
      var ok = b.getAttribute("data-c") === "1";
      answer(clone, b);
      var src = ITEMS[id].node; resetQuestionUI(src); resetConfidence(src); restoreQuestion(src);
      RV.done++; if (ok) RV.right++;
      var nx = $("#rvwNext"); nx.hidden = false;
      nx.textContent = RV.i + 1 >= RV.queue.length ? "Finish" : "Next item";
      nx.focus();
    });
  });
  var hb = $(".hint-btn", clone); if (hb) hb.addEventListener("click", function(){ nextHint(clone); });
  var first = $(".conf button", clone); if (first) first.focus();
}

/* ---- unlock moments: celebrate what was earned, once ---- */
var SNAP = null;
function snapshot(){
  return { m: ORDER.filter(unitMastered), p: PARTS.filter(function(p){ return partUnlocked(p.key); }).map(function(p){ return p.key; }),
           c: certReady() };
}
function detectMoments(){
  var s = snapshot();
  if (SNAP){
    var newM = s.m.filter(function(n){ return SNAP.m.indexOf(n) < 0; });
    var newP = s.p.filter(function(k){ return SNAP.p.indexOf(k) < 0; });
    if (newP.length){
      var ps = document.getElementById("part" + newP[0]);
      toast("Part " + newP[0] + " unlocked", (ps && ps.getAttribute("data-title") ? ps.getAttribute("data-title") + " · " : "") + "earned by mastering every unit before it.", "big");
      burst();
    } else if (newM.length){
      toast("Unit " + newM[0] + " mastered", s.m.length + " of " + ORDER.length + " units · it will return for spaced retrieval.", "ok");
    }
    if (s.c && !SNAP.c) toast("Coverage and retention met", "The final assessment is now worth sitting.", "big");
  }
  SNAP = s;
}
function burst(){
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var host = $("#toastHost"); if (!host) return;
  var b = el("div", "burst"); b.setAttribute("aria-hidden","true");
  for (var i = 0; i < 14; i++){ var s = el("i"); s.style.setProperty("--a", (i * 360 / 14) + "deg"); s.style.setProperty("--h", "var(--p" + "ABCDE".charAt(i % 5) + ")"); b.appendChild(s); }
  document.body.appendChild(b);
  setTimeout(function(){ b.remove(); }, 1100);
}

/* ---- Vikkypaedia Passport: one learner, every module, no server ---- */
function passportRead(){
  try { var p = JSON.parse(localStorage.getItem(PASSPORT_KEY) || "null"); if (p && p.v === 1) return p; } catch(e){}
  return { v:1, profile:null, modules:{} };
}
function passportWrite(){
  try {
    var p = passportRead();
    if (S.profile && S.profile.name){
      if (!p.profile || (S.profile.updatedAt || 0) >= (p.profile.updatedAt || 0)) p.profile = S.profile;
    }
    var best = 0; (S.exam.attempts || []).forEach(function(a){ if (a.pct > best) best = a.pct; });
    p.modules[MODULE.id] = {
      id: MODULE.id, title: MODULE.title, url: location.href.split("#")[0], version: VERSION,
      units: ORDER.length, mastered: masteredCount(), checkpoints: checkpointsOK(), items: totalItems(),
      retainedUnits: retainedUnits(), retainNeeded: cfg("retainUnits"), due: dueItems().length,
      examBest: best, cut: cfg("cut"), certified: certReady() && best >= cfg("cut"),
      studyDays: Object.keys(S.days || {}).length, lastActive: now(),
      started: S.started, target: S.plan ? S.plan.target : null
    };
    p.updatedAt = now();
    localStorage.setItem(PASSPORT_KEY, JSON.stringify(p));
  } catch(e){}
}
function passportPrefill(){
  if (S.profile && S.profile.name) return false;
  var pp = passportRead().profile; if (!pp || !pp.name) return false;
  var map = { enName:"name", enInst:"institution", enReg:"reg", enEmail:"email" };
  Object.keys(map).forEach(function(k){ var i = document.getElementById(k); if (i && !i.value && pp[map[k]]) i.value = pp[map[k]]; });
  var n = $("#enPassport"); if (n) n.hidden = false;
  return true;
}

/* ---- print any appendix (the drug annex belongs on the resus trolley) ---- */
function printAppendix(sec){
  var pd = $("#printDoc"); if (!pd) return;
  var h = $("h3", sec), body = $(".app-body", sec);
  var wasHidden = body.hidden; body.hidden = false;
  pd.innerHTML = '<p class="pd-brand">VIKKYPAEDIA · ' + esc(MODULE.title) + ' · v' + VERSION + '</p>' +
    '<h1>' + (h ? esc(h.textContent.replace(/\s*Print.*$/,"")) : "") + '</h1>' + body.innerHTML +
    '<p class="pd-foot">Printed ' + esc(fmtDate(now())) + '. Verify every dose against the current guideline and your unit protocol before use.</p>';
  $$(".printbtn", pd).forEach(function(n){ n.remove(); });
  body.hidden = wasHidden;
  document.documentElement.classList.add("printing-doc");
  setTimeout(function(){ window.print(); }, 60);
}
function wirePrintButtons(){
  $$(".appendix").forEach(function(sec){
    var body = $(".app-body", sec); if (!body || $(".printbtn", body)) return;
    var b = el("button", "btn ghost sm printbtn noprint", "Print this appendix"); b.type = "button";
    b.addEventListener("click", function(e){ e.stopPropagation(); printAppendix(sec); });
    body.insertBefore(b, body.firstChild);
  });
  window.addEventListener("afterprint", function(){
    document.documentElement.classList.remove("printing-doc");
    var pd = $("#printDoc"); if (pd) pd.innerHTML = "";
  });
}

/* ---- wiring + render ---- */
function renderLoops(){
  renderDueBadge();
  renderNextStep();
  renderStudyDays();
  renderCalibration();
  detectMoments();
  passportWrite();
}
/* ---- a one-time note for learners who used an earlier edition of this module ---- */
function legacyNotice(){
  try{
    var keys = (window.VKP_MODULE && window.VKP_MODULE.legacyKeys) || [];
    if (S.legacyNoted || !keys.some(function(k){ return localStorage.getItem(k) != null; })) return;
    S.legacyNoted = true; save();
    setTimeout(function(){ toast("Welcome to the new edition",
      "This module was rebuilt to current guidelines. Earlier progress is not carried over, because the units and questions have changed. Experienced learners can clear Parts quickly by answering checkpoints cold.", "big"); }, 1200);
  } catch(e){}
}
function wireLoops(){
  legacyNotice();
  var d = $("#dueBtn"); if (d) d.addEventListener("click", openReview);
  var g = $("#nsGo");   if (g) g.addEventListener("click", function(){ if (NS_ACT) NS_ACT(); });
  $("#rvwClose").addEventListener("click", closeReview);
  $("#rvwNext").addEventListener("click", function(){ RV.i++; drawReview(); });
  $("#rvw").addEventListener("click", function(e){ if (e.target === $("#rvw")) closeReview(); });
  document.addEventListener("keydown", function(e){
    var m = $("#rvw");
    if (e.key === "Escape" && m && !m.hidden){ closeReview(); return; }
    var tag = (e.target && e.target.tagName) || "";
    if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    if (m && !m.hidden && /^[1-4]$/.test(e.key)){
      var o = $$("#rvwSlot .opt")[parseInt(e.key,10)-1]; if (o && !o.disabled) o.click();
    }
  });
  wirePrintButtons();
}
