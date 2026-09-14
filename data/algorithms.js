export const algorithms = {
  cardiacArrest: {
    title: "Pediatric Cardiac Arrest Algorithm",
    description: "Step-by-step interactive pathway for managing VF/pVT and Asystole/PEA.",
    startNode: "node_start",
    nodes: {
      "node_start": {
        text: "Start CPR\n• Begin bag-mask ventilation\n• Give 100% Oxygen\n• Attach monitor/defibrillator",
        type: "action",
        options: [
          { text: "Rhythm is Shockable (VF/pVT)", next: "node_vf" },
          { text: "Rhythm is Non-shockable (Asystole/PEA)", next: "node_asystole" }
        ]
      },
      "node_vf": {
        text: "VF / pVT Detected",
        type: "decision",
        options: [
          { text: "Deliver Shock (2 J/kg)", next: "node_cpr_1" }
        ]
      },
      "node_cpr_1": {
        text: "CPR 2 min\n• IV/IO access",
        type: "action",
        options: [
          { text: "Check Rhythm", next: "node_rhythm_check_1" }
        ]
      },
      "node_rhythm_check_1": {
        text: "Is rhythm still shockable?",
        type: "decision",
        options: [
          { text: "Yes (Shockable)", next: "node_shock_2" },
          { text: "No (Non-shockable)", next: "node_check_pulse" }
        ]
      },
      "node_shock_2": {
        text: "Deliver Shock (4 J/kg)",
        type: "action",
        options: [
          { text: "Continue CPR", next: "node_cpr_2" }
        ]
      },
      "node_cpr_2": {
        text: "CPR 2 min\n• Epinephrine every 3-5 min\n• Consider advanced airway",
        type: "action",
        options: [
          { text: "Check Rhythm", next: "node_rhythm_check_2" }
        ]
      },
      "node_rhythm_check_2": {
        text: "Is rhythm still shockable?",
        type: "decision",
        options: [
          { text: "Yes", next: "node_shock_3" },
          { text: "No", next: "node_check_pulse" }
        ]
      },
      "node_shock_3": {
        text: "Deliver Shock (≥4 J/kg, max 10 J/kg or adult dose)",
        type: "action",
        options: [
          { text: "Continue CPR", next: "node_cpr_3" }
        ]
      },
      "node_cpr_3": {
        text: "CPR 2 min\n• Amiodarone or Lidocaine\n• Treat reversible causes (H's and T's)",
        type: "action",
        options: [
          { text: "Check Rhythm", next: "node_rhythm_check_1" } // loops back
        ]
      },
      "node_asystole": {
        text: "Asystole / PEA Detected",
        type: "decision",
        options: [
          { text: "Give Epinephrine ASAP", next: "node_epi_asystole" }
        ]
      },
      "node_epi_asystole": {
        text: "CPR 2 min\n• IV/IO access\n• Epinephrine every 3-5 min\n• Consider advanced airway",
        type: "action",
        options: [
          { text: "Check Rhythm", next: "node_rhythm_check_asystole" }
        ]
      },
      "node_rhythm_check_asystole": {
        text: "Is rhythm shockable?",
        type: "decision",
        options: [
          { text: "Yes (Shockable)", next: "node_vf" },
          { text: "No (Non-shockable)", next: "node_cpr_asystole_2" }
        ]
      },
      "node_cpr_asystole_2": {
        text: "CPR 2 min\n• Treat reversible causes (H's and T's)",
        type: "action",
        options: [
          { text: "Check Rhythm", next: "node_rhythm_check_asystole" } // loop
        ]
      },
      "node_check_pulse": {
        text: "Check for signs of return of spontaneous circulation (ROSC).",
        type: "decision",
        options: [
          { text: "Pulse Present (ROSC)", next: "node_rosc" },
          { text: "No Pulse", next: "node_asystole" }
        ]
      },
      "node_rosc": {
        text: "ROSC Achieved!\n• Go to Post-Cardiac Arrest Care",
        type: "end",
        options: [
          { text: "Restart Algorithm", next: "node_start" }
        ]
      }
    }
  }
};
