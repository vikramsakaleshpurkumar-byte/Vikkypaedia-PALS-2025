import { algorithms } from '../data/algorithms.js';

export class AlgorithmViewer {
  constructor(containerEl) {
    this.containerEl = containerEl;
    this.currentAlgo = algorithms.cardiacArrest; // Default to Cardiac Arrest
    this.history = []; // Array of node IDs
    this.currentNodeId = this.currentAlgo.startNode;
  }

  start() {
    this.history = [];
    this.currentNodeId = this.currentAlgo.startNode;
    this.render();
  }

  render() {
    if (!this.containerEl) return;

    let historyHtml = '';
    if (this.history.length > 0) {
      historyHtml = '<div class="algo-history">';
      this.history.forEach((id, index) => {
        const node = this.currentAlgo.nodes[id];
        historyHtml += `
          <div class="algo-history-node">
            <span class="step-num">${index + 1}</span>
            <span class="step-text">${node.text.replace(/\n/g, '<br>')}</span>
          </div>
          <div class="algo-arrow">↓</div>
        `;
      });
      historyHtml += '</div>';
    }

    const currentNode = this.currentAlgo.nodes[this.currentNodeId];
    
    let optionsHtml = '';
    if (currentNode.options && currentNode.options.length > 0) {
      optionsHtml = '<div class="algo-options">';
      currentNode.options.forEach(opt => {
        optionsHtml += `<button class="algo-btn" data-next="${opt.next}">${opt.text}</button>`;
      });
      optionsHtml += '</div>';
    }

    this.containerEl.innerHTML = `
      <div class="algorithm-viewer">
        <div class="algo-header">
          <div class="algo-header-left">
            <h2>🗺️ Interactive Algorithm</h2>
            <p class="algo-title">${this.currentAlgo.title}</p>
          </div>
          <button class="icon-btn algo-close-btn" aria-label="Close">✕</button>
        </div>
        
        <div class="algo-body">
          ${historyHtml}
          
          <div class="algo-current-node type-${currentNode.type}">
            <h3>${currentNode.type === 'decision' ? 'Decision Point' : 'Action Required'}</h3>
            <div class="node-text">${currentNode.text.replace(/\n/g, '<br>')}</div>
            ${optionsHtml}
          </div>
        </div>

        <div class="algo-footer">
          <button class="algo-outline-btn" id="algo-restart">↺ Restart Algorithm</button>
        </div>
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    // Option buttons
    this.containerEl.querySelectorAll('.algo-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const nextId = e.target.dataset.next;
        this.advance(nextId);
      });
    });

    // Restart button
    const restartBtn = this.containerEl.querySelector('#algo-restart');
    if (restartBtn) {
      restartBtn.addEventListener('click', () => this.start());
    }
    
    // Close button
    const closeBtn = this.containerEl.querySelector('.algo-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this.containerEl.remove();
      });
    }
  }

  advance(nextId) {
    this.history.push(this.currentNodeId);
    this.currentNodeId = nextId;
    this.render();
    
    // Auto-scroll to bottom
    setTimeout(() => {
      const body = this.containerEl.querySelector('.algo-body');
      if (body) body.scrollTop = body.scrollHeight;
    }, 50);
  }
}
