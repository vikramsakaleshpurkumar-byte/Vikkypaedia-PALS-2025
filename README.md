# 🏥 Vikkypaedia PALS 2025

### A World-Class MOOC for Pediatric Advanced Life Support

> Based on the **AHA PALS 2025 Provider Manual** — the most comprehensive, interactive, and beautifully designed PALS learning platform ever built.

---

## ✨ What Makes This Special

| Feature | Description |
|---|---|
| 🔴🟡🟢 **Three-Tier Knowledge** | Every unit has **Must Know**, **Nice to Know**, and **Good to Know** sections |
| 🔒 **Sequential Learning** | Units unlock one-by-one as you progress — no skipping ahead |
| 📝 **Embedded Quizzes** | Must-know knowledge checks gate your progression (80% to pass) |
| 🃏 **Spaced Repetition** | SM-2 flashcard engine for medication dosing mastery |
| 🩺 **Clinical Simulator** | Branching decision scenarios with live patient vitals |
| 📊 **Progress Dashboard** | SVG ring chart, streaks, 8 achievement badges |
| 🌙☀️ **Dark/Light Theme** | Toggle between dark medical-grade and light themes |
| 📱 **Mobile Responsive** | Works on phone, tablet, and desktop |

---

## 📚 Course Modules

| # | Module | Content |
|---|---|---|
| 1 | Course Overview & Science Update | 2025 AHA guidelines changes |
| 2 | BLS & AED Review | CPR techniques, compression, ventilation |
| 3 | High-Performance Teams | Team roles, closed-loop communication |
| 4 | Systematic Approach | PAT, ABCDE, SAMPLE, vital signs |
| 5 | Recognizing Respiratory Problems | Upper/lower airway, distress vs failure |
| 6 | Managing Respiratory Problems | O2, airway adjuncts, bag-mask, advanced airway |
| 7 | Recognizing Shock | 4 types, compensated vs hypotensive |
| 8 | Managing Shock | Fluids, septic shock algorithm, vasoactives |
| 9 | Recognizing Arrhythmias | 8 core rhythms |
| 10 | Managing Arrhythmias | Bradycardia, SVT, VT algorithms |
| 11 | Cardiac Arrest | Shockable vs nonshockable pathways |
| 12 | Post-Cardiac Arrest Care | Respiratory, cardiovascular, neurologic goals |
| 13 | Capstone Assessment | Integrated case scenarios + comprehensive exam |

---

## 🚀 Quick Start

1. Clone this repository
2. Open `index.html` in your browser (or serve with any static file server)
3. Start learning from Module 1!

```bash
# Option 1: Direct open
open index.html

# Option 2: Local server
npx serve .
# Then visit http://localhost:3000
```

---

## 🛠️ Tech Stack

- **Vanilla JavaScript** (ES Modules) — no frameworks, no build step
- **CSS Custom Properties** — complete design system with tier colors
- **localStorage** — progress persistence, no backend needed
- **JSON-driven curriculum** — all content loaded from `data/curriculum.json`

---

## 📁 Project Structure

```
├── index.html              # SPA shell
├── styles.css              # Complete design system (960+ lines)
├── app.js                  # Main application engine
├── data/
│   ├── curriculum.json     # 13 modules with three-tier content (69KB)
│   ├── medications.json    # 13 PALS medications with doses
│   └── vital-signs.json    # Age-based vital signs reference
└── components/
    ├── quiz-engine.js      # MCQ assessment with feedback
    ├── algorithm-viewer.js # Interactive algorithm walkthroughs
    ├── flashcard-engine.js # SM-2 spaced repetition
    ├── clinical-sim.js     # Branching clinical simulator
    └── progress-tracker.js # Progress, streaks, badges
```

---

## 📋 Key PALS 2025 Updates Covered

- ❌ **2-finger technique eliminated** for infant compressions
- 💉 **Early epinephrine** for nonshockable rhythms
- ⚡ **Rapid defibrillation** priority for shockable rhythms
- 🫁 **20-30 breaths/min** with advanced airway (changed from 2020)
- 🌡️ **Prevent hyperthermia** (>37.5°C) post-arrest
- 📊 **ETCO2** as CPR quality indicator
- 💊 **Naloxone** for suspected opioid overdose

---

## 👨‍⚕️ Author

**Vikkypaedia** — Building world-class medical education for India and beyond.

---

## ⚠️ Disclaimer

This MOOC is an educational tool based on the AHA PALS 2025 Guidelines. It is not a substitute for formal PALS Provider certification. Always follow your institution's protocols and current guidelines.

---

*Built with ❤️ for every healthcare professional saving pediatric lives.*
