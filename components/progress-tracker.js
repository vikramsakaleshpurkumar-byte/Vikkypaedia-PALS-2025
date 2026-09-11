/**
 * Progress Tracker Component
 * 
 * Tracks module/unit completion, quiz scores, study streaks, and badges.
 * Persists all data to localStorage under 'pals-mooc-progress'.
 */

export class ProgressTracker {
  constructor() {
    this.storageKey = 'pals-mooc-progress';
    this.data = {
      completedUnits: {},   // { moduleId: [unitId, unitId, ...] }
      quizScores: {},       // { moduleId: { unitId: score } }
      lastActive: null,     // { moduleId, unitIndex }
      streaks: { current: 0, lastStudyDate: null },
      badges: [],
      totalTimeMinutes: 0,
    };
    this.load();
  }

  /* ── Persistence ── */
  load() {
    try {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        const parsed = JSON.parse(saved);
        this.data = { ...this.data, ...parsed };
      }
    } catch (e) {
      console.warn('Could not load progress:', e);
    }
  }

  save() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.data));
      window.PALSApp?.emit('progressUpdated', this.data);
    } catch (e) {
      console.warn('Could not save progress:', e);
    }
  }

  /* ── Last Active ── */
  getLastActive() {
    return this.data.lastActive;
  }

  setLastActive(moduleId, unitIndex) {
    this.data.lastActive = { moduleId, unitIndex };
    this.save();
  }

  /* ── Unit Completion ── */
  markUnitComplete(moduleId, unitId) {
    if (!this.data.completedUnits[moduleId]) {
      this.data.completedUnits[moduleId] = [];
    }
    if (!this.data.completedUnits[moduleId].includes(unitId)) {
      this.data.completedUnits[moduleId].push(unitId);
      this.updateStreak();
      this.checkBadges();
      this.save();
    }
  }

  isUnitComplete(moduleId, unitId) {
    return (this.data.completedUnits[moduleId] || []).includes(unitId);
  }

  markQuizPassed(moduleId, unitId, score) {
    if (!this.data.quizScores[moduleId]) this.data.quizScores[moduleId] = {};
    this.data.quizScores[moduleId][unitId] = score;
    if (score >= 84) {
      this.markUnitComplete(moduleId, unitId);
    }
    this.save();
  }

  /* ── Module Progress ── */
  getModuleProgress(moduleId) {
    // Get total units from curriculum data if available
    const curriculum = window.PALSApp?.data?.curriculum;
    const mod = curriculum?.modules?.find(m => m.id === moduleId);
    const totalUnits = mod?.units?.length || 1;
    const completed = (this.data.completedUnits[moduleId] || []).length;

    return {
      completed,
      total: totalUnits,
      percentage: totalUnits > 0 ? Math.round((completed / totalUnits) * 100) : 0,
    };
  }

  /* ── Overall Progress ── */
  getOverallProgress(curriculum) {
    if (!curriculum?.modules) return { completed: 0, total: 0, percentage: 0 };

    let totalUnits = 0;
    let completedUnits = 0;

    curriculum.modules.forEach(mod => {
      const unitCount = mod.units?.length || 0;
      totalUnits += unitCount;
      completedUnits += (this.data.completedUnits[mod.id] || []).length;
    });

    return {
      completed: completedUnits,
      total: totalUnits,
      percentage: totalUnits > 0 ? Math.round((completedUnits / totalUnits) * 100) : 0,
    };
  }

  /* ── Streaks ── */
  updateStreak() {
    const today = new Date().toDateString();
    if (this.data.streaks.lastStudyDate !== today) {
      if (this.data.streaks.lastStudyDate) {
        const last = new Date(this.data.streaks.lastStudyDate);
        const now = new Date();
        const diffMs = Math.abs(now.getTime() - last.getTime());
        const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 1) {
          this.data.streaks.current++;
        } else if (diffDays > 1) {
          this.data.streaks.current = 1;
        }
      } else {
        this.data.streaks.current = 1;
      }
      this.data.streaks.lastStudyDate = today;
    }
  }

  getStreak() {
    return this.data.streaks.current;
  }

  /* ── Badges ── */
  checkBadges() {
    const award = (id) => {
      if (!this.data.badges.includes(id)) {
        this.data.badges.push(id);
        window.PALSApp?.emit('badgeEarned', { id });
      }
    };

    // First Steps: Complete any unit in Module 1
    if ((this.data.completedUnits['module-01'] || []).length > 0) award('first-steps');

    // BLS Master: Complete all units in Module 2
    const curriculum = window.PALSApp?.data?.curriculum;
    const mod2 = curriculum?.modules?.find(m => m.id === 'module-02');
    if (mod2?.units && (this.data.completedUnits['module-02'] || []).length >= mod2.units.length) {
      award('bls-master');
    }

    // Systematic Thinker: Complete Module 4
    const mod4 = curriculum?.modules?.find(m => m.id === 'module-04');
    if (mod4?.units && (this.data.completedUnits['module-04'] || []).length >= mod4.units.length) {
      award('systematic-thinker');
    }

    // 7-Day Streak
    if (this.data.streaks.current >= 7) award('7-day-streak');

    // Perfect Score: Any quiz with 100%
    Object.values(this.data.quizScores).forEach(modScores => {
      Object.values(modScores).forEach(score => {
        if (score >= 100) award('perfect-score');
      });
    });
  }

  getBadges() {
    return this.data.badges;
  }

  /* ── Badge Metadata ── */
  static getBadgeInfo(badgeId) {
    const badges = {
      'first-steps':        { icon: '🏅', title: 'First Steps',        desc: 'Completed your first unit' },
      'bls-master':         { icon: '💓', title: 'BLS Master',         desc: 'Completed all BLS & AED units' },
      'systematic-thinker': { icon: '🔬', title: 'Systematic Thinker', desc: 'Mastered the systematic approach' },
      'pharmacology-pro':   { icon: '💊', title: 'Pharmacology Pro',   desc: 'Reviewed all medication flashcards' },
      'rhythm-reader':      { icon: '⚡', title: 'Rhythm Reader',      desc: 'Identified all 8 core rhythms' },
      'pals-champion':      { icon: '🏆', title: 'PALS Champion',     desc: 'Completed the entire course' },
      '7-day-streak':       { icon: '🔥', title: '7-Day Streak',      desc: 'Studied 7 consecutive days' },
      'perfect-score':      { icon: '🌟', title: 'Perfect Score',      desc: 'Scored 100% on a quiz' },
    };
    return badges[badgeId] || { icon: '🎖️', title: badgeId, desc: '' };
  }

  /* ── Progress Dashboard Renderer ── */
  renderProgressDashboard(containerEl, curriculum) {
    if (!containerEl) return;

    const overall = this.getOverallProgress(curriculum);
    const streak = this.getStreak();
    const badges = this.getBadges();
    const allBadgeIds = ['first-steps', 'bls-master', 'systematic-thinker', 'pharmacology-pro',
                         'rhythm-reader', 'pals-champion', '7-day-streak', 'perfect-score'];

    // Module-by-module progress
    const moduleProgressHTML = (curriculum?.modules || []).map(mod => {
      const prog = this.getModuleProgress(mod.id);
      return `
        <div class="prog-module-row">
          <span class="prog-module-icon">${mod.icon}</span>
          <span class="prog-module-title">${mod.number}. ${mod.title}</span>
          <div class="progress-bar-bg flex-grow">
            <div class="progress-bar-fill" style="width: ${prog.percentage}%"></div>
          </div>
          <span class="prog-module-pct">${prog.percentage}%</span>
        </div>
      `;
    }).join('');

    // Badge gallery
    const badgeGalleryHTML = allBadgeIds.map(id => {
      const info = ProgressTracker.getBadgeInfo(id);
      const earned = badges.includes(id);
      return `
        <div class="badge-card ${earned ? 'earned' : 'locked'}">
          <span class="badge-icon">${earned ? info.icon : '🔒'}</span>
          <span class="badge-title">${info.title}</span>
          <span class="badge-desc">${info.desc}</span>
        </div>
      `;
    }).join('');

    containerEl.innerHTML = `
      <div class="progress-dashboard">
        <!-- Overall Ring -->
        <div class="overall-progress-section">
          <div class="progress-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="54" fill="none" stroke="var(--border-glass)" stroke-width="8"/>
              <circle cx="60" cy="60" r="54" fill="none" stroke="var(--accent-primary)" stroke-width="8"
                stroke-dasharray="${Math.PI * 2 * 54}" 
                stroke-dashoffset="${Math.PI * 2 * 54 * (1 - overall.percentage / 100)}"
                stroke-linecap="round" transform="rotate(-90 60 60)"/>
            </svg>
            <div class="ring-center">
              <span class="ring-pct">${overall.percentage}%</span>
              <span class="ring-label">Complete</span>
            </div>
          </div>
          <div class="overall-stats">
            <div class="stat-item">
              <span class="stat-value">${overall.completed}</span>
              <span class="stat-label">Units Done</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">${overall.total}</span>
              <span class="stat-label">Total Units</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">${streak}</span>
              <span class="stat-label">Day Streak 🔥</span>
            </div>
          </div>
        </div>

        <!-- Module Breakdown -->
        <div class="module-progress-section">
          <h3>Module Progress</h3>
          ${moduleProgressHTML}
        </div>

        <!-- Badges -->
        <div class="badges-section">
          <h3>🏅 Badges (${badges.length}/${allBadgeIds.length})</h3>
          <div class="badge-gallery">
            ${badgeGalleryHTML}
          </div>
        </div>
      </div>
    `;
  }
}
