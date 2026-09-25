# -*- coding: utf-8 -*-
"""Interactive megacodes: Paediatric Advanced Life Support 2025.

Every dose, energy and target here is taken from Appendix E of this module (2025 AHA/AAP, with
2020 recommendations carried forward) and worked for the stated weight:
  epinephrine IV/IO 0.01 mg/kg of 0.1 mg/mL (max 1 mg) | defibrillation 2 J/kg, then 4 J/kg, later >=4 (max 10 J/kg or adult)
  amiodarone 5 mg/kg (max 300 mg/dose) | lidocaine 1 mg/kg | adenosine 0.1 mg/kg (max 6), then 0.2 mg/kg (max 12)
  synchronised cardioversion 0.5-1 J/kg, then 2 J/kg | atropine 0.02 mg/kg
  septic shock fluids per SSC 2026 as taught in Unit 9 | post-ROSC targets per E5.
Compile with:  python megacodes/make.py
"""

def O(t, fb, ok=False, to=None, dt=0, crit=False, mark=None, mt=None):
    o = {"t": t, "fb": fb, "dt": dt}
    if ok: o["ok"] = 1
    if crit: o["crit"] = 1
    if to: o["to"] = to
    if mark: o["mark"] = mark
    if mt is not None: o["mt"] = mt
    return o

def N(text, ask, opts, **mon):
    return {"text": text, "ask": ask, "opts": opts, "mon": mon}

def E(kind, text, **mon):
    return {"end": kind, "text": text, "mon": mon}

INTRO = ("Six branching cases played against a monitor, one decision at a time. Wrong calls change the patient, "
         "cost time, or are flagged as critical errors, and every choice is explained. The options are shuffled on "
         "every run, so a repeat run tests reasoning rather than memory. A case opens when its Part opens. "
         "<b>Practice only:</b> results appear in your completion record and your faculty's class report, but they are "
         "not part of the certificate. Hands-on megacodes on a manikin (Appendix B) are still essential.")

ARREST = ["rhythm", "hr", "spo2", "bp", "etco2"]

CASES = [

# ---------------------------------------------------------------- 1 · bradycardia
{
 "id": "p-brady", "title": "The bradycardic infant", "patient": "8 months · 8 kg · bronchiolitis · ward, 3 a.m.",
 "part": "C", "units": [4, 10], "minutes": 5, "monitor": ARREST[:4],
 "brief": "You are the doctor on call. The nurse has called you to an infant with bronchiolitis who has become floppy.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>The infant is floppy and grey, with shallow, infrequent breaths. A pulse is present but weak.</p>",
          "What is your first action?", [
     O("Call for help; open the airway and start bag-mask ventilation with 100% oxygen.",
       "In infants, bradycardia is usually caused by hypoxia, and ventilation with oxygen is the first treatment.", ok=True, to="n2", dt=30, mark="ppv"),
     O("Atropine 0.16 mg IV (0.02 mg/kg).",
       "Atropine does not treat hypoxia. Hypoxic bradycardia continues until oxygenation is restored.", crit=True, to="n1x", dt=90),
     O("Start chest compressions at once.",
       "There is a pulse. Oxygenate and ventilate first. Start compressions if HR stays below 60/min with poor perfusion <i>despite</i> effective ventilation.", dt=20),
     O("Increase the nasal cannula flow and review in 15 minutes.",
       "A floppy infant with HR 55/min is peri-arrest. Waiting is how this becomes a cardiac arrest.", crit=True, to="n1x", dt=120),
   ], rhythm="brady", hr=55, spo2=68, bp="58/30", flag="Pulse weak"),
  "n1x": N("<p>Two minutes pass. The heart rate has fallen to 40/min and he has almost stopped breathing.</p>",
           "What now?", [
     O("Open the airway and ventilate by bag-mask with 100% oxygen.",
       "Right, and now urgent. Ventilation fixes the hypoxia behind this bradycardia.", ok=True, to="n2", dt=30, mark="ppv"),
     O("Give the atropine, then reassess.", "It still does not treat hypoxia. Ventilate.", dt=30),
     O("Transcutaneous pacing.", "Pacing does not oxygenate. Ventilation first.", dt=60),
   ], rhythm="brady", hr=40, spo2=55, bp="50/24", flag="Deteriorating"),
  "n2": N("<p>After 30 seconds of good bag-mask ventilation, the chest is rising and SpO₂ is climbing. The heart rate is still 50/min, pulses are weak, and capillary refill is 5 seconds.</p>",
          "What now?", [
     O("Start CPR at 15:2 (two-thumb encircling technique) while ventilation continues, and get IO access.",
       "HR below 60/min with poor perfusion despite effective oxygenation and ventilation is the threshold for compressions.", ok=True, to="n3", dt=30, mark="cpr"),
     O("Ventilate for another 2 minutes before doing anything else.",
       "Ventilation is working (SpO₂ is rising) but perfusion is not. HR below 60 with poor perfusion despite effective ventilation means CPR now.", dt=120),
     O("Two-finger compressions over the lower sternum.",
       "The two-finger technique is no longer recommended (2025). Use two-thumb encircling with two rescuers, or the heel of one hand.", dt=30),
     O("Atropine 0.16 mg: this is vagal.",
       "Nothing here is vagal: this is hypoxic bradycardia. Atropine is for increased vagal tone or primary AV block, after oxygenation.", dt=30),
   ], rhythm="brady", hr=50, spo2=84, bp="52/26", flag="Poor perfusion"),
  "n3": N("<p>IO access is in the proximal tibia. At the pause the heart rate is 48/min, still with poor perfusion.</p>",
          "Which drug, and what dose?", [
     O("Epinephrine 0.08 mg IO (0.01 mg/kg = 0.8 mL of 0.1 mg/mL), then a flush; repeat every 3–5 minutes.",
       "Epinephrine 0.01 mg/kg of the 0.1 mg/mL solution. Say the concentration aloud whenever you order it.", ok=True, to="n4", dt=120, mark="epi1"),
     O("Epinephrine 0.8 mL of the 1 mg/mL ampoule.",
       "That is 0.8 mg, a tenfold overdose. The dose is 0.01 mg/kg of the 0.1 mg/mL solution (0.1 mL/kg).", crit=True, dt=30),
     O("Adenosine 0.8 mg rapid push.",
       "Adenosine blocks the AV node and is for SVT. In bradycardia it can cause asystole.", crit=True, dt=30),
     O("Amiodarone 40 mg (5 mg/kg).", "Amiodarone has no role in bradycardia.", dt=30),
   ], rhythm="cpr", hr=48, spo2=88, bp=None, flag="CPR in progress"),
  "n4": N("<p>Two minutes later: HR 128/min, strong pulses, SpO₂ 93% with bag-mask ventilation, but no effective breathing of his own.</p>",
          "What next?", [
     O("Stop compressions; keep supporting breathing (non-invasive support or intubation by the most experienced person); check glucose; call PICU.",
       "The circulation is back, but the cause (respiratory failure with apnoea) is unchanged. Keep supporting breathing and escalate.", ok=True, to="end", dt=120),
     O("Stop all support: he has recovered.",
       "The cause is unchanged. Without support he will become bradycardic again.", crit=True, dt=30),
     O("Continue compressions for another 2 minutes to be safe.",
       "Compressions are for HR below 60/min with poor perfusion. At 128/min with strong pulses, stop them.", dt=30),
   ], rhythm="stach", hr=128, spo2=93, bp="82/46"),
  "end": E("good", "<p>He is intubated by the anaesthetist and moved to the PICU. He goes home 9 days later.</p>",
           rhythm="sinus", hr=132, spo2=96, bp="86/48"),
 },
 "timers": [{"mark": "ppv", "label": "Ventilation started", "target": "target ≤ 1:00", "max": 60},
            {"mark": "cpr", "label": "Compressions started", "target": "once HR < 60/min with poor perfusion despite ventilation"}],
 "debrief": ["In infants, bradycardia is usually hypoxia: ventilate with oxygen first.",
             "HR below 60/min with poor perfusion despite effective ventilation: start CPR.",
             "Two-thumb encircling or the heel of one hand; the two-finger technique has gone (2025).",
             "Epinephrine 0.01 mg/kg of 0.1 mg/mL every 3–5 minutes. Atropine only for vagal bradycardia or primary AV block.",
             "Treat the cause: support breathing and plan escalation before the next apnoea."],
},

# ---------------------------------------------------------------- 2 · SVT
{
 "id": "p-svt", "title": "Unstable SVT", "patient": "4 months · 6 kg · poor feeding · emergency room",
 "part": "C", "units": [11], "minutes": 5, "monitor": ARREST[:4],
 "brief": "A 4-month-old has been feeding poorly for a day. Her mother says she is breathing fast and looks pale.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>She is grey and irritable. Capillary refill 5 seconds, BP 55/30 mmHg. The monitor shows this rhythm, and the rate does not vary.</p>",
          "How do you read this, and what do you do first?", [
     O("SVT with poor perfusion: put on pads, get IV or IO access, and prepare adenosine and synchronised cardioversion together.",
       "A fixed rate near 290/min with no P waves is SVT, not sinus tachycardia. Poor perfusion makes it unstable, so prepare both treatments at once.", ok=True, to="n2", dt=90),
     O("Sinus tachycardia from dehydration: give a 20 mL/kg saline bolus.",
       "Sinus tachycardia in infants rarely exceeds 220/min and varies with activity. A fixed 290 with no P waves is SVT, and fluid will not fix it.", dt=60),
     O("Prolonged vagal manoeuvres: ice to the face for several minutes.",
       "One brief vagal attempt is reasonable only if it causes no delay. In an unstable infant, prolonged attempts waste time.", dt=120),
     O("Unsynchronised defibrillation at 24 J (4 J/kg).",
       "An unsynchronised shock in a rhythm with a pulse can cause VF. Unstable SVT is treated with <i>synchronised</i> cardioversion.", crit=True, dt=30),
   ], rhythm="svt", hr=290, spo2=94, bp="55/30", flag="Poor perfusion"),
  "n2": N("<p>An IV cannula is in the antecubital fossa and the pads are on. The rhythm is unchanged.</p>",
          "Adenosine: which dose, and how is it given?", [
     O("0.6 mg (0.1 mg/kg) as a rapid push, immediately followed by a rapid saline flush (two-syringe technique), with the rhythm strip recording.",
       "Adenosine lasts only seconds, so it must be pushed fast and chased with a flush. Record the strip: it shows what happened even if the rhythm does not convert.", ok=True, to="n3", dt=30, mark="aden1"),
     O("0.6 mg as a slow push over one minute.",
       "Adenosine lasts only seconds, so a slow push never reaches the heart. Give a rapid push with a flush.", dt=30),
     O("6 mg.", "That is 1 mg/kg, ten times the dose. Give 0.1 mg/kg (max 6 mg) first, then 0.2 mg/kg (max 12 mg).", crit=True, dt=30),
     O("Verapamil 0.6 mg IV.", "Verapamil can cause severe hypotension and asystole in infants. It is not used for SVT in infancy.", crit=True, dt=30),
   ], rhythm="svt", hr=290, spo2=94, bp="54/30", flag="Poor perfusion"),
  "n3": N("<p>After the push there are 3 seconds of asystole, then SVT at 290/min returns. She is still grey.</p>",
          "What next?", [
     O("Adenosine 1.2 mg (0.2 mg/kg) as a rapid push with a flush.",
       "The transient block shows the drug reached the heart. The second dose is 0.2 mg/kg (max 12 mg). Synchronised cardioversion would also be right.", ok=True, to="n4", dt=30, mark="conv"),
     O("Synchronised cardioversion at 3–6 J (0.5–1 J/kg), with sedation if it causes no delay.",
       "Right: synchronised cardioversion is an equally valid next step, as is a second dose of adenosine.", ok=True, to="n3c", dt=45),
     O("Repeat 0.6 mg; the first dose nearly worked.", "The dose has to go up: the second dose is doubled to 0.2 mg/kg.", dt=30),
     O("Unsynchronised shock at 12 J.", "With a pulse, shocks must be synchronised. An unsynchronised shock can cause VF.", crit=True, dt=30),
   ], rhythm="svt", hr=290, spo2=93, bp="52/28", flag="Poor perfusion"),
  "n3c": N("<p>A synchronised shock at 6 J is delivered. The SVT persists.</p>", "What next?", [
     O("Synchronised cardioversion at 12 J (2 J/kg).",
       "Escalate to 2 J/kg. If this fails, get expert help for drug options (amiodarone or procainamide; 2025 adds IV sotalol when expert advice is not available).", ok=True, to="n4", dt=30, mark="conv"),
     O("Repeat 6 J several more times.", "Escalate the energy: 0.5–1 J/kg, then 2 J/kg.", dt=60),
     O("Switch the device to unsynchronised mode.", "With a pulse, stay synchronised. Unsynchronised shocks can cause VF.", crit=True, dt=30),
   ], rhythm="svt", hr=290, spo2=92, bp="50/28", flag="Poor perfusion"),
  "n4": N("<p>Sinus rhythm at 150/min. Her colour returns and capillary refill is 2 seconds.</p>", "What next?", [
     O("Record a 12-lead ECG in sinus rhythm (look for pre-excitation), keep her monitored for recurrence, and discuss with paediatric cardiology.",
       "Recurrence is common, and pre-excitation (WPW) changes which drugs are safe.", ok=True, to="end", dt=120),
     O("Discharge her home: the episode is over.",
       "She was haemodynamically unstable and SVT often recurs. She needs monitoring, an ECG and cardiology input.", crit=True, dt=30),
     O("Start digoxin loading today without an ECG.",
       "Digoxin can be dangerous with pre-excitation. Get a 12-lead ECG and expert advice first.", dt=30),
   ], rhythm="sinus", hr=150, spo2=98, bp="78/44"),
  "end": E("good", "<p>The ECG in sinus rhythm shows no pre-excitation. Cardiology starts preventive treatment and plans a follow-up.</p>",
           rhythm="sinus", hr=140, spo2=99, bp="80/46"),
 },
 "timers": [{"mark": "conv", "label": "Second treatment given", "target": "within minutes, without a long pause"}],
 "debrief": ["A fixed rate with no P waves, above 220/min in an infant: SVT, not sinus tachycardia.",
             "Unstable SVT: prepare adenosine and synchronised cardioversion together, and do not delay for prolonged vagal manoeuvres.",
             "Adenosine 0.1 mg/kg (max 6 mg), then 0.2 mg/kg (max 12 mg), as a rapid push with a flush.",
             "Synchronised cardioversion at 0.5–1 J/kg, then 2 J/kg. Never unsynchronised when there is a pulse.",
             "No verapamil in infants. After conversion, get a 12-lead ECG to look for pre-excitation."],
},

# ---------------------------------------------------------------- 3 · septic shock
{
 "id": "p-sepsis", "title": "Septic shock without a PICU", "patient": "2 years · 12 kg · fever and drowsiness · district hospital",
 "part": "C", "units": [9], "minutes": 6, "monitor": ["hr", "spo2", "bp", "temp"], "clockLabel": "Since arrival",
 "brief": "Your district hospital has no PICU; the nearest is 3 hours away by road. A 2-year-old boy with two days of fever is brought in drowsy.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>HR 178/min, RR 44/min, cold mottled limbs, capillary refill 5 seconds, BP 68/38 mmHg. No liver enlargement, no crackles, no gallop.</p>",
          "What do you do in the first 15 minutes?", [
     O("Oxygen; IV or IO access; blood culture and glucose; first antibiotic dose within the hour; a 10–20 mL/kg (120–240 mL) balanced crystalloid bolus, then reassess.",
       "He is hypotensive, so boluses are indicated even without intensive care (up to 40 mL/kg in 10–20 mL/kg steps, SSC 2026). Antibiotics must not wait for results.", ok=True, to="n2", dt=900, mark="abx", mt=600),
     O("No bolus: FEAST showed that boluses kill children where there is no intensive care.",
       "The advice against boluses without intensive care applies to children who are <i>not</i> hypotensive. He is hypotensive: give 10–20 mL/kg boluses, up to 40 mL/kg, and reassess after each.", dt=300),
     O("60 mL/kg as fast as possible, then reassess.",
       "Without intensive care, give up to 40 mL/kg, in 10–20 mL/kg boluses with reassessment after each. A large volume given without reassessment risks overload, and there is no ventilator to rescue him.", crit=True, dt=600),
     O("Take a blood culture and wait for the result before starting antibiotics.",
       "In septic shock, give antibiotics within the first hour. Take the culture first only if it causes no delay, and never wait for the result.", crit=True, dt=900),
   ], hr=178, spo2=93, bp="68/38", temp="39.4", flag="Hypotensive"),
  "n2": N("<p>After 20 mL/kg: HR 170/min, BP 70/40 mmHg, capillary refill 4 seconds. The liver edge is at the costal margin, the chest is clear, and there is no gallop. Glucose 5.6 mmol/L. The antibiotic has been given.</p>",
          "What next?", [
     O("A second 10–20 mL/kg bolus, then examine again for liver enlargement, crackles and a gallop.",
       "He is still hypotensive and shows no overload, so a second bolus is appropriate (up to 40 mL/kg in total), reassessing after it.", ok=True, to="n3", dt=900, mark="fluid2"),
     O("Stop fluids and observe for an hour.", "He is still hypotensive with no overload. Stopping now leaves the shock untreated.", dt=900),
     O("Give 40 mL/kg more in one go.",
       "That would take him to 60 mL/kg, beyond the 40 mL/kg ceiling where there is no intensive care, and without reassessment.", crit=True, dt=600),
   ], hr=170, spo2=93, bp="70/40", temp="39.0", flag="Hypotensive"),
  "n3": N("<p>After 40 mL/kg in total: HR 168/min, BP 66/36 mmHg. The liver is now 3 cm below the costal margin and there are fine crackles at both bases. SpO₂ 91%.</p>",
          "What now?", [
     O("Stop boluses; start an epinephrine (or norepinephrine) infusion through the peripheral line or IO, titrated to perfusion; support breathing; call the referral centre now.",
       "Fluid-refractory shock with signs of overload: no more fluid. Start epinephrine or norepinephrine without waiting for central access.", ok=True, to="n4", dt=900, mark="vaso", mt=300),
     O("A third 20 mL/kg bolus: he is still hypotensive.",
       "A growing liver and crackles mean fluid overload, and more fluid will push him into pulmonary oedema. Switch to a vasoactive.", crit=True, dt=600),
     O("Dopamine, but only after a central line is in.",
       "Epinephrine or norepinephrine is preferred, and a peripheral or IO infusion is acceptable at first. Waiting for central access delays treatment.", dt=900),
     O("Furosemide and fluid restriction; no vasoactive.",
       "He is overloaded <i>and</i> still in shock. He needs circulatory support, not diuresis alone.", dt=600),
   ], hr=168, spo2=91, bp="66/36", temp="38.8", flag="Crackles · liver 3 cm"),
  "n4": N("<p>On an epinephrine infusion: HR 150/min, BP 84/50 mmHg, capillary refill 3 seconds, passing urine. The PICU accepts him.</p>",
          "Before the 3-hour transfer, what matters most?", [
     O("Stabilise before transfer: secure lines, the infusion on a dedicated pump, oxygen, glucose checks, a trained escort, a clear handover, and an explanation for the family.",
       "A stable transfer beats a fast one. Most deaths in transit follow a preventable loss of lines, drugs or oxygen.", ok=True, to="end", dt=1200),
     O("Send him now in a private vehicle with a relative, to save time.",
       "A child on a vasoactive needs a staffed ambulance with a trained escort, oxygen and monitoring.", crit=True, dt=60),
     O("Stop the infusion for the journey: the pump is heavy.",
       "Stopping a vasoactive in fluid-refractory shock will cause collapse on the road.", crit=True, dt=60),
   ], hr=150, spo2=95, bp="84/50", temp="38.4"),
  "end": E("good", "<p>He reaches the PICU with good perfusion. The blood culture grows <i>Streptococcus pneumoniae</i>.</p>",
           hr=138, spo2=97, bp="90/54", temp="37.9"),
 },
 "timers": [{"mark": "abx", "label": "Antibiotic and first bolus", "target": "within the first hour", "max": 3600},
            {"mark": "vaso", "label": "Vasoactive started", "target": "once shock is fluid-refractory"}],
 "debrief": ["In children, shock is tachycardia and poor perfusion; hypotension is a late sign.",
             "Know your setting (SSC 2026). With intensive care: 10–20 mL/kg boluses up to 40–60 mL/kg. Without it: no boluses unless the child is hypotensive, then up to 40 mL/kg.",
             "Reassess after every bolus: liver, crackles, gallop, work of breathing.",
             "Fluid-refractory shock: epinephrine or norepinephrine through a peripheral line or IO, without waiting for central access.",
             "Antibiotics within the first hour. A stable transfer beats a fast one."],
},

# ---------------------------------------------------------------- 4 · PEA / hypovolaemia
{
 "id": "p-pea", "title": "PEA after diarrhoea", "patient": "3 years · 15 kg · profuse diarrhoea · emergency room",
 "part": "D", "units": [7, 13, 15], "minutes": 6, "monitor": ARREST,
 "brief": "A 3-year-old girl with two days of profuse watery diarrhoea is brought to the emergency room. As you assess her, she stops responding.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>She is unresponsive and apnoeic. The monitor shows a narrow-complex rhythm at 48/min. You feel no central pulse in 10 seconds.</p>",
          "What do you do first?", [
     O("Start CPR now: 15:2 with two rescuers and bag-mask ventilation with 100% oxygen, and call the resuscitation team.",
       "Organised electrical activity without a pulse is PEA, which is cardiac arrest. CPR starts at once.", ok=True, to="n2", dt=30, mark="cpr"),
     O("The monitor shows a heart rate, so give atropine 0.3 mg and watch.",
       "The monitor shows electrical activity, not circulation. No pulse means arrest: start CPR. Atropine has no role in PEA.", crit=True, dt=60),
     O("Recheck the blood pressure and oximeter before deciding.",
       "No pulse on a 10-second check is enough. Waiting for a cuff or an oximeter reading delays CPR.", dt=40),
     O("Defibrillate at 30 J (2 J/kg).", "PEA is not shockable. A shock does nothing for it and interrupts compressions.", crit=True, dt=20),
   ], rhythm="pea", hr=48, spo2=None, bp=None, etco2=None, flag="No pulse"),
  "n2": N("<p>CPR is under way. Two attempts at a peripheral cannula have failed; her veins are collapsed.</p>",
          "How do you get vascular access?", [
     O("An intraosseous needle in the proximal tibia, now.",
       "When IV access is not rapidly available in arrest, go straight to IO. It is fast, and any drug or fluid can be given through it.", ok=True, to="n3", dt=60, mark="io"),
     O("A third and then a fourth peripheral attempt, because IO is painful.",
       "Repeated failed attempts delay the first epinephrine. In arrest, use IO after failed IV attempts, or first.", dt=150),
     O("Insert a central venous line.", "Central access takes too long and interrupts CPR. Use IO first.", dt=300),
     O("Give epinephrine down a tracheal tube and skip vascular access.",
       "Tracheal epinephrine is a last resort with unreliable absorption, and she also needs volume, which cannot go down a tube. IO is quick.", dt=60),
   ], rhythm="cpr", hr=None, spo2=None, bp=None, etco2="12", flag="CPR in progress"),
  "n3": N("<p>The IO needle is in and flushes easily.</p>", "Which drug and dose, and when?", [
     O("Epinephrine 0.15 mg IO now (0.01 mg/kg = 1.5 mL of 0.1 mg/mL), then a flush; repeat every 3–5 minutes.",
       "In nonshockable arrest, give epinephrine as soon as there is access. Every minute of delay lowers survival.", ok=True, to="n4", dt=30, mark="epi1"),
     O("Wait until after two cycles of CPR, as in VF.",
       "Waiting for the second shock applies to shockable rhythms. In asystole and PEA, give epinephrine as soon as possible.", dt=240),
     O("Epinephrine 1.5 mL of the 1 mg/mL ampoule.",
       "That is 1.5 mg, a tenfold overdose. The IV/IO arrest dose is 0.01 mg/kg of the 0.1 mg/mL solution: 1.5 mL of 0.1 mg/mL for 15 kg.", crit=True, dt=30),
     O("Amiodarone 75 mg (5 mg/kg).", "Amiodarone is for shock-refractory VF or pulseless VT, not PEA.", dt=30),
   ], rhythm="cpr", hr=None, spo2=None, bp=None, etco2="12", flag="CPR in progress"),
  "n4": N("<p>Rhythm check at 2 minutes: the same slow narrow-complex rhythm, still no pulse. Her mother says she has drunk nothing for a day. Capillary glucose is 4.8 mmol/L (86 mg/dL).</p>",
          "Which reversible cause do you treat, and how?", [
     O("Hypovolaemia: 20 mL/kg (300 mL) of isotonic crystalloid rapidly through the IO while CPR continues, and send electrolytes, including potassium.",
       "Profuse diarrhoea plus PEA points to hypovolaemia. Fast volume replacement treats the cause, and the electrolytes check another H: potassium.", ok=True, to="n5", dt=240, mark="fluid", mt=10),
     O("Hyperkalaemia: give calcium and bicarbonate routinely.",
       "Calcium and bicarbonate are not routine. Give them only for proven or strongly suspected hyperkalaemia, hypocalcaemia or specific toxicity. The history here points to volume loss.", dt=30),
     O("Hypoglycaemia: 10% glucose 5 mL/kg.", "Her glucose is normal (4.8 mmol/L). Checking it was right, but treating a normal value delays the real cause.", dt=30),
     O("Tension pneumothorax: needle decompression on both sides.", "Nothing suggests a pneumothorax. Treat the cause that the history points to.", dt=60),
   ], rhythm="pea", hr=52, spo2=None, bp=None, etco2="14", flag="No pulse"),
  "n5": N("<p>Six minutes into the arrest (about 4 minutes after the first epinephrine), CPR is continuing. The bolus is in, and the rhythm on the pause is faster (70/min), but there is still no pulse.</p>",
          "What now?", [
     O("Continue CPR, repeat epinephrine 0.15 mg IO (3–5 minutes after the first), and give a second 20 mL/kg bolus.",
       "Repeat epinephrine every 3–5 minutes, and keep treating the cause.", ok=True, to="n6", dt=120, mark="epi2"),
     O("Epinephrine every minute until the pulse returns.", "The interval is every 3–5 minutes. More frequent doses add nothing and cause harm after ROSC.", dt=30),
     O("Stop: 6 minutes of PEA is futile.", "A reversible cause is being treated and the arrest is only minutes old. Continue.", crit=True, dt=30),
     O("High-dose epinephrine, 0.1 mg/kg IV.", "High-dose IV epinephrine is not recommended; it gives no benefit and may harm. The dose is 0.01 mg/kg.", dt=30),
   ], rhythm="pea", hr=70, spo2=None, bp=None, etco2="18", flag="No pulse"),
  "n6": N("<p>After the second bolus a pulse returns: sinus rhythm at 136/min, BP 70/40 mmHg, capillary refill 4 seconds, SpO₂ 91%.</p>",
          "What are your post-ROSC priorities?", [
     O("Titrate oxygen to SpO₂ 94–99%; give further fluid in 10–20 mL/kg boluses, reassessing after each (liver, crackles); keep BP above the 10th centile; recheck glucose and electrolytes; avoid fever; arrange PICU.",
       "These are the 2025 post-ROSC targets, applied to a child who is still shocked.", ok=True, to="end", dt=300),
     O("She has a pulse, so stop close monitoring and replace the deficit orally.",
       "After ROSC the circulation is fragile, and her low BP shows it. She needs continued resuscitation.", crit=True, dt=60),
     O("Give 60 mL/kg straight away, without reassessing.", "Give fluid in 10–20 mL/kg steps and reassess after each one, looking for overload.", dt=60),
   ], rhythm="stach", hr=136, spo2=91, bp="70/40", etco2="34", flag="ROSC"),
  "end": E("good", "<p>She stabilises after one more bolus and is transferred to the PICU. Her sodium was 128 and potassium 2.9 mmol/L, both corrected slowly.</p>",
           rhythm="sinus", hr=124, spo2=96, bp="88/52", etco2="38"),
 },
 "timers": [{"mark": "cpr", "label": "CPR started", "target": "target ≤ 0:30", "max": 30},
            {"mark": "epi1", "label": "First epinephrine", "target": "as soon as possible; ≤ 5:00 from arrest", "max": 300}],
 "debrief": ["PEA is cardiac arrest: the monitor shows electrical activity, not circulation.",
             "Access: go to IO after failed IV attempts. Do not let access delay epinephrine.",
             "Nonshockable rhythm: epinephrine 0.01 mg/kg as soon as possible, then every 3–5 minutes.",
             "Name and treat the cause (Hs and Ts). Here it was hypovolaemia from diarrhoea, a common road to arrest in Indian children.",
             "After ROSC: titrate oxygen, give fluid in reassessed steps, keep BP above the 10th centile, and check glucose and electrolytes."],
},

# ---------------------------------------------------------------- 5 · VF
{
 "id": "p-vf", "title": "Collapse in the corridor: VF", "patient": "13 years · 45 kg · sudden collapse · hospital corridor",
 "part": "D", "units": [5, 12, 14, 17], "minutes": 6, "monitor": ARREST,
 "brief": "A 13-year-old boy (slightly built, prepubertal, so paediatric sequences apply) collapses in the outpatient corridor after running up the stairs. You are the first doctor there; a manual defibrillator is on the nearest crash trolley.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>He is unresponsive, with occasional gasping breaths. You feel for a carotid pulse for 10 seconds: there is none.</p>",
          "What do you do first?", [
     O("Shout for help and the defibrillator, and start chest compressions now (30:2 until a second rescuer arrives).",
       "Gasping is not breathing. No pulse with agonal breaths is cardiac arrest: compressions start immediately, and you call for help and the defibrillator at the same time.", ok=True, to="n2", dt=45, mark="cpr"),
     O("Put him in the recovery position: he is breathing.",
       "Agonal gasps are a sign of cardiac arrest, not breathing. The recovery position delays CPR, and every minute without compressions lowers survival.", crit=True, to="n1x", dt=90),
     O("Check the pulse again for a full 30 seconds to be sure.",
       "Pulse checks last no more than 10 seconds. If you are not sure there is a pulse, start compressions.", dt=30),
     O("Give five rescue breaths first, then reassess.",
       "A witnessed sudden collapse in an adolescent is most likely cardiac, with a shockable rhythm. Start compressions and get the defibrillator; do not delay compressions for rescue breaths.", dt=20),
   ], rhythm="none", hr=None, spo2=None, bp=None, etco2=None, flag="No pulse"),
  "n1x": N("<p>Ninety seconds later he has stopped gasping and is mottled. A nurse arrives with the defibrillator.</p>", "What now?", [
     O("Start compressions immediately and attach the pads while compressions continue.",
       "Yes, now. The pads go on without stopping compressions.", ok=True, to="n2", dt=30, mark="cpr"),
     O("Wait for the paediatric team before starting.", "Every minute of waiting costs survival. Any trained rescuer starts CPR.", crit=True, dt=60),
     O("Give rescue breaths only: his heart may restart once he is oxygenated.", "Without compressions there is no circulation to carry the oxygen. Compressions first.", dt=20),
   ], rhythm="none", hr=None, spo2=None, bp=None, etco2=None, flag="No pulse"),
  "n2": N("<p>Compressions are under way. The pads are on, and during a brief pause for a rhythm check the monitor shows this rhythm.</p>",
          "What is the rhythm, and what do you do?", [
     O("VF: resume compressions while the defibrillator charges to 90 J (2 J/kg), clear everyone, deliver one shock, and restart compressions immediately for 2 minutes.",
       "Shock first at 2 J/kg. Charging during compressions keeps the pre-shock pause short, and compressions restart straight after the shock without a pulse check.", ok=True, to="n3", dt=140, mark="shock1"),
     O("VF: shock at 90 J, then stop to check for a pulse for 10 seconds.",
       "After a shock, resume compressions immediately for 2 minutes. A pulse check straight after the shock wastes perfusion time, and an organised rhythm rarely produces a pulse at once.", dt=30),
     O("Asystole with artefact: continue CPR and give epinephrine.",
       "A chaotic, irregular waveform with no QRS complexes is VF, which is shockable. Missing it delays the one treatment that works.", crit=True, dt=60),
     O("VF: synchronised cardioversion at 90 J.",
       "VF has no QRS complex to synchronise with, so the device may never fire. Pulseless VF and VT need unsynchronised defibrillation.", crit=True, dt=30),
   ], rhythm="vf", hr=None, spo2=None, bp=None, etco2=None, flag="No pulse"),
  "n3": N("<p>After 2 minutes of good-quality CPR, a colleague has placed an IO needle in the proximal tibia. At the rhythm check the monitor still shows VF.</p>",
          "What next?", [
     O("Shock at 180 J (4 J/kg) and resume compressions immediately.", "The second shock is 4 J/kg. Then straight back to compressions.", ok=True, to="n4", dt=15, mark="shock2"),
     O("Shock at 90 J again: the energy only goes up after three failed shocks.",
       "The energy goes up from the second shock: 2 J/kg, then 4 J/kg, then ≥4 J/kg up to 10 J/kg or the adult dose.", dt=15),
     O("Give amiodarone before shocking again.",
       "Shock first. Drugs are given during CPR after the shock, not instead of it, and the antiarrhythmic comes after the third shock.", dt=30),
     O("Stop CPR: VF after 2 minutes means the arrest is unsurvivable.",
       "Shockable arrest has the best prognosis of all paediatric arrests. Nothing here justifies stopping.", crit=True, dt=30),
   ], rhythm="vf", hr=None, spo2=None, bp=None, etco2="18", flag="No pulse"),
  "n4": N("<p>Compressions restarted after the second shock. The IO line is flushed and working.</p>",
          "Which drug now, and what exact dose?", [
     O("Epinephrine 0.45 mg IO (0.01 mg/kg = 4.5 mL of 0.1 mg/mL), then a saline flush; repeat every 3–5 minutes.",
       "In shockable arrest, epinephrine follows the second shock: 0.01 mg/kg of the 0.1 mg/mL solution, every 3–5 minutes.", ok=True, to="n5", dt=105, mark="epi1"),
     O("Epinephrine 4.5 mL of the 1 mg/mL ampoule.",
       "That is 4.5 mg, a tenfold overdose. The IV/IO arrest dose is 0.01 mg/kg of 0.1 mg/mL (0.1 mL/kg). Always say the concentration aloud.", crit=True, dt=30),
     O("Atropine 0.02 mg/kg.", "Atropine has no role in VF. The drug here is epinephrine.", dt=20),
     O("Sodium bicarbonate 1 mEq/kg to correct the acidosis.", "Bicarbonate is not routine in arrest. Good CPR and ventilation treat the acidosis.", dt=20),
   ], rhythm="cpr", hr=None, spo2=None, bp=None, etco2="16", flag="CPR in progress"),
  "n5": N("<p>Two minutes later, at the rhythm check, it is still VF. End-tidal CO₂ during compressions was 16 mmHg.</p>", "What next?", [
     O("Shock at 180 J (≥4 J/kg), resume CPR, and give amiodarone 225 mg IO (5 mg/kg) or lidocaine 45 mg (1 mg/kg).",
       "Shock-refractory VF after the third shock: add an antiarrhythmic, either amiodarone 5 mg/kg (max 300 mg per dose) or lidocaine 1 mg/kg.", ok=True, to="n6", dt=130, mark="anti"),
     O("Shock, then amiodarone 450 mg (10 mg/kg) to be sure.",
       "The bolus is 5 mg/kg (225 mg here), with a maximum of 300 mg per dose. 450 mg is double the dose and above the single-dose limit.", crit=True, dt=130),
     O("Shock, then a second epinephrine dose now.",
       "The first epinephrine was 2 minutes ago, and the interval is 3–5 minutes. The drug for this cycle is the antiarrhythmic.", dt=30),
     O("Switch to synchronised cardioversion: standard shocks are not working.",
       "Pulseless VF is never synchronised. Keep defibrillating, add an antiarrhythmic, and look for a reversible cause.", crit=True, dt=60),
   ], rhythm="vf", hr=None, spo2=None, bp=None, etco2="16", flag="No pulse"),
  "n6": N("<p>At the next rhythm check there is an organised rhythm at 112/min. A moment earlier, end-tidal CO₂ jumped from 16 to 42 mmHg.</p>",
          "What do you do?", [
     O("Check the pulse for no more than 10 seconds. A strong carotid pulse is present, so stop compressions and assess breathing and blood pressure.",
       "An organised rhythm with a sudden rise in EtCO₂ suggests ROSC. Confirm it with a brief pulse check.", ok=True, to="n7", dt=20, mark="rosc"),
     O("Continue compressions for another 2 minutes without checking: ROSC is rarely sustained.",
       "When the rhythm check shows an organised rhythm, check for a pulse (≤10 s). Otherwise you miss the start of post-ROSC care.", dt=30),
     O("Shock again at 180 J.", "Never shock an organised rhythm that may be perfusing. Check for a pulse.", crit=True, dt=20),
   ], rhythm="sinus", hr=112, spo2=None, bp=None, etco2="42", flag="Check pulse"),
  "n7": N("<p>He has a pulse. He is intubated and ventilated, and unresponsive. BP 84/48 mmHg, SpO₂ 100% on FiO₂ 1.0, temperature 37.9 °C.</p>",
          "Which post-ROSC targets do you set?", [
     O("Wean oxygen to SpO₂ 94–99%; aim for a PaCO₂ appropriate to his condition (usually normocapnia); keep systolic and mean BP above the 10th centile (fluid or a vasoactive); prevent fever (≤37.5 °C); get a 12-lead ECG and look for the cause.",
       "These are the 2025 post-ROSC targets. His BP (84/48) is hypotensive for 13 years (systolic below 90) and needs fluid or a vasoactive now, and the ECG may show why he collapsed on exertion.", ok=True, to="end", dt=300),
     O("Keep FiO₂ at 1.0 so that SpO₂ stays at 100%.", "Hyperoxia after arrest is associated with harm. Titrate to 94–99%.", dt=30),
     O("Hyperventilate to a PaCO₂ of 25 mmHg to protect the brain.", "Low CO₂ constricts cerebral vessels. Aim for normocapnia.", dt=30),
     O("Let the temperature run: fever helps fight infection.", "Fever worsens brain injury after arrest. Keep him at ≤37.5 °C, or follow a TTM protocol.", dt=30),
   ], rhythm="sinus", hr=118, spo2=100, bp="84/48", etco2="38", flag="ROSC"),
  "end": E("good", "<p>He is admitted to the PICU. The 12-lead ECG shows a long QT interval: a channelopathy was the likely cause. His family will be offered cardiac screening.</p>",
           rhythm="sinus", hr=104, spo2=97, bp="98/58", etco2="40"),
 },
 "timers": [{"mark": "cpr", "label": "Compressions started", "target": "target ≤ 0:30", "max": 30},
            {"mark": "shock1", "label": "First shock", "target": "as soon as the defibrillator is on (≤ 3:00)", "max": 180}],
 "debrief": ["Gasping with no pulse is cardiac arrest: compressions within seconds.",
             "Shockable arrest: shock first at 2 J/kg, then 4 J/kg. Charge during compressions, and restart CPR immediately after every shock.",
             "Epinephrine after the second shock (0.01 mg/kg of 0.1 mg/mL), then every 3–5 minutes.",
             "Antiarrhythmic after the third shock: amiodarone 5 mg/kg (max 300 mg) or lidocaine 1 mg/kg.",
             "A young person who collapses on exertion needs a 12-lead ECG after ROSC to look for a cardiac cause."],
},

# ---------------------------------------------------------------- 6 · trauma PEA
{
 "id": "p-trauma", "title": "Arrest after trauma", "patient": "7 years · 22 kg · hit by a motorbike · emergency room",
 "part": "E", "units": [15, 16, 17, 19], "minutes": 6, "monitor": ARREST,
 "brief": "A 7-year-old girl hit by a motorbike arrives on a spinal board with a pelvic binder. Your emergency room has a trauma team, but the surgeon is 10 minutes away.",
 "start": "n1",
 "nodes": {
  "n1": N("<p>On arrival she becomes unresponsive, apnoeic and pulseless. The monitor shows a narrow-complex rhythm at 150/min.</p>",
          "What are your first actions?", [
     O("PEA: start CPR with bag-mask oxygen, search aloud for reversible causes and treat them, get IO access, and give epinephrine 0.22 mg IO (0.01 mg/kg) once access is in.",
       "Organised rhythm without a pulse is PEA. In traumatic arrest, finding and treating the reversible causes (hypoxia, tension pneumothorax, haemorrhage, tamponade) comes first: that is what saves her.", ok=True, to="n2", dt=60, mark="cpr", mt=10),
     O("Defibrillate at 44 J (2 J/kg).", "PEA is not shockable.", crit=True, dt=20),
     O("Take her straight to theatre without CPR.", "No circulation means CPR now. Moving an arrested child without CPR guarantees death.", crit=True, dt=60),
     O("Give 60 mL/kg of crystalloid and wait for a pulse.",
       "Volume may be part of the answer, but she needs CPR now, and large volumes of crystalloid worsen traumatic bleeding. Find the cause.", dt=60),
   ], rhythm="pea", hr=150, spo2=None, bp=None, etco2=None, flag="No pulse"),
  "n2": N("<p>During compressions, breath sounds are absent on the right and the right chest is hyper-resonant. Bag ventilation is getting stiffer, and the neck veins are distended.</p>",
          "What is the most likely cause, and what do you do?", [
     O("Tension pneumothorax: immediate needle decompression on the right (site as your trauma protocol specifies), then a chest drain, with CPR continuing.",
       "Tension pneumothorax is diagnosed on clinical signs. Decompress now, without waiting for imaging.", ok=True, to="n3", dt=60, mark="decomp", mt=20),
     O("Get a chest X-ray first to confirm.", "In arrest, tension pneumothorax is treated on clinical signs. An X-ray costs minutes she does not have.", crit=True, dt=240),
     O("Cardiac tamponade: pericardiocentesis.",
       "Tamponade causes muffled heart sounds and distended neck veins, but not a silent, hyper-resonant hemithorax or a stiffening bag.", dt=60),
     O("Increase the ventilation rate to 40/min.",
       "Over-ventilation raises intrathoracic pressure and reduces venous return even further, which is especially dangerous with a tension pneumothorax.", dt=30),
   ], rhythm="cpr", hr=None, spo2=None, bp=None, etco2="10", flag="CPR in progress"),
  "n3": N("<p>Air hisses out on decompression, and within a minute there is a pulse: HR 140/min, BP 72/40 mmHg. Her abdomen is distending and she is pale.</p>",
          "What now?", [
     O("Control the haemorrhage: warmed blood products early, minimal crystalloid, call the surgeon, FAST scan, keep her warm; SpO₂ 94–99% and normal ventilation.",
       "After ROSC in haemorrhagic shock, bleeding is the next killer. Use blood early and get surgical control.", ok=True, to="n4", dt=600, mark="blood", mt=120),
     O("60 mL/kg of crystalloid to bring the BP up to normal.",
       "In haemorrhage, large volumes of crystalloid dilute clotting factors and worsen bleeding. Use blood products early.", dt=300),
     O("She has ROSC: send her for a whole-body CT now.", "An unstable, bleeding child does not go to the CT scanner. Control the bleeding first.", crit=True, dt=300),
   ], rhythm="stach", hr=140, spo2=90, bp="72/40", etco2="30", flag="ROSC"),
  "n4": N("<p>She is going to theatre. Her father is waiting in the corridor, and the police have not been informed.</p>",
          "What must happen before she leaves the resuscitation room?", [
     O("Tell her father, in plain words and with a nurse present, what happened and what comes next; register a medicolegal case and inform the police as your hospital requires; record the times and interventions.",
       "Families should hear early and honestly, even when there is uncertainty. In India a road-traffic injury is a medicolegal case, and times recorded during the event hold up later.", ok=True, to="end", dt=300),
     O("Tell the family nothing until surgery is over.", "Families should be told early and honestly, even while the outcome is uncertain.", dt=60),
     O("Treatment only: the surgeons will do the medicolegal paperwork later.",
       "A road-traffic injury is a medicolegal case. Register it and inform the police as required, and record the times as they happen.", dt=60),
   ], rhythm="stach", hr=128, spo2=97, bp="90/54", etco2="36"),
  "end": E("good", "<p>A splenic laceration is repaired in theatre. She is extubated on day 2 in the PICU, neurologically intact.</p>",
           rhythm="sinus", hr=112, spo2=98, bp="98/60", etco2="38"),
 },
 "timers": [{"mark": "decomp", "label": "Chest decompressed", "target": "on clinical signs, without imaging (≤ 3:00)", "max": 180}],
 "debrief": ["Traumatic arrest: CPR, IO, early epinephrine, and a spoken search for the Hs and Ts.",
             "Tension pneumothorax is a clinical diagnosis: decompress, then place a chest drain.",
             "After ROSC in haemorrhage: blood products early, little crystalloid, surgical control and warmth.",
             "Never send an unstable child to the CT scanner.",
             "In India a road-traffic injury is a medicolegal case: inform the police, record times, and talk to the family early."],
},
]
