from gen import *

part("B", "Basic life support, airway and drugs", "Units 4&ndash;7 · ~5 hours",
     "High-quality CPR is the foundation that every advanced skill stands on, and the 2025 guidelines changed how infants' chests are compressed and how choking is managed. This Part covers compressions, defibrillation, the airway during arrest, and getting drugs in fast.")

# ------------------------------------------------------------------ UNIT 4
unit(4, "B", "High-quality CPR",
  "Compressions generate the only blood flow the brain and heart get during arrest. Their quality &mdash; rate, depth, recoil and few pauses &mdash; is the one thing every rescuer controls.",
  [("e", "Recognise cardiac arrest and start CPR within 10 seconds of the pulse check."),
   ("e", "Deliver compressions at the correct rate, depth and ratio for age."),
   ("a", "Use the 2025 infant compression techniques: two-thumb encircling or one-hand."),
   ("x", "Minimise interruptions and use feedback to keep CPR high-quality.")],
  [
   roles({"ug": "Perform high-quality CPR on infant and child manikins with feedback.",
          "nurse": "Start compressions, swap every 2 minutes, and speak up when quality drops.",
          "pg": "Monitor CPR quality as leader: rate, depth, recoil, pauses, ventilation.",
          "fac": "Use a feedback manikin; measure the pause before and after each shock."}),
   sec(1, "Recognise arrest and start", '''
  <p>Unresponsive, not breathing or only gasping: shout for help, activate the emergency response, and check a pulse (brachial in infants, carotid or femoral in children) for <b>no more than 10 seconds</b>. No definite pulse &mdash; start compressions. A pulse below 60/min with poor perfusion despite oxygenation and ventilation also needs compressions.</p>'''),

   sec(2, "The numbers", table(
     ["", "Infant (under 1 year)", "Child (1 year to puberty)"],
     [["Rate", "100&ndash;120/min", "100&ndash;120/min"],
      ["Depth", "At least one-third of chest depth, about 4 cm", "At least one-third of chest depth, about 5 cm"],
      ["Technique", "<b>Two-thumb encircling</b> or <b>heel of one hand</b> (2025: two-finger technique removed)", "Heel of one or two hands, lower half of the sternum"],
      ["Ratio, 1 rescuer", "30:2", "30:2"],
      ["Ratio, 2 rescuers", "15:2", "15:2"],
      ["With advanced airway", "Continuous compressions; 1 breath every 2&ndash;3 s (20&ndash;30/min)", "Same"]]) + evidence('''<p>2025 AHA/AAP: the two-finger technique for infants is no longer recommended because it often fails to reach adequate depth. Adolescents after puberty receive adult CPR (5&ndash;6 cm depth).</p>''')),

   sec(3, "Quality, not just quantity", '''
  <ul>
    <li><b>Allow full recoil</b> &mdash; do not lean on the chest between compressions.</li>
    <li><b>Minimise interruptions</b> &mdash; pauses for rhythm checks and shocks under 10 seconds; charge the defibrillator while compressions continue.</li>
    <li><b>Swap compressors every 2 minutes</b>, or sooner if tired.</li>
    <li><b>Avoid excessive ventilation</b> &mdash; each breath just enough to make the chest rise.</li>
    <li>Use a firm surface and CPR feedback devices where available.</li>
  </ul>''' + pitfall('''<p>Long pauses for pulse checks, intubation or line placement. Every second without compressions lets coronary and cerebral perfusion pressure fall, and it takes several compressions to build it up again.</p>''')),

   sec(4, "Monitoring CPR quality", '''
  <p>With an arterial line, a <b>diastolic blood pressure of at least 25 mmHg in infants and 30 mmHg in children</b> 1 year and older is a 2025 hemodynamic target. With an advanced airway, <b>ETCO₂</b> reflects blood flow: a falling value suggests poor compressions or a tired compressor; a sudden rise may signal return of circulation. A specific ETCO₂ cut-off should not be used alone to stop resuscitation.</p>''' + tracks(
     ["Arterial line, ETCO₂, feedback manikins and devices",
      "Real-time CPR quality displayed to the team"],
     ["No arterial line or ETCO₂: watch depth, rate and recoil directly; count aloud; swap every 2 minutes",
      "A metronome app at 110/min on a phone keeps the rate right",
      "Practise on manikins monthly; skills decay within months"]), lvl="a"),
  ],
  [Q("A nurse starts CPR on a 4-month-old. She uses two fingers in the centre of the chest. What does the 2025 guidance recommend instead?",
     ["Continue with two fingers; it is the standard infant technique.",
      "Use the two-thumb encircling technique, or the heel of one hand.",
      "Use two hands, as for adults.",
      "Give breaths only, as infants arrest from hypoxia."],
     1,
     "Which infant technique was removed in 2025, and why?",
     "Two fingers often fail to reach one-third of chest depth. Which two techniques replaced it?",
     "The 2025 AHA/AAP guidelines removed the <b>two-finger</b> technique because it often does not reach adequate depth. Use <b>two-thumb encircling</b> hands or the <b>heel of one hand</b>.",
     "<b>A</b> &mdash; two fingers is no longer recommended. <b>C</b> &mdash; two hands is too much for an infant. <b>D</b> &mdash; arrest needs compressions as well as breaths.",
     "Infant CPR 2025: two thumbs or one hand, never two fingers.",
     "section 2, ‘The numbers’"),
   Q("Two healthcare providers are resuscitating a 5-year-old without an advanced airway. What compression-to-ventilation ratio should they use?",
     ["30:2.",
      "15:2.",
      "5:1.",
      "Continuous compressions with 1 breath every 6 seconds."],
     1,
     "Does the ratio change with the number of rescuers in children?",
     "With two rescuers, children get proportionally more breaths than adults. Which ratio?",
     "For infants and children with <b>two rescuers</b> and no advanced airway, use <b>15:2</b>. A single rescuer uses 30:2.",
     "<b>A</b> &mdash; 30:2 is for a single rescuer. <b>C</b> &mdash; 5:1 is outdated. <b>D</b> &mdash; continuous compressions apply once an advanced airway is placed, with 1 breath every 2&ndash;3 seconds in children.",
     "Two rescuers, child: 15:2.",
     "section 2, ‘The numbers’")]
)

# ------------------------------------------------------------------ UNIT 5
unit(5, "B", "Choking and defibrillation",
  "Two emergencies where a single correct action saves a life: clearing an obstructed airway, and delivering a shock to a shockable rhythm without delay.",
  [("e", "Relieve severe foreign-body airway obstruction in infants and children (2025 technique)."),
   ("e", "Use an AED safely in a child, including infants."),
   ("a", "Choose pad size and position; use a manual defibrillator."),
   ("x", "Minimise the pause around each shock.")],
  [
   roles({"ug": "Practise back blows, chest thrusts and abdominal thrusts on manikins, and switch on an AED.",
          "nurse": "Know your defibrillator: paediatric pads, energy selection, and daily checks.",
          "pg": "Deliver a manual shock at the right energy with compressions continuing during charging.",
          "fac": "Run a choking-to-arrest scenario: the child becomes unresponsive halfway through."}),
   sec(1, "Choking: 2025 guidance", table(
     ["", "Infant (under 1 year)", "Child"],
     [["Severe obstruction, responsive", "Repeated cycles of <b>5 back blows and 5 chest thrusts</b> (no abdominal thrusts)", "Repeated cycles of <b>5 back blows and 5 abdominal thrusts</b>"],
      ["Becomes unresponsive", "Start CPR; look in the mouth before breaths and remove a visible object; no blind finger sweeps", "Same"]]) + evidence('''<p>2025 AHA/AAP: for children, alternating back blows and abdominal thrusts; for infants, back blows and chest thrusts. Mild obstruction (the child can cough and speak): encourage coughing and watch closely.</p>''')),

   sec(2, "AED in children and infants", '''
  <ul>
    <li>Use an AED as soon as it arrives. In children under 8 years, use a <b>paediatric attenuator</b> (child pads or key) if available; if not, use adult pads.</li>
    <li>In infants, a manual defibrillator is preferred; if unavailable, an AED with an attenuator; if neither, an AED without an attenuator.</li>
    <li>Pads must not touch: if the chest is small, place one on the front and one on the back.</li>
  </ul>'''),

   sec(3, "Manual defibrillation", algo("Shock with minimal pause", '''  Compressions continue while pads are placed and the device charges
  Rhythm check (under 10 s): VF or pulseless VT?
  "Charging — everyone else keep compressing"
  "Stand clear — oxygen away — shocking"   → SHOCK
  Resume compressions IMMEDIATELY for 2 minutes (no pulse check)

  Energy: first shock 2 J/kg (2–4 J/kg acceptable)
          second shock 4 J/kg; later ≥4 J/kg, max 10 J/kg or adult dose''') + pitfall('''<p>Stopping compressions while the defibrillator charges, then checking a pulse after the shock. Both add pauses without benefit. Charge during compressions and resume compressions straight after the shock.</p>''')),

   sec(4, "Safety", '''
  <p>Oxygen away from the chest at the moment of shock; no one touching the child or bed; dry the chest; remove medication patches. Single shocks, not stacked shocks, are recommended.</p>''' + india('''<p>Many Indian wards and clinics lack a defibrillator, and AEDs in public places are rare. Know where the nearest one is, check it daily, and practise with it. Paediatric pads are often missing from trolleys; if absent, use adult pads in front-and-back position.</p>'''), lvl="a"),
  ],
  [Q("A 7-month-old is choking on a piece of food. She is conscious but cannot cry or breathe. What should you do?",
     ["Give abdominal thrusts.",
      "Give repeated cycles of 5 back blows and 5 chest thrusts.",
      "Perform a blind finger sweep.",
      "Give 2 rescue breaths and wait."],
     1,
     "What is the 2025 technique for infants with severe choking?",
     "Abdominal thrusts are not used in infants. What alternates with back blows?",
     "For an infant with severe obstruction, give <b>5 back blows then 5 chest thrusts</b>, repeated until the object comes out or the infant becomes unresponsive (then start CPR).",
     "<b>A</b> &mdash; abdominal thrusts are not used in infants. <b>C</b> &mdash; blind finger sweeps can push the object deeper. <b>D</b> &mdash; breaths will not pass a complete obstruction while she is responsive.",
     "Infant choking: back blows and chest thrusts. Child: back blows and abdominal thrusts.",
     "section 1, ‘Choking: 2025 guidance’"),
   Q("A 20 kg child is in VF. The first shock has been given. After 2 minutes of CPR the rhythm is still VF. What energy should the second shock be?",
     ["20 J (1 J/kg).",
      "40 J (2 J/kg).",
      "80 J (4 J/kg).",
      "360 J."],
     2,
     "What are the first and subsequent defibrillation doses?",
     "First 2 J/kg; subsequent 4 J/kg. What is 4 J/kg for 20 kg?",
     "The first shock is 2 J/kg (2&ndash;4 J/kg acceptable); the second is <b>4 J/kg</b> = 80 J. Later shocks may be increased up to 10 J/kg or the adult maximum.",
     "<b>A</b> &mdash; 1 J/kg is too low. <b>B</b> &mdash; 2 J/kg is the first dose. <b>D</b> &mdash; 360 J is an adult monophasic dose, far above 10 J/kg here.",
     "Defibrillation: 2 J/kg, then 4 J/kg.",
     "section 3, ‘Manual defibrillation’")]
)

# ------------------------------------------------------------------ UNIT 6
unit(6, "B", "Airway and ventilation in arrest",
  "Oxygenation and ventilation matter more in children's arrests than in adults', because most start with hypoxia. Effective bag-mask ventilation is the core skill; an advanced airway is a team decision, not a reflex.",
  [("e", "Give effective bag-mask ventilation during CPR."),
   ("e", "Know the ventilation rate with and without an advanced airway."),
   ("a", "Confirm tube position with ETCO₂ and examination; use cuffed tubes."),
   ("x", "Decide when to place an advanced airway during CPR.")],
  [
   roles({"ug": "Give two-person bag-mask ventilation with visible chest rise.",
          "nurse": "Prepare suction, bag, masks, airway adjuncts and ETCO₂; watch chest rise.",
          "pg": "Decide when to intubate, confirm with waveform ETCO₂, and prevent hyperventilation.",
          "fac": "Assess bag-mask skill with DOPS before assessing intubation."}),
   sec(1, "Bag-mask first", '''
  <p>Bag-mask ventilation (BMV) with oxygen is effective for most children in arrest and may be as good as intubation in out-of-hospital arrest. Two-person technique gives a better seal. Each breath over about 1 second, enough to make the chest rise. Oropharyngeal airways help if the airway obstructs. See OxyVent Unit 7 for the full skill.</p>'''),

   sec(2, "Ventilation rates", table(
     ["Situation", "Rate"],
     [["CPR without advanced airway", "Breaths within compression cycles: 30:2 (1 rescuer) or 15:2 (2 rescuers)"],
      ["CPR with advanced airway", "<b>1 breath every 2&ndash;3 seconds (20&ndash;30/min)</b>, compressions continuous"],
      ["Pulse present, breathing inadequate", "1 breath every 2&ndash;3 seconds (20&ndash;30/min)"]]) + danger('''<p>Hyperventilation raises intrathoracic pressure, reduces venous return and coronary perfusion, and can worsen outcome. Squeeze just enough for chest rise, at the set rate.</p>''')),

   sec(3, "Advanced airway", '''
  <ul>
    <li><b>Cuffed tubes</b> are reasonable for infants and children; watch cuff pressure. Size: (age &divide; 4) + 3.5 mm for cuffed tubes; depth at the lips about 3 &times; tube size (cm).</li>
    <li>Confirm placement with <b>waveform capnography</b> plus chest rise and auscultation. Absent ETCO₂ in arrest can mean very low blood flow, but the tube must be re-checked.</li>
    <li>Cricoid pressure is not recommended routinely during intubation; routine atropine premedication is not needed.</li>
    <li>Intubation attempts should not interrupt compressions for more than a few seconds; a supraglottic airway is an option for trained staff.</li>
  </ul>'''),

   sec(4, "When to intubate during CPR", '''
  <p>There is no benefit from early intubation if bag-mask ventilation is effective. Intubate when BMV is failing, when prolonged ventilation will be needed, or for transport &mdash; by the most skilled person available, without long pauses in compressions.</p>''' + india('''<p>Most arrests in Indian district hospitals are managed without capnography. If intubated without ETCO₂, confirm with chest rise, bilateral air entry, misting, rising SpO₂ and heart rate, and a colorimetric CO₂ detector if available. When in doubt, take it out and go back to bag-mask.</p>'''), lvl="a"),
  ],
  [Q("A 3-year-old in arrest has been intubated. What ventilation rate should be used during continuous compressions?",
     ["1 breath every 6 seconds (10/min).",
      "1 breath every 2–3 seconds (20–30/min).",
      "40–60 breaths/min.",
      "As fast as possible to clear CO₂."],
     1,
     "Which rate applies to children with an advanced airway during CPR?",
     "The paediatric rate is higher than the adult rate of 10/min. Which range?",
     "With an advanced airway, give <b>1 breath every 2&ndash;3 seconds (20&ndash;30/min)</b> during continuous compressions, just enough for chest rise.",
     "<b>A</b> &mdash; 10/min is the adult rate. <b>C</b> &mdash; 40&ndash;60/min is the newborn delivery-room rate. <b>D</b> &mdash; hyperventilation reduces venous return and coronary perfusion.",
     "Child with a tube in arrest: 20–30 breaths/min.",
     "section 2, ‘Ventilation rates’"),
   Q("During CPR, bag-mask ventilation is producing good chest rise. A junior doctor wants to stop compressions for 60 seconds to intubate. What is the best response?",
     ["Allow it; intubation always improves outcome.",
      "Continue effective bag-mask ventilation and compressions; intubation can wait or be done by the most skilled person without long pauses.",
      "Stop ventilating and give compressions only.",
      "Insert a nasogastric tube first."],
     1,
     "Does early intubation improve outcome if bag-mask ventilation is effective?",
     "A 60-second pause in compressions is very harmful. What should happen?",
     "When BMV is effective, there is no benefit from early intubation, and a long pause in compressions is harmful. <b>Continue effective BMV and compressions</b>; intubate later if needed, by the most skilled person, with minimal interruption.",
     "<b>A</b> &mdash; intubation does not always improve outcome and the pause harms. <b>C</b> &mdash; ventilation matters in paediatric arrest. <b>D</b> &mdash; a nasogastric tube may help gastric distension but is not the priority.",
     "Good bag-mask ventilation is enough; protect the compressions.",
     "section 4, ‘When to intubate during CPR’")]
)

# ------------------------------------------------------------------ UNIT 7
unit(7, "B", "Access and drugs",
  "Drugs in arrest only help if they reach the circulation quickly. Intraosseous access is fast and reliable, and a length-based tape removes the need to guess weight and calculate under pressure.",
  [("e", "Obtain IV or IO access rapidly."),
   ("e", "Calculate and draw up epinephrine for arrest correctly."),
   ("a", "Know the main resuscitation drugs and when bicarbonate and calcium are used."),
   ("x", "Use weight estimation tools and double-check high-risk drugs.")],
  [
   roles({"ug": "Locate IO sites on a model and calculate epinephrine for three weights.",
          "nurse": "Draw up epinephrine 0.1 mg/mL correctly and double-check doses aloud.",
          "pg": "Place IO access within 1–2 minutes if IV fails; prescribe drugs by weight.",
          "fac": "Run a drug-calculation drill against the clock; count 10-fold errors."}),
   sec(1, "Get access fast", '''
  <p>Intravenous or <b>intraosseous</b> (IO) access &mdash; whichever is fastest in skilled hands. IO sites: proximal tibia (1&ndash;2 cm below and medial to the tibial tuberosity), distal femur, proximal humerus in older children. Everything given IV can be given IO. Endotracheal drugs are a last resort.</p>'''),

   sec(2, "Epinephrine (adrenaline) in arrest", table(
     ["", "Detail"],
     [["Dose", "<b>0.01 mg/kg IV/IO</b> (0.1 mL/kg of 0.1 mg/mL solution), maximum 1 mg"],
      ["Endotracheal", "0.1 mg/kg (0.1 mL/kg of 1 mg/mL) if no IV/IO"],
      ["Timing, nonshockable (asystole/PEA)", "<b>As soon as possible</b> (2025), then every 3&ndash;5 minutes"],
      ["Timing, shockable (VF/pVT)", "After 2 shocks, or sooner only if rapid defibrillation is not possible (2025)"]]) + danger('''<p>Epinephrine comes as 1 mg/mL (1:1000) and 0.1 mg/mL (1:10,000). Confusing them causes 10-fold errors. Label syringes, say the concentration aloud, and double-check.</p>''')),

   sec(3, "Other drugs", table(
     ["Drug", "Use", "Dose"],
     [["Amiodarone", "Shock-refractory VF/pVT", "5 mg/kg bolus; may repeat to a total of 15 mg/kg (max 300 mg single dose)"],
      ["Lidocaine", "Shock-refractory VF/pVT (alternative)", "1 mg/kg loading"],
      ["Adenosine", "SVT (Unit 11)", "0.1 mg/kg rapid push (max 6 mg); then 0.2 mg/kg (max 12 mg)"],
      ["Atropine", "Bradycardia from vagal tone or AV block (Unit 10)", "0.02 mg/kg; max single dose 0.5 mg"],
      ["Glucose 10%", "Hypoglycaemia", "5 mL/kg (WHO ETAT; some protocols use 2 mL/kg); recheck in 15&ndash;30 min"],
      ["Calcium, sodium bicarbonate", "Not routine (2025: no benefit)", "Only for hyperkalaemia, hypocalcaemia, calcium-channel-blocker or sodium-channel-blocker toxicity"]])),

   sec(4, "Weight and double-checks", '''
  <p>Use the child's known weight or a <b>length-based tape</b>; age-based formulas are less accurate, especially in malnourished or obese children. Pre-calculated weight charts on the crash trolley reduce errors. Say every high-risk drug, dose and route aloud and have a second person check.</p>''' + india('''<p>Weight formulas derived from Western children overestimate the weight of many Indian children, and severe malnutrition makes this worse. Use a length-based tape validated locally, or weigh the child as soon as possible. Keep IO needles on every paediatric crash trolley; a standard 16&ndash;18 G needle can be used in an emergency if IO needles are unavailable.</p>'''), lvl="a"),
  ],
  [Q("A 15 kg child is in asystole. IV access has failed twice. What is the best next step for drug access?",
     ["Keep trying IV for another 10 minutes.",
      "Place an intraosseous needle and give epinephrine 0.15 mg as soon as possible.",
      "Give epinephrine 1.5 mg via the endotracheal tube before any other route.",
      "Wait for a central line."],
     1,
     "What is the fastest reliable access in arrest when IV fails?",
     "Asystole needs epinephrine as early as possible. What is 0.01 mg/kg for 15 kg?",
     "Place an <b>IO needle</b> and give <b>epinephrine 0.01 mg/kg = 0.15 mg</b> as soon as possible (2025: early epinephrine in nonshockable arrest).",
     "<b>A</b> &mdash; prolonged IV attempts delay the drug. <b>C</b> &mdash; ETT is a last resort; the correct ETT dose would be 0.1 mg/kg (1.5 mg), but IO is preferred. <b>D</b> &mdash; central access takes too long.",
     "IV fails twice: go IO.",
     "section 1, ‘Get access fast’"),
   Q("A nurse draws up epinephrine for a 12 kg infant in PEA. Which syringe is correct?",
     ["1.2 mL of 1 mg/mL (1.2 mg).",
      "1.2 mL of 0.1 mg/mL (0.12 mg).",
      "0.12 mL of 0.1 mg/mL (0.012 mg).",
      "12 mL of 0.1 mg/mL (1.2 mg)."],
     1,
     "What is the IV/IO epinephrine dose per kg, and in what volume of 0.1 mg/mL?",
     "0.01 mg/kg is 0.1 mL/kg of 0.1 mg/mL. What is that for 12 kg?",
     "Epinephrine 0.01 mg/kg = <b>0.12 mg</b>, which is <b>1.2 mL of 0.1 mg/mL</b> (0.1 mL/kg).",
     "<b>A</b> &mdash; 1.2 mL of 1 mg/mL is a 10-fold overdose. <b>C</b> &mdash; 0.012 mg is 10 times too little. <b>D</b> &mdash; 1.2 mg is a 10-fold overdose and above the 1 mg maximum.",
     "0.1 mL/kg of the 0.1 mg/mL strength.",
     "section 2, ‘Epinephrine (adrenaline) in arrest’")]
)
