document.addEventListener('DOMContentLoaded', () => {
    const webapp = window.Telegram.WebApp;
    webapp.ready();
    webapp.expand();

    const modal = document.getElementById('signalModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalContent');
    const closeModal = document.getElementById('closeModal');
    const openButtons = document.querySelectorAll('.open-btn');

    let countdownInterval;
    let selectedMines = 3;

    openButtons.forEach(button => {
        button.addEventListener('click', () => {
            webapp.HapticFeedback.impactOccurred('medium');
            const card = button.closest('.game-card');
            const gameName = card.querySelector('.game-title').innerText;
            showSignalWindow(gameName);
        });
    });

    function showSignalWindow(game) {
        if (countdownInterval) clearInterval(countdownInterval);
        modalTitle.innerText = game;
        
        // Mines layout or Multiplier layout
        if (game.toLowerCase().includes('mines')) {
            setupMinesUI();
        } else {
            setupMultiplierUI(game);
        }
        
        modal.classList.add('active');
    }

    function setupMinesUI() {
        modalContent.innerHTML = `
            <div class="mines-selector">
                <button class="mines-count-btn ${selectedMines === 1 ? 'active' : ''}" data-count="1">1</button>
                <button class="mines-count-btn ${selectedMines === 3 ? 'active' : ''}" data-count="3">3</button>
                <button class="mines-count-btn ${selectedMines === 5 ? 'active' : ''}" data-count="5">5</button>
                <button class="mines-count-btn ${selectedMines === 7 ? 'active' : ''}" data-count="7">7</button>
            </div>
            <div class="grid-container">
                <div id="gridOverlay" class="grid-loading-overlay">
                    <div class="spinner"></div>
                    <p style="font-size: 12px; margin-top: 10px;">Tahlil qilinmoqda...</p>
                </div>
                <div class="mines-grid" id="minesGrid">
                    ${Array(25).fill('<div class="mine-cell"><span class="star-icon">⭐</span></div>').join('')}
                </div>
            </div>
            <button id="getSignalBtn" class="next-signal-btn" style="margin-top: 10px;">SIGNAL OLISH</button>
            <span id="timerText" class="timer-text" style="display:none">Kuting: 30s</span>
        `;

        // Add events for mine selector
        document.querySelectorAll('.mines-count-btn').forEach(btn => {
            btn.onclick = () => {
                webapp.HapticFeedback.impactOccurred('light');
                document.querySelectorAll('.mines-count-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedMines = parseInt(btn.dataset.count);
            };
        });

        document.getElementById('getSignalBtn').onclick = () => handleGetSignal('mines');
    }

    function setupMultiplierUI(game) {
        modalContent.innerHTML = `
            <div id="multiplierLoading" class="signal-loading">
                <div class="spinner"></div>
                <p>Koeffitsient hisoblanmoqda...</p>
            </div>
            <div id="multiplierResult" style="display:none"></div>
            <button id="getSignalBtn" class="next-signal-btn" style="margin-top: 20px;">SIGNAL OLISH</button>
            <span id="timerText" class="timer-text" style="display:none">Kuting: 30s</span>
        `;
        document.getElementById('getSignalBtn').onclick = () => handleGetSignal('multiplier');
    }

    function handleGetSignal(type) {
        const getBtn = document.getElementById('getSignalBtn');
        const timerText = document.getElementById('timerText');
        const overlay = document.getElementById('gridOverlay');
        const multiplierLoading = document.getElementById('multiplierLoading');
        const multiplierResult = document.getElementById('multiplierResult');
        
        webapp.HapticFeedback.impactOccurred('medium');
        getBtn.disabled = true;

        if (type === 'mines') {
            overlay.style.display = 'flex';
            // Clear existing stars
            document.querySelectorAll('.mine-cell').forEach(c => c.classList.remove('active-star'));
        } else {
            multiplierLoading.style.display = 'flex';
            multiplierResult.style.display = 'none';
        }

        // 2 Second Loading
        setTimeout(() => {
            if (type === 'mines') {
                overlay.style.display = 'none';
                generateMinesSignal();
            } else {
                multiplierLoading.style.display = 'none';
                generateMultiplierSignal();
            }
            startTimer(getBtn, timerText);
        }, 2000);
    }

    function generateMinesSignal() {
        const cells = document.querySelectorAll('.mine-cell');
        const starPositions = [];
        // Show 3 to 5 stars as requested
        const starCount = Math.floor(Math.random() * 3) + 3; 

        while(starPositions.length < starCount) {
            const pos = Math.floor(Math.random() * 25);
            if(!starPositions.includes(pos)) starPositions.push(pos);
        }

        starPositions.forEach((pos, index) => {
            setTimeout(() => {
                cells[pos].classList.add('active-star');
                webapp.HapticFeedback.impactOccurred('light');
            }, index * 150);
        });
        webapp.HapticFeedback.notificationOccurred('success');
    }

    function generateMultiplierSignal() {
        const multiplierResult = document.getElementById('multiplierResult');
        const randomSignal = (Math.random() * (4.5 - 1.2) + 1.2).toFixed(2);
        multiplierResult.innerHTML = `
            <div class="signal-result">
                <span class="signal-value">x${randomSignal}</span>
                <p class="signal-desc">Kutilayotgan koeffitsient</p>
            </div>
        `;
        multiplierResult.style.display = 'block';
        webapp.HapticFeedback.notificationOccurred('success');
    }

    function startTimer(btn, text) {
        let timeLeft = 30;
        text.style.display = 'block';
        text.innerText = `Kuting: ${timeLeft}s`;

        countdownInterval = setInterval(() => {
            timeLeft--;
            text.innerText = `Kuting: ${timeLeft}s`;
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                btn.disabled = false;
                text.style.display = 'none';
            }
        }, 1000);
    }

    closeModal.addEventListener('click', () => {
        modal.classList.remove('active');
        if (countdownInterval) clearInterval(countdownInterval);
        webapp.HapticFeedback.impactOccurred('light');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            if (countdownInterval) clearInterval(countdownInterval);
        }
    });
});
