"""Appendices A–G for Paediatric Advanced Life Support 2025. Reuses the Standard's generic
faculty material (C3–C6, PEARLS, G) and adds topic-specific content."""
import os, re
from gen import table, box
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "build", "80_appendices.html")
STD = os.path.join(HERE, "_standard_appendix_source.html")   # NRP-2025 v1.5 appendices — source of the shared faculty and design blocks
std = open(STD, encoding="utf-8").read().split("\n")
pearls = "\n".join(std[242:266]).replace("where the blender was", "where the IO needles and the pads were")
appC_generic = "\n".join(std[271 - 1 + 32:271 - 1 + 111 - 4])   # C3 … C6, without closing divs
appG = "\n".join(std[597:666])

def app(letter, title, body):
    return '''
<!-- ===================================================== APPENDIX %s -->
<div class="appendix" id="app%s">
  <h3><span class="caret">▸</span>%s · %s</h3>
  <div class="app-body">
%s
  </div>
</div>
''' % (letter, letter, letter, title, body)

# ------------------------------------------------------------------ A
A = """    <h4>A1 · Blueprint against Miller's pyramid</h4>
    <p>No single instrument samples all four levels. This is what each part of the programme can honestly claim.</p>
""" + table(["Miller level", "What it means", "Instrument here", "Weight"],
  [["<b>Knows</b>", "Recalls doses, energies, ratios, thresholds", "Unit checkpoints; final assessment", "~25%"],
   ["<b>Knows how</b>", "Applies knowledge to a resuscitation problem", "Case-vignette checkpoints; integrative items; key-feature problems", "~40%"],
   ["<b>Shows how</b>", "Demonstrates on a manikin", "OSCE stations (A3); megacode scenarios (Appendix B)", "~25%"],
   ["<b>Does</b>", "Performs in real resuscitations", "Debriefs, MSF, entrustment (A4)", "~10%"]]) + box("pitfall", "What the written assessment cannot do", "<p>The certificate covers only the top two rows. CPR, defibrillation, bag-mask ventilation and team leadership must be assessed hands-on, on a manikin, by an instructor. This module is not the AHA PALS course and does not replace it.</p>") + """
    <h4>A2 · Key-feature problems</h4>
    <p>Short answers, no options. They test only the decisions on which the case turns.</p>
    <h5 class="sub">KF1 — The bradycardic infant</h5>
    <p><i>8 months, bronchiolitis, HR 50, SpO₂ 70%, floppy.</i></p>
    <ol>
      <li><b>First action?</b><br><small>Model: open airway, bag-mask ventilation with oxygen.</small></li>
      <li><b>After 30 s of effective ventilation, HR still 50 with poor perfusion?</b><br><small>Model: start CPR 15:2; epinephrine 0.01 mg/kg IV/IO.</small></li>
    </ol>
    <h5 class="sub">KF2 — PEA on the ward</h5>
    <p><i>15 kg child, PEA, IV failed twice.</i></p>
    <ol>
      <li><b>Access and drug?</b><br><small>Model: IO; epinephrine 0.15 mg (1.5 mL of 0.1 mg/mL) as soon as possible.</small></li>
      <li><b>Name four reversible causes to look for.</b><br><small>Model: any four H's and T's — hypoxia, hypovolaemia, acidosis, potassium, glucose, hypothermia, tension pneumothorax, tamponade, toxins, thrombosis.</small></li>
    </ol>
    <h5 class="sub">KF3 — VF in a teenager</h5>
    <p><i>40 kg, collapsed at school, VF on the AED.</i></p>
    <ol>
      <li><b>Energies for the first two shocks (manual)?</b><br><small>Model: 80 J (2 J/kg), then 160 J (4 J/kg).</small></li>
      <li><b>When is epinephrine given?</b><br><small>Model: after the second shock, then every 3–5 minutes.</small></li>
    </ol>
    <h5 class="sub">KF4 — After ROSC</h5>
    <p><i>2-year-old, ROSC after 10 minutes, comatose.</i></p>
    <ol>
      <li><b>Name four targets.</b><br><small>Model: temperature ≤37.5 °C; systolic and mean BP above the 10th centile; SpO₂ 94–99%; normal PaCO₂; glucose normal; treat seizures.</small></li>
      <li><b>What do you tell the family about prognosis today?</b><br><small>Model: too early to know; multiple assessments over several days.</small></li>
    </ol>

    <h4>A3 · OSCE stations</h4>
    <p>Twelve stations, 6&ndash;8 minutes each, on infant and child manikins with a rhythm simulator or printed strips. Score with the six-domain rubric in Appendix C.</p>
""" + table(["#", "Station", "Tests", "Critical failure"],
  [["1", "Infant CPR, 2 rescuers", "Two-thumb or one-hand technique, depth, 15:2, recoil", "Two-finger technique or inadequate depth"],
   ["2", "Child CPR, 1 rescuer, with AED", "30:2, AED pads, safe shock", "Pause over 10 seconds around the shock"],
   ["3", "Choking infant and child", "Back blows with chest or abdominal thrusts (2025)", "Abdominal thrusts in an infant"],
   ["4", "Bag-mask ventilation", "Seal, rate, chest rise", "No chest rise, not corrected"],
   ["5", "IO insertion", "Site, technique, confirmation", "Wrong site"],
   ["6", "Drug calculation", "Epinephrine, amiodarone, adenosine by weight", "10-fold error"],
   ["7", "Rhythm recognition", "Four arrest rhythms, SVT, bradycardia", "Calls PEA shockable"],
   ["8", "Bradycardia management", "Ventilate first; CPR threshold; epinephrine", "Atropine before ventilation in hypoxia"],
   ["9", "SVT management", "Vagal, adenosine technique, cardioversion energy", "Unsynchronised shock with a pulse"],
   ["10", "Megacode: nonshockable arrest", "Early epinephrine, reversible causes, leadership", "Epinephrine delayed beyond the first cycle"],
   ["11", "Megacode: shockable arrest", "Shock 2 then 4 J/kg, epinephrine after 2nd shock", "Long pre-shock pause"],
   ["12", "Post-ROSC and family", "Targets, handover, telling parents", "No temperature or BP targets"]]) + """
    <h4>A4 · Workplace-based assessment</h4>
""" + table(["Tool", "Use it for", "Frequency", "Note"],
  [["<b>Debrief review</b>", "Every real resuscitation the learner took part in", "After each event", "Focus on system and team"],
   ["<b>DOPS</b>", "CPR quality, bag-mask ventilation, IO, defibrillation", "Until entrustment, then 6-monthly", "Skills decay within months"],
   ["<b>MSF</b>", "Leadership and communication", "Annual", "Detects the behaviours that cause harm"]]) + """
    <h5 class="sub">Entrustment scale for the core EPA</h5>
    <p><b>EPA:</b> <i>Recognise the deteriorating child and lead the first 10 minutes of a paediatric resuscitation.</i></p>
""" + table(["Level", "Descriptor"],
  [["1", "Observes only"], ["2", "Performs with direct supervision"], ["3", "Performs with indirect supervision, supervisor reachable within minutes"],
   ["4", "Performs unsupervised; supervisor available for the unexpected"], ["5", "Supervises and teaches others"]]) + """
    <p><b>Suggested minimum for a doctor covering a paediatric ward alone at night:</b> level 4 for recognition, high-quality CPR, bag-mask ventilation, IO access and the arrest pathways, confirmed by a hands-on course.</p>"""

# ------------------------------------------------------------------ B
def scenario(n, title, setup, stages, points):
    rows = "".join("<tr><td class='num'>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % s for s in stages)
    return """    <h4>Scenario %d — %s</h4>
    <p>%s</p>
    <div class="tw"><table class="reflow"><thead><tr><th class="num">Stage</th><th>Results card</th><th>Expected actions</th><th>Facilitator trigger</th></tr></thead><tbody>%s</tbody></table></div>
    <p><b>Debrief points:</b> %s</p>
""" % (n, title, setup, rows, points)

B = """    <p>Four branching megacode scenarios that run on a manikin with a rhythm simulator or printed rhythm cards. Show the next card only when the team has done, or clearly failed to do, the expected actions.</p>
""" + scenario(1, "The bradycardic infant",
  "Ward, 3 a.m. 8-month-old, 8 kg, bronchiolitis. One doctor, two nurses.",
  [("1", "HR 55, SpO₂ 68%, floppy", "Call for help; open airway; bag-mask with oxygen", "If atropine is drawn up first: HR falls to 40"),
   ("2", "HR 50 after 30 s of good ventilation, poor perfusion", "Start CPR 15:2; IO; epinephrine 0.08 mg", "If no compressions: pulse lost → PEA card"),
   ("3", "HR 120, SpO₂ 92%", "Post-ROSC care; call PICU; transfer", "Parent enters the room: who supports her?")],
  "ventilation first; CPR threshold; early epinephrine.") + scenario(2, "Sudden collapse at school",
  "Sports ground. 13-year-old, 45 kg, collapses while running. AED on site; ambulance 15 minutes away.",
  [("1", "Unresponsive, gasping, no pulse", "CPR 30:2; AED on; shock", "If CPR is delayed for a pulse check over 10 s: facilitator counts aloud"),
   ("2", "Hospital: VF persists after 1 shock", "Shock 4 J/kg (180 J); CPR; epinephrine after 2nd shock", "If epinephrine before the 2nd shock: discuss 2025 timing"),
   ("3", "VF after 3 shocks", "Amiodarone 5 mg/kg or lidocaine 1 mg/kg; reversible causes", "ROSC card: ECG shows long QT")],
  "shock first; minimal pauses; think channelopathy.") + scenario(3, "Unstable SVT",
  "Emergency room. 4-month-old, 6 kg, poor feeding, HR 290, grey, CRT 5 s, BP 55/30.",
  [("1", "Narrow-complex tachycardia, no P waves", "Recognise unstable SVT; pads; IV if available", "If vagal manoeuvres prolonged: BP falls"),
   ("2", "IV in place", "Adenosine 0.6 mg rapid push with flush, or synchronised cardioversion 3–6 J", "If unsynchronised shock chosen: rhythm becomes VF"),
   ("3", "Sinus rhythm 150", "12-lead ECG; look for pre-excitation; cardiology", "&mdash;")],
  "stable versus unstable; adenosine technique; synchronised energy.") + scenario(4, "PEA after trauma",
  "Emergency room. 7-year-old, 22 kg, hit by a motorbike. Arrests on arrival.",
  [("1", "PEA, narrow and fast", "CPR; IO; epinephrine 0.22 mg early; think T's", "Chest: absent breath sounds on the right"),
   ("2", "Tension pneumothorax suspected", "Decompress; blood; control bleeding", "If decompression delayed: no change"),
   ("3", "ROSC", "Post-ROSC targets; trauma team; family", "Police intimation: medicolegal case")],
  "reversible causes; trauma specifics; medicolegal steps in India.") + pearls

C = '''    <h4>C1 · Three delivery models</h4>
''' + table(["Model", "Shape", "Best for", "Watch out for"],
  [["<b>Fully self-paced</b>", "Learners work through alone; one skills session at the end", "Large cohorts, interns, CME", "The skills session becoming a demonstration. Cap at 6 learners per doll."],
   ["<b>Flipped, Part by Part</b>", "Learners master a Part before each session; sessions are simulation and discussion", "PG residents, nursing cohorts", "Verify mastery first, or you end up teaching content"],
   ["<b>Intensive, 2 days</b>", "Parts A&ndash;C day one with simulation; D&ndash;E day two", "District outreach, visiting faculty", "Retention: schedule the review checks and a 6-week follow-up"]]) + '''
    <h4>C2 · A worked flipped-classroom session &mdash; Part D, cardiac arrest</h4>
    <p>90 minutes, 8&ndash;12 learners, 2 manikins, a defibrillator trainer, printed rhythm cards, 2 facilitators. Prerequisite: Units 12&ndash;16 mastered.</p>
''' + table(["Time", "Activity", "Purpose"],
  [["0&ndash;5", "Learning contract: &ldquo;Nobody here is being examined.&rdquo;", "Psychological safety"],
   ["5&ndash;15", "Rapid retrieval: the four arrest rhythms; epinephrine dose and 2025 timing; defibrillation energies", "Retrieval practice; shows where the cohort is"],
   ["15&ndash;35", "Deliberate practice: CPR with feedback, and charge-during-compressions defibrillation, in pairs", "The highest-yield skills in Part D"],
   ["35&ndash;55", "Megacodes 1 and 2 (Appendix B)", "Both arrest pathways under time pressure"],
   ["55&ndash;75", "Debrief both runs, PEARLS, two points maximum", "Consolidation"],
   ["75&ndash;85", "Drug calculation relay against the clock", "Makes weight-based dosing a habit"],
   ["85&ndash;90", "&ldquo;One thing to keep, one thing to change.&rdquo;", "Commitment to change"]]) + "\n" + appC_generic

C = C.replace("A cut score chosen by preference — including the 90%", "A cut score chosen by preference — including the 80%")
C = C.replace("&ldquo;a labour-room nurse who would reliably ventilate a flat baby within 60 seconds and recognise when it was not working, but would hesitate over an unfamiliar drug dose.&rdquo;",
              "&ldquo;a first-year resident who would reliably start high-quality CPR, give early epinephrine in asystole and defibrillate VF at the right energy, but would hesitate over antiarrhythmics or post-ROSC targets.&rdquo;")
C = re.sub(r"Delivery-room audit: time to PPV, DCC rate, routine suction rate, admission temperature", "Resuscitation audit: time to CPR, time to first epinephrine, time to first shock, debrief held", C)
C = C.replace("with a labour-room audit", "with a resuscitation audit")
C = re.sub(r"Admission hypothermia, early neonatal mortality, HIE referrals within window", "Arrests outside intensive care, survival to discharge, neurological outcome at discharge, early warning score compliance", C)

# ------------------------------------------------------------------ D
D = """    <p>Map each unit to the <b>competency descriptors</b> of the NMC CBME curriculum (UG) and the MD Paediatrics curriculum (PG), and to nursing curricula. The code column is deliberately blank: codes were revised in the September 2024 guidelines, and Volume II is the only authority. <b>Do not invent codes</b>.</p>
""" + table(["Unit", "Competency descriptor (paraphrased)", "NMC code (verify)", "Domain", "Teaching method", "Assessment"],
  [["1&ndash;3", "Recognise the seriously ill child; work in a resuscitation team", "", "K, S, A", "Self-paced; simulation", "Checkpoints; MSF"],
   ["4&ndash;7", "Perform paediatric BLS, choking relief, defibrillation, bag-mask ventilation and IO access", "", "S", "Skills lab", "OSCE 1&ndash;6; DOPS"],
   ["8&ndash;11", "Manage respiratory failure, shock, bradycardia and tachycardia", "", "K, S", "Simulation", "OSCE 7&ndash;9"],
   ["12&ndash;16", "Lead paediatric cardiac arrest resuscitation", "", "K, S, A", "Flipped session (C2); megacodes", "OSCE 10&ndash;11"],
   ["17&ndash;19", "Provide post-arrest care; communicate with families; improve systems", "", "K, S, A, C", "Role play; audit", "OSCE 12; MSF"],
   ["20", "Integrate the resuscitation pathway", "", "K, S, A", "Capstone", "Debrief review"]]) + box("pitfall", "Why the code column is empty", "<p>Invented or outdated competency codes are worse than none. Fill the column from NMC CBME Volume II (2024) at your institution.</p>")

# ------------------------------------------------------------------ E
E = box("danger", "Verify before every use", "<p>Doses here are drawn from the 2025 AHA/AAP guidelines (and 2020 recommendations carried forward) for learning. Check every dose against your institution's protocol, a current formulary and the child in front of you. This annex is never locked.</p>") + """
    <h4>E1 · CPR (2025)</h4>
""" + table(["", "Infant", "Child"],
  [["Compression rate", "100&ndash;120/min", "100&ndash;120/min"],
   ["Depth", "&ge;1/3 chest depth, about 4 cm", "&ge;1/3 chest depth, about 5 cm"],
   ["Technique", "Two-thumb encircling or heel of one hand (no two-finger)", "One or two hands"],
   ["Ratio", "30:2 (1 rescuer), 15:2 (2 rescuers)", "30:2 (1 rescuer), 15:2 (2 rescuers)"],
   ["With advanced airway", "1 breath every 2&ndash;3 s (20&ndash;30/min)", "Same"],
   ["Pulse check", "Up to 10 seconds", "Up to 10 seconds"]]) + """
    <h4>E2 · Arrest drugs and electricity</h4>
""" + table(["Item", "Dose", "Notes"],
  [["Epinephrine IV/IO", "0.01 mg/kg (0.1 mL/kg of 0.1 mg/mL), max 1 mg", "Nonshockable: as soon as possible; shockable: after 2nd shock; every 3&ndash;5 min"],
   ["Epinephrine ETT", "0.1 mg/kg (0.1 mL/kg of 1 mg/mL)", "Only if no IV/IO"],
   ["Defibrillation", "2 J/kg (2&ndash;4), then 4 J/kg; later &ge;4 J/kg, max 10 J/kg or adult dose", "Single shocks"],
   ["Amiodarone", "5 mg/kg bolus in arrest; may repeat to 15 mg/kg total (max 300 mg per dose)", "Shock-refractory VF/pVT"],
   ["Lidocaine", "1 mg/kg loading", "Alternative to amiodarone"],
   ["Magnesium sulfate", "25&ndash;50 mg/kg (max 2 g)", "Torsades de pointes"],
   ["Calcium, sodium bicarbonate", "Not routine", "Hyperkalaemia, hypocalcaemia, specific toxicities"]]) + """
    <h4>E3 · Rhythms with a pulse</h4>
""" + table(["Item", "Dose", "Notes"],
  [["Adenosine", "0.1 mg/kg rapid push (max 6 mg); then 0.2 mg/kg (max 12 mg)", "Two-syringe technique with flush"],
   ["Synchronised cardioversion", "0.5&ndash;1 J/kg, then 2 J/kg", "Sedate if possible without delay"],
   ["Atropine", "0.02 mg/kg; max single dose 0.5 mg", "Vagal bradycardia or primary AV block"],
   ["Epinephrine for bradycardia", "0.01 mg/kg IV/IO every 3&ndash;5 min", "With CPR if HR &lt;60 and poor perfusion"],
   ["Sotalol IV", "Per expert/local protocol", "2025: refractory SVT with compromise when expert consultation is unavailable"]]) + """
    <h4>E4 · Other emergency drugs</h4>
""" + table(["Drug", "Dose", "Notes"],
  [["Epinephrine IM (anaphylaxis)", "0.01 mg/kg of 1 mg/mL, max 0.5 mg", "Anterolateral thigh; repeat after 5 min"],
   ["Glucose 10%", "5 mL/kg (WHO ETAT; some protocols 2 mL/kg)", "Recheck in 15&ndash;30 min"],
   ["Naloxone", "Per local protocol and route", "Opioid toxicity with respiratory depression"],
   ["Prostaglandin E1", "Per cardiology advice", "Duct-dependent lesions; apnoea risk"]]) + """
    <h4>E5 · After ROSC (2025)</h4>
""" + table(["Target", "Value"],
  [["Central temperature", "Avoid &gt;37.5 °C; TTM 32&ndash;34 °C then 36&ndash;37.5 °C, or 36&ndash;37.5 °C, for comatose children 24 h&ndash;18 y"],
   ["Blood pressure", "Systolic and MAP above the 10th percentile for age"],
   ["SpO₂", "94&ndash;99%"],
   ["PaCO₂", "Appropriate to the condition; avoid hypo- and hypercapnia"],
   ["During CPR (arterial line)", "Diastolic &ge;25 mmHg infants; &ge;30 mmHg children &ge;1 year"]]) + """
    <h4>E6 · Equipment by age and weight</h4>
""" + table(["", "Guide"],
  [["Cuffed tracheal tube size", "(age &divide; 4) + 3.5 mm"],
   ["Tube depth at lips", "About 3 &times; tube internal diameter (cm)"],
   ["Hypotension (systolic)", "Neonate &lt;60; infant &lt;70; 1&ndash;10 y &lt;70 + 2 &times; age; &gt;10 y &lt;90 mmHg"],
   ["Weight", "Measured weight or length-based tape"]])

# ------------------------------------------------------------------ F
F = """    <h4>Primary guidelines &mdash; the sources this module is written to</h4>
    <ul>
      <li><b>Part 8: Pediatric Advanced Life Support.</b> 2025 American Heart Association and American Academy of Pediatrics Guidelines for Cardiopulmonary Resuscitation and Emergency Cardiovascular Care. Circulation 2025; Pediatrics 2026;157(1):e2025074351. <a href="https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/pediatric-advanced-life-support">AHA</a></li>
      <li><b>Part 6: Pediatric Basic Life Support.</b> 2025 AHA/AAP Guidelines for CPR and ECC. <a href="https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/pediatric-basic-life-support">AHA</a></li>
      <li><b>Part 1: Executive Summary.</b> 2025 AHA Guidelines for CPR and ECC. Circulation 2025.</li>
      <li>International Liaison Committee on Resuscitation. <b>2025 International Consensus on CPR and ECC Science with Treatment Recommendations.</b></li>
      <li>Weiss SL, Peters MJ, et&nbsp;al. <b>Surviving Sepsis Campaign International Guidelines for the Management of Sepsis and Septic Shock in Children 2026.</b> Pediatr Crit Care Med 2026.</li>
      <li>Topjian AA, et&nbsp;al. <b>Part 4: Pediatric Basic and Advanced Life Support</b>, 2020 AHA Guidelines (for recommendations carried forward unchanged in 2025).</li>
    </ul>
    <h4>Key trials and studies</h4>
    <ul>
      <li>Moler FW, et&nbsp;al. <b>Therapeutic hypothermia after out-of-hospital cardiac arrest in children (THAPCA-OH).</b> N Engl J Med 2015;372:1898&ndash;908.</li>
      <li>Moler FW, et&nbsp;al. <b>Therapeutic hypothermia after in-hospital cardiac arrest in children (THAPCA-IH).</b> N Engl J Med 2017;376:318&ndash;29.</li>
      <li>Maitland K, et&nbsp;al. <b>Mortality after fluid bolus in African children with severe infection (FEAST).</b> N Engl J Med 2011;364:2483&ndash;95.</li>
      <li>Parshuram CS, et&nbsp;al. <b>Effect of a pediatric early warning system on all-cause mortality (EPOCH).</b> JAMA 2018;319:1002&ndash;12.</li>
    </ul>
    <h4>Other Vikkypaedia modules referred to</h4>
    <ul>
      <li><b>OxyVent: Oxygen and Ventilation</b> &mdash; respiratory failure, bag-mask ventilation, airway, transport.</li>
      <li><b>Approach to the Sick Child</b> &mdash; shock, sepsis (SSC 2026), poisoning, envenomation.</li>
      <li><b>Neonatal Resuscitation 2025</b> &mdash; resuscitation at birth.</li>
    </ul>
    <h4>Educational evidence base</h4>
    <ul>
      <li>Cheng A, et&nbsp;al. <b>Resuscitation education science: educational strategies to improve outcomes from cardiac arrest</b> (AHA scientific statement). Circulation 2018.</li>
      <li>Larsen DP, Butler AC, Roediger HL (2009) &mdash; test-enhanced learning. Cepeda NJ, et&nbsp;al. (2006) &mdash; distributed practice. Butterfield B, Metcalfe J (2001) &mdash; the hypercorrection effect.</li>
      <li><b>Ottawa 2020 Consensus Statements</b> on programmatic assessment. McKinley RK, Norcini JJ. <b>AMEE Guide No. 85</b> &mdash; standard setting.</li>
    </ul>
    <p style="font-size:.85rem;color:var(--ink-2)">PALS&reg; is a trademark of the American Heart Association. This module is not the AHA PALS course, does not reproduce the AHA provider manual, and confers no provider status.</p>
""" + box("danger", "Check the edition before you teach from anything", "<p>Resuscitation guidelines are revised on a 5-year cycle with interim updates. Confirm any dose, energy or target against the current AHA/AAP or ILCOR publication before teaching or treating. If you are reading this more than three years after the build date in the footer, assume something here is out of date.</p>")

# ------------------------------------------------------------------ G (generic, adapted)
G = appG
G = G.replace("sample 50 items from a pool of 78", "sample 50 items from a pool of 70")
G = G.replace("This module has no evidence that it changes delivery-room behaviour or neonatal outcomes.", "This module has no evidence yet that it changes resuscitation performance or child outcomes.")
G = G.replace("WHO guidance on newborn care", "the 2025 AHA/AAP resuscitation guidelines")
G = G.replace("Part D is unintelligible without Part C", "Part D's arrest pathways make no sense without Part B's high-quality CPR")
# strip wrapper lines from the NRP block so we can re-wrap consistently
G = G[G.index('<div class="app-body">') + len('<div class="app-body">'):]
G = G[:G.rindex("</div>\n</div>")] if "</div>\n</div>" in G else G

head = '''<section class="part" id="appendices">
  <div class="part-head">
    <div>
      <span class="pk">Appendices</span>
      <h2>Appendices A&ndash;G</h2>
    </div>
    <span class="part-meta"><span class="app-open-note">Never locked</span></span>
  </div>
  <p class="part-lede">Open from the first minute, whatever your progress. Appendix E (drugs, energies and targets) and Appendix F (references) are clinical safety material, and clinical safety material behind a quiz is a patient-safety problem. Every appendix can be printed on its own.</p>
'''
html = head + app("A", "Assessment bank", A) + app("B", "Simulation library", B) + app("C", "Faculty guide", C) + \
       app("D", "Curriculum mapping", D) + app("E", "Drug, energy and target annex", E) + app("F", "References", F) + \
       app("G", "Evidence-governed design", G) + "\n</section>\n"
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html) // 1024, "KB")
for bad in ["ammonia", "metabol", "labour", "IEM"]:
    n = len(re.findall(bad, html, re.I))
    if n: print("  check:", bad, n)
