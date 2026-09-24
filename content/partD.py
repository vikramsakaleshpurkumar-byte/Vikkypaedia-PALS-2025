from gen import *

part("D", "Cardiac arrest", "Units 12&ndash;16 · ~7 hours",
     "The 2025 guidelines sharpened the two arrest pathways: epinephrine as early as possible when the rhythm cannot be shocked, and defibrillation first when it can. This Part covers the rhythms, both pathways, how to tell whether CPR is working, the reversible causes, and the arrests that need something different.")

# ------------------------------------------------------------------ UNIT 12
unit(12, "D", "The rhythms of arrest",
  "Four rhythms, two pathways. The question at every rhythm check is simply: can this be shocked?",
  [("e", "Recognise asystole, PEA, ventricular fibrillation and pulseless ventricular tachycardia."),
   ("e", "Sort each rhythm into the shockable or nonshockable pathway."),
   ("a", "Perform a rhythm check in under 10 seconds."),
   ("x", "Recognise torsades de pointes and its specific treatment.")],
  [
   roles({"ug": "Identify the four arrest rhythms on strips.",
          "nurse": "Call the rhythm at each check and prepare the next action.",
          "pg": "Decide the pathway in under 10 seconds and restart compressions.",
          "fac": "Test rhythm recognition with printed strips before simulation."}),
   sec(1, "Four arrest rhythms", table(
     ["Rhythm", "Looks like", "Pathway"],
     [["<b>Asystole</b>", "Flat line (check leads, gain, pads)", "Nonshockable"],
      ["<b>Pulseless electrical activity (PEA)</b>", "Organised electrical activity, no palpable pulse; often slow and wide", "Nonshockable"],
      ["<b>Ventricular fibrillation (VF)</b>", "Chaotic irregular waves, no QRS complexes", "Shockable"],
      ["<b>Pulseless ventricular tachycardia (pVT)</b>", "Wide, regular complexes, no pulse", "Shockable"]]) + '''
  <p>In children, asystole and PEA are the commonest initial arrest rhythms (usually after hypoxia or shock). VF/pVT is more likely with heart disease, sudden witnessed collapse, some poisonings, and in adolescents.</p>'''),

   sec(2, "The rhythm check", '''
  <p>Every 2 minutes: stop compressions briefly (under 10 seconds), look at the monitor, and decide shockable or not. Check a pulse only if an organised rhythm appears. Then restart compressions immediately &mdash; charging, drug preparation and role swaps happen during compressions, not during the pause.</p>'''),

   sec(3, "Torsades de pointes", '''
  <p>A polymorphic VT that twists around the baseline, associated with long QT (congenital or drug-induced: macrolides, antipsychotics, ondansetron and others, or hypomagnesaemia). Pulseless: defibrillate. Give <b>magnesium sulfate</b> (25&ndash;50 mg/kg, max 2 g) and correct electrolytes.</p>''', lvl="x"),

   sec(4, "Artefacts", '''
  <p>Movement, a loose lead or a low gain can mimic asystole or VF. Before calling asystole, check leads and connections and increase the gain. Fine VF can look like asystole; if uncertain, treat as the pathway that fits the clinical picture and re-check at the next cycle.</p>''', tier="good"),
  ],
  [Q("During CPR, the monitor shows a regular narrow-complex rhythm at 90/min, but no pulse is palpable. What is this rhythm and which pathway applies?",
     ["VF; shockable pathway.",
      "Pulseless VT; shockable pathway.",
      "Sinus rhythm; stop CPR.",
      "Pulseless electrical activity; nonshockable pathway."],
     3,
     "What do you call organised electrical activity without a pulse?",
     "The rhythm looks organised but there is no pulse. Can it be shocked?",
     "Organised electrical activity without a palpable pulse is <b>PEA</b>, a <b>nonshockable</b> rhythm: continue CPR, give epinephrine as soon as possible and look for reversible causes.",
     "<b>A</b> &mdash; VF is chaotic with no organised complexes. <b>B</b> &mdash; pVT is a wide, fast rhythm. <b>C</b> &mdash; no pulse means arrest, whatever the monitor shows.",
     "Rhythm without a pulse is still arrest.",
     "section 1, ‘Four arrest rhythms’"),
   Q("At a rhythm check the monitor shows a flat line. What should be done before calling it asystole?",
     ["Nothing; start epinephrine immediately.",
      "Check leads and connections, and increase the gain, while keeping the pause under 10 seconds.",
      "Defibrillate at 4 J/kg in case it is fine VF.",
      "Stop CPR for 1 minute to watch the monitor."],
     1,
     "What can make a rhythm look falsely flat?",
     "A loose lead or low gain can hide a rhythm. How do you check quickly?",
     "A flat line can be a disconnected lead or low gain. <b>Check the leads and increase the gain</b> quickly, keeping the pause under 10 seconds, then continue the correct pathway.",
     "<b>A</b> &mdash; epinephrine is right for true asystole, but check first. <b>C</b> &mdash; shocking asystole does not help. <b>D</b> &mdash; a 1-minute pause is harmful.",
     "Confirm a flat line is really flat.",
     "section 4, ‘Artefacts’")]
)

# ------------------------------------------------------------------ UNIT 13
unit(13, "D", "Nonshockable arrest: asystole and PEA",
  "Most children arrest in asystole or PEA. High-quality CPR, early epinephrine and a hunt for reversible causes are what the evidence supports.",
  [("e", "Follow the nonshockable pathway."),
   ("e", "Give epinephrine as soon as possible (2025)."),
   ("a", "Search actively for reversible causes during each cycle."),
   ("x", "Explain the evidence behind early epinephrine in nonshockable arrest.")],
  [
   roles({"ug": "Describe the nonshockable pathway and the timing of epinephrine.",
          "nurse": "Draw up epinephrine as soon as the rhythm is called; call the time for repeat doses.",
          "pg": "Get access fast, give epinephrine early, and lead the search for reversible causes.",
          "fac": "Time from arrest recognition to first epinephrine in simulation; aim for as short as possible."}),
   sec(1, "The pathway", algo("Asystole / PEA", '''  CPR: push hard, push fast, full recoil, minimise pauses
  Oxygen, bag-mask; attach monitor/defibrillator
        │
  EPINEPHRINE 0.01 mg/kg IV/IO AS SOON AS POSSIBLE (2025)
        │
  2 minutes CPR · IV/IO access if not done · consider advanced airway
        │
  Rhythm check every 2 minutes
     still nonshockable → epinephrine every 3–5 min; treat reversible causes
     shockable          → shockable pathway (Unit 14)
     organised rhythm   → pulse check; if pulse → post-arrest care (Unit 17)''')),

   sec(2, "Why early epinephrine", evidence('''<p>Observational data from in-hospital paediatric arrests show that longer times to the first epinephrine dose in nonshockable rhythms are associated with lower survival. The 2025 AHA/AAP guidelines therefore recommend giving the initial dose <b>as early as possible</b> (Class 2a), then every 3&ndash;5 minutes (Class 2b).</p>''') + '''
  <p>This makes fast IV or IO access (Unit 7) part of the treatment: an IO needle in the first 2 minutes is the difference between early and late epinephrine.</p>'''),

   sec(3, "Hunt for reversible causes", '''
  <p>During every 2-minute cycle, the leader asks what could have caused this arrest and what can be reversed now (Unit 15): hypoxia, hypovolaemia, hydrogen ion (acidosis), hypo- or hyperkalaemia, hypoglycaemia, hypothermia; tension pneumothorax, tamponade, toxins, thrombosis.</p>''' + pearl('''<p>PEA with a narrow complex and a fast rate often means a mechanical cause: hypovolaemia, tension pneumothorax or tamponade. Look, listen and use ultrasound if you have it.</p>''')),

   sec(4, "Across settings", tracks(
     ["IO access in the first minutes, pre-filled epinephrine syringes, arterial line, point-of-care ultrasound",
      "Recorder with a timer calling each 2-minute cycle"],
     ["IO needle on every trolley; a timer on a phone",
      "Pre-drawn epinephrine by weight band on a chart",
      "A named person to phone the senior doctor and parents"]), lvl="a"),
  ],
  [Q("A 2-year-old is found in asystole on the ward. CPR has started and IO access is in place. When should the first dose of epinephrine be given?",
     ["After 3 cycles of CPR.",
      "As soon as possible.",
      "Only after an advanced airway is placed.",
      "After two shocks."],
     1,
     "What changed in 2025 about epinephrine timing in nonshockable arrest?",
     "Delay to epinephrine is linked to lower survival in asystole and PEA. When should it be given?",
     "In nonshockable arrest, give epinephrine 0.01 mg/kg <b>as soon as possible</b>, then every 3&ndash;5 minutes.",
     "<b>A</b> and <b>C</b> &mdash; delaying epinephrine is associated with lower survival. <b>D</b> &mdash; asystole is not shocked; 'after two shocks' applies to the shockable pathway.",
     "Nonshockable: epinephrine early.",
     "section 2, ‘Why early epinephrine’"),
   Q("A 5-year-old in PEA after a road traffic crash has a narrow-complex rhythm at 140/min, absent breath sounds on the left, and a trachea shifted to the right. What is the most important immediate action besides CPR?",
     ["Give a second dose of epinephrine and wait.",
      "Decompress the left chest for tension pneumothorax.",
      "Defibrillate.",
      "Give calcium."],
     1,
     "Which reversible cause fits unilateral absent breath sounds and tracheal deviation?",
     "A mechanical obstruction to circulation needs a mechanical fix. What is it?",
     "Absent breath sounds on one side with tracheal shift and PEA after trauma suggest <b>tension pneumothorax</b>. Immediate <b>decompression</b> of the left chest (needle or finger thoracostomy by a trained person) is needed.",
     "<b>A</b> &mdash; epinephrine will not relieve the obstruction. <b>C</b> &mdash; PEA is not shocked. <b>D</b> &mdash; calcium is not indicated.",
     "Fast narrow PEA: look for a mechanical cause.",
     "section 3, ‘Hunt for reversible causes’")]
)

# ------------------------------------------------------------------ UNIT 14
unit(14, "D", "Shockable arrest: VF and pulseless VT",
  "In VF and pulseless VT, the single most effective treatment is a shock delivered quickly with minimal interruption to compressions. Drugs come after that.",
  [("e", "Follow the shockable pathway."),
   ("e", "Defibrillate at 2 J/kg, then 4 J/kg."),
   ("a", "Give epinephrine after the second shock (2025), and amiodarone or lidocaine for refractory VF/pVT."),
   ("x", "Recognise causes of shockable arrest in children.")],
  [
   roles({"ug": "Describe the shockable pathway and the energy doses.",
          "nurse": "Place pads, charge during compressions, and call 'stand clear' safely.",
          "pg": "Minimise the pre- and post-shock pause; give drugs at the right time.",
          "fac": "Measure pre-shock and post-shock pauses in simulation; target under 10 seconds total."}),
   sec(1, "The pathway", algo("VF / pulseless VT", '''  CPR, oxygen, attach defibrillator
  SHOCK 2 J/kg (2–4 J/kg)  → CPR 2 min, IV/IO access
  Rhythm check: still shockable?
  SHOCK 4 J/kg             → CPR 2 min
                             EPINEPHRINE 0.01 mg/kg every 3–5 min
                             (after 2 shocks; sooner only if rapid
                              defibrillation is not possible — 2025)
                             consider advanced airway
  Rhythm check: still shockable?
  SHOCK ≥4 J/kg (max 10 J/kg or adult dose) → CPR 2 min
                             AMIODARONE 5 mg/kg or LIDOCAINE 1 mg/kg
                             treat reversible causes''')),

   sec(2, "What changed in 2025", evidence('''<p>Rapid defibrillation is the priority for shockable rhythms. The 2025 AHA/AAP guidelines suggest giving epinephrine <b>after two attempts at defibrillation</b>, or sooner only when rapid defibrillation is not possible (Class 2b). Single shocks rather than stacked shocks are recommended. Amiodarone or lidocaine may be considered for shock-refractory VF/pVT.</p>''')),

   sec(3, "Causes of shockable arrest", '''
  <p>Congenital heart disease (especially after surgery), myocarditis, cardiomyopathy, channelopathies (long QT, Brugada, catecholaminergic polymorphic VT), commotio cordis (blow to the chest), electrocution, drugs (tricyclic antidepressants, stimulants), hyperkalaemia, hypothermia. A shockable rhythm in a child should prompt an ECG, echo and family screening after recovery.</p>'''),

   sec(4, "Across settings", tracks(
     ["Manual defibrillator with paediatric pads on every ward; defibrillation within 2 minutes of IHCA",
      "Amiodarone and lidocaine on the trolley"],
     ["If only an AED is available, use it; paediatric attenuator for children under 8 years",
      "Practise charging during compressions; the pause is where survival is lost",
      "Lidocaine is often more available than amiodarone; know which you stock"]) + india('''<p>Sudden cardiac arrest in Indian schoolchildren and young athletes, often from undiagnosed cardiomyopathy or channelopathy, is increasingly reported. School and sports-ground AED programmes and CPR training are expanding in some states; teachers and coaches are the true first responders.</p>'''), lvl="a"),
  ],
  [Q("A 12-year-old collapses while playing football. An AED shows VF and delivers a shock. After 2 minutes of CPR the rhythm is still VF, and a second shock is given. When is the first dose of epinephrine given?",
     ["Before the first shock.",
      "After the second shock, during the next 2 minutes of CPR.",
      "Only after 5 shocks.",
      "Epinephrine is not used in VF."],
     1,
     "What is the 2025 timing of epinephrine in shockable arrest?",
     "Defibrillation comes first. After how many shocks is epinephrine suggested?",
     "In VF/pVT, <b>defibrillation is the priority</b>; the 2025 guideline suggests epinephrine <b>after two shocks</b> (or sooner only if rapid defibrillation is not possible), then every 3&ndash;5 minutes.",
     "<b>A</b> &mdash; epinephrine before a shock delays the most effective treatment. <b>C</b> &mdash; waiting 5 shocks is too late. <b>D</b> &mdash; epinephrine is used in shockable arrest.",
     "Shockable: shock first, epinephrine after the second shock.",
     "section 2, ‘What changed in 2025’"),
   Q("A 25 kg child remains in VF after three shocks and two doses of epinephrine. Which drug should be considered?",
     ["Adenosine 0.1 mg/kg.",
      "Amiodarone 5 mg/kg (125 mg) or lidocaine 1 mg/kg (25 mg).",
      "Atropine 0.02 mg/kg.",
      "Calcium chloride routinely."],
     1,
     "Which antiarrhythmics are used for shock-refractory VF?",
     "Adenosine is for SVT and atropine for bradycardia. What is 5 mg/kg of amiodarone for 25 kg?",
     "For <b>shock-refractory VF/pVT</b>, give <b>amiodarone 5 mg/kg</b> (125 mg for 25 kg) or <b>lidocaine 1 mg/kg</b> (25 mg), and keep defibrillating and treating causes.",
     "<b>A</b> &mdash; adenosine is for SVT. <b>C</b> &mdash; atropine is for bradycardia. <b>D</b> &mdash; routine calcium has no benefit.",
     "Refractory VF: amiodarone or lidocaine, and keep shocking.",
     "section 1, ‘The pathway’")]
)

# ------------------------------------------------------------------ UNIT 15
unit(15, "D", "Is CPR working? Monitoring and reversible causes",
  "Resuscitation is not a fixed sequence performed blind. Physiological monitoring shows whether compressions are producing blood flow, and the search for a reversible cause is what turns a long arrest into a survivor.",
  [("e", "List the reversible causes of arrest (H's and T's)."),
   ("e", "Use ETCO₂ as a guide to CPR quality."),
   ("a", "Use diastolic blood pressure targets during CPR when an arterial line is in place (2025)."),
   ("x", "Use point-of-care ultrasound without prolonging pauses.")],
  [
   roles({"ug": "List the H's and T's and one clue for each.",
          "nurse": "Report ETCO₂ and arterial pressure trends aloud to the leader.",
          "pg": "Adjust CPR to physiological targets and treat reversible causes.",
          "fac": "Build scenarios where the arrest only responds when the cause is treated."}),
   sec(1, "The H's and T's", table(
     ["H's", "T's"],
     [["Hypoxia", "Tension pneumothorax"],
      ["Hypovolaemia", "Tamponade (cardiac)"],
      ["Hydrogen ion (acidosis)", "Toxins"],
      ["Hypo- or hyperkalaemia", "Thrombosis (pulmonary or coronary)"],
      ["Hypoglycaemia", ""],
      ["Hypothermia", ""]])),

   sec(2, "Physiological targets during CPR", table(
     ["Measure", "Use (2025 AHA/AAP)"],
     [["Diastolic blood pressure (arterial line)", "Target <b>&ge;25 mmHg in infants</b> and <b>&ge;30 mmHg in children &ge;1 year</b>"],
      ["ETCO₂ (advanced airway)", "Indicator of CPR quality; a sudden rise may signal ROSC. <b>Do not use a specific cut-off alone to stop resuscitation</b>"],
      ["CPR feedback devices", "Reasonable to optimise rate and depth"]]) + '''
  <p>If targets are not met: improve compression depth, swap compressors, check for over-ventilation, give epinephrine if due, and look for a reversible cause.</p>'''),

   sec(3, "Ultrasound and other tests", '''
  <p>Point-of-care ultrasound may identify tamponade, tension pneumothorax, hypovolaemia or cardiac activity, but only if it does not prolong pauses &mdash; place the probe during compressions and image during the rhythm check. Blood gas, potassium, glucose and haemoglobin during CPR guide treatment of H causes.</p>''', lvl="a"),

   sec(4, "Extracorporeal CPR", '''
  <p>ECPR (ECMO during CPR) may be considered for in-hospital arrest refractory to conventional CPR in selected children &mdash; typically cardiac patients &mdash; in centres with ECPR protocols and expertise. It is not an option in most hospitals; the decision to call the team must be made early.</p>''', tier="good", lvl="x"),
  ],
  [Q("During CPR on an intubated 6-year-old with an arterial line, the diastolic pressure is 18 mmHg and ETCO₂ is 8 mmHg. What should the team do first?",
     ["Stop resuscitation because ETCO₂ is low.",
      "Improve CPR quality: check depth and recoil, swap compressors, avoid over-ventilation, and consider epinephrine if due.",
      "Increase the ventilation rate to 40/min.",
      "Give sodium bicarbonate routinely."],
     1,
     "What diastolic pressure target applies to children over 1 year during CPR?",
     "The target is at least 30 mmHg. ETCO₂ is also low. What does that suggest about compressions?",
     "A diastolic pressure below 30 mmHg and low ETCO₂ suggest <b>poor CPR quality</b>. Improve depth and recoil, swap compressors, avoid over-ventilation, give epinephrine if due, and look for reversible causes.",
     "<b>A</b> &mdash; a specific ETCO₂ value should not be used alone to stop. <b>C</b> &mdash; over-ventilation reduces venous return. <b>D</b> &mdash; routine bicarbonate has no benefit.",
     "Use the numbers to fix the CPR, not to give up.",
     "section 2, ‘Physiological targets during CPR’"),
   Q("A 16-month-old arrests after 3 days of vomiting and diarrhoea. The blood gas during CPR shows potassium 7.8 mmol/L. Which reversible cause is present, and what treatment is indicated?",
     ["Hypokalaemia; give potassium.",
      "Hyperkalaemia; give calcium, and consider sodium bicarbonate and insulin with glucose.",
      "Hypothermia; warm the child only.",
      "Tamponade; perform pericardiocentesis."],
     1,
     "Which H is shown by the potassium result?",
     "Potassium of 7.8 mmol/L is dangerously high. Which drugs stabilise the heart and shift potassium into cells?",
     "Potassium 7.8 mmol/L is <b>hyperkalaemia</b> (for example from acute kidney injury). Give <b>calcium</b> to stabilise the myocardium, and consider sodium bicarbonate and insulin with glucose to shift potassium, while continuing CPR.",
     "<b>A</b> &mdash; potassium is high, not low. <b>C</b> &mdash; nothing suggests hypothermia. <b>D</b> &mdash; nothing suggests tamponade.",
     "Check potassium in any arrest after dehydration or kidney injury.",
     "section 1, ‘The H's and T's’")]
)

# ------------------------------------------------------------------ UNIT 16
unit(16, "D", "Special circumstances",
  "Some arrests need a specific extra step: naloxone for opioids, rewarming for hypothermia, relief of obstruction in trauma, prostaglandin for a duct-dependent baby. Knowing these turns standard CPR into targeted resuscitation.",
  [("e", "Give naloxone for suspected opioid overdose with respiratory depression."),
   ("e", "Manage drowning with early ventilation."),
   ("a", "Adapt resuscitation for trauma, anaphylaxis and poisoning."),
   ("x", "Recognise special considerations in single-ventricle physiology, pulmonary hypertension and myocarditis.")],
  [
   roles({"ug": "Know the special circumstances and the one extra step each needs.",
          "nurse": "Prepare naloxone, adrenaline for anaphylaxis, and warming equipment.",
          "pg": "Adapt the pathway to the cause, and call specialists early.",
          "fac": "Run one special-circumstance scenario in every simulation cycle."}),
   sec(1, "Common special circumstances", table(
     ["Situation", "Extra step"],
     [["<b>Opioid overdose</b>", "Ventilate first; naloxone if respiratory arrest with a pulse; standard CPR if no pulse"],
      ["<b>Drowning</b>", "Start with breaths (hypoxic arrest); cervical spine precautions only if injury is likely"],
      ["<b>Anaphylaxis</b>", "IM epinephrine 0.01 mg/kg (max 0.5 mg) early; IV epinephrine in arrest; large fluid volumes"],
      ["<b>Trauma</b>", "Treat reversible causes: haemorrhage control, volume, relieve tension pneumothorax, tamponade"],
      ["<b>Hypothermia</b>", "Rewarm; prolonged CPR may be successful; drugs and shocks per protocol for temperature"],
      ["<b>Poisoning</b>", "Specific antidotes: bicarbonate for tricyclics and sodium-channel blockers, calcium and insulin for calcium-channel blockers, lipid emulsion for local anaesthetic toxicity; call poison centre"]])),

   sec(2, "Congenital heart disease", '''
  <ul>
    <li><b>Single-ventricle physiology</b> (after Norwood, Glenn or Fontan operations): balance of pulmonary and systemic flow is fragile; involve cardiology early; ECPR may be considered in cardiac centres.</li>
    <li><b>Duct-dependent lesions</b> in newborns: shock or cyanosis in the first weeks as the duct closes; <b>prostaglandin E1</b> reopens it.</li>
    <li><b>Pulmonary hypertension:</b> avoid hypoxia, acidosis and hypercapnia; inhaled nitric oxide and careful sedation; arrest risk during intubation.</li>
  </ul>'''),

   sec(3, "Myocarditis and cardiomyopathy", '''
  <p>These children have a high risk of arrhythmia and arrest, especially at induction of anaesthesia. Recognise early (tachycardia out of proportion to fever, gallop, hepatomegaly, poor perfusion), avoid large fluid boluses, and transfer early to a centre with mechanical circulatory support.</p>'''),

   sec(4, "Across settings", tracks(
     ["Poison centre, ECMO/ECPR programme, cardiac intensive care",
      "Lipid emulsion and specific antidotes stocked"],
     ["Naloxone, IM epinephrine and calcium on every trolley",
      "Drowning and snakebite (neurotoxic, with respiratory arrest) need ventilation above all",
      "Phone a poison information centre (e.g. AIIMS New Delhi National Poisons Information Centre) early"]) + india('''<p>In India, drowning, snakebite with respiratory paralysis, organophosphate poisoning and kerosene aspiration are important special circumstances. For neurotoxic snakebite, prolonged bag-mask ventilation can keep a child alive until anti-snake venom works; for organophosphates, atropine is titrated to a dry chest (see the Approach to the Sick Child module).</p>'''), lvl="a"),
  ],
  [Q("A 14-year-old is found unresponsive with pinpoint pupils and breathing at 4/min. He has a pulse. What should be done first?",
     ["Start chest compressions.",
      "Open the airway and ventilate with a bag-mask, and give naloxone.",
      "Defibrillate.",
      "Give flumazenil."],
     1,
     "What does respiratory depression with pinpoint pupils suggest?",
     "He has a pulse but is barely breathing. What restores oxygenation, and which antidote reverses opioids?",
     "Pinpoint pupils with respiratory depression suggest <b>opioid toxicity</b>. With a pulse present, <b>ventilate</b> and give <b>naloxone</b>. If there is no pulse, start standard CPR.",
     "<b>A</b> &mdash; he has a pulse; compressions are not indicated. <b>C</b> &mdash; there is no shockable arrest. <b>D</b> &mdash; flumazenil is for benzodiazepines and can precipitate seizures.",
     "Opioid with a pulse: breathe for them and give naloxone.",
     "section 1, ‘Common special circumstances’"),
   Q("A 3-week-old presents grey, with poor pulses and a large liver. He was well at birth. Which treatment should be considered urgently alongside resuscitation?",
     ["Adenosine.",
      "Prostaglandin E1 infusion for a possible duct-dependent heart lesion.",
      "Amiodarone.",
      "Sodium bicarbonate only."],
     1,
     "Which newborns deteriorate in the first weeks as the ductus arteriosus closes?",
     "A previously well baby in shock at 3 weeks with a large liver may have a duct-dependent lesion. What keeps the duct open?",
     "Shock in the first weeks of life in a previously well baby can be a <b>duct-dependent congenital heart lesion</b> (e.g. coarctation, hypoplastic left heart). <b>Prostaglandin E1</b> reopens the duct; be ready to ventilate, as it can cause apnoea.",
     "<b>A</b> &mdash; adenosine is for SVT. <b>C</b> &mdash; amiodarone is for arrhythmias. <b>D</b> &mdash; bicarbonate does not treat the cause.",
     "Shock in the first month: think duct.",
     "section 2, ‘Congenital heart disease’")]
)
