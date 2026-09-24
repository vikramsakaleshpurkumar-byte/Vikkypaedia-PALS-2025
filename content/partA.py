from gen import *

part("A", "Foundations", "Units 1&ndash;3 · ~4 hours",
     "Most children who arrest do not have a heart problem. They run out of oxygen or circulation first, and the arrest is the end of a slope that could often have been seen. This Part sets out why children arrest, how to look at a sick child in the same order every time, and how a team works so that everyone does the right thing at once.")

# ------------------------------------------------------------------ UNIT 1
unit(1, "A", "Why children arrest",
  "Adults usually arrest from a primary heart rhythm problem. Children usually arrest because breathing or circulation failed first. That difference decides what the team does before, during and after the arrest.",
  [("e", "Describe the respiratory and circulatory pathways to paediatric cardiac arrest."),
   ("e", "Explain why early recognition prevents more deaths than resuscitation does."),
   ("a", "Describe the 2025 unified Chain of Survival for in-hospital and out-of-hospital arrest."),
   ("x", "Compare in-hospital and out-of-hospital arrest outcomes and what drives them.")],
  [
   roles({"ug": "Explain why a child with worsening breathing is heading towards arrest.",
          "nurse": "Recognise and escalate the deteriorating child; know where the resuscitation trolley and defibrillator are and check them.",
          "pg": "Lead early recognition and treatment so that arrest does not happen; know your unit's arrest data.",
          "fac": "Use one real deterioration from your unit (anonymised) to ask: when could we have acted earlier?"}),
   sec(1, "Two roads to arrest", algo("How children arrest", '''  RESPIRATORY failure   →  hypoxia + hypercapnia  →  bradycardia  →  arrest
  CIRCULATORY failure   →  shock, poor perfusion  →  acidosis     →  arrest
  (both roads often run together: pneumonia with sepsis, dehydration with
   aspiration)

  SUDDEN cardiac arrest (VF/pVT) is less common: congenital heart disease,
  myocarditis, cardiomyopathy, channelopathy, commotio cordis, drugs''') + '''
  <p>The usual first arrest rhythm in children is <b>bradycardia progressing to asystole or PEA</b>, not VF. A shockable rhythm is more likely with known heart disease, sudden collapse during exercise, or in adolescents.</p>'''),

   sec(2, "Prevention beats resuscitation", '''
  <p>Survival to discharge after paediatric in-hospital arrest is far higher than after out-of-hospital arrest, but both are poor compared with preventing the arrest. Most in-hospital arrests are preceded by hours of abnormal vital signs. Early warning scores, a rapid-response or medical emergency team, and a culture where any nurse can call for help reduce arrests outside intensive care.</p>''' + pearl('''<p>Bradycardia in a hypoxic child is a pre-arrest sign, not a heart problem. Oxygenate and ventilate first: the heart rate usually follows.</p>''')),

   sec(3, "The 2025 Chain of Survival", '''
  <p>The 2025 AHA guidelines introduced a <b>single Chain of Survival</b> for adults and children, in and out of hospital: prevention and preparedness, early recognition and activation, high-quality CPR, early defibrillation when needed, advanced resuscitation, post&ndash;cardiac arrest care, and recovery. The emphasis on <b>prevention and recovery</b> at the two ends is deliberate: most of what changes outcome happens before the arrest and after the child leaves intensive care.</p>'''),

   sec(4, "Across settings", tracks(
     ["Rapid-response team, early warning score, PICU, arterial lines, manual defibrillator in every ward",
      "Regular in-situ simulation and debriefing after every arrest"],
     ["One doctor, two nurses, one crash trolley: check it every shift and after every use",
      "A written early warning chart and a clear rule for calling the doctor",
      "Know the fastest route to a defibrillator, and who can use it at night"]) + india('''<p>In India most children who die in hospital die of pneumonia, sepsis, diarrhoea with dehydration and neonatal problems &mdash; all pathways to respiratory or circulatory arrest. Out-of-hospital arrest survival is very low: bystander CPR is uncommon and ambulance response (108/102) varies. Hospital-based prevention and recognition are where the largest gains lie.</p>'''), lvl="a"),
  ],
  [Q("A 2-year-old with pneumonia has been increasingly breathless for 6 hours. His heart rate falls from 170 to 70/min, and his SpO₂ is 72%. What is the most likely mechanism, and the first priority?",
     ["Primary heart block; give atropine first.",
      "Hypoxia from respiratory failure; open the airway and ventilate with oxygen.",
      "Ventricular fibrillation; defibrillate.",
      "Vasovagal reaction; observe."],
     1,
     "What usually causes bradycardia in a sick child with lung disease?",
     "His oxygen is critically low after hours of worsening breathing. What does the heart need first?",
     "In children, bradycardia with severe hypoxaemia is usually a <b>pre-arrest sign of respiratory failure</b>. Open the airway and give bag-mask ventilation with oxygen; start CPR if the heart rate stays below 60/min with poor perfusion despite ventilation.",
     "<b>A</b> &mdash; atropine does not fix hypoxia. <b>C</b> &mdash; he has a pulse and a slow rhythm, not VF. <b>D</b> &mdash; this is a peri-arrest emergency.",
     "In a hypoxic child, slow heart rate means give breaths now.",
     "section 1, ‘Two roads to arrest’"),
   Q("Which intervention is most likely to reduce the number of cardiac arrests on a paediatric ward?",
     ["Buying a newer defibrillator.",
      "An early warning system with a clear rule and a team to call when a child deteriorates.",
      "Giving routine oxygen to every admitted child.",
      "Teaching every nurse to intubate."],
     1,
     "Most in-hospital arrests are preceded by what?",
     "Hours of abnormal vital signs usually come first. What system acts on them?",
     "Most in-hospital arrests follow hours of abnormal vital signs. An <b>early warning system with an escalation rule and a responding team</b> catches deterioration before arrest.",
     "<b>A</b> &mdash; defibrillators help only in shockable arrest, which is uncommon. <b>C</b> &mdash; routine oxygen does not prevent deterioration and may mask it. <b>D</b> &mdash; intubation is a skill for trained staff and does not prevent arrest.",
     "The best resuscitation is the one you never need.",
     "section 2, ‘Prevention beats resuscitation’")]
)

# ------------------------------------------------------------------ UNIT 2
unit(2, "A", "The systematic approach",
  "The same order every time &mdash; first impression, then ABCDE, then history and tests &mdash; means nothing important is missed when the room is noisy and the child is getting worse.",
  [("e", "Use the Paediatric Assessment Triangle for a first impression in seconds."),
   ("e", "Apply the evaluate&ndash;identify&ndash;intervene cycle with a primary ABCDE assessment."),
   ("a", "Classify problems by type (respiratory, circulatory) and severity."),
   ("x", "Integrate the secondary assessment and investigations without delaying treatment.")],
  [
   roles({"ug": "Perform the first impression and a primary ABCDE assessment aloud on a manikin.",
          "nurse": "Take a full set of vital signs, recognise abnormal values for age and escalate.",
          "pg": "Classify the problem, intervene, and reassess after every intervention.",
          "fac": "Watch whether the learner reassesses after each action, not only whether they assess well once."}),
   sec(1, "First impression: the Paediatric Assessment Triangle", table(
     ["Side", "Look for"],
     [["<b>Appearance</b>", "Tone, interaction, consolability, look/gaze, speech/cry"],
      ["<b>Work of breathing</b>", "Abnormal sounds, recession, nasal flaring, head bobbing, tripod position"],
      ["<b>Circulation to skin</b>", "Pallor, mottling, cyanosis"]]) + '''
  <p>A child who is unresponsive, not breathing normally or without a pulse needs CPR now (Unit 4). Otherwise, move to the primary assessment.</p>'''),

   sec(2, "Evaluate, identify, intervene", algo("The cycle", '''  EVALUATE   primary assessment (ABCDE), vital signs, SpO₂
  IDENTIFY   type: respiratory / circulatory / both
             severity: distress or failure; compensated or hypotensive shock
  INTERVENE  oxygen, airway, ventilation, access, fluids, drugs
  → EVALUATE again after every intervention and whenever the child changes''') + table(
     ["Primary assessment", "Key checks"],
     [["A Airway", "Clear, maintainable, or not maintainable"],
      ["B Breathing", "Rate, effort, air entry, SpO₂, abnormal sounds"],
      ["C Circulation", "Heart rate, pulses, capillary refill, skin, blood pressure, urine output"],
      ["D Disability", "AVPU or GCS, pupils, glucose"],
      ["E Exposure", "Temperature, rash, injuries"]])),

   sec(3, "Classify type and severity", '''
  <p>Name the problem so the team can act on it: &ldquo;respiratory failure from lower-airway disease&rdquo;, &ldquo;hypotensive septic shock&rdquo;. Respiratory problems and shock are taught in full in the OxyVent and Approach to the Sick Child modules; Units 8 and 9 here are short recaps focused on stopping the slide to arrest.</p>''' + table(
     ["Age", "Hypotension (systolic, mmHg)"],
     [["Term neonate (0&ndash;28 days)", "Below 60"],
      ["Infant (1&ndash;12 months)", "Below 70"],
      ["Child 1&ndash;10 years", "Below 70 + (age in years &times; 2)"],
      ["Over 10 years", "Below 90"]])),

   sec(4, "Secondary assessment and tests", '''
  <p>Once immediate threats are treated: a focused history (SAMPLE: signs and symptoms, allergies, medications, past history, last meal, events), a head-to-toe examination, and targeted tests &mdash; blood gas, glucose, lactate, electrolytes, haemoglobin, chest X-ray, ECG, point-of-care ultrasound where available. Tests guide treatment; they do not delay it.</p>''', lvl="a"),
  ],
  [Q("A 4-year-old is drowsy, grunting, with capillary refill of 4 seconds and mottled skin. Which is the correct next step?",
     ["Take a full SAMPLE history before any treatment.",
      "Proceed to the primary ABCDE assessment and treat problems as you find them.",
      "Send the child for a chest X-ray first.",
      "Wait for blood results before deciding."],
     1,
     "What does the first impression tell you, and what comes next in the sequence?",
     "Abnormal appearance, breathing and circulation: which assessment finds and treats immediate threats?",
     "The first impression is abnormal on all three sides. Move straight to the <b>primary ABCDE assessment</b>, intervening as each problem is found, and reassess after each intervention.",
     "<b>A</b> &mdash; the history comes after immediate threats are treated. <b>C</b> and <b>D</b> &mdash; tests must not delay resuscitation.",
     "Treat what kills first, in the order it kills.",
     "section 2, ‘Evaluate, identify, intervene’"),
   Q("A 6-year-old in shock has a systolic blood pressure of 78 mmHg. Is she hypotensive?",
     ["No; the limit at 6 years is 60 mmHg.",
      "No; the limit at 6 years is 70 mmHg.",
      "Yes; the limit at 6 years is 70 + (6 × 2) = 82 mmHg.",
      "Yes; any systolic pressure below 100 mmHg is hypotension in children."],
     2,
     "Which formula gives the hypotension threshold for children aged 1–10 years?",
     "70 plus twice the age in years. What is that at 6 years?",
     "For children 1&ndash;10 years, hypotension is a systolic pressure below <b>70 + (age &times; 2)</b>. At 6 years that is 82 mmHg, so 78 mmHg is <b>hypotensive</b> shock.",
     "<b>A</b> and <b>B</b> &mdash; these are the thresholds for neonates and infants. <b>D</b> &mdash; 100 mmHg is not the paediatric threshold.",
     "Know the formula: 70 + 2 × age.",
     "section 3, ‘Classify type and severity’")]
)

# ------------------------------------------------------------------ UNIT 3
unit(3, "A", "High-performance teams",
  "A resuscitation is performed by a team, not a person. Clear roles, closed-loop communication and one leader who stays hands-off are what turn good individual skills into good outcomes.",
  [("e", "Describe the roles in a resuscitation team."),
   ("e", "Use closed-loop communication."),
   ("a", "Lead a resuscitation: assign roles, share a mental model, and summarise aloud."),
   ("x", "Run a structured debrief after an arrest or simulation.")],
  [
   roles({"ug": "Know the team roles and practise closed-loop communication.",
          "nurse": "Take the compressor, airway, access or recorder role; speak up when you see a problem.",
          "pg": "Lead: assign roles, stay hands-off, summarise every 2 minutes, and ask for input.",
          "fac": "Debrief every simulation with a structured method (Appendix B, PEARLS)."}),
   sec(1, "Roles", table(
     ["Role", "Main task"],
     [["Team leader", "Assigns roles, directs care, stays hands-off, summarises, decides"],
      ["Compressor(s)", "High-quality compressions; swap every 2 minutes"],
      ["Airway", "Opens the airway, ventilates, monitors chest rise and ETCO₂"],
      ["Monitor/defibrillator", "Attaches pads, analyses rhythm, shocks, times cycles"],
      ["Vascular access and drugs", "IV/IO access, prepares and gives drugs with a double check"],
      ["Recorder", "Times events, drugs and shocks; prompts the leader"]]) + '''
  <p>With fewer people, roles combine. In a small team the leader may also manage the airway; the rule is that someone always owns each task.</p>'''),

   sec(2, "Closed-loop communication", algo("Closed loop", '''  LEADER:    "Priya, give adrenaline 0.2 mg IV now."
  PRIYA:     "Adrenaline 0.2 mg IV — giving now."
  PRIYA:     "Adrenaline 0.2 mg given at 10:04."
  LEADER:    "Thank you. Next dose due at 10:08."''') + '''
  <p>Use names, clear dose and route, and a read-back. If a team member thinks an order is wrong, they say so: &ldquo;I am concerned the dose is 10 times too high.&rdquo;</p>'''),

   sec(3, "Shared mental model and summaries", '''
  <p>Every 2 minutes, at the rhythm check, the leader summarises: what has happened, what the current rhythm is, what has been given, and what comes next. Invite input: &ldquo;Anything I have missed?&rdquo; Knowledge-sharing and mutual respect prevent fixation on one diagnosis.</p>''' + pitfall('''<p>The leader doing compressions or intubating. Once hands-on, the leader loses the overview: rhythm checks drift, drug timing slips, and reversible causes are forgotten.</p>''')),

   sec(4, "Debrief every time", '''
  <p>After every arrest or simulation, debrief within the hour when possible: what happened, what went well, what to change. Hot debriefs after real events improve CPR quality in later events. Use a structured method, and look at systems (equipment, staffing, access) as well as individuals.</p>''' + india('''<p>In many Indian hospitals the team is one resident and one or two nurses. Train and simulate with the team you will actually have: rehearse who compresses, who ventilates, who draws up drugs, and who calls for help. A phone number for the senior on call written on the crash trolley saves minutes.</p>'''), lvl="a"),
  ],
  [Q("During a resuscitation the leader says 'Give adrenaline'. The nurse gives 1 mg to a 10 kg child without responding. What communication failure occurred?",
     ["None; the order was followed.",
      "No closed loop: the order lacked a dose and route, and there was no read-back before giving.",
      "The recorder should have given the drug.",
      "The nurse should have waited for the next rhythm check."],
     1,
     "What should every drug order and response contain?",
     "The dose for 10 kg should be 0.1 mg. How would a closed loop have caught the error?",
     "A drug order must include <b>drug, dose and route</b>, and the receiver reads it back before giving it. A read-back of &ldquo;1 mg&rdquo; would have prompted a check: the dose for 10 kg is 0.01 mg/kg = 0.1 mg.",
     "<b>A</b> &mdash; a 10-fold overdose was given. <b>C</b> &mdash; the recorder records; the issue is communication. <b>D</b> &mdash; timing was not the problem.",
     "Name, drug, dose, route, read-back.",
     "section 2, ‘Closed-loop communication’"),
   Q("The team leader in a paediatric arrest starts doing chest compressions because the compressor looks tired. What is the main risk?",
     ["The compressions will be too slow.",
      "The leader loses the overview, so rhythm checks, drug timing and reversible causes are missed.",
      "The defibrillator will not work.",
      "There is no risk."],
     1,
     "What is the leader's main job?",
     "If the leader is hands-on, who is watching the whole resuscitation?",
     "The leader should stay <b>hands-off</b> to keep the overview. Assign another team member to take over compressions; swap compressors every 2 minutes.",
     "<b>A</b> &mdash; the rate may be fine; the problem is loss of leadership. <b>C</b> &mdash; unrelated. <b>D</b> &mdash; loss of overview is a well-recognised risk.",
     "The leader's hands stay free so the leader's head stays clear.",
     "section 3, ‘Shared mental model and summaries’")]
)
