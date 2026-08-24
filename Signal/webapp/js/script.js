// webapp/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();

    const signalModal = document.getElementById('signal-modal');
    const minesGrid = document.getElementById('mines-grid');
    const cooldownTimer = document.getElementById('cooldown-timer');
    const generateBtn = document.getElementById('generate-btn');

    let currentMines = 1;

    // Modals
    window.openSignalModal = (gameName) => {
        document.getElementById('modal-title').innerText = gameName + " Signal";
        signalModal.classList.remove('hidden');
        createMinesGrid();
    };
    window.closeSignalModal = () => signalModal.classList.add('hidden');

    function createMinesGrid() {
        minesGrid.innerHTML = '';
        for (let i = 0; i < 25; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            minesGrid.appendChild(cell);
        }
    }

    window.setMines = (count) => {
        currentMines = count;
        // Highlight active button (logic to be added if buttons exist)
    };

    window.generateSignal = () => {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(c => c.classList.remove('star'));
        
        let count = 0;
        let targets = [];
        while (count < 5) {
            const i = Math.floor(Math.random() * 25);
            if (!targets.includes(i)) {
                targets.push(i);
                count++;
            }
        }
        
        targets.forEach(i => {
            setTimeout(() => {
                cells[i].classList.add('star');
            }, i * 50); // Animation delay
        });
        
        // Cooldown
        let timeLeft = 30;
        generateBtn.disabled = true;
        const timer = setInterval(() => {
            timeLeft--;
            cooldownTimer.innerText = "Yangi signal: " + timeLeft + "s";
            if (timeLeft <= 0) {
                clearInterval(timer);
                generateBtn.disabled = false;
                cooldownTimer.innerText = "";
            }
        }, 1000);
    };

    // User Data
    const user = window.Telegram.WebApp.initDataUnsafe.user;
    if (user) {
        document.getElementById('username').innerText = user.first_name;
        document.getElementById('userid').innerText = user.id;
    }
});
