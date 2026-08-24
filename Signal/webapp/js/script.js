// webapp/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();

    const adOverlay = document.getElementById('ad-overlay');
    const dashboard = document.getElementById('dashboard');
    const adBtn = document.getElementById('ad-btn');
    const signalModal = document.getElementById('signal-modal');
    const langModal = document.getElementById('lang-modal');
    const minesGrid = document.getElementById('mines-grid');
    const cooldownTimer = document.getElementById('cooldown-timer');

    adBtn.addEventListener('click', () => {
        adOverlay.classList.add('hidden');
        dashboard.classList.remove('hidden');
    });

    // Modals
    window.openSignalModal = (gameName) => {
        document.getElementById('modal-title').innerText = gameName + " Signal";
        signalModal.classList.remove('hidden');
        createMinesGrid();
    };
    window.closeSignalModal = () => signalModal.classList.add('hidden');
    window.toggleLangModal = () => langModal.classList.toggle('hidden');

    // Signal Logic
    function createMinesGrid() {
        minesGrid.innerHTML = '';
        for (let i = 0; i < 25; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            minesGrid.appendChild(cell);
        }
    }

    window.generateSignal = () => {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(c => c.classList.remove('star'));
        let count = 0;
        while (count < 5) {
            const i = Math.floor(Math.random() * 25);
            if (!cells[i].classList.contains('star')) {
                cells[i].classList.add('star');
                count++;
            }
        }
        
        // Cooldown
        let timeLeft = 30;
        const btn = document.getElementById('generate-btn');
        btn.disabled = true;
        const timer = setInterval(() => {
            timeLeft--;
            cooldownTimer.innerText = "Yangi signal: " + timeLeft + "s";
            if (timeLeft <= 0) {
                clearInterval(timer);
                btn.disabled = false;
                cooldownTimer.innerText = "";
            }
        }, 1000);
    };

    // Language
    window.setLang = (lang) => {
        alert("Til o'zgartirildi: " + lang);
        toggleLangModal();
    };

    // User Data
    const user = window.Telegram.WebApp.initDataUnsafe.user;
    if (user) {
        document.getElementById('username').innerText = user.first_name;
        document.getElementById('userid').innerText = user.id;
    }
});
