/**
 * Algorithm Viewer Component
 */

export class AlgorithmViewer {
    /**
     * @param {HTMLElement} containerEl 
     * @param {Object} algorithmData 
     */
    constructor(containerEl, algorithmData) {
        this.containerEl = containerEl;
        this.algorithmData = algorithmData;
        this.currentStep = 0;
    }

    render() {
        if (!this.containerEl) return;
        
        this.containerEl.innerHTML = `
            <div class="algorithm-viewer">
                <h2>${this.algorithmData.title || 'Algorithm'}</h2>
                <div class="algorithm-canvas" id="algo-canvas">
                    <!-- Flowchart nodes rendered here -->
                </div>
                <div class="algorithm-controls">
                    <button id="algo-step-btn">Step Through</button>
                    <button id="algo-reset-btn">Reset</button>
                </div>
            </div>
        `;

        this.renderNodes();
        this.bindEvents();
    }

    renderNodes() {
        const canvas = this.containerEl.querySelector('#algo-canvas');
        canvas.innerHTML = '';
        
        if (!this.algorithmData.nodes) return;

        this.algorithmData.nodes.forEach(node => {
            const el = document.createElement('div');
            el.className = `algo-node type-${node.type}`;
            el.id = `node-${node.id}`;
            el.innerText = node.text;
            canvas.appendChild(el);
        });
    }

    bindEvents() {
        this.containerEl.querySelector('#algo-step-btn').addEventListener('click', () => this.stepThrough());
        this.containerEl.querySelector('#algo-reset-btn').addEventListener('click', () => this.reset());
    }

    stepThrough() {
        if (!this.algorithmData.nodes || this.algorithmData.nodes.length === 0) return;
        
        // Remove highlight from all
        this.containerEl.querySelectorAll('.algo-node').forEach(el => el.classList.remove('highlighted'));
        
        if (this.currentStep < this.algorithmData.nodes.length) {
            const node = this.algorithmData.nodes[this.currentStep];
            this.highlightNode(node.id);
            this.currentStep++;
        } else {
            this.currentStep = 0; // Wrap around or end
        }
    }

    highlightNode(nodeId) {
        const el = this.containerEl.querySelector(`#node-${nodeId}`);
        if (el) {
            el.classList.add('highlighted');
        }
    }

    reset() {
        this.currentStep = 0;
        this.containerEl.querySelectorAll('.algo-node').forEach(el => el.classList.remove('highlighted'));
    }
}
