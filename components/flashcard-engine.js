/**
 * Flashcard Engine Component using SM-2
 */

export class FlashcardEngine {
    /**
     * @param {HTMLElement} containerEl 
     */
    constructor(containerEl) {
        this.containerEl = containerEl;
        this.decks = {};
        this.storageKey = 'pals-flashcards';
        this.loadProgress();
    }

    loadProgress() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            this.progress = JSON.parse(saved);
        } else {
            this.progress = {};
        }
    }

    saveProgress() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.progress));
    }

    addDeck(deckId, cards) {
        this.decks[deckId] = cards.map(c => ({
            ...c,
            id: c.id || Math.random().toString(36).substr(2, 9),
            easeFactor: 2.5,
            interval: 0,
            repetitions: 0,
            nextReview: Date.now()
        }));
        
        // merge with saved progress
        if (this.progress[deckId]) {
            this.decks[deckId].forEach(c => {
                const savedCard = this.progress[deckId].find(sc => sc.id === c.id);
                if (savedCard) Object.assign(c, savedCard);
            });
        }
    }

    getDueCards(deckId) {
        const now = Date.now();
        return this.decks[deckId]?.filter(c => c.nextReview <= now) || [];
    }

    /**
     * @param {string} deckId 
     * @param {string} cardId 
     * @param {number} quality (0-5)
     */
    reviewCard(deckId, cardId, quality) {
        const card = this.decks[deckId].find(c => c.id === cardId);
        if (!card) return;

        if (quality < 2) {
            card.repetitions = 0;
            card.interval = 1;
        } else if (quality === 2) {
            card.interval = 1;
        } else {
            if (card.repetitions === 0) card.interval = 1;
            else if (card.repetitions === 1) card.interval = 6;
            else card.interval = Math.round(card.interval * card.easeFactor);
            
            card.repetitions++;
        }

        card.easeFactor = Math.max(1.3, card.easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)));
        card.nextReview = Date.now() + card.interval * 24 * 60 * 60 * 1000;

        if (!this.progress[deckId]) this.progress[deckId] = [];
        
        const savedIdx = this.progress[deckId].findIndex(c => c.id === cardId);
        if (savedIdx >= 0) this.progress[deckId][savedIdx] = card;
        else this.progress[deckId].push(card);

        this.saveProgress();
    }

    render(deckId) {
        if (!this.containerEl) return;
        const due = this.getDueCards(deckId);
        
        if (due.length === 0) {
            this.containerEl.innerHTML = `<div class="flashcard-done">You're all caught up for this deck!</div>`;
            return;
        }

        const card = due[0];
        
        this.containerEl.innerHTML = `
            <div class="flashcard-engine">
                <div class="flashcard">
                    <div class="front">${card.front}</div>
                    <div class="back" style="display:none;">${card.back}</div>
                </div>
                <div class="controls">
                    <button id="fc-flip">Flip</button>
                    <div id="fc-rating" style="display:none;">
                        <button data-q="0">Again</button>
                        <button data-q="2">Hard</button>
                        <button data-q="3">Good</button>
                        <button data-q="5">Easy</button>
                    </div>
                </div>
            </div>
        `;

        this.containerEl.querySelector('#fc-flip').addEventListener('click', (e) => {
            this.containerEl.querySelector('.back').style.display = 'block';
            e.target.style.display = 'none';
            this.containerEl.querySelector('#fc-rating').style.display = 'block';
        });

        this.containerEl.querySelectorAll('#fc-rating button').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const q = parseInt(e.target.dataset.q);
                this.reviewCard(deckId, card.id, q);
                this.render(deckId);
            });
        });
    }

    getStats(deckId) {
        const deck = this.decks[deckId] || [];
        return {
            total: deck.length,
            due: this.getDueCards(deckId).length,
            mastered: deck.filter(c => c.interval > 21).length
        };
    }
}
