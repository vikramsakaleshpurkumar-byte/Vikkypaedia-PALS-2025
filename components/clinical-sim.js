/**
 * Advanced Clinical Simulator Component (Code Blue ER)
 */

export class ClinicalSimulator {
  constructor(containerEl) {
    this.containerEl = containerEl;
    this.timer = null;
    this.time = 0;
    this.cprActive = false;
    this.cprTimer = 0;
    this.epiDoses = 0;
    this.shocks = 0;
    
    // Patient State Machine
    this.patient = {
      rhythm: 'VFib',
      hr: '---',
      spo2: '---',
      bp: '---/---',
      rr: 0,
      state: 'arrest' // arrest, cpr, rosc, dead
    };
    
    this.logs = [];
  }

  start() {
    this.time = 0;
    this.cprActive = false;
    this.cprTimer = 0;
    this.epiDoses = 0;
    this.shocks = 0;
    this.patient = { rhythm: 'VFib', hr: '---', spo2: '---', bp: '---/---', rr: 0, state: 'arrest' };
    this.logs = [];
    
    this.log('Patient arrives in ER. 5-year-old child, unresponsive, apneic. No palpable pulse.', 'critical');
    
    this.render();
    this.timer = setInterval(() => this.tick(), 1000);
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
  }

  tick() {
    this.time++;
    
    // CPR Logic
    if (this.cprActive) {
      this.cprTimer++;
      if (this.cprTimer >= 120) {
        this.cprActive = false;
        this.log('2 minutes of CPR completed. Pause for rhythm check.', 'critical');
        this.patient.hr = '---';
        this.patient.bp = '---/---';
        this.patient.spo2 = '---';
      } else {
        // Mock CPR vitals
        this.patient.hr = '110';
        this.patient.bp = '60/40';
        this.patient.spo2 = '88';
      }
    }

    this.updateUI();
  }

  formatTime(s) {
    const mins = Math.floor(s / 60).toString().padStart(2, '0');
    const secs = (s % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  }

  log(msg, type = 'normal') {
    this.logs.unshift({ time: this.formatTime(this.time), msg, type });
    this.updateLogUI();
  }

  handleAction(action) {
    switch(action) {
      case 'cpr':
        if (this.patient.state === 'rosc') {
          this.log('Patient has ROSC. CPR not indicated.');
          return;
        }
        this.cprActive = true;
        this.cprTimer = 0;
        this.log('Initiated high-quality CPR (15:2 ratio).', 'success');
        break;
      
      case 'shock':
        if (this.patient.rhythm !== 'VFib') {
          this.log(`Defibrillation not indicated for ${this.patient.rhythm}.`);
          return;
        }
        if (!this.cprActive && this.cprTimer === 0 && this.time > 10) {
           this.log('Shock delivered. Note: Minimize interruptions in CPR!', 'critical');
        } else {
           this.log(`Shock delivered at 2J/kg.`, 'success');
        }
        this.shocks++;
        
        // State transition logic
        if (this.shocks >= 2 && this.epiDoses >= 1) {
          this.patient.rhythm = 'Sinus';
          this.patient.state = 'rosc';
          this.patient.hr = 115;
          this.patient.bp = '90/60';
          this.patient.spo2 = 98;
          this.patient.rr = 16;
          this.cprActive = false;
          this.log('ROSC Achieved! Palpable pulse present.', 'success');
          setTimeout(() => this.endGame(true), 2000);
        } else {
          this.log('Rhythm remains VFib. Resume CPR immediately.');
          this.cprActive = true;
          this.cprTimer = 0;
        }
        break;

      case 'epi':
        if (this.patient.state === 'rosc') return;
        this.epiDoses++;
        this.log(`Epinephrine 0.01 mg/kg IV/IO given (Dose ${this.epiDoses}).`, 'success');
        break;

      case 'amio':
        if (this.shocks < 2) {
          this.log('Amiodarone is indicated AFTER 2nd shock for refractory VFib.', 'critical');
        } else {
          this.log('Amiodarone 5 mg/kg IV/IO given.', 'success');
        }
        break;
        
      case 'airway':
        this.log('Bag-mask ventilation optimized. 100% O2 attached.');
        break;
        
      case 'assess':
        if (this.patient.state === 'rosc') {
          this.log(`Pulse: Strong. Cap refill: 2s. Breathing: Spontaneous.`, 'success');
        } else {
          this.log('Pulse: None. Cap refill: N/A. Breathing: Apneic.', 'critical');
        }
        break;
    }
    this.updateUI();
  }

  endGame(win) {
    this.stop();
    if (win) {
      if (typeof confetti === 'function') confetti({ particleCount: 150, spread: 80 });
      this.log('SCENARIO COMPLETE: Successful Resuscitation!', 'success');
    }
  }

  render() {
    this.containerEl.innerHTML = `
      <div class="sim-overlay">
        <!-- Vitals Monitor -->
        <div class="sim-monitor">
          <div class="monitor-box monitor-hr">
            <div class="monitor-label">HR / ECG</div>
            <div class="monitor-val" id="sim-val-hr">${this.patient.hr}</div>
            <div class="monitor-wave" id="sim-wave-hr"></div>
          </div>
          <div class="monitor-box monitor-spo2">
            <div class="monitor-label">SpO2 %</div>
            <div class="monitor-val" id="sim-val-spo2">${this.patient.spo2}</div>
            <div class="monitor-wave"></div>
          </div>
          <div class="monitor-box monitor-bp">
            <div class="monitor-label">NIBP mmHg</div>
            <div class="monitor-val" style="font-size: 2.5rem; margin-top:1.2rem" id="sim-val-bp">${this.patient.bp}</div>
          </div>
          <div class="monitor-box monitor-rr">
            <div class="monitor-label">RESP</div>
            <div class="monitor-val" id="sim-val-rr">${this.patient.rr}</div>
          </div>
        </div>

        <div class="sim-body">
          <!-- Log Panel -->
          <div class="sim-log" id="sim-log-panel"></div>

          <!-- Controls Panel -->
          <div class="sim-controls">
            <div class="sim-timer-bar" id="sim-timer-display">00:00</div>
            
            <div class="sim-actions">
              <div class="action-group">
                <h4>Assess & Airway</h4>
                <div class="action-grid">
                  <button class="sim-btn" data-act="assess">Check Pulse/Rhythm</button>
                  <button class="sim-btn" data-act="airway">Bag-Mask Vent</button>
                </div>
              </div>
              
              <div class="action-group">
                <h4>Resuscitation</h4>
                <div class="action-grid">
                  <button class="sim-btn" style="background: var(--accent-primary);" data-act="cpr">Start/Resume CPR</button>
                  <button class="sim-btn" style="background: var(--accent-danger);" data-act="shock">Defibrillate (Shock)</button>
                </div>
              </div>
              
              <div class="action-group">
                <h4>Medications</h4>
                <div class="action-grid">
                  <button class="sim-btn" data-act="epi">Epinephrine</button>
                  <button class="sim-btn" data-act="amio">Amiodarone</button>
                </div>
              </div>
            </div>
            
            <div style="padding: 1rem; text-align: center; border-top: 1px solid #333;">
              <button class="sim-btn sim-exit-btn" style="width: 100%; background: var(--accent-danger);">✕ Exit Simulator</button>
            </div>
          </div>
        </div>
      </div>
    `;

    this.containerEl.querySelectorAll('.sim-btn[data-act]').forEach(btn => {
      btn.addEventListener('click', (e) => this.handleAction(e.target.dataset.act));
    });

    // Exit button
    const exitBtn = this.containerEl.querySelector('.sim-exit-btn');
    if (exitBtn) {
      exitBtn.addEventListener('click', () => {
        this.stop();
        const overlay = this.containerEl.querySelector('.sim-overlay');
        if (overlay) overlay.remove();
      });
    }
    this.updateUI();
  }

  updateUI() {
    const elHr = this.containerEl.querySelector('#sim-val-hr');
    const elSpo2 = this.containerEl.querySelector('#sim-val-spo2');
    const elBp = this.containerEl.querySelector('#sim-val-bp');
    const elRr = this.containerEl.querySelector('#sim-val-rr');
    const elWave = this.containerEl.querySelector('#sim-wave-hr');
    const elTime = this.containerEl.querySelector('#sim-timer-display');

    if (elHr) elHr.textContent = this.patient.hr;
    if (elSpo2) elSpo2.textContent = this.patient.spo2;
    if (elBp) elBp.textContent = this.patient.bp;
    if (elRr) elRr.textContent = this.patient.rr;
    if (elTime) elTime.textContent = this.formatTime(this.time);

    if (elWave) {
      elWave.className = 'monitor-wave ' + (this.patient.rhythm === 'VFib' ? 'vf' : '');
    }
  }

  updateLogUI() {
    const panel = this.containerEl.querySelector('#sim-log-panel');
    if (!panel) return;
    
    panel.innerHTML = this.logs.map(l => `
      <div class="log-entry ${l.type}">
        <span class="log-time">[${l.time}]</span> ${l.msg}
      </div>
    `).join('');
  }
}
