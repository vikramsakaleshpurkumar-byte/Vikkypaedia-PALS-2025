from gen import *

part("E", "After the arrest, and systems", "Units 17&ndash;20 · ~5 hours",
     "Return of circulation is the start of the most dangerous hours, not the end. The 2025 guidelines added new targets for blood pressure and temperature, first-ever advice on predicting neurological outcome, and a new focus on what happens to survivors after they leave hospital. This Part closes with families, stopping, systems in India, and one child followed from arrest to recovery.")

# ------------------------------------------------------------------ UNIT 17
unit(17, "E", "Post-cardiac arrest care",
  "After return of spontaneous circulation (ROSC), the brain and heart are at their most vulnerable. Avoiding fever, hypotension, hypoxia and hyperoxia, and treating seizures, protects them.",
  [("e", "Recognise ROSC and start post-arrest care."),
   ("e", "Keep central temperature at or below 37.5 °C."),
   ("a", "Maintain blood pressure above the 10th centile for age and SpO₂ 94–99%."),
   ("x", "Plan targeted temperature management, ventilation and seizure monitoring.")],
  [
   roles({"ug": "List the post-arrest targets: temperature, blood pressure, oxygen, CO₂, glucose.",
          "nurse": "Monitor temperature continuously, blood pressure closely, and report seizures.",
          "pg": "Set and adjust targets; arrange transfer to intensive care.",
          "fac": "Teach the first hour after ROSC as its own scenario, not an afterthought."}),
   sec(1, "Targets after ROSC", table(
     ["Target", "2025 AHA/AAP recommendation"],
     [["Temperature", "Continuous central monitoring; <b>avoid central temperature above 37.5 °C</b>"],
      ["Temperature management", "For ages 24 hours to 18 years who remain comatose: 5 days of targeted temperature management, either 32&ndash;34 °C then 36&ndash;37.5 °C, or 36&ndash;37.5 °C throughout"],
      ["Blood pressure", "<b>Systolic and mean arterial pressure above the 10th percentile for age</b> (and sex); continuous arterial monitoring"],
      ["Oxygen", "Normoxaemia: wean oxygen to <b>SpO₂ 94&ndash;99%</b>"],
      ["Carbon dioxide", "PaCO₂ appropriate to the child's condition; avoid hypocapnia and hypercapnia"],
      ["Seizures", "Continuous EEG in persistent encephalopathy where available; treat clinical seizures"]])),

   sec(2, "The first hour after ROSC", algo("Post-ROSC checklist", '''  A/B  secure airway; confirm tube; SpO₂ 94–99%; normal PaCO₂; chest X-ray
  C    BP > 10th centile; fluids or inotropes; 12-lead ECG; echo
  D    glucose; pupils; seizures; sedation and analgesia
  E    central temperature ≤ 37.5 °C; treat fever actively
       blood gas, lactate, electrolytes, calcium, haemoglobin
       find and treat the CAUSE of the arrest
       transfer to PICU with a trained team''')),

   sec(3, "Fever is the enemy", evidence('''<p>Fever after cardiac arrest is associated with worse neurological outcome. The THAPCA trials compared hypothermia (32&ndash;34 °C) with normothermia (36&ndash;37.5 °C); neither showed a clear benefit in the original analyses, and a later Bayesian reanalysis suggested a modest benefit from hypothermia. Both strategies are acceptable; what matters most is <b>avoiding fever</b>.</p>''')),

   sec(4, "Across settings", tracks(
     ["PICU, arterial line, continuous EEG, servo-controlled cooling",
      "Transfer team with ventilator and infusion pumps"],
     ["Paracetamol, exposure and cool sponging to keep temperature ≤37.5 °C",
      "Manual blood pressure every 5–15 minutes; epinephrine or dopamine infusion if hypotensive",
      "Transfer with oxygen, bag and mask, and a trained escort (see OxyVent Unit 19)"]) + india('''<p>Most Indian district hospitals have no PICU. Post-ROSC care there means keeping the child alive for transfer: secure airway, oxygen to target, blood pressure support, glucose, temperature control, and a structured phone handover to the receiving team.</p>'''), lvl="a"),
  ],
  [Q("A 4-year-old has ROSC after a 12-minute arrest. One hour later his temperature is 38.4 °C. What is the priority?",
     ["No action; fever is expected after arrest.",
      "Treat the fever actively to keep central temperature at or below 37.5 °C.",
      "Warm him to 39 °C to support circulation.",
      "Give antibiotics only."],
     1,
     "What temperature does the 2025 guideline advise avoiding after arrest?",
     "Fever after arrest worsens neurological outcome. What target should be kept?",
     "The 2025 guideline recommends <b>avoiding central temperatures above 37.5 °C</b> after arrest. Treat fever actively with antipyretics and cooling, and monitor temperature continuously.",
     "<b>A</b> &mdash; fever worsens brain injury. <b>C</b> &mdash; warming to 39 °C is harmful. <b>D</b> &mdash; antibiotics may be needed for the cause but do not control the temperature.",
     "After arrest, fever is the enemy.",
     "section 3, ‘Fever is the enemy’"),
   Q("After ROSC, a ventilated 2-year-old has SpO₂ 100% on FiO₂ 1.0 and a blood pressure below the 5th centile for age. What should be done?",
     ["Keep FiO₂ 1.0 and accept the blood pressure.",
      "Wean oxygen to SpO₂ 94–99% and support blood pressure above the 10th centile with fluids or inotropes.",
      "Increase the ventilation rate to lower CO₂ as far as possible.",
      "Stop monitoring and transfer."],
     1,
     "What are the post-arrest oxygen and blood pressure targets?",
     "SpO₂ 100% on full oxygen may mean hyperoxia; the BP is below target. What should change?",
     "After ROSC, wean oxygen to <b>SpO₂ 94&ndash;99%</b> to avoid hyperoxia, and keep systolic and mean pressures <b>above the 10th centile</b> for age with fluids or inotropes.",
     "<b>A</b> &mdash; hyperoxia and hypotension both harm. <b>C</b> &mdash; hypocapnia reduces brain blood flow. <b>D</b> &mdash; monitoring must continue during transfer.",
     "After ROSC: normal oxygen, normal CO₂, no fever, good blood pressure.",
     "section 1, ‘Targets after ROSC’")]
)

# ------------------------------------------------------------------ UNIT 18
unit(18, "E", "Predicting outcome and life after arrest",
  "Families ask two questions after an arrest: will my child wake up, and what will life be like? The 2025 guidelines give the first evidence-based advice on the first, and a new emphasis on the second.",
  [("e", "Explain why no single test predicts outcome after paediatric arrest."),
   ("e", "Know the multimodal approach to neuroprognostication (2025)."),
   ("a", "Describe the ongoing needs of survivors."),
   ("x", "Communicate uncertainty to families honestly and repeatedly.")],
  [
   roles({"ug": "Explain why prognosis is not decided in the first hours.",
          "nurse": "Support families and record neurological signs accurately over time.",
          "pg": "Use multiple modalities at the right times; avoid early withdrawal based on one test.",
          "fac": "Practise a family meeting about uncertain prognosis with an actor."}),
   sec(1, "Multimodal, over time", table(
     ["Modality", "2025 AHA/AAP guidance (examples)"],
     [["Pupillary reflexes", "Bilateral reactive pupils in the first 12 hours may support a favourable outcome; absence at 48&ndash;72 hours may support an unfavourable one"],
      ["Lactate", "Plasma lactate below 2 mmol/L in the first 12 hours may support a favourable outcome"],
      ["EEG", "Within 72 hours: a continuous, reactive background with sleep spindles supports favourable; burst suppression or status epilepticus supports unfavourable"],
      ["Imaging and biomarkers", "MRI and serum markers add information; none is decisive alone"]]) + danger('''<p>Do not rely on a single finding, or on findings in the first hours while the child is sedated, cooled or unstable. Multiple modalities over several days are needed.</p>''')),

   sec(2, "Life after arrest", '''
  <p>Survivors often have physical, cognitive, emotional and behavioural difficulties that appear weeks to months later: attention, memory, learning, mood, fatigue. The 2025 guidelines recommend <b>evaluation for rehabilitation needs</b> before discharge and follow-up afterwards, and support for families, who often have post-traumatic stress symptoms themselves.</p>'''),

   sec(3, "Talking to families", '''
  <p>Meet early and often. Say what is known, what is not, and when you expect to know more. Avoid false reassurance and premature pessimism. Use plain language and check understanding. Involve the family in decisions and support their presence at the bedside.</p>''' + pearl('''<p>&ldquo;It is too early to know how much his brain has been affected. Over the next three days we will look at his pupils, his brain waves and a scan. We will meet you each afternoon and tell you what we have learnt.&rdquo;</p>''')),

   sec(4, "Across settings", '''
  <p>Where EEG and MRI are unavailable, repeated clinical examination off sedation over several days, and transfer for specialist assessment when appropriate, are the tools. Follow-up and rehabilitation (physiotherapy, developmental assessment, school support) matter as much as the acute care.</p>''', lvl="a"),
  ],
  [Q("Six hours after ROSC, a sedated, cooled child has sluggish pupils. The family asks whether he will recover. What is the most accurate answer?",
     ["He will certainly have severe brain damage.",
      "It is too early to know; prognosis needs several tests over the next few days, and we will keep you updated.",
      "He will certainly recover fully.",
      "We should withdraw treatment now."],
     1,
     "Can a single finding in the first hours, under sedation and cooling, predict outcome?",
     "The 2025 guidance says prognosis needs multiple modalities over time. What should the family be told?",
     "Neuroprognostication after paediatric arrest needs <b>multiple modalities at several time points</b>. At 6 hours, under sedation and cooling, it is <b>too early to know</b>. Explain the plan and meet again.",
     "<b>A</b> and <b>C</b> &mdash; neither certainty is justified. <b>D</b> &mdash; decisions based on one early finding are unsafe.",
     "Early certainty after arrest is usually wrong.",
     "section 1, ‘Multimodal, over time’"),
   Q("A 9-year-old survived an arrest 3 months ago and appears physically well. His mother reports poor concentration and falling grades. What does this reflect?",
     ["Nothing related to the arrest.",
      "A recognised cognitive effect in arrest survivors, which needs assessment and support.",
      "A behaviour problem needing punishment.",
      "A reason to repeat the resuscitation training."],
     1,
     "What long-term problems do arrest survivors often have?",
     "Attention and learning difficulties can appear months later. What does the 2025 guidance recommend?",
     "Cardiac arrest survivors often have <b>cognitive and behavioural difficulties</b> that appear later. The 2025 guidelines recommend <b>assessment for rehabilitation needs</b> and ongoing support, including school support.",
     "<b>A</b> &mdash; these are recognised effects of hypoxic injury. <b>C</b> &mdash; punishment is inappropriate. <b>D</b> &mdash; unrelated.",
     "Survival is not the end of care.",
     "section 2, ‘Life after arrest’")]
)

# ------------------------------------------------------------------ UNIT 19
unit(19, "E", "Families, stopping, and systems",
  "Resuscitation involves decisions that are not in any algorithm: whether parents stay in the room, when to stop, how to tell a family, and how a hospital makes sure the next arrest goes better than the last.",
  [("e", "Support family presence during resuscitation."),
   ("e", "Describe how the decision to stop resuscitation is made."),
   ("a", "Break bad news with a structured approach."),
   ("x", "Build and audit a resuscitation system in an Indian hospital.")],
  [
   roles({"ug": "Know how to support a parent in the room during resuscitation.",
          "nurse": "Act as family support person; explain what is happening in simple words.",
          "pg": "Make and communicate the decision to stop; lead the conversation with the family.",
          "fac": "Audit every arrest in your hospital: time to CPR, time to first epinephrine, time to shock, debrief held."}),
   sec(1, "Family presence", '''
  <p>Most parents want to be present, and presence does not disrupt resuscitation when a staff member is assigned to support them. Offer the choice, explain what they will see, and have someone stay with them.</p>'''),

   sec(2, "When to stop", '''
  <p>There is no single rule. The decision considers the duration of arrest, the cause, the response to treatment, reversible causes still untreated, and the family's understanding. Specific ETCO₂ values should not be used alone to stop. Prolonged resuscitation may be appropriate in hypothermia, drowning in cold water, poisoning and where ECPR is possible. The team leader makes the decision after asking the team: &ldquo;Does anyone have a reason to continue?&rdquo;</p>'''),

   sec(3, "Breaking bad news", algo("A structured approach (SPIKES)", '''  Setting      private room, sit down, phone off, key people present
  Perception   "What have you understood so far?"
  Invitation   "Would you like me to explain what happened?"
  Knowledge    warning shot, then clear words: "Your son has died."
  Emotions     silence; acknowledge; stay
  Strategy     next steps: seeing the child, religious needs, formalities''') + india('''<p>Use the family's language, and use the word &ldquo;died&rdquo; rather than euphemisms. Allow religious and cultural practices. In India, medicolegal cases (trauma, poisoning, unexplained death) require police intimation and may require post-mortem; explain this gently and clearly.</p>''')),

   sec(4, "Building the system", '''
  <ul>
    <li><b>Equipment:</b> a standardised paediatric crash trolley, checked every shift; weight-based drug charts; IO needles; defibrillator with paediatric pads.</li>
    <li><b>People:</b> regular training and in-situ simulation for the teams who actually respond at night.</li>
    <li><b>Process:</b> an early warning system, a clear call number, debriefing after every arrest.</li>
    <li><b>Data:</b> a simple register: time to CPR, first epinephrine, first shock, ROSC, survival, debrief held.</li>
  </ul>''' + tracks(
     ["Resuscitation committee, registry participation, quarterly in-situ simulation",
      "Dedicated paediatric resuscitation team"],
     ["A one-page arrest record and a monthly review meeting",
      "Night-shift drills with the actual staff on duty",
      "Link with the district emergency response (108/102) for transfers"]), lvl="a"),
  ],
  [Q("A mother asks to stay in the resuscitation room while her child receives CPR. What is the best response?",
     ["Refuse, as parents always disrupt resuscitation.",
      "Offer her the choice to stay, with a staff member assigned to support and explain.",
      "Let her stay without support.",
      "Ask her to wait until the child is stable."],
     1,
     "What does the evidence say about family presence?",
     "Presence is valued by families and does not disrupt care when someone supports them. What makes it safe?",
     "Most families want the option to be present, and presence does not disrupt resuscitation when a <b>staff member is assigned to support</b> them. Offer the choice.",
     "<b>A</b> &mdash; refusal is not evidence-based. <b>C</b> &mdash; unsupported presence is distressing and can disrupt care. <b>D</b> &mdash; she may lose the chance to be present if the child dies.",
     "Offer presence, with support.",
     "section 1, ‘Family presence’"),
   Q("After 40 minutes of resuscitation for asystole with no reversible cause found, ETCO₂ has been 8 mmHg throughout. How should the decision to stop be made?",
     ["Stop automatically because ETCO₂ is below 10 mmHg.",
      "The leader weighs duration, cause, response and remaining reversible causes, asks the team for any reason to continue, and then decides.",
      "Continue indefinitely.",
      "Let the most junior member decide."],
     1,
     "Can a single ETCO₂ value be used alone to stop resuscitation?",
     "The 2025 guidance advises against using ETCO₂ alone. What factors does the leader consider?",
     "Termination is a clinical decision that considers <b>duration, cause, response and reversible causes</b>. A specific ETCO₂ value should not be used alone. The leader checks with the team before deciding.",
     "<b>A</b> &mdash; ETCO₂ alone should not guide termination. <b>C</b> &mdash; futile resuscitation is not in the child's interest. <b>D</b> &mdash; the leader is responsible.",
     "Stopping is a team decision led by the leader, not a number.",
     "section 2, ‘When to stop’")]
)

# ------------------------------------------------------------------ UNIT 20
unit(20, "E", "Capstone: follow the child",
  "One fictional child, Kabir, from the first warning sign on the ward to his first day back at school. At each stage, name the problem, the action and the next check. Then look at where the field is going.",
  [("e", "Apply recognition, BLS and the arrest pathways to an evolving case."),
   ("e", "Give drugs and shocks at the right time and dose."),
   ("a", "Deliver post-arrest care to 2025 targets."),
   ("x", "Discuss current developments in paediatric resuscitation.")],
  [
   roles({"ug": "At each stage, say what you would see, do and report.",
          "nurse": "At each stage, say which role you would take and what you would prepare.",
          "pg": "Lead the decisions: pathway, drugs, shocks, targets and family communication.",
          "fac": "Run the capstone as a table-top simulation and debrief on time to CPR, epinephrine and shock."}),
   sec(1, "Stage 1: the warning", '''
  <p><b>Kabir, 3 years, 14 kg</b>, admitted with pneumonia. At 2 a.m. his breathing rate is 60/min, SpO₂ 86% on 2 L/min, heart rate 180/min, and he is drowsy. <b>Problem:</b> respiratory failure (Unit 8). <b>Action:</b> call for help, increase oxygen, open the airway, prepare bag-mask ventilation, call the senior and PICU. <b>Next check:</b> 5 minutes.</p>'''),

   sec(2, "Stage 2: the arrest", fig("arrest", "Paediatric cardiac arrest: the two pathways", '''  Unresponsive, no normal breathing, no pulse → CPR (15:2), oxygen, monitor
  Rhythm check: shockable?
  NO  (asystole/PEA): epinephrine 0.01 mg/kg ASAP, then every 3–5 min;
                      CPR 2 min; reversible causes; recheck
  YES (VF/pVT):       shock 2 J/kg → CPR 2 min → shock 4 J/kg → CPR 2 min
                      + epinephrine after 2nd shock; amiodarone or lidocaine
                      if refractory; reversible causes; recheck
  ROSC → post-arrest care: temperature ≤37.5 °C, BP >10th centile, SpO₂ 94–99%''') + '''
  <p>Kabir becomes unresponsive; heart rate 40/min, then no pulse. The monitor shows <b>PEA</b>. <b>Action:</b> start CPR 15:2, IO access, <b>epinephrine 0.14 mg (1.4 mL of 0.1 mg/mL) as soon as possible</b>, ventilate with oxygen, look for causes: hypoxia is the likeliest (Units 12&ndash;13, 15).</p>'''),

   sec(3, "Stage 3: ROSC", '''
  <p>After 6 minutes and two doses of epinephrine, a pulse returns. <b>Action:</b> secure the airway, SpO₂ 94&ndash;99%, normal CO₂, blood pressure above the 10th centile, glucose, temperature at or below 37.5 °C, and transfer to PICU (Unit 17). Tell his parents what has happened, and that it is too early to know how his brain has been affected (Unit 18).</p>'''),

   sec(4, "Stage 4: afterwards", '''
  <p>Kabir wakes on day 3 and goes home on day 12. At 3 months his mother notices he tires easily and has trouble concentrating. He is referred for developmental assessment and school support. The team debriefs: the early warning score was high at midnight; the call came at 2 a.m. The fix: a clear escalation rule and a night-time drill.</p>'''),

   sec(5, "Future directions", '''
  <ul>
    <li><b>Physiology-directed CPR:</b> diastolic pressure and ETCO₂ targets entered the 2025 guidelines; trials are testing whether titrating CPR to them improves survival.</li>
    <li><b>Early epinephrine and drug timing:</b> randomised data in children are still scarce; most recommendations remain based on observational studies.</li>
    <li><b>ECPR and post-arrest bundles:</b> expanding in cardiac centres; access in low- and middle-income countries is limited.</li>
    <li><b>Survivorship:</b> long-term follow-up of child survivors is now part of the Chain of Survival, and core outcome sets are being developed.</li>
    <li><b>Community CPR:</b> school CPR training and public-access AEDs are growing in India, where most out-of-hospital arrests still receive no bystander CPR.</li>
  </ul>''', tier="nice"),
  ],
  [Q("Kabir (14 kg) is in PEA. IO access is in place. What is the correct first drug action?",
     ["Wait 10 minutes, then give epinephrine 1.4 mg.",
      "Give epinephrine 0.14 mg (1.4 mL of 0.1 mg/mL) as soon as possible.",
      "Give amiodarone 70 mg.",
      "Give atropine 0.28 mg."],
     1,
     "What is the dose, and what is the 2025 timing in nonshockable arrest?",
     "0.01 mg/kg for 14 kg, given early. Which syringe?",
     "In PEA, give <b>epinephrine 0.01 mg/kg = 0.14 mg</b> (1.4 mL of 0.1 mg/mL) <b>as soon as possible</b>, then every 3&ndash;5 minutes.",
     "<b>A</b> &mdash; delayed and a 10-fold overdose. <b>C</b> &mdash; amiodarone is for shock-refractory VF/pVT. <b>D</b> &mdash; atropine is not used in arrest.",
     "PEA: epinephrine early, 0.1 mL/kg of 0.1 mg/mL.",
     "section 2, ‘Stage 2: the arrest’"),
   Q("After ROSC, Kabir's team debriefs. The early warning score was high at midnight, but the doctor was called at 2 a.m. What is the most useful system change?",
     ["Buy a new defibrillator.",
      "A clear escalation rule tied to the early warning score, with a night-time drill for the staff on duty.",
      "Blame the nurse on duty.",
      "No change; the outcome was good."],
     1,
     "What was the delay, and what prevents it next time?",
     "The warning was there two hours before the arrest. What turns a score into action?",
     "The delay was between the warning and the call. A <b>clear escalation rule</b> linked to the score, practised in <b>drills with the night staff</b>, addresses the system problem.",
     "<b>A</b> &mdash; the defibrillator was not the problem. <b>C</b> &mdash; blame does not fix systems. <b>D</b> &mdash; good outcomes can hide near misses.",
     "Debrief the system, not just the individual.",
     "section 4, ‘Stage 4: afterwards’")]
)
