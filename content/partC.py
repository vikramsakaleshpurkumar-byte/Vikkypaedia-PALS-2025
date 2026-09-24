from gen import *

part("C", "Before the arrest", "Units 8&ndash;11 · ~5 hours",
     "Every arrest prevented is worth more than one resuscitated. This Part recaps respiratory failure and shock in the language of the arrest team &mdash; the full teaching is in the OxyVent and Approach to the Sick Child modules &mdash; and then covers the two rhythm problems every paediatric team must manage with a pulse: bradycardia and tachycardia.")

# ------------------------------------------------------------------ UNIT 8
unit(8, "C", "Respiratory failure: stopping the slide",
  "Respiratory arrest usually comes before cardiac arrest in children. Recognising failure &mdash; not just distress &mdash; and supporting ventilation early stops the slide.",
  [("e", "Distinguish respiratory distress from respiratory failure."),
   ("e", "Identify upper-airway, lower-airway, lung-tissue and disordered-control problems."),
   ("a", "Start oxygen, bag-mask ventilation and escalation at the right time."),
   ("x", "Recognise the child who needs an advanced airway before arrest.")],
  [
   roles({"ug": "Recognise the signs of respiratory failure: drowsiness, falling effort, cyanosis, bradycardia.",
          "nurse": "Escalate falling consciousness or effort even if SpO₂ looks acceptable on oxygen.",
          "pg": "Classify the problem and decide on bag-mask ventilation, non-invasive support or intubation.",
          "fac": "Link this unit to OxyVent Units 2, 3 and 7 for learners who need depth."}),
   deeper([("oxy", 2, "recognising distress and failure"), ("oxy", 3, "oxygenation is not ventilation"), ("oxy", 8, "high-flow, CPAP and NIV (Units 8–10)")]),
   sec(1, "Distress or failure?", table(
     ["Respiratory distress", "Respiratory failure"],
     [["Fast breathing, recession, flaring, noisy breathing", "Slow or irregular breathing, weak effort, apnoea"],
      ["Alert, anxious", "Drowsy, floppy, unresponsive"],
      ["Tachycardia", "Bradycardia (late, pre-arrest)"],
      ["SpO₂ may be normal or low", "Low SpO₂ despite oxygen; rising CO₂"]]) + danger('''<p>A tired child whose recession is improving and who is getting sleepy may be getting worse, not better. Falling effort with falling consciousness is failure.</p>''')),

   sec(2, "Four types of problem", table(
     ["Type", "Examples", "First action"],
     [["Upper airway obstruction", "Croup, foreign body, anaphylaxis, epiglottitis", "Position of comfort, oxygen, specific treatment; call airway expert"],
      ["Lower airway obstruction", "Asthma, bronchiolitis", "Bronchodilators in asthma; oxygen, support"],
      ["Lung tissue disease", "Pneumonia, ARDS, pulmonary oedema", "Oxygen, CPAP or high-flow, treat cause"],
      ["Disordered control of breathing", "Raised ICP, poisoning, seizures, neuromuscular disease", "Airway, ventilation, treat cause"]])),

   sec(3, "Support before arrest", '''
  <p>Give oxygen, open the airway, and <b>start bag-mask ventilation</b> at 1 breath every 2&ndash;3 seconds when breathing is absent or inadequate. Escalate to CPAP, high-flow or intubation according to the cause and the trajectory (OxyVent Units 8&ndash;11). Anticipate: a child who needs increasing support is heading towards intubation, which is safer done early and prepared than late in a crisis.</p>'''),

   sec(4, "Across settings", tracks(
     ["PICU outreach, capnography, high-flow and NIV on the ward",
      "Planned intubation by an experienced team with a checklist"],
     ["Bag-mask ventilation is the life-saving skill; practise it",
      "Bubble CPAP for pneumonia where trained monitoring exists",
      "Transfer early: a child who needs escalating support should travel before arrest"]), lvl="a"),
  ],
  [Q("A 3-year-old with severe asthma was very distressed an hour ago. She is now quiet, drowsy, with poor air entry and SpO₂ 88% on a mask. Her heart rate has fallen from 170 to 110/min. What does this indicate?",
     ["Improvement: she is calmer and her heart rate is lower.",
      "Respiratory failure with impending arrest; call for help and prepare to assist ventilation.",
      "Sleepiness from salbutamol.",
      "A normal response to oxygen."],
     1,
     "What does a quiet chest with drowsiness mean in severe asthma?",
     "Falling effort, poor air entry, drowsiness and a falling heart rate together point to what?",
     "A quiet chest, drowsiness, hypoxaemia and a falling heart rate indicate <b>respiratory failure and impending arrest</b>. Call for help, give maximal treatment, and prepare to assist ventilation and intubate.",
     "<b>A</b> &mdash; quietness here means exhaustion, not improvement. <b>C</b> &mdash; salbutamol causes tachycardia, not drowsiness with a falling heart rate. <b>D</b> &mdash; SpO₂ 88% on a mask is not a normal response.",
     "A quiet asthmatic who is getting sleepy is dying, not settling.",
     "section 1, ‘Distress or failure?’"),
   Q("A 6-year-old has a head injury. He is unresponsive, with slow irregular breathing at 6/min and SpO₂ 90% on a mask. What type of respiratory problem is this?",
     ["Upper airway obstruction.",
      "Lower airway obstruction.",
      "Lung tissue disease.",
      "Disordered control of breathing."],
     3,
     "Is the problem in the airway, the lungs or the drive to breathe?",
     "Slow, irregular breathing after a brain injury. What has failed?",
     "Slow, irregular breathing after brain injury is <b>disordered control of breathing</b>. He needs airway opening, bag-mask ventilation and neurosurgical care; oxygen alone will not fix hypoventilation.",
     "<b>A</b>, <b>B</b> and <b>C</b> &mdash; the airway and lungs are not the primary problem here; the drive to breathe is.",
     "Name the type: it tells you the treatment.",
     "section 2, ‘Four types of problem’")]
)

# ------------------------------------------------------------------ UNIT 9
unit(9, "C", "Shock: stopping the slide",
  "Shock kills by starving tissues of oxygen. Recognising it while blood pressure is still normal, and treating it by type, prevents the circulatory road to arrest.",
  [("e", "Recognise compensated and hypotensive shock."),
   ("e", "Classify shock: hypovolaemic, distributive (septic), cardiogenic, obstructive."),
   ("a", "Give fluids in a setting-appropriate way and start vasoactive drugs early when needed."),
   ("x", "Recognise cardiogenic and obstructive shock, where fluids can harm.")],
  [
   roles({"ug": "Recognise tachycardia, cool peripheries and slow capillary refill as shock with a normal blood pressure.",
          "nurse": "Reassess after every fluid bolus: heart rate, perfusion, liver size, crackles.",
          "pg": "Match fluids to the setting (SSC 2026) and start a vasoactive infusion when fluid is not enough.",
          "fac": "Link this unit to the Approach to the Sick Child module, Part C, for the full shock teaching."}),
   deeper([("sc", 8, "fluids done right"), ("sc", 9, "sepsis: the first hour (SSC 2026)"), ("sc", 10, "vasoactives and the failing heart")]),
   sec(1, "Compensated or hypotensive", '''
  <p><b>Compensated shock</b>: tachycardia, cool peripheries, prolonged capillary refill, weak peripheral pulses, reduced urine output, with a <b>normal</b> blood pressure. <b>Hypotensive shock</b>: systolic pressure below the age threshold (Unit 2). Hypotension is a late sign in children and signals imminent arrest.</p>'''),

   sec(2, "Four types", table(
     ["Type", "Examples", "Key treatment"],
     [["Hypovolaemic", "Diarrhoea, haemorrhage, burns", "Replace volume; stop bleeding"],
      ["Distributive", "Sepsis, anaphylaxis, spinal injury", "Fluids by setting, antibiotics, epinephrine (anaphylaxis), vasoactives"],
      ["Cardiogenic", "Myocarditis, cardiomyopathy, arrhythmia, congenital heart disease", "Small cautious fluid boluses, inotropes, expert help"],
      ["Obstructive", "Tension pneumothorax, tamponade, duct-dependent lesion, pulmonary embolism", "Relieve the obstruction; prostaglandin for duct-dependent lesions"]])),

   sec(3, "Fluids: setting matters", '''
  <p>The Surviving Sepsis Campaign paediatric guideline (2026) distinguishes settings: <b>with intensive care</b>, give 10&ndash;20 mL/kg crystalloid boluses up to 40&ndash;60 mL/kg in the first hour, reassessing after each; <b>without intensive care</b>, do not give boluses to children with sepsis who are not hypotensive, and give up to 40 mL/kg in 10&ndash;20 mL/kg boluses to those who are. Balanced crystalloid is preferred. Stop fluids at signs of overload: crackles, a growing liver, rising work of breathing.</p>''' + danger('''<p>In cardiogenic shock, a large bolus can tip the child into pulmonary oedema and arrest. Give small volumes (5&ndash;10 mL/kg) slowly, reassess, and get expert help.</p>''')),

   sec(4, "Vasoactives and escalation", '''
  <p>If shock persists after fluids, start epinephrine or norepinephrine through a peripheral line or IO rather than waiting for central access. Treat hypoglycaemia and hypocalcaemia. Obtain expert help early; a child needing escalating vasoactive support is at high risk of arrest.</p>''' + india('''<p>Sepsis, diarrhoea with dehydration and severe anaemia are the commonest roads to circulatory arrest in Indian children. Many district hospitals have no intensive care, which is exactly the setting where the 2026 guideline advises against boluses in non-hypotensive sepsis (the FEAST lesson). See the Approach to the Sick Child module for the full teaching.</p>'''), lvl="a"),
  ],
  [Q("A 4-year-old with fever has a heart rate of 165/min, capillary refill of 4 seconds, cold hands and a blood pressure of 96/60 mmHg. Which statement is correct?",
     ["He is not in shock because the blood pressure is normal.",
      "He has compensated shock; blood pressure is maintained but perfusion is poor.",
      "He has hypotensive shock.",
      "He has cardiogenic shock."],
     1,
     "What is the hypotension threshold at 4 years, and what does poor perfusion with a normal BP mean?",
     "70 + (4 × 2) = 78 mmHg. His BP is above that, but his perfusion is poor.",
     "His systolic pressure (96 mmHg) is above the threshold (78 mmHg), but tachycardia, cold hands and slow capillary refill show poor perfusion: <b>compensated shock</b>.",
     "<b>A</b> &mdash; children maintain blood pressure until late. <b>C</b> &mdash; his pressure is above the hypotension threshold. <b>D</b> &mdash; nothing here points specifically to a cardiac cause.",
     "In children, normal blood pressure does not rule out shock.",
     "section 1, ‘Compensated or hypotensive’"),
   Q("A 7-year-old with a recent viral illness has shock, a gallop rhythm, a large liver and crackles. What is the safest fluid approach?",
     ["20 mL/kg bolus repeated three times rapidly.",
      "Small boluses (5–10 mL/kg) given slowly with reassessment, early inotropes and expert help.",
      "No monitoring is needed.",
      "Oral fluids only."],
     1,
     "Which type of shock is suggested by gallop, hepatomegaly and crackles after a viral illness?",
     "This looks like myocarditis. What do large boluses do to a failing heart?",
     "Gallop, hepatomegaly and crackles after a viral illness suggest <b>cardiogenic shock</b> (myocarditis). Large boluses can cause pulmonary oedema and arrest. Give <b>small, slow boluses</b>, start inotropes early and get expert help.",
     "<b>A</b> &mdash; large rapid boluses can precipitate arrest. <b>C</b> &mdash; close monitoring is essential. <b>D</b> &mdash; oral fluids do not treat shock.",
     "Cardiogenic shock: small volumes, slowly, with help.",
     "section 3, ‘Fluids: setting matters’")]
)

# ------------------------------------------------------------------ UNIT 10
unit(10, "C", "Bradycardia",
  "In children a slow heart rate is usually the result of hypoxia, not a primary heart problem. Oxygenation and ventilation come first; CPR starts at a heart rate below 60 with poor perfusion.",
  [("e", "Recognise bradycardia with cardiopulmonary compromise."),
   ("e", "Support airway, oxygenation and ventilation first."),
   ("a", "Start CPR at a heart rate below 60/min with poor perfusion despite ventilation, and give epinephrine."),
   ("x", "Use atropine and pacing for the specific causes they treat.")],
  [
   roles({"ug": "Recognise bradycardia with poor perfusion and give bag-mask breaths.",
          "nurse": "Attach the monitor and pads, start compressions when told, prepare epinephrine.",
          "pg": "Decide when to start CPR, give epinephrine, and look for causes.",
          "fac": "Assess whether learners ventilate before reaching for drugs."}),
   sec(1, "Think hypoxia first", '''
  <p>Causes of bradycardia: <b>hypoxia</b> (commonest), acidosis, hypothermia, raised intracranial pressure, vagal stimulation (suction, intubation), heart block (congenital, after cardiac surgery), drugs (beta-blockers, calcium-channel blockers, digoxin, opioids, clonidine), hyperkalaemia.</p>'''),

   sec(2, "The bradycardia pathway", fig("brady", "Bradycardia with a pulse and cardiopulmonary compromise", '''  Support ABC: open airway, OXYGEN, VENTILATE with bag-mask if needed
  Attach monitor/defibrillator, IV/IO access, 12-lead ECG if possible
        │
  Heart rate < 60/min with poor perfusion DESPITE oxygenation and ventilation?
        │ YES
  START CPR
        │
  Epinephrine 0.01 mg/kg IV/IO every 3–5 min
  Atropine 0.02 mg/kg (max single dose 0.5 mg) for increased vagal tone
     or primary AV block
  Consider transcutaneous/transvenous pacing; treat causes
  (If pulseless at any point → cardiac arrest pathway)''')),

   sec(3, "Atropine and pacing", '''
  <p><b>Atropine</b> helps bradycardia from vagal stimulation (e.g. during intubation or suctioning) or primary AV block; it does not fix hypoxic bradycardia. <b>Pacing</b> is for complete heart block or sinus node dysfunction unresponsive to oxygenation, ventilation, compressions and drugs &mdash; it is not helpful in bradycardia from hypoxia or asystole.</p>''' + pitfall('''<p>Reaching for atropine in a hypoxic, bradycardic child while the airway is not open. Ventilate first; the heart rate usually recovers.</p>''')),

   sec(4, "Specific causes", '''
  <ul>
    <li><b>Hyperkalaemia:</b> calcium, insulin with glucose, salbutamol, bicarbonate if acidotic, remove potassium.</li>
    <li><b>Beta-blocker or calcium-channel-blocker poisoning:</b> calcium, glucagon, high-dose insulin under toxicology advice.</li>
    <li><b>Raised intracranial pressure:</b> bradycardia with hypertension and irregular breathing (Cushing response) needs neurosurgical treatment.</li>
    <li><b>Post-cardiac surgery heart block:</b> temporary pacing wires.</li>
  </ul>''', lvl="a"),
  ],
  [Q("A 9-month-old with bronchiolitis becomes floppy with a heart rate of 50/min, pale mottled skin and SpO₂ 70%. The team has just started bag-mask ventilation with oxygen. After 30 seconds of effective ventilation the heart rate is still 50/min with poor perfusion. What next?",
     ["Give atropine and continue ventilation only.",
      "Start chest compressions and give epinephrine 0.01 mg/kg IV/IO.",
      "Wait another 5 minutes to see if ventilation works.",
      "Start transcutaneous pacing immediately."],
     1,
     "What is the heart rate threshold for starting CPR with a pulse?",
     "Heart rate below 60 with poor perfusion despite effective ventilation. What does the pathway say?",
     "Heart rate <b>below 60/min with poor perfusion despite oxygenation and ventilation</b> means start <b>CPR</b> and give <b>epinephrine 0.01 mg/kg</b> IV/IO every 3&ndash;5 minutes.",
     "<b>A</b> &mdash; atropine is for vagal or AV block causes, not hypoxic bradycardia. <b>C</b> &mdash; waiting risks arrest. <b>D</b> &mdash; pacing does not help hypoxic bradycardia.",
     "Below 60 with poor perfusion despite breaths: compress.",
     "section 2, ‘The bradycardia pathway’"),
   Q("During suctioning of the endotracheal tube, an intubated 4-year-old's heart rate suddenly falls from 120 to 55/min. Oxygenation is good. What is the most appropriate drug if the bradycardia persists after stopping suction?",
     ["Adenosine.",
      "Atropine 0.02 mg/kg.",
      "Amiodarone.",
      "Sodium bicarbonate."],
     1,
     "Which bradycardias does atropine treat?",
     "Suctioning stimulates the vagus nerve. Oxygenation is fine. Which drug blocks vagal slowing?",
     "Suction-induced bradycardia with good oxygenation is <b>vagal</b>. Stop the stimulus; if it persists with poor perfusion, <b>atropine 0.02 mg/kg</b> (max single dose 0.5 mg) is appropriate.",
     "<b>A</b> &mdash; adenosine slows the heart further. <b>C</b> &mdash; amiodarone is for tachyarrhythmias. <b>D</b> &mdash; bicarbonate is not indicated.",
     "Atropine for vagal and AV-block bradycardia, not for hypoxia.",
     "section 3, ‘Atropine and pacing’")]
)

# ------------------------------------------------------------------ UNIT 11
unit(11, "C", "Tachycardia",
  "A fast heart rate is usually sinus tachycardia from fever, pain, dehydration or shock. The skill is recognising SVT and wide-complex tachycardia, and knowing when the child is unstable.",
  [("e", "Distinguish sinus tachycardia from supraventricular tachycardia (SVT)."),
   ("e", "Use vagal manoeuvres and adenosine for SVT."),
   ("a", "Use synchronised cardioversion for unstable tachycardia."),
   ("x", "Manage wide-complex tachycardia and know the 2025 place of IV sotalol.")],
  [
   roles({"ug": "Read the rhythm strip: rate, P waves, variability, QRS width.",
          "nurse": "Prepare adenosine with a rapid flush (two-syringe technique) and pads for cardioversion.",
          "pg": "Decide stable or unstable, and choose vagal manoeuvres, adenosine or cardioversion.",
          "fac": "Use printed strips: sinus tachycardia, SVT, VT, and ask learners to decide in 10 seconds."}),
   sec(1, "Sinus tachycardia or SVT?", table(
     ["", "Sinus tachycardia", "SVT"],
     [["History", "Fever, pain, dehydration, blood loss", "Sudden onset; vague in infants (poor feeding, irritability)"],
      ["Rate", "Infants usually below 220; children below 180", "Infants usually 220 or more; children 180 or more"],
      ["P waves", "Present, normal", "Absent or abnormal"],
      ["Variability", "Varies with activity and treatment", "Fixed rate"],
      ["Onset/offset", "Gradual", "Abrupt"]])),

   sec(2, "SVT with a pulse", algo("Narrow-complex (SVT) with a pulse", '''  Stable (adequate perfusion):
     Vagal manoeuvres: ice to face (infant); blow through a straw or
     modified Valsalva (older child) — do not press on the eyes
     Adenosine 0.1 mg/kg (max 6 mg) rapid IV push + rapid flush
     Adenosine 0.2 mg/kg (max 12 mg) if no response
  Unstable (hypotension, poor perfusion, altered consciousness):
     Synchronised cardioversion 0.5–1 J/kg; if ineffective, 2 J/kg
     (sedate if possible, without delaying cardioversion)
     Adenosine may be tried first if IV access is immediately available
  Expert consultation for refractory SVT''') + evidence('''<p>2025 AHA/AAP: IV <b>sotalol</b> may be considered for SVT with cardiopulmonary compromise unresponsive to vagal manoeuvres, IV adenosine and synchronised cardioversion when expert consultation is not available.</p>''')),

   sec(3, "Wide-complex tachycardia", '''
  <p>A wide QRS (over 0.09 s) with a pulse is ventricular tachycardia until proved otherwise. <b>Unstable:</b> synchronised cardioversion 0.5&ndash;1 J/kg, then 2 J/kg. <b>Stable:</b> seek expert consultation; adenosine may help if the rhythm is regular and monomorphic (SVT with aberrancy); amiodarone (5 mg/kg over 20&ndash;60 minutes) or procainamide may be used under expert advice, but not both together. <b>Pulseless:</b> this is cardiac arrest &mdash; defibrillate (Unit 14).</p>'''),

   sec(4, "Causes worth looking for", '''
  <p>Electrolyte disturbance (potassium, magnesium, calcium), drug toxicity (tricyclic antidepressants cause wide-complex tachycardia; treat with sodium bicarbonate), myocarditis, congenital heart disease, and channelopathies (long QT, Brugada). A child who presents with SVT needs an ECG after conversion and follow-up for pre-excitation (Wolff&ndash;Parkinson&ndash;White).</p>''' + india('''<p>Adenosine is available in most Indian district hospitals, but many staff are unfamiliar with it; the short half-life means it must be pushed fast into a large, proximal vein with an immediate flush. Keep a laminated SVT card on the crash trolley with doses by weight.</p>'''), lvl="a"),
  ],
  [Q("A 6-week-old is irritable and feeding poorly. The monitor shows a regular narrow-complex tachycardia at 280/min with no visible P waves and no variation. She is alert with capillary refill of 2 seconds. What is the first step?",
     ["Synchronised cardioversion at 2 J/kg.",
      "Vagal manoeuvre (ice to the face), then adenosine 0.1 mg/kg if needed.",
      "Fluid bolus for sinus tachycardia.",
      "Defibrillation at 4 J/kg."],
     1,
     "Is this sinus tachycardia or SVT, and is she stable?",
     "Rate 280, no P waves, fixed rate: SVT. Perfusion is good. Which treatment comes first?",
     "A fixed rate of 280/min without P waves in an infant is <b>SVT</b>. She is <b>stable</b>, so start with a <b>vagal manoeuvre</b> (ice to the face), then <b>adenosine 0.1 mg/kg</b> rapid push if needed.",
     "<b>A</b> &mdash; cardioversion is for unstable SVT. <b>C</b> &mdash; this is not sinus tachycardia. <b>D</b> &mdash; defibrillation is for pulseless VF/VT.",
     "Stable SVT: vagal, then adenosine.",
     "section 2, ‘SVT with a pulse’"),
   Q("A 10-year-old with SVT at 240/min is now drowsy with a systolic blood pressure of 70 mmHg. What is the most appropriate treatment?",
     ["Oral propranolol.",
      "Synchronised cardioversion at 0.5–1 J/kg (adenosine first only if IV access is immediately available).",
      "Unsynchronised defibrillation at 4 J/kg.",
      "Wait for cardiology review tomorrow."],
     1,
     "Is he stable or unstable?",
     "Drowsy and hypotensive: unstable. Which electrical treatment, and at what energy?",
     "Drowsiness and hypotension mean <b>unstable SVT</b>. Give <b>synchronised cardioversion at 0.5&ndash;1 J/kg</b>, increasing to 2 J/kg if needed. Adenosine can be tried first only if IV access is already in place, without delaying cardioversion.",
     "<b>A</b> &mdash; oral drugs are too slow. <b>C</b> &mdash; unsynchronised shocks are for pulseless rhythms. <b>D</b> &mdash; waiting risks arrest.",
     "Unstable tachycardia with a pulse: synchronised cardioversion.",
     "section 2, ‘SVT with a pulse’")]
)
