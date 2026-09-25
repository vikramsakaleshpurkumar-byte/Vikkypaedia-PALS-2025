# Paediatric Advanced Life Support 2025

**Live:** https://vikramsakaleshpurkumar-byte.github.io/Vikkypaedia-PALS-2025/
**All Vikkypaedia modules:** https://vikramsakaleshpurkumar-byte.github.io/

A mastery-based, self-paced module on paediatric resuscitation, covering:

- the deteriorating child
- high-quality CPR
- the arrest pathways
- arrhythmias
- post-arrest care
- life after arrest

It is written from the **2025 AHA/AAP Guidelines for CPR and Emergency Cardiovascular Care** (Part 6, Pediatric Basic Life Support; Part 8, Pediatric Advanced Life Support) and ILCOR 2025, and it reads the content across the resource gradient.

> **This is not the AHA PALS course.** It does not reproduce the AHA provider manual, gives no provider card and confers no PALS provider status. PALS® is a trademark of the American Heart Association. CPR, defibrillation and airway skills need a hands-on, instructor-led course.

**Version 4.0.0** (built 2026-09-24) is a complete rebuild on the Vikkypaedia Standard engine (v2.1). It replaces the earlier 13-module app. The rebuild removes that app's dependence on external fonts and a confetti CDN, and its badges, points and streaks. The earlier app described itself as based on the AHA provider manual; this edition is written from the published guidelines instead. Progress from the earlier app is not carried over; learners who used it see a one-time notice.

## What it is

- One self-contained HTML file. No CDN, no framework, no network request. It works offline on a phone.
- 20 units in 5 Parts, about 28 notional hours.
- 40 checkpoint questions with two-tier hints and rationales that explain why the wrong options are wrong, plus 30 fresh integrative items for the final assessment.
- Parts:
  - **A Foundations:** why children arrest; the systematic approach; teams.
  - **B BLS, airway and drugs:** CPR 2025; choking and defibrillation; ventilation in arrest; access and drugs.
  - **C Before the arrest:** respiratory failure and shock recaps; bradycardia; tachycardia.
  - **D Cardiac arrest:** arrest rhythms; nonshockable and shockable pathways; monitoring and reversible causes; special circumstances.
  - **E After the arrest and systems:** post-arrest care; prognosis and survivorship; families, stopping and systems; capstone and future directions.
- **Arrest and rhythm focus.** Respiratory failure and shock are taught in depth in the OxyVent and Approach to the Sick Child modules. Units 8 and 9 here are short recaps that link to them.
- **"Your role" box** in every unit for Student, Nurse, PG resident and Faculty.
- **Two diagrams:** the two arrest pathways, and bradycardia with a pulse.

## What changed in 2025, and how the module teaches it

- **Infant compressions:** two-thumb encircling or the heel of one hand. The two-finger technique is removed.
- **Choking:**
  - Infants: back blows alternating with chest thrusts.
  - Children: back blows alternating with abdominal thrusts.
- **Nonshockable arrest:** epinephrine **as early as possible**, then every 3–5 minutes.
- **Shockable arrest:** defibrillation first (2 J/kg, then 4 J/kg). Epinephrine after the second shock, or sooner only if rapid defibrillation is not possible.
- **CPR monitoring:**
  - Diastolic blood pressure targets of ≥25 mmHg in infants and ≥30 mmHg in children.
  - ETCO₂ indicates CPR quality, but no ETCO₂ cut-off alone should end resuscitation.
- **After ROSC:**
  - Avoid central temperatures >37.5 °C, and consider 5 days of targeted temperature management.
  - Keep systolic and mean blood pressure above the 10th percentile.
  - Target SpO₂ 94–99%.
- **New topics:** neuroprognostication (first time in the guidelines), survivorship care, IV sotalol for refractory SVT, and a single Chain of Survival.

## Certification

The certificate requires three criteria:

1. **Coverage:** all 40 checkpoints currently correct.
2. **Retention:** at least 15 of 20 units retained after 24 hours.
3. **Applied performance:** a 50-item closed-book assessment in 75 minutes, with 2 attempts, a 24-hour lock between attempts, and a **provisional** 80% cut score.

The certificate prints its own limits: it is not the AHA PALS course and confers no provider status.

## Enrolment and completion records

Learner details stay in the browser. `verify.html` checks a downloaded completion record offline. **Records are self-attested.**

## Faculty adoption

- Appendix A: key-feature problems, 12 OSCE stations (infant CPR, AED, choking, IO, rhythms, SVT, megacodes, post-ROSC) and an entrustment scale.
- Appendix B: four megacode scenarios on a manikin.
- Appendix C: a worked flipped session on Part D, plus standard-setting worksheets.

## Rebuilding and testing it

```bash
python content/build_content.py && python content/appendices.py && python build.py
python tests/test_full.py; python tests/test_ui.py; python tests/test_enrol.py
python tests/test_search.py; python tests/test_sig.py; python tests/test_loops.py
python tests/contrast.py; python tests/offline_test.py; python tests/print_test.py
```

## Privacy

Everything is stored in the learner's browser. There is no account, no server, no analytics and no telemetry.

## Known limitations

- Reading this module does not teach CPR, defibrillation or airway skills. Book a hands-on course.
- Most paediatric resuscitation recommendations rest on low-certainty, observational evidence. Several 2020 recommendations were carried forward without a new evidence review in 2025.
- Drug doses carried forward from 2020 (adenosine, amiodarone, atropine) are standard values; check them against your formulary.
- The platform has the standard limitations: fixed Leitner intervals, thin item sampling, an unproctored assessment, self-attested records and a provisional cut score. The clinical content has not been externally peer reviewed.

## Contributing, licence and citation

See `CONTRIBUTING.md`. The module is licensed CC BY-NC-SA 4.0, **excluding** the Vikkypaedia name, the name and likeness of Dr Vikram Sakaleshpur Kumar, and the certificate signature block.

> Sakaleshpur Kumar V. *Paediatric Advanced Life Support 2025: an evidence-governed, competency-based digital module for resource-constrained settings.* Vikkypaedia; 2026. Available from: https://vikramsakaleshpurkumar-byte.github.io/Vikkypaedia-PALS-2025/

## Disclaimer

This module is education, not a clinical protocol, and not certification to practise. Verify every dose against your institution's protocol.

## Interactive megacodes (engine v2.2)

Six branching cases played one decision at a time against a patient monitor, in their own section before the final assessment. Each case opens when its Part opens. Wrong calls cost time or change the patient, critical errors (tenfold doses, a shock with a pulse, compressions before effective ventilation, and similar) are flagged, and every option is explained. Options are shuffled on every run. The debrief shows right decisions, critical errors, key times against targets, and links back to the units.

- **Formative only.** Results are stored locally, appear in the completion record (`detail.megacodes`, covered by the detail checksum) and in the faculty class report on the hub. They are not a certification criterion.
- **Authoring:** cases live in `megacodes/cases.py`. Every dose is taken from this module's drug annex (Appendix E) and worked out for the stated weight. Compile with `python megacodes/make.py`, which validates the graph (every node reachable, a correct option at every step, correct-only paths acyclic and ending well, only `<b>`/`<i>` markup) and writes `build/86_megacodes.html`. Then run `python build.py`.
- The player (`build/87_megacode.js`) is shared by every Vikkypaedia module and does nothing in a module without cases.
- Clinically reviewed against the 2025 AHA/AAP guidelines before release (2026-09-24). Re-review whenever the guidelines change.
