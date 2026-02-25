/*********************** 
 * Samochodzik - Test *
 ***********************/

import { core, visual, util, data, sound, hardware } from './lib/psychojs-2025.1.1.js';
const { PsychoJS } = core;
const { Scheduler } = util;

// 1. Inicjalizacja PsychoJS
const psychoJS = new PsychoJS({
    debug: false
});

// Otwarcie okna
psychoJS.openWindow({
    fullscr: false,
    color: new util.Color([0, 0, 0]),
    units: 'height',
    waitBlanking: true
});

// Harmonogramy
const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);

// --- KONFIGURACJA ---
let expName = 'samochodzik';
let expInfo = { 'participant': 'test' };

// --- STAN GRY ---
let trackImage, carSprite, welcomeText;
let carX = -0.336, carY = -0.322, carRotation = 0;
let collisionCount = 0, startTime = null, finished = false;
let trackPixels = null;
let trackImgElement = null;
let carImgElement = null;
const activeKeys = new Set();

// Obsługa klawiszy
document.addEventListener('keydown', (e) => activeKeys.add(e.key));
document.addEventListener('keyup', (e) => activeKeys.delete(e.key));

// --- RUTYNY ---

async function experimentInit() {
    const loadImg = (src) => new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
    });

    try {
        trackImgElement = await loadImg('resources/trasa.png');
        carImgElement = await loadImg('resources/sam.png');

        const cv = document.createElement('canvas');
        cv.width = 800; cv.height = 444;
        const ctx = cv.getContext('2d');
        ctx.drawImage(trackImgElement, 0, 0, 800, 444);
        trackPixels = ctx.getImageData(0, 0, 800, 444).data;
    } catch (e) {
        console.error("Błąd ładowania obrazów:", e);
    }

    trackImage = new visual.ImageStim({
        win: psychoJS.window, name: 'track',
        image: trackImgElement, pos: [0, 0], size: [1.6, 1.6 * 0.555]
    });

    carSprite = new visual.ImageStim({
        win: psychoJS.window, name: 'car',
        image: carImgElement, pos: [carX, carY], size: [0.03, 0.05]
    });

    welcomeText = new visual.TextStim({
        win: psychoJS.window, text: "SAMOCHODZIK\n\nNaciśnij SPACJĘ aby rozpocząć",
        color: new util.Color('white'), height: 0.05
    });

    // Zablokowanie standardowego zapisu PsychoJS CSV (wymagane przez Nous)
    if (typeof window.electronTest !== 'undefined') {
        psychoJS.experiment.save = () => Promise.resolve();
    }
    return Scheduler.Event.NEXT;
}

function welcomeRoutine() {
    return async function () {
        if (welcomeText.status === PsychoJS.Status.NOT_STARTED) {
            welcomeText.status = PsychoJS.Status.STARTED;
            welcomeText.setAutoDraw(true);
        }

        if (activeKeys.has(' ') || activeKeys.has('Spacebar')) {
            welcomeText.setAutoDraw(false);
            startTime = Date.now();
            return Scheduler.Event.NEXT;
        }

        // ESC na ekranie powitalnym = wyjście bez zapisu
        if (activeKeys.has('Escape') || activeKeys.has('escape')) {
            return quitPsychoJS('Wyjście', false);
        }

        return Scheduler.Event.FLIP_REPEAT;
    };
}

function gameRoutine() {
    return async function () {
        if (trackImage.status === PsychoJS.Status.NOT_STARTED) {
            trackImage.setAutoDraw(true);
            carSprite.setAutoDraw(true);
            trackImage.status = PsychoJS.Status.STARTED;
        }

        if (finished) {
            trackImage.setAutoDraw(false);
            carSprite.setAutoDraw(false);
            return Scheduler.Event.NEXT;
        }

        // ESC w trakcie gry = wyjście bez zapisu
        if (activeKeys.has('Escape') || activeKeys.has('escape')) {
            return quitPsychoJS('Przerwano', false);
        }

        let dx = 0, dy = 0;
        if (activeKeys.has('ArrowLeft')) dx -= 1;
        if (activeKeys.has('ArrowRight')) dx += 1;
        if (activeKeys.has('ArrowUp')) dy += 1;
        if (activeKeys.has('ArrowDown')) dy -= 1;

        if (dx !== 0 || dy !== 0) {
            const len = Math.sqrt(dx * dx + dy * dy);
            carX += (dx / len) * 0.007;
            carY += (dy / len) * 0.007;
            carRotation = Math.atan2(dx, dy);
        }

        // Kolizja
        if (trackPixels) {
            const px = Math.floor((carX / 1.6 + 0.5) * 800);
            const py = Math.floor((0.2775 - carY / 1.6) * (444 / 0.555));
            const idx = (Math.max(0, Math.min(443, py)) * 800 + Math.max(0, Math.min(799, px))) * 4;
            const r = trackPixels[idx], g = trackPixels[idx + 1], b = trackPixels[idx + 2];

            if (r > 200 && g < 100 && b < 100) { // Meta
                finished = true;
                return Scheduler.Event.NEXT;
            }
            if (r < 50 && g < 50 && b < 50) { // Ściana
                carX = -0.336; carY = -0.322; carRotation = 0;
                collisionCount++;
            }
        }

        carSprite.setPos([carX, carY]);
        carSprite.setOri(carRotation * (180 / Math.PI));

        return Scheduler.Event.FLIP_REPEAT;
    };
}

function finishRoutine() {
    let finishClock = null;
    let finishText = null;

    return async function () {
        if (finishClock === null) {
            finishClock = new util.Clock();
            finishText = new visual.TextStim({
                win: psychoJS.window, text: "META!\n\nZapisywanie punktów...",
                color: new util.Color('green'), height: 0.1
            });
            finishText.setAutoDraw(true);
        }

        if (finishClock.getTime() > 2.0) {
            finishText.setAutoDraw(false);
            return quitPsychoJS('Koniec', true);
        }

        return Scheduler.Event.FLIP_REPEAT;
    };
}

/**
 * Zamykanie testu i wysyłka wyników zgodnie z PORADNIK_AGENTA.md
 */
async function quitPsychoJS(message, isCompleted) {
    if (typeof window.electronTest !== 'undefined') {
        if (isCompleted) {
            // Ujednolicone nazewnictwo wyników (Sekcja 2 i 3 Poradnika)
            window.electronTest.sendResults({
                testId: 'samochodzik',
                subjectId: expInfo['participant'],
                timestamp: new Date().toISOString(),
                ilosc_poprawnych_nacisniec: 1, // Dojechanie do mety to 1 poprawny przebieg
                ilosc_blednych_nacisniec: collisionCount,
                ogolna_ilosc_nacisniec: 1 + collisionCount,
                czas_pokonania_trasy_sek: Math.round((Date.now() - startTime) / 1000),
                // Nie dodajemy sredni_czas_reakcji, bo test go nie mierzy (Sekcja 2.52)
                score: `Meta osiągnięta! Kolizje: ${collisionCount} | Czas: ${Math.round((Date.now() - startTime) / 1000)}s`,
                statystyki: {
                    czas_trwania_ms: Date.now() - startTime,
                    liczba_kolizji: collisionCount
                }
            });
        } else {
            // Wyjście przez ESC bez zapisu
            window.electronTest.close();
        }
    }

    psychoJS.window.close();
    psychoJS.quit({ message: message, isCompleted: isCompleted });
    return Scheduler.Event.QUIT;
}

// --- FLOW ---
psychoJS.scheduleCondition(function () { return true; }, flowScheduler, dialogCancelScheduler);

flowScheduler.add(experimentInit);
flowScheduler.add(welcomeRoutine());
flowScheduler.add(gameRoutine());
flowScheduler.add(finishRoutine());

psychoJS.start({
    expName: expName,
    expInfo: expInfo,
    resources: []
});
