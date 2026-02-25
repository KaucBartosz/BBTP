/**
 * Samochodzik - Test nawigacji
 * Sterowanie: strzałki klawiatury
 * Mechanika: wykrywanie kolizji z białą trasą, reset na start po wyjechaniu poza trasę
 */

// Globalne zmienne
let psychoJS;
let win;
let carSprite;
let trackImage;
let carX, carY;
let carSpeed = 0.005;
let carRotation = 0;
let carWidth = 0.05;
let carHeight = 0.08;
let trackPixels = null;
let trackWidth, trackHeight;
let startArea = { x: 0.232, y: 0.383, width: 0.05, height: 0.05 };
let isGameOver = false;
let startTime = null;
let collisionCount = 0;
let globalClock;
let routineTimer;
let welcomeClock;
let gameClock;
let welcomeText;
let welcomeKey;

// Inicjalizacja PsychoJS
function initPsychoJS() {
    psychoJS = new PsychoJS({
        debug: false
    });

    // Konfiguracja okna
    win = new visual.Window({
        fullscr: true,
        color: new util.Color([0, 0, 0]),
        units: 'height',
        waitBlanking: false
    });

    // Inicjalizacja myszy
    psychoJS.experiment.setMouseVisible(true);
    
    // Inicjalizacja klawiatury
    psychoJS.experiment.setKeyboard(new core.Keyboard());
    
    // Ustawienia eksperymentu
    psychoJS.experiment.extraInfo = {
        'expName': 'Samochodzik',
        'participant': 'test'
    };
    
    // Inicjalizacja globalnych timerów
    globalClock = new util.Clock();
    routineTimer = new util.CountdownTimer();
    
    // Inicjalizacja komponentów ekranu powitalnego
    welcomeClock = new util.Clock();
    welcomeText = new visual.TextStim({
        win: win,
        name: 'welcomeText',
        text: 'TEST NAWIGACJI SAMOCHODZIKIEM\n\n' +
              'Sterowanie:\n' +
              'Strzałka w górę - jazda do przodu\n' +
              'Strzałka w dół - jazda do tyłu\n' +
              'Strzałka w lewo - skręt w lewo\n' +
              'Strzałka w prawo - skręt w prawo\n\n' +
              'Cel: poruszaj się po białej trasie\n' +
              'Jeśli wyjedziesz poza trasę - reset do pozycji startowej\n\n' +
              'Naciśnij SPACJĘ aby rozpocząć\n' +
              'Naciśnij ESC aby wyjść',
        font: 'Arial',
        units: 'height',
        pos: [0, 0],
        height: 0.04,
        color: new util.Color('white'),
        wrapWidth: 1.5
    });
    
    welcomeKey = new core.Keyboard({ psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true });
    
    // --- NOUS INTEGRATION: INIT ---
    if (typeof window.electronTest !== 'undefined') {
        psychoJS.experiment.save = function() { return Promise.resolve(); };
    }
    
    // --- KONFIGURACJA OKNA: Ustawienia zgodne z PsychoJS ---
    win._renderer.view.style.position = 'absolute';
    win._renderer.view.style.left = '0px';
    win._renderer.view.style.top = '0px';
    win._renderer.view.style.width = '100%';
    win._renderer.view.style.height = '100%';
}

// Wczytanie obrazów
async function loadAssets() {
    // Wczytanie tła (trasa)
    trackImage = new visual.ImageStim({
        win: win,
        image: 'resources/trasa.png',
        pos: [0, 0],
        size: [1.0, 0.555], // 800x444 w stosunku do wysokości
        opacity: 1.0
    });

    // Wczytanie samochodu
    carSprite = new visual.ImageStim({
        win: win,
        image: 'resources/sam.png',
        pos: [startArea.x, startArea.y],
        size: [carWidth, carHeight],
        opacity: 1.0
    });

    // Ustawienie początkowej pozycji
    carX = startArea.x;
    carY = startArea.y;
    carSprite.setPos([carX, carY]);
    
    // Wczytanie pikseli tła dla detekcji kolizji
    await loadTrackPixels();
}

// Wczytanie pikseli tła
async function loadTrackPixels() {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
            trackWidth = img.width;
            trackHeight = img.height;
            
            // Utworzenie canvas do analizy pikseli
            const canvas = document.createElement('canvas');
            canvas.width = trackWidth;
            canvas.height = trackHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            
            // Pobranie danych pikseli
            const imageData = ctx.getImageData(0, 0, trackWidth, trackHeight);
            trackPixels = imageData.data;
            
            resolve();
        };
        img.src = 'resources/trasa.png';
    });
}

// Konwersja współrzędnych PsychoJS na piksele
function psychoToPixels(psychoX, psychoY) {
    // PsychoJS: środek (0,0), zakres x: -0.5 do 0.5, y: -0.2775 do 0.2775 (units: 'height')
    // Obraz: 800x444, środek (400, 222)
    const pixelX = (psychoX + 0.5) * trackWidth;
    const pixelY = (0.2775 - psychoY) * trackHeight;
    return { x: pixelX, y: pixelY };
}

// Sprawdzenie czy punkt jest na białej trasie
function isOnTrack(psychoX, psychoY) {
    const { x: pixelX, y: pixelY } = psychoToPixels(psychoX, psychoY);
    
    // Sprawdzenie granic obrazu
    if (pixelX < 0 || pixelX >= trackWidth || pixelY < 0 || pixelY >= trackHeight) {
        return false;
    }
    
    // Obliczenie indeksu piksela
    const index = Math.floor(pixelY) * trackWidth * 4 + Math.floor(pixelX) * 4;
    
    // Sprawdzenie czy piksel jest biały (trasą)
    const r = trackPixels[index];
    const g = trackPixels[index + 1];
    const b = trackPixels[index + 2];
    
    // Biały piksel: R, G, B > 200
    return (r > 200 && g > 200 && b > 200);
}

// Sprawdzenie kolizji samochodu z trasą
function checkCollision() {
    // Sprawdzenie czterech rogów samochodu
    const halfW = carWidth / 2;
    const halfH = carHeight / 2;
    
    // Punkty rogów w przestrzeni PsychoJS
    const corners = [
        { x: carX - halfW, y: carY - halfH }, // lewy dolny
        { x: carX + halfW, y: carY - halfH }, // prawy dolny
        { x: carX - halfW, y: carY + halfH }, // lewy górny
        { x: carX + halfW, y: carY + halfH }  // prawy górny
    ];
    
    // Sprawdzenie każdego rogu
    for (const corner of corners) {
        if (!isOnTrack(corner.x, corner.y)) {
            return true; // Kolizja - punkt poza trasą
        }
    }
    
    return false; // Brak kolizji
}

// Reset do pozycji startowej
function resetToStart() {
    carX = startArea.x;
    carY = startArea.y;
    carRotation = 0;
    carSprite.setPos([carX, carY]);
    carSprite.setOri(0);
    collisionCount++;
    
    // Wizualna informacja o kolizji
    console.log(`Kolizja! Reset do pozycji startowej. Licznik: ${collisionCount}`);
}

// Obsługa klawiatury
function handleInput() {
    const keys = psychoJS.experiment._keyboard.getKeys();
    
    // Sprawdzenie klawiszy
    const upPressed = keys.includes('up') || keys.includes('ArrowUp');
    const downPressed = keys.includes('down') || keys.includes('ArrowDown');
    const leftPressed = keys.includes('left') || keys.includes('ArrowLeft');
    const rightPressed = keys.includes('right') || keys.includes('ArrowRight');
    const escapePressed = keys.includes('escape') || keys.includes('Escape');
    
    // Wyjście z gry
    if (escapePressed) {
        quitPsychoJS('Gra przerwana przez użytkownika', false);
        return;
    }
    
    // Sterowanie
    if (upPressed) {
        // Jazda do przodu
        carX += Math.sin(carRotation) * carSpeed;
        carY += Math.cos(carRotation) * carSpeed;
    }
    
    if (downPressed) {
        // Jazda do tyłu
        carX -= Math.sin(carRotation) * carSpeed * 0.5;
        carY -= Math.cos(carRotation) * carSpeed * 0.5;
    }
    
    if (leftPressed) {
        // Skręt w lewo
        carRotation += 0.1;
    }
    
    if (rightPressed) {
        // Skręt w prawo
        carRotation -= 0.1;
    }
    
    // Aktualizacja pozycji samochodu
    carSprite.setPos([carX, carY]);
    carSprite.setOri(carRotation * (180 / Math.PI));
}

// Główna pętla gry
function gameLoop() {
    if (isGameOver) return;
    
    // Obsługa wejść
    handleInput();
    
    // Sprawdzenie kolizji
    if (checkCollision()) {
        resetToStart();
    }
    
    // Rysowanie
    trackImage.draw();
    carSprite.draw();
    
    // Aktualizacja ekranu
    win.flip();
    
    // Kontynuacja pętli
    requestAnimationFrame(gameLoop);
}

// Funkcja wyjścia z PsychoJS
async function quitPsychoJS(message, isCompleted) {
    if (typeof window.electronTest !== 'undefined') {
        if (isCompleted) {
            // Zapis wyników
            window.electronTest.sendResults({
                testId: 'Samochodzik',
                subjectId: 'test',
                timestamp: new Date().toISOString(),
                ilosc_poprawnych_nacisniec: 0,
                ilosc_blednych_nacisniec: collisionCount,
                ogolna_ilosc_nacisniec: 0,
                czas_trwania: startTime ? (Date.now() - startTime) : 0,
                liczba_kolizji: collisionCount,
                wyniki: {
                    start_time: startTime,
                    end_time: Date.now(),
                    collisions: collisionCount
                }
            });
        } else {
            // Wyjście bez zapisu
            window.electronTest.close();
        }
    }
    
    win.close();
    psychoJS.quit({ message: message, isCompleted: isCompleted });
}

// Instrukcje
function showInstructions() {
    const instr = new visual.TextStim({
        win: win,
        text: 'Test nawigacji samochodzikiem\n\n' +
              'Sterowanie:\n' +
              'Strzałka w górę - jazda do przodu\n' +
              'Strzałka w dół - jazda do tyłu\n' +
              'Strzałka w lewo - skręt w lewo\n' +
              'Strzałka w prawo - skręt w prawo\n\n' +
              'Cel: poruszaj się po białej trasie\n' +
              'Jeśli wyjedziesz poza trasę - reset do pozycji startowej\n\n' +
              'Naciśnij spację aby rozpocząć\n' +
              'Naciśnij ESC aby wyjść',
        color: 'white',
        height: 0.05,
        wrapWidth: 1.5
    });
    
    instr.draw();
    win.flip();
    
    // Oczekiwanie na spację lub ESC
    return new Promise((resolve) => {
        const checkKeys = () => {
            const keys = psychoJS.experiment._keyboard.getKeys();
            if (keys.includes('space') || keys.includes(' ')) {
                resolve('start');
            } else if (keys.includes('escape') || keys.includes('Escape')) {
                resolve('exit');
            } else {
                requestAnimationFrame(checkKeys);
            }
        };
        checkKeys();
    });
}

// Główna funkcja inicjalizująca
async function main() {
    try {
        // Inicjalizacja
        initPsychoJS();
        
        // Wczytanie zasobów
        await loadAssets();
        
        // Ekran powitalny
        await welcomeRoutine();
        
        // Rozpoczęcie gry
        startTime = Date.now();
        gameLoop();
        
    } catch (error) {
        console.error('Błąd inicjalizacji:', error);
        quitPsychoJS('Błąd inicjalizacji', false);
    }
}

// Ekran powitalny
async function welcomeRoutine() {
    return new Promise((resolve) => {
        // Wyświetlenie tekstu powitalnego
        welcomeText.setAutoDraw(true);
        welcomeKey.start();
        welcomeKey.clearEvents();
        
        // Pętla sprawdzająca klawisze
        function checkWelcomeKeys() {
            const keys = welcomeKey.getKeys({ keyList: ['space', 'escape'], waitRelease: false });
            
            if (keys.length > 0) {
                const keyName = keys[0].name;
                if (keyName === 'space') {
                    // Rozpoczęcie gry
                    welcomeText.setAutoDraw(false);
                    resolve();
                } else if (keyName === 'escape') {
                    // Wyjście
                    welcomeText.setAutoDraw(false);
                    quitPsychoJS('Gra przerwana przez użytkownika', false);
                }
            } else {
                // Kontynuacja pętli
                requestAnimationFrame(checkWelcomeKeys);
            }
        }
        
        checkWelcomeKeys();
    });
}

// Uruchomienie gry
main().catch(error => {
    console.error('Błąd:', error);
});

// --- NOUS INTEGRATION: INIT ---
if (typeof window.electronTest !== 'undefined') {
    psychoJS.experiment.save = function() { return Promise.resolve(); };
}
