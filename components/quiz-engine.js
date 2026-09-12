/**
 * Quiz Engine Component
 * 
 * Renders MCQ questions with instant feedback, rationale, and score tracking.
 * Supports an onComplete callback for integration with the app engine.
 */

export class QuizEngine {
  /**
   * @param {HTMLElement} containerEl 
   * @param {Array} questions - [{text, options: [{text, correct}], rationale}]
   * @param {Object} options - {onComplete: (score) => void}
   */
  constructor(containerEl, questions, options = {}) {
    this.containerEl = containerEl;
    this.questions = questions;
    this.options = options;
    this.currentIndex = 0;
    this.score = 0;
    this.answered = false;
  }

  render() {
    if (!this.containerEl || !this.questions.length) return;
    this.currentIndex = 0;
    this.score = 0;
    this.renderQuestion();
  }

  renderQuestion() {
    const q = this.questions[this.currentIndex];
    const qNum = this.currentIndex + 1;
    const total = this.questions.length;
    this.answered = false;

    this.containerEl.innerHTML = `
      <div class="quiz-container">
        <div class="quiz-progress-info">
          <span>Question ${qNum} of ${total}</span>
        </div>
        <h3>${q.text}</h3>
        <div class="quiz-options-list">
          ${q.options.map((opt, i) =>
            `<button class="quiz-option" data-index="${i}">${opt.text}</button>`
          ).join('')}
        </div>
        <div class="quiz-feedback" style="display:none;"></div>
        <button class="quiz-next-btn" style="display:none;">
          ${qNum < total ? 'Next Question →' : 'See Results'}
        </button>
      </div>
    `;

    // Bind option clicks
    this.containerEl.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        if (this.answered) return;
        this.checkAnswer(parseInt(btn.dataset.index));
      });
    });

    // Bind next button
    this.containerEl.querySelector('.quiz-next-btn')?.addEventListener('click', () => {
      this.currentIndex++;
      if (this.currentIndex < this.questions.length) {
        this.renderQuestion();
      } else {
        this.showResults();
      }
    });
  }

  checkAnswer(selectedIndex) {
    this.answered = true;
    const q = this.questions[this.currentIndex];
    const isCorrect = q.options[selectedIndex]?.correct === true;

    if (isCorrect) this.score++;

    // Highlight options
    this.containerEl.querySelectorAll('.quiz-option').forEach((btn, i) => {
      btn.disabled = true;
      btn.style.pointerEvents = 'none';
      if (q.options[i].correct) {
        btn.classList.add('correct');
        btn.innerHTML = `✓ ${q.options[i].text}`;
      } else if (i === selectedIndex && !isCorrect) {
        btn.classList.add('wrong');
        btn.innerHTML = `✗ ${q.options[i].text}`;
      }
    });

    // Show feedback
    const fbEl = this.containerEl.querySelector('.quiz-feedback');
    if (fbEl) {
      fbEl.style.display = 'block';
      fbEl.innerHTML = `
        <div class="${isCorrect ? 'quiz-rationale correct' : 'quiz-rationale wrong'}">
          <strong>${isCorrect ? '✅ Correct!' : '❌ Incorrect.'}</strong>
          ${q.rationale ? `<p>${q.rationale}</p>` : ''}
        </div>
      `;
    }

    // Show next button
    const nextBtn = this.containerEl.querySelector('.quiz-next-btn');
    if (nextBtn) nextBtn.style.display = 'block';
  }

  showResults() {
    const stats = this.getScore();
    const passed = stats.percentage >= 80;

    this.containerEl.innerHTML = `
      <div class="quiz-results">
        <h3>${passed ? '🎉 Knowledge Check Passed!' : '📝 Try Again'}</h3>
        <div class="quiz-score-ring">
          <span class="score-pct">${stats.percentage}%</span>
          <span class="score-detail">${stats.correct}/${stats.total} correct</span>
        </div>
        <p>${passed
          ? 'Great work! You\'ve demonstrated mastery of this content.'
          : 'You need at least 80% to continue. Review the content and try again.'
        }</p>
        ${!passed ? '<button class="quiz-retry-btn">🔄 Retry Quiz</button>' : ''}
      </div>
    `;

    // Retry button
    this.containerEl.querySelector('.quiz-retry-btn')?.addEventListener('click', () => {
      this.score = 0;
      this.currentIndex = 0;
      this.render();
    });

    // Fire Confetti if passed
    if (passed && typeof confetti === 'function') {
      confetti({
        particleCount: 100, spread: 70, origin: { y: 0.6 },
        colors: ['#22c55e', '#3b82f6', '#f59e0b']
      });
    }

    // Fire onComplete callback
    if (this.options.onComplete) {
      this.options.onComplete(stats);
    }
  }

  getScore() {
    return {
      correct: this.score,
      total: this.questions.length,
      percentage: this.questions.length > 0
        ? Math.round((this.score / this.questions.length) * 100)
        : 0,
    };
  }
}
