/**
 * Clinical Simulator Component
 */

export class ClinicalSimulator {
    /**
     * @param {HTMLElement} containerEl 
     * @param {Object} scenarioData 
     */
    constructor(containerEl, scenarioData) {
        this.containerEl = containerEl;
        this.scenario = scenarioData;
        this.currentStepIdx = 0;
        this.score = 0;
        this.vitals = { ...this.scenario.initialVitals };
        this.timer = null;
        this.seconds = 0;
    }

    start() {
        this.currentStepIdx = 0;
        this.score = 0;
        this.seconds = 0;
        this.vitals = { ...this.scenario.initialVitals };
        
        this.timer = setInterval(() => {
            this.seconds++;
            this.updateTimerDisplay();
        }, 1000);
        
        this.render();
    }

    makeDecision(optionId) {
        const step = this.scenario.steps[this.currentStepIdx];
        const opt = step.options.find(o => o.id === optionId);
        
        if (!opt) return;

        if (opt.correct) {
            this.score += 10;
        } else if (opt.penalty) {
            this.score -= 5;
        }

        this.updateVitals(opt);
        this.showFeedback(opt, () => {
            if (opt.nextStep === 'end' || this.currentStepIdx >= this.scenario.steps.length - 1) {
                this.end();
            } else {
                // Find next step idx
                const nextIdx = this.scenario.steps.findIndex(s => s.id === opt.nextStep);
                if (nextIdx !== -1) {
                    this.currentStepIdx = nextIdx;
                    this.render();
                } else {
                    this.end();
                }
            }
        });
    }

    updateVitals(option = null) {
        // Mock logic for changing vitals based on decisions
        // E.g. if correct med given, HR improves
        if (option && option.correct) {
            if (this.vitals.hr === 0) this.vitals.hr = 60; // ROSC mock
        }
    }

    showFeedback(option, callback) {
        const fbEl = this.containerEl.querySelector('#sim-feedback');
        fbEl.innerHTML = `<div class="${option.correct ? 'text-accent-success' : 'text-accent-danger'}">${option.feedback}</div>`;
        fbEl.style.display = 'block';
        
        setTimeout(() => {
            fbEl.style.display = 'none';
            callback();
        }, 2500);
    }

    end() {
        clearInterval(this.timer);
        this.containerEl.innerHTML = `
            <div class="sim-debrief">
                <h2>Scenario Complete</h2>
                <p>Time: ${this.seconds}s</p>
                <p>Score: ${this.score}</p>
                <button onclick="this.start()">Restart</button>
            </div>
        `;
    }

    render() {
        if (!this.containerEl) return;
        const step = this.scenario.steps[this.currentStepIdx];
        
        this.containerEl.innerHTML = `
            <div class="sim-container bg-bg-secondary text-text-primary p-4 rounded">
                <div class="vitals-monitor bg-bg-primary text-accent-success p-2 font-mono flex gap-4 mb-4">
                    <span>HR: ${this.vitals.hr}</span>
                    <span>RR: ${this.vitals.rr}</span>
                    <span>SpO2: ${this.vitals.spo2}</span>
                    <span>BP: ${this.vitals.bp}</span>
                    <span>Rhythm: ${this.vitals.rhythm}</span>
                    <span id="sim-timer" class="ml-auto">Time: ${this.seconds}s</span>
                </div>
                
                <div class="sim-narrative mb-4">
                    <p>${step.narrative}</p>
                    <p class="font-bold">${step.prompt}</p>
                </div>
                
                <div class="sim-options flex flex-col gap-2">
                    ${step.options.map(o => `<button class="sim-opt-btn bg-bg-primary p-2 border border-border-glass rounded text-left hover:bg-bg-glass" data-id="${o.id}">${o.text}</button>`).join('')}
                </div>
                
                <div id="sim-feedback" class="mt-4 p-2 rounded" style="display:none;"></div>
            </div>
        `;

        this.containerEl.querySelectorAll('.sim-opt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.makeDecision(e.target.dataset.id));
        });
    }

    updateTimerDisplay() {
        const el = this.containerEl?.querySelector('#sim-timer');
        if (el) el.innerText = `Time: ${this.seconds}s`;
    }
}
