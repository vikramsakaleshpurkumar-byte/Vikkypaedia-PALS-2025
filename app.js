/**
 * PALS 2025 MOOC — Main Application Engine (v2)
 * 
 * REDESIGNED for world-class guided learning experience:
 * - Sequential unit flow (complete one → unlock next)
 * - Three-tier content within each unit (Must/Nice/Good to Know)
 * - Unit progress stepper with connected dots
 * - Breadcrumb navigation
 * - "Complete & Continue →" guided progression
 */

import { QuizEngine } from './components/quiz-engine.js';
import { FlashcardEngine } from './components/flashcard-engine.js';
import { AlgorithmViewer } from './components/algorithm-viewer.js';
import { ClinicalSimulator } from './components/clinical-sim.js';
import { ProgressTracker } from './components/progress-tracker.js';

/* ──────────────────────────────────────────
   1. Global Event Bus & State
   ────────────────────────────────────────── */
window.PALSApp = {
  state: { 
    currentModuleId: null, 
    currentUnitIndex: 0,
    profile: JSON.parse(localStorage.getItem('pals-profile')) || { role: 'PG', mode: 'all' }
  },
  events: new EventTarget(),
  emit(ev, detail) { this.events.dispatchEvent(new CustomEvent(ev, { detail })); },
  on(ev, fn) { this.events.addEventListener(ev, fn); },
  data: { curriculum: null, medications: null, vitalSigns: null },
};

/* ──────────────────────────────────────────
   2. Application Class
   ────────────────────────────────────────── */
class PALSApplication {
  constructor() {
    this.progress = new ProgressTracker();
    this.flashcards = null;
    this.currentQuiz = null;
    this.quizPassed = false;
  }

  /* ── Initialization ── */
  async init() {
    await this.loadData();
    this.bindGlobalListeners();
    this.renderSidebar();
    this.updateOverallProgress();
    
    // Set initial role label
    const roleLabel = document.getElementById('course-role-label');
    if (roleLabel) roleLabel.textContent = window.PALSApp.state.profile.role + ' Track';

    const last = this.progress.getLastActive();
    this.navigateTo(last?.moduleId || 'module-01', last?.unitIndex || 0);
  }

  async loadData() {
    try {
      const [curriculum, medications, vitalSigns] = await Promise.all([
        fetch('data/curriculum.json').then(r => r.json()),
        fetch('data/medications.json').then(r => r.json()),
        fetch('data/vital-signs.json').then(r => r.json()),
      ]);
      window.PALSApp.data.curriculum = curriculum;
      window.PALSApp.data.medications = medications;
      window.PALSApp.data.vitalSigns = vitalSigns;
    } catch (err) {
      console.error('Data load failed:', err);
      this.toast('Failed to load course data. Please refresh.', 'error');
    }
  }

  /* ────────────────────────────────────
     SIDEBAR
     ──────────────────────────────────── */
  renderSidebar() {
    const el = document.getElementById('sidebar-modules');
    const curriculum = window.PALSApp.data.curriculum;
    if (!el || !curriculum) return;

    el.innerHTML = curriculum.modules.map(mod => {
      const prog = this.progress.getModuleProgress(mod.id);
      const isCurrent = mod.id === window.PALSApp.state.currentModuleId;
      const isLocked = this.isModuleLocked(mod);
      const isComplete = prog.percentage >= 100;

      return `
        <li class="sb-module ${isCurrent ? 'active' : ''} ${isLocked ? 'locked' : ''} ${isComplete ? 'complete' : ''}"
            data-module-id="${mod.id}" ${isLocked ? '' : ''}>
          <div class="sb-module-icon">${isComplete ? '✅' : isLocked ? '🔒' : mod.icon}</div>
          <div class="sb-module-body">
            <span class="sb-module-num">Module ${mod.number}</span>
            <span class="sb-module-title">${mod.title}</span>
            <div class="sb-progress-track">
              <div class="sb-progress-fill" style="width:${prog.percentage}%"></div>
            </div>
          </div>
        </li>
      `;
    }).join('');

    el.querySelectorAll('.sb-module:not(.locked)').forEach(item => {
      item.addEventListener('click', () => {
        this.navigateTo(item.dataset.moduleId, 0);
      });
    });
  }

  isModuleLocked(mod) {
    const curriculum = window.PALSApp.data.curriculum;
    const idx = curriculum.modules.findIndex(m => m.id === mod.id);
    if (idx <= 0) return false; // Module 1 never locked
    // Module is locked if previous module has < 50% completion
    const prevMod = curriculum.modules[idx - 1];
    const prevProg = this.progress.getModuleProgress(prevMod.id);
    return prevProg.percentage < 50;
  }

  /* ────────────────────────────────────
     NAVIGATION
     ──────────────────────────────────── */
  navigateTo(moduleId, unitIndex = 0) {
    const curriculum = window.PALSApp.data.curriculum;
    if (!curriculum) return;

    const mod = curriculum.modules.find(m => m.id === moduleId);
    if (!mod) return;

    const units = mod.units || [];
    unitIndex = Math.max(0, Math.min(unitIndex, units.length - 1));

    window.PALSApp.state.currentModuleId = moduleId;
    window.PALSApp.state.currentUnitIndex = unitIndex;
    this.progress.setLastActive(moduleId, unitIndex);
    this.quizPassed = false;

    this.renderSidebar();
    this.renderBreadcrumbs(mod, units[unitIndex]);
    this.renderUnitStepper(mod, unitIndex);
    this.renderUnitContent(mod, units[unitIndex], unitIndex);
    this.updateOverallProgress();
    this.updateCompleteButton(mod, units[unitIndex], unitIndex);

    // Close mobile sidebar
    document.getElementById('sidebar')?.classList.remove('open');

    // Scroll to top of learning area
    document.getElementById('learning-area')?.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ────────────────────────────────────
     BREADCRUMBS
     ──────────────────────────────────── */
  renderBreadcrumbs(mod, unit) {
    const el = document.getElementById('breadcrumbs');
    if (!el) return;
    el.innerHTML = `
      <span class="crumb crumb-root">PALS 2025</span>
      <span class="crumb-sep">›</span>
      <span class="crumb crumb-module" data-module-id="${mod.id}">Module ${mod.number}: ${mod.title}</span>
      ${unit ? `
        <span class="crumb-sep">›</span>
        <span class="crumb crumb-unit">${unit.title}</span>
      ` : ''}
    `;
    el.querySelector('.crumb-module')?.addEventListener('click', () => {
      this.navigateTo(mod.id, 0);
    });
  }

  /* ────────────────────────────────────
     UNIT PROGRESS STEPPER
     ──────────────────────────────────── */
  renderUnitStepper(mod, currentIdx) {
    const el = document.getElementById('unit-stepper');
    if (!el) return;
    const units = mod.units || [];

    let html = '<div class="stepper-dots">';
    units.forEach((unit, i) => {
      const isComplete = this.progress.isUnitComplete(mod.id, unit.id);
      const isCurrent = i === currentIdx;
      const isLocked = i > 0 && !this.isUnitAccessible(mod, i);

      let dotClass = 'step-dot';
      if (isComplete) dotClass += ' completed';
      else if (isCurrent) dotClass += ' current';
      else if (isLocked) dotClass += ' locked';

      if (i > 0) {
        const connClass = isComplete || isCurrent ? 'step-conn filled' : 'step-conn';
        html += `<div class="${connClass}"></div>`;
      }

      html += `<div class="${dotClass}" data-unit-index="${i}" title="${unit.title}">
        ${isComplete ? '✓' : isLocked ? '🔒' : i + 1}
      </div>`;
    });
    html += '</div>';
    html += `<div class="stepper-label">Unit ${currentIdx + 1} of ${units.length}</div>`;
    el.innerHTML = html;

    // Allow clicking accessible dots
    el.querySelectorAll('.step-dot:not(.locked)').forEach(dot => {
      dot.addEventListener('click', () => {
        const idx = parseInt(dot.dataset.unitIndex);
        this.navigateTo(mod.id, idx);
      });
    });
  }

  isUnitAccessible(mod, unitIndex) {
    if (unitIndex === 0) return true;
    const prevUnit = mod.units[unitIndex - 1];
    return this.progress.isUnitComplete(mod.id, prevUnit.id);
  }

  /* ────────────────────────────────────
     UNIT CONTENT RENDERING (Three-Tier)
     ──────────────────────────────────── */
  renderUnitContent(mod, unit, unitIndex) {
    if (!unit) {
      this.renderPlaceholder(mod);
      return;
    }

    // Unit header
    const headerEl = document.getElementById('unit-header');
    if (headerEl) {
      headerEl.innerHTML = `
        <div class="uh-top">
          <span class="uh-number">Unit ${unitIndex + 1}</span>
          <span class="uh-time">⏱️ ${unit.estimatedMinutes || 5} min</span>
        </div>
        <h2 class="uh-title">${unit.title}</h2>
      `;
    }

    // Three-tier content
    const tierEl = document.getElementById('tier-content');
    if (!tierEl) return;

    tierEl.innerHTML = '';

    // 🔴 MUST KNOW — always open
    tierEl.innerHTML += this.renderTierSection('must', '🔴', 'Must Know',
      'Critical — You must master this', unit.mustKnow, false);

    // 🟡 NICE TO KNOW — collapsible, starts collapsed (skip if must-only)
    if (unit.niceToKnow?.points?.length > 0 && window.PALSApp.state.profile.mode !== 'must-only') {
      tierEl.innerHTML += this.renderTierSection('nice', '🟡', 'Nice to Know',
        'Important context — Deepen your understanding', unit.niceToKnow, true);
    }

    // 🟢 GOOD TO KNOW — collapsible, starts collapsed (skip if must-only)
    if (unit.goodToKnow?.points?.length > 0 && window.PALSApp.state.profile.mode !== 'must-only') {
      tierEl.innerHTML += this.renderTierSection('good', '🟢', 'Good to Know',
        'Enrichment — Go deeper if you\'re curious', unit.goodToKnow, true);
    }

    // Set up accordions
    tierEl.querySelectorAll('.tier-toggle').forEach(toggle => {
      toggle.addEventListener('click', () => {
        const section = toggle.closest('.tier-section');
        section.classList.toggle('collapsed');
        const chevron = toggle.querySelector('.tier-chevron');
        if (chevron) chevron.textContent = section.classList.contains('collapsed') ? '▼' : '▲';
      });
    });

    // Initialize must-know quiz
    this.initMustKnowQuiz(mod, unit);
  }

  renderTierSection(tier, icon, title, subtitle, data, collapsible) {
    const contentHTML = (data?.points || []).map(pt => this.renderPoint(pt)).join('');
    const collapsed = collapsible ? ' collapsed' : '';
    const headerTag = collapsible ? 'button' : 'div';
    const toggleClass = collapsible ? ' tier-toggle' : '';
    const chevron = collapsible ? '<span class="tier-chevron">▼</span>' : '';

    return `
      <section class="tier-section tier-${tier}${collapsed}">
        <${headerTag} class="tier-header${toggleClass}">
          <span class="tier-icon">${icon}</span>
          <div class="tier-header-text">
            <h3>${title}</h3>
            <span class="tier-subtitle">${subtitle}</span>
          </div>
          ${chevron}
        </${headerTag}>
        <div class="tier-body">
          ${contentHTML}
          ${tier === 'must' && data?.quiz?.length > 0 ? `
            <div class="tier-quiz-area">
              <h4 class="quiz-title">📝 Knowledge Check</h4>
              <div id="must-quiz-container"></div>
            </div>
          ` : ''}
        </div>
      </section>
    `;
  }

  renderPoint(pt) {
    let html = '';
    switch (pt.type) {
      case 'callout':
        html = `
          <div class="content-callout">
            <span class="callout-marker">⚡</span>
            <div>
              ${pt.heading ? `<strong>${pt.heading}</strong><br>` : ''}
              <p>${this.fmt(pt.body)}</p>
            </div>
          </div>`;
        break;

      case 'list':
        html = `
          <div class="content-block">
            ${pt.heading ? `<h4>${pt.heading}</h4>` : ''}
            <ul class="content-list">
              ${(pt.items || []).map(li => `<li>${this.fmt(li)}</li>`).join('')}
            </ul>
          </div>`;
        break;

      case 'table':
        html = `
          <div class="content-block table-wrap">
            ${pt.heading ? `<h4>${pt.heading}</h4>` : ''}
            <div class="table-scroll">
              <table>
                <thead><tr>${(pt.headers || []).map(h => `<th>${h}</th>`).join('')}</tr></thead>
                <tbody>${(pt.rows || []).map(row =>
                  `<tr>${row.map(c => `<td>${c}</td>`).join('')}</tr>`
                ).join('')}</tbody>
              </table>
            </div>
          </div>`;
        break;

      default: // 'text'
        html = `
          <div class="content-block">
            ${pt.heading ? `<h4>${pt.heading}</h4>` : ''}
            <p>${this.fmt(pt.body || '')}</p>
          </div>`;
        break;
    }

    if (pt.imageUrl) {
      html += `
        <div class="content-image-wrapper">
          <img src="${pt.imageUrl}" alt="${pt.heading || 'Illustration'}" class="content-image" loading="lazy">
        </div>`;
    }

    return html;
  }

  fmt(text) {
    if (!text) return '';
    return text
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>');
  }

  /* ────────────────────────────────────
     MUST-KNOW QUIZ
     ──────────────────────────────────── */
  initMustKnowQuiz(mod, unit) {
    const container = document.getElementById('must-quiz-container');
    if (!container || !unit.mustKnow?.quiz?.length) {
      this.quizPassed = true; // No quiz means auto-pass
      this.updateCompleteButton(mod, unit, window.PALSApp.state.currentUnitIndex);
      return;
    }

    const questions = unit.mustKnow.quiz.map(q => ({
      text: q.stem,
      options: q.options.map((opt, i) => ({
        text: typeof opt === 'string' ? opt : opt.text,
        correct: i === q.correctIndex,
      })),
      rationale: q.rationale || '',
    }));

    this.currentQuiz = new QuizEngine(container, questions, {
      onComplete: (score) => {
        this.quizPassed = score.percentage >= 80;
        if (this.quizPassed) {
          this.progress.markQuizPassed(mod.id, unit.id, score.percentage);
          this.toast(`Knowledge check passed! ${score.percentage}%`, 'success');
        } else {
          this.toast(`You need 80% to continue. Try again!`, 'error');
        }
        this.updateCompleteButton(mod, unit, window.PALSApp.state.currentUnitIndex);
      }
    });
    this.currentQuiz.render();
  }

  /* ────────────────────────────────────
     COMPLETE & CONTINUE BUTTON
     ──────────────────────────────────── */
  updateCompleteButton(mod, unit, unitIndex) {
    const btn = document.getElementById('btn-complete');
    if (!btn) return;

    const isAlreadyComplete = this.progress.isUnitComplete(mod.id, unit?.id);
    const units = mod.units || [];
    const isLastUnit = unitIndex >= units.length - 1;
    const hasQuiz = unit?.mustKnow?.quiz?.length > 0;
    const canComplete = !hasQuiz || this.quizPassed || isAlreadyComplete;

    if (isAlreadyComplete) {
      // Already done — show "Continue to Next"
      if (isLastUnit) {
        btn.innerHTML = '<span>Module Complete ✅</span>';
        btn.className = 'btn-complete completed';
        btn.disabled = false;
        btn.onclick = () => this.goToNextModule(mod);
      } else {
        btn.innerHTML = `<span>Continue to: ${units[unitIndex + 1]?.title}</span><span class="btn-arrow">→</span>`;
        btn.className = 'btn-complete';
        btn.disabled = false;
        btn.onclick = () => this.navigateTo(mod.id, unitIndex + 1);
      }
    } else if (canComplete) {
      // Ready to complete
      btn.innerHTML = '<span>Complete & Continue</span><span class="btn-arrow">→</span>';
      btn.className = 'btn-complete ready';
      btn.disabled = false;
      btn.onclick = () => {
        this.progress.markUnitComplete(mod.id, unit.id);
        this.toast('Unit completed! 🎉', 'success');
        this.renderUnitStepper(mod, unitIndex);
        this.updateOverallProgress();
        this.renderSidebar();

        // Auto-advance after brief delay
        setTimeout(() => {
          if (!isLastUnit) {
            this.navigateTo(mod.id, unitIndex + 1);
          } else {
            this.goToNextModule(mod);
          }
        }, 800);
      };
    } else {
      // Quiz not passed yet
      btn.innerHTML = '<span>🔒 Pass the Knowledge Check to continue</span>';
      btn.className = 'btn-complete locked';
      btn.disabled = true;
      btn.onclick = null;
    }
  }

  goToNextModule(currentMod) {
    const curriculum = window.PALSApp.data.curriculum;
    const idx = curriculum.modules.findIndex(m => m.id === currentMod.id);
    if (idx < curriculum.modules.length - 1) {
      this.navigateTo(curriculum.modules[idx + 1].id, 0);
    } else {
      this.toast('🏆 Congratulations! You have completed the course!', 'success');
    }
  }

  /* ────────────────────────────────────
     PROGRESS
     ──────────────────────────────────── */
  updateOverallProgress() {
    const overall = this.progress.getOverallProgress(window.PALSApp.data.curriculum);
    const fill = document.querySelector('.nav-progress-fill');
    const pct = document.querySelector('.nav-progress-pct');
    if (fill) fill.style.width = `${overall.percentage}%`;
    if (pct) pct.textContent = `${overall.percentage}%`;
  }

  /* ────────────────────────────────────
     PLACEHOLDER
     ──────────────────────────────────── */
  renderPlaceholder(mod) {
    const tierEl = document.getElementById('tier-content');
    if (!tierEl) return;
    tierEl.innerHTML = `
      <div class="placeholder-card">
        <div class="placeholder-icon">${mod.icon}</div>
        <h3>${mod.title}</h3>
        <p>This module is coming soon with full interactive content.</p>
        <h4>You'll learn:</h4>
        <ul>${(mod.learningObjectives || []).map(o => `<li>${o}</li>`).join('')}</ul>
      </div>
    `;
  }

  /* ────────────────────────────────────
     MODALS
     ──────────────────────────────────── */
  showModal(title, html) {
    const overlay = document.getElementById('modal-overlay');
    if (!overlay) return;
    overlay.innerHTML = `
      <div class="modal-backdrop" id="modal-backdrop"></div>
      <div class="modal-panel">
        <div class="modal-head">
          <h2>${title}</h2>
          <button class="modal-x" id="modal-x">&times;</button>
        </div>
        <div class="modal-body">${html}</div>
      </div>
    `;
    overlay.classList.add('visible');
    document.getElementById('modal-x')?.addEventListener('click', () => this.closeModal());
    document.getElementById('modal-backdrop')?.addEventListener('click', () => this.closeModal());
  }

  closeModal() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
      overlay.classList.remove('visible');
      overlay.innerHTML = '';
    }
  }

  showMedsModal() {
    const meds = window.PALSApp.data.medications?.medications || [];
    const html = meds.map(m => `
      <div class="med-row">
        <div class="med-name">${m.name}</div>
        <div class="med-class">${m.class || ''}</div>
        <div class="med-dose-list">
          ${Object.entries(m.doses || {}).map(([k, v]) =>
            `<div class="med-dose-item"><span class="dose-label">${k}:</span> <span class="dose-val">${typeof v === 'object' ? v.dose || '' : v}</span></div>`
          ).join('')}
        </div>
      </div>
    `).join('');
    this.showModal('💊 PALS Medications Reference', `<div class="meds-grid">${html}</div>`);
  }

  showProgressModal() {
    const html = '<div id="prog-dash"></div>';
    this.showModal('📊 My Progress', html);
    const c = document.getElementById('prog-dash');
    if (c) this.progress.renderProgressDashboard(c, window.PALSApp.data.curriculum);
  }

  showFlashcardsModal() {
    const html = '<div id="fc-container"></div>';
    this.showModal('🃏 Flashcard Review', html);
    const c = document.getElementById('fc-container');
    if (c) {
      if (!this.flashcards) {
        this.flashcards = new FlashcardEngine(c);
        const meds = window.PALSApp.data.medications?.medications || [];
        this.flashcards.addDeck('medications', meds.map(m => ({
          id: `med-${m.name.replace(/\s/g, '-').toLowerCase()}`,
          front: `<h3>${m.name}</h3><p>${(m.indications || []).slice(0, 2).join(', ')}</p>`,
          back: `<h3>${m.name}</h3>${Object.entries(m.doses || {}).map(([k, v]) =>
            `<p><strong>${k}:</strong> ${typeof v === 'object' ? v.dose || '' : v}</p>`).join('')}`,
        })));
      }
      this.flashcards.containerEl = c;
      this.flashcards.render();
    }
  }

  showSettingsModal() {
    const p = window.PALSApp.state.profile;
    const html = `
      <div class="settings-form">
        <p style="margin-bottom: 1.5rem; color: var(--text-secondary);">Customize your learning experience based on your clinical background and available time.</p>
        
        <div class="setting-group">
          <label style="display:block; font-weight:600; margin-bottom:0.5rem;">👤 Your Role</label>
          <select id="set-role" class="settings-select">
            <option value="Nurse" ${p.role==='Nurse'?'selected':''}>Nurse</option>
            <option value="UG" ${p.role==='UG'?'selected':''}>Undergraduate Medical (UG)</option>
            <option value="PG" ${p.role==='PG'?'selected':''}>Postgraduate Resident (PG)</option>
            <option value="Faculty" ${p.role==='Faculty'?'selected':''}>Faculty / Senior Clinician</option>
          </select>
        </div>

        <div class="setting-group" style="margin-top: 1.5rem;">
          <label style="display:block; font-weight:600; margin-bottom:0.5rem;">📚 Content Depth</label>
          <div class="radio-group" style="display:flex; flex-direction:column; gap:0.5rem;">
            <label class="radio-card" style="display:flex; gap:0.75rem; padding:1rem; border:1px solid var(--border-glass); border-radius:6px; cursor:pointer;">
              <input type="radio" name="set-mode" value="must-only" ${p.mode==='must-only'?'checked':''}>
              <div class="rc-content">
                <strong style="display:block;">Express Mode (Must Know Only)</strong>
                <span style="font-size:0.875rem; color:var(--text-secondary);">Only the absolute critical content & quizzes. Saves time by hiding extra tiers.</span>
              </div>
            </label>
            <label class="radio-card" style="display:flex; gap:0.75rem; padding:1rem; border:1px solid var(--border-glass); border-radius:6px; cursor:pointer;">
              <input type="radio" name="set-mode" value="all" ${p.mode==='all'?'checked':''}>
              <div class="rc-content">
                <strong style="display:block;">Comprehensive (All Tiers)</strong>
                <span style="font-size:0.875rem; color:var(--text-secondary);">Includes "Nice to Know" and "Good to Know" sections. Recommended.</span>
              </div>
            </label>
          </div>
        </div>
        
        <button id="btn-save-settings" class="btn-complete ready" style="margin-top: 2rem; width: 100%;">Save Preferences</button>
      </div>
    `;
    this.showModal('⚙️ Customise Learning', html);
    
    document.getElementById('btn-save-settings').addEventListener('click', () => {
      const role = document.getElementById('set-role').value;
      const mode = document.querySelector('input[name="set-mode"]:checked').value;
      window.PALSApp.state.profile = { role, mode };
      localStorage.setItem('pals-profile', JSON.stringify({ role, mode }));
      this.closeModal();
      this.toast('Preferences saved! Experience updated.', 'success');
      
      // Update UI elements
      document.getElementById('course-role-label').textContent = role + ' Track';
      
      // Re-render current unit to apply depth settings
      const mod = window.PALSApp.data.curriculum.modules.find(m => m.id === window.PALSApp.state.currentModuleId);
      if(mod) {
        const unit = mod.units[window.PALSApp.state.currentUnitIndex];
        this.renderUnitContent(mod, unit, window.PALSApp.state.currentUnitIndex);
      }
    });
  }

  showCertificateModal() {
    const stats = this.progress.getOverallProgress(window.PALSApp.data.curriculum);
    const isComplete = stats.percentage === 100;
    
    let html = '';
    
    if (!isComplete) {
      html = `
        <div style="text-align: center; padding: 2rem;">
          <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">🔒🎓</div>
          <h3 style="margin-bottom: 1rem;">Certificate Locked</h3>
          <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            You have completed <strong>${stats.percentage}%</strong> of the course. 
            Finish all modules and pass all knowledge checks to unlock your official PALS 2025 Certificate!
          </p>
          <div class="sb-progress-track" style="height: 10px; border-radius: 5px; margin-bottom: 2rem;">
            <div class="sb-progress-fill" style="width: ${stats.percentage}%;"></div>
          </div>
          <button class="btn-complete ready no-print" onclick="document.getElementById('modal-overlay').classList.remove('active')">Continue Learning</button>
        </div>
      `;
    } else {
      let userName = localStorage.getItem('pals-user-name') || '';
      
      html = `
        <div id="cert-setup" style="display: ${userName ? 'none' : 'block'}; text-align: center; padding: 2rem;">
          <h3>🎉 Congratulations!</h3>
          <p style="margin: 1rem 0; color: var(--text-secondary);">You've completed the entire course. Enter your name as you want it to appear on your certificate:</p>
          <input type="text" id="cert-name-input" value="${userName}" placeholder="Dr. Jane Doe" style="width: 100%; padding: 1rem; border-radius: 8px; border: 1px solid var(--border-glass); background: var(--bg-tertiary); color: white; font-size: 1.1rem; margin-bottom: 1rem;">
          <button id="btn-generate-cert" class="btn-complete ready">Generate Certificate</button>
        </div>
        
        <div id="cert-display" style="display: ${userName ? 'block' : 'none'};">
          <div class="certificate-wrap certificate-print-area">
            <div class="cert-inner">
              <div class="cert-header">CERTIFICATE OF COMPLETION</div>
              <div class="cert-body">
                <p>This is to formally certify that</p>
                <h1 class="cert-name" id="display-cert-name">${userName}</h1>
                <p>has successfully completed all modules and knowledge checks for</p>
                <h2 class="cert-course">Pediatric Advanced Life Support (PALS) 2025</h2>
                <p class="cert-role">Track: ${window.PALSApp.state.profile.role}</p>
              </div>
              <div class="cert-footer">
                <div class="cert-sig">
                  <div class="sig-line"></div>
                  <p>Course Director<br>Vikkypaedia</p>
                </div>
                <div class="cert-seal">🎓</div>
                <div class="cert-date">
                  <div class="sig-line"></div>
                  <p>Date<br>${new Date().toLocaleDateString()}</p>
                </div>
              </div>
            </div>
          </div>
          <div style="text-align: center; margin-top: 2rem;" class="no-print">
            <button class="btn-complete ready" onclick="window.print()" style="display: inline-flex; width: auto; padding: 0.75rem 2rem; font-size: 1rem;"><span class="quiz-icon">🖨️</span> Print / Save as PDF</button>
            <button class="btn-complete" onclick="document.getElementById('cert-setup').style.display='block'; document.getElementById('cert-display').style.display='none';" style="display: inline-flex; width: auto; padding: 0.75rem 2rem; font-size: 1rem; background: transparent; box-shadow: none; border: 1px solid var(--border-glass);">Edit Name</button>
          </div>
        </div>
      `;
    }
    
    this.showModal('Course Certificate', html);
    
    if (isComplete) {
      const btnGen = document.getElementById('btn-generate-cert');
      if (btnGen) {
        btnGen.addEventListener('click', () => {
          const inputName = document.getElementById('cert-name-input').value.trim();
          if (inputName) {
            localStorage.setItem('pals-user-name', inputName);
            document.getElementById('display-cert-name').textContent = inputName;
            document.getElementById('cert-setup').style.display = 'none';
            document.getElementById('cert-display').style.display = 'block';
            
            // Fire Confetti!
            if (typeof confetti === 'function') {
              var duration = 3000;
              var end = Date.now() + duration;
              (function frame() {
                confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#3b82f6', '#10b981', '#f59e0b'] });
                confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#3b82f6', '#10b981', '#f59e0b'] });
                if (Date.now() < end) { requestAnimationFrame(frame); }
              }());
            }
          }
        });
      }
    }
  }

  /* ────────────────────────────────────
     GLOBAL LISTENERS
     ──────────────────────────────────── */
  bindGlobalListeners() {
    // Mobile menu
    document.getElementById('hamburger')?.addEventListener('click', () => {
      document.getElementById('sidebar')?.classList.toggle('open');
    });

    // Theme toggle
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      document.body.classList.toggle('light-theme');
    });

    // Quick-access buttons
    document.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        if (action === 'settings') this.showSettingsModal();
        if (action === 'certificate') this.showCertificateModal();
        if (action === 'meds') this.showMedsModal();
        if (action === 'algos') this.showModal('🗺️ Algorithms', '<p>Interactive algorithms coming in Phase 2.</p>');
        if (action === 'cards') this.showFlashcardsModal();
        if (action === 'progress') this.showProgressModal();
        if (action === 'learn') document.getElementById('sidebar')?.classList.toggle('open');
      });
    });

    // Keyboard
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeModal();
        document.getElementById('sidebar')?.classList.remove('open');
      }
    });
  }

  /* ── Toast ── */
  toast(msg, type = 'info') {
    const c = document.getElementById('toast-container');
    if (!c) return;
    const t = document.createElement('div');
    t.className = `toast toast-${type}`;
    t.innerHTML = `<span>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span> <span>${msg}</span>`;
    c.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 300); }, 3500);
  }
}

/* ──────────────────────────────────────────
   Bootstrap
   ────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const app = new PALSApplication();
  app.init();
});
