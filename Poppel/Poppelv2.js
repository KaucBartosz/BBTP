/***************** 
 * Poppelv2 *
 *****************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.1.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Poppelv2';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};
let PILOTING = util.getUrlParameters().has('__pilotToken');

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true,
  backgroundImage: '',
  backgroundFit: 'none',
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); },flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(trialsRoutineBegin());
flowScheduler.add(trialsRoutineEachFrame());
flowScheduler.add(trialsRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'resources/gwBLA.png', 'path': 'resources/gwBLA.png'},
    {'name': 'resources/gwBLU.png', 'path': 'resources/gwBLU.png'},
    {'name': 'resources/gwGRE.png', 'path': 'resources/gwGRE.png'},
    {'name': 'resources/gwRED.png', 'path': 'resources/gwRED.png'},
    {'name': 'resources/gwYEL.png', 'path': 'resources/gwYEL.png'},
    {'name': 'resources/koBLA.png', 'path': 'resources/koBLA.png'},
    {'name': 'resources/koBLU.png', 'path': 'resources/koBLU.png'},
    {'name': 'resources/koGRE.png', 'path': 'resources/koGRE.png'},
    {'name': 'resources/koRED.png', 'path': 'resources/koRED.png'},
    {'name': 'resources/koYEL.png', 'path': 'resources/koYEL.png'},
    {'name': 'resources/kwBLA.png', 'path': 'resources/kwBLA.png'},
    {'name': 'resources/kwBLU.png', 'path': 'resources/kwBLU.png'},
    {'name': 'resources/kwGRE.png', 'path': 'resources/kwGRE.png'},
    {'name': 'resources/kwRED.png', 'path': 'resources/kwRED.png'},
    {'name': 'resources/kwYEL.png', 'path': 'resources/kwYEL.png'},
    {'name': 'resources/pkBLA.png', 'path': 'resources/pkBLA.png'},
    {'name': 'resources/pkBLU.png', 'path': 'resources/pkBLU.png'},
    {'name': 'resources/pkGRE.png', 'path': 'resources/pkGRE.png'},
    {'name': 'resources/pkRED.png', 'path': 'resources/pkRED.png'},
    {'name': 'resources/pkYEL.png', 'path': 'resources/pkYEL.png'},
    {'name': 'resources/trBLA.png', 'path': 'resources/trBLA.png'},
    {'name': 'resources/trBLU.png', 'path': 'resources/trBLU.png'},
    {'name': 'resources/trGRE.png', 'path': 'resources/trGRE.png'},
    {'name': 'resources/trRED.png', 'path': 'resources/trRED.png'},
    {'name': 'resources/trYEL.png', 'path': 'resources/trYEL.png'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2025.1.1';
  expInfo['OS'] = window.navigator.platform;


  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  

  
  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);
  psychoJS.experiment.field_separator = '\t';


  return Scheduler.Event.NEXT;
}


var trialsClock;
var mouse;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "trials"
  trialsClock = new util.Clock();
  // --- NOUS INTEGRATION: INIT ---
  if (typeof window.electronTest !== 'undefined') {
      console.log("Nous Launcher wykryty. Blokowanie zapisu CSV.");
      psychoJS.experiment.save = function() {
          return Promise.resolve(); 
      };
  }
  
  // --- GLOBAL VARIABLES & CONFIG ---
  window.IMAGE_PATH = 'resources/';
  
  // Parametry układu
  window.N_PER_ROW = 6;
  window.SIZE_TOP = 0.22;
  window.SIZE_BOTTOM = 0.14;
  window.TOP_Y = 0.32;
  window.ROW1_Y = -0.10;
  window.ROW2_Y = -0.30;
  window.GAP = 0.07;
  
  // Parametry gry
  window.TRIAL_DURATION = 60;
  window.TARGET_CHANGE_TIME = 30;
  window.SEQUENCE_SECONDS = 30;
  window.APPEAR_X = 0;
  
  // Pula obrazków
  window.POOL = [
    'gwBLA.png','gwBLU.png','gwGRE.png','gwRED.png','gwYEL.png',
    'koBLA.png','koBLU.png','koGRE.png','koRED.png','koYEL.png',
    'kwBLA.png','kwBLU.png','kwGRE.png','kwRED.png','kwYEL.png',
    'pkBLA.png','pkBLU.png','pkGRE.png','pkRED.png','pkYEL.png',
    'trBLA.png','trBLU.png','trGRE.png','trRED.png','trYEL.png'
  ];
  
  // --- HELPER FUNCTIONS ---
  
  // 1. Shuffle (Mieszanie tablicy)
  window.shuffle = function(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };
  
  // 2. Safe Sample (Bezpieczne losowanie n elementów bez powtórzeń)
  window.safeSample = function(arr, n) {
    let a = arr.slice();
    let out = [];
    while (out.length < n && a.length) {
      let idx = Math.floor(Math.random() * a.length);
      out.push(a.splice(idx,1)[0]);
    }
    return out;
  };
  
  // 3. Make Sequence (Tworzenie losowej sekwencji)
  window.makeSequence = function(pool, n) {
    let seq = [];
    for (let i = 0; i < n; i++) {
      seq.push(pool[Math.floor(Math.random() * pool.length)]);
    }
    return seq;
  };
  
  // 4. Get Stim Image Name (Pomocnicza do wyciągania nazwy pliku)
  window.getStimImageName = function(stim) {
    try {
      let img = stim.image;
      if (typeof img === 'string') return img.split('/').pop().split('\\').pop();
      if (img && typeof img.name === 'string') return img.name;
      return String(img).split('/').pop().split('\\').pop();
    } catch (e) {
      return '';
    }
  };
  
  // Inicjalizacja globalnych buforów
  window.targets = [];
  window.bottom_sequence = [];
  window.top_stims = [];
  window.bottom_stims = [];
  window.prev_x = [];
  window.items_needed_per_row = 0;
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var trialsMaxDurationReached;
var gotValidClick;
var trialsMaxDuration;
var trialsComponents;
function trialsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'trials' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    trialsClock.reset();
    routineTimer.reset();
    trialsMaxDurationReached = false;
    // update component parameters for each repeat
    // --- INIT ROUTINE VARS ---
    
    // 1. Zabezpieczenie obiektu Myszki i Zegara
    if (typeof mouse === 'undefined') {
        mouse = new core.Mouse({ win: psychoJS.window });
    }
    window.mouse = mouse; 
    
    if (typeof window.mouse.mouseClock === 'undefined') {
        window.mouse.mouseClock = new util.Clock();
    }
    window.mouse.mouseClock.reset();
    
    // 2. INICJALIZACJA ZEGARA PRÓBY (NAPRAWA BŁĘDU)
    window.trialClock = new util.Clock(); 
    
    // 3. Reset liczników
    window.total_presses = 0;
    window.target_presses = 0;
    window.target_appearances = 0;
    window.clicked_records = [];
    window.change_done = false;
    window._prevMouseButtons = [false, false, false];
    
    // 4. Konfiguracja parametrów wizualnych
    window.SPEED = Number(window.SPEED || 0.25);
    window.GAP = 0.07;
    window.X_STEP = window.SIZE_BOTTOM + window.GAP;
    
    // 5. Centrowanie i wymiary siatki
    window.N_PER_ROW = 6; 
    window.X_START = -((window.N_PER_ROW - 1) / 2) * window.X_STEP;
    window.WRAP_DISTANCE = window.N_PER_ROW * window.X_STEP;
    
    // 6. Losowanie Celów (Targets)
    let rawTargets = window.safeSample(window.POOL, 2);
    window.targets = rawTargets.map(t => t.split('/').pop().split('\\').pop());
    
    // 7. Tworzenie Stimulów Górnych (Cele)
    window.top_stims = [];
    for (let i = 0; i < 2; i++) {
      let xPos = (i === 0) ? -0.25 : 0.25;
      let stim = new visual.ImageStim({
        win: psychoJS.window,
        image: window.IMAGE_PATH + window.targets[i],
        pos: [xPos, window.TOP_Y],
        size: [window.SIZE_TOP, window.SIZE_TOP],
        units: 'height'
      });
      stim.imgName = window.targets[i];
      stim.clicked = false;
      window.top_stims.push(stim);
    }
    
    // 8. Przygotowanie sekwencji
    let items_per_sec = window.SPEED / window.X_STEP;
    window.items_needed_per_row = Math.ceil(items_per_sec * 35) + (window.N_PER_ROW * 2);
    
    let baseSeq = window.makeSequence(window.POOL, window.items_needed_per_row * 2);
    baseSeq.splice(4, 0, window.targets[0]); 
    baseSeq.splice(8, 0, window.targets[1]);
    window.bottom_sequence = baseSeq;
    
    window.bottom_stims = [];
    window.prev_x = [];
    
    // 9. TWORZENIE FIGUR DOLNYCH (Start poza ekranem)
    for (let idx = 0; idx < window.N_PER_ROW * 2; idx++) {
      let col = idx % window.N_PER_ROW;
      let row = Math.floor(idx / window.N_PER_ROW);
    
      // Pozycja X przesunięta w lewo
      let standardX = window.X_START + (col * window.X_STEP);
      let x = standardX - 1.8; 
      let y = (row === 0) ? window.ROW1_Y : window.ROW2_Y;
    
      let imgFile = window.bottom_sequence.shift();
      let cleanName = imgFile.split('/').pop().split('\\').pop();
    
      let stim = new visual.ImageStim({
        win: psychoJS.window,
        image: window.IMAGE_PATH + imgFile,
        pos: [x, y],
        size: [window.SIZE_BOTTOM, window.SIZE_BOTTOM],
        units: 'height'
      });
    
      stim.imgName = cleanName;
      stim.clicked = false;
      stim.counted = false;
      stim.setOpacity(1.0);
    
      window.bottom_stims.push(stim);
      window.prev_x.push(x);
    }
    
    // 10. Licznik
    window.correctCounter = new visual.TextStim({
      win: psychoJS.window,
      text: 'Poprawne: 0',
      pos: [0.6, 0.45],
      height: 0.035,
      color: new util.Color('white'),
      units: 'height'
    });
    
    window._fixed_spacing_done = true;
    // setup some python lists for storing info about the mouse
    // current position of the mouse:
    mouse.x = [];
    mouse.y = [];
    mouse.leftButton = [];
    mouse.midButton = [];
    mouse.rightButton = [];
    mouse.time = [];
    gotValidClick = false; // until a click is received
    psychoJS.experiment.addData('trials.started', globalClock.getTime());
    trialsMaxDuration = null
    // keep track of which components have finished
    trialsComponents = [];
    trialsComponents.push(mouse);
    
    for (const thisComponent of trialsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var dt;
var prevButtonState;
var _mouseButtons;
var _mouseXYs;
function trialsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trials' ---
    // get current time
    t = trialsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    // --- HANDLE CLICKS ---
    let dt = 1.0 / 60.0;
    if (typeof frameClock !== 'undefined') {
        dt = frameClock.getTime();
        frameClock.reset();
    }
    
    // Czas od początku próby
    let elapsed = window.trialClock.getTime();
    
    // Obsługa myszy
    let buttons = window.mouse.getPressed();
    let isNewClick = buttons[0] && !window._prevMouseButtons[0];
    window._prevMouseButtons = [buttons[0], buttons[1], buttons[2]];
    
    if (isNewClick) {
        window.total_presses++;
        let clickPos = window.mouse.getPos();
        
        let candidates = [];
        let hitBoxSize = window.SIZE_BOTTOM * 1.3; 
    
        for (let stim of window.bottom_stims) {
            if (stim.clicked) continue; 
            
            let dx = Math.abs(clickPos[0] - stim.pos[0]);
            let dy = Math.abs(clickPos[1] - stim.pos[1]);
            
            if (dx < (hitBoxSize / 2) && dy < (hitBoxSize / 2)) {
                let distSq = dx * dx + dy * dy;
                candidates.push({ stim: stim, dist: distSq });
            }
        }
        
        if (candidates.length > 0) {
            candidates.sort((a, b) => a.dist - b.dist);
            let selectedStim = candidates[0].stim;
            let isCorrect = window.targets.includes(selectedStim.imgName) ? 1 : 0;
            
            if (isCorrect) {
                window.target_presses++;
                selectedStim.clicked = true;
                selectedStim.setOpacity(0.0);
            } else {
                selectedStim.clicked = true; 
                selectedStim.setOpacity(0.2);
            }
            
            window.clicked_records.push({
                time: elapsed,
                stim_image: selectedStim.imgName,
                is_correct: isCorrect,
                x: clickPos[0],
                y: clickPos[1]
            });
            
            window.correctCounter.setText('Poprawne: ' + window.target_presses);
        }
    }
    
    // Ruch dolnych figur
    for (let i = 0; i < window.bottom_stims.length; i++) {
        let stim = window.bottom_stims[i];
        let newX = stim.pos[0] + (window.SPEED * dt);
        
        let prevX = window.prev_x[i];
        if (prevX < window.APPEAR_X && newX >= window.APPEAR_X && !stim.counted) {
            if (window.targets.includes(stim.imgName)) {
                window.target_appearances++;
            }
            stim.counted = true;
        }
    
        if (newX > (window.X_START + window.WRAP_DISTANCE)) {
            newX -= window.WRAP_DISTANCE;
            
            let nextImg = window.bottom_sequence.length > 0 
                          ? window.bottom_sequence.shift() 
                          : window.POOL[Math.floor(Math.random() * window.POOL.length)];
            
            let cleanName = nextImg.split('/').pop().split('\\').pop();
            
            stim.setImage(window.IMAGE_PATH + nextImg);
            stim.imgName = cleanName;
            stim.clicked = false;
            stim.counted = false;
            stim.setOpacity(1.0);
        }
        
        stim.setPos([newX, stim.pos[1]]);
        window.prev_x[i] = newX;
        
        if (stim.opacity > 0) {
            stim.draw();
        }
    }
    
    for (let topStim of window.top_stims) topStim.draw();
    window.correctCounter.draw();
    
    // Zmiana celów w połowie
    if (!window.change_done && elapsed >= window.TARGET_CHANGE_TIME) {
        let newTargets = window.safeSample(window.POOL, 2).map(t => t.split('/').pop().split('\\').pop());
        window.targets = newTargets;
        for (let j = 0; j < window.top_stims.length; j++) {
            window.top_stims[j].setImage(window.IMAGE_PATH + window.targets[j]);
            window.top_stims[j].imgName = window.targets[j];
        }
        let injection = window.makeSequence(window.targets, 4);
        window.bottom_sequence = injection.concat(window.bottom_sequence);
        window.change_done = true;
    }
    
    if (window.bottom_sequence.length < 20) {
        window.bottom_sequence = window.bottom_sequence.concat(window.makeSequence(window.POOL, 20));
    }
    
    // --- NAPRAWA: ZAKOŃCZENIE PRÓBY PO CZASIE ---
    if (elapsed >= window.TRIAL_DURATION) {
        continueRoutine = false;
    }
    // *mouse* updates
    if (t >= 0.0 && mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse.tStart = t;  // (not accounting for frame time here)
      mouse.frameNStart = frameN;  // exact frame index
      
      mouse.status = PsychoJS.Status.STARTED;
      mouse.mouseClock.reset();
      prevButtonState = mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse is active this frame...
    if (mouse.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
          _mouseXYs = mouse.getPos();
          mouse.x.push(_mouseXYs[0]);
          mouse.y.push(_mouseXYs[1]);
          mouse.leftButton.push(_mouseButtons[0]);
          mouse.midButton.push(_mouseButtons[1]);
          mouse.rightButton.push(_mouseButtons[2]);
          mouse.time.push(mouse.mouseClock.getTime());
          if (gotValidClick === true) { // end routine on response
            continueRoutine = false;
          }
        }
      }
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      routineForceEnded = true;
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of trialsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function trialsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'trials' ---
    for (const thisComponent of trialsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('trials.stopped', globalClock.getTime());
    // ===== END ROUTINE (trials) =====
    psychoJS.experiment.addData('Total_Clicks', window.total_presses);
    psychoJS.experiment.addData('Correct_Clicks', window.target_presses);
    psychoJS.experiment.addData('Target_Appearances', window.target_appearances);
    
    // zapis clicków
    for (let idx = 0; idx < window.clicked_records.length; idx++) {
      let rec = window.clicked_records[idx];
      psychoJS.experiment.addData('click_' + idx + '_time', rec.time !== undefined ? rec.time : -1);
      psychoJS.experiment.addData('click_' + idx + '_rt', rec.rt !== undefined ? rec.rt : -1);
      psychoJS.experiment.addData('click_' + idx + '_image', rec.stim_image !== undefined ? rec.stim_image : 'none');
      psychoJS.experiment.addData('click_' + idx + '_is_correct', rec.is_correct !== undefined ? rec.is_correct : 0);
      psychoJS.experiment.addData('click_' + idx + '_x', rec.click_x !== undefined ? rec.click_x : null);
      psychoJS.experiment.addData('click_' + idx + '_y', rec.click_y !== undefined ? rec.click_y : null);
    }
    
    // store mouse trace
    psychoJS.experiment.addData('mouse.x', window.mouse.x);
    psychoJS.experiment.addData('mouse.y', window.mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', window.mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', window.mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', window.mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', window.mouse.time);
    
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    
    // the Routine "trials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  // --- NOUS INTEGRATION: SEND DATA ---
  if (typeof window.electronTest !== 'undefined') {
      
      let standardData = psychoJS.experiment._trialsData;
      let customData = window.clicked_records || [];
  
      let correctCount = window.target_presses || 0;
      let totalClicks = window.total_presses || 0;
      let appearances = window.target_appearances || 0;
      
      // Obliczamy skuteczność (Celność trafień)
      let accuracy = totalClicks > 0 ? Math.round((correctCount / totalClicks) * 100) : 0;
      
      // Opcjonalnie: Skuteczność wykrywania (ile celów wyłapał spośród wszystkich, które przeleciały)
      let detectionRate = appearances > 0 ? Math.round((correctCount / appearances) * 100) : 0;
  
      let payload = {
          testId: expInfo['expName'] || "Poppelv2",
          subjectId: expInfo['participant'],
          timestamp: new Date().toISOString(),
          
          // GŁÓWNY WYNIK: Ustawiamy 0 lub Skuteczność, bo RT nie jest mierzone
          // W platformie Nous pole to często jest wymagane jako "liczba" do sortowania.
          czas_reakcji: accuracy, // Tutaj wysyłamy % skuteczności jako główny "score" liczbowy
          
          // OPIS DLA UŻYTKOWNIKA
          score: `Trafienia: ${correctCount} | Skuteczność: ${accuracy}%`,
          
          statystyki: {
              poprawne: correctCount,
              bledy: totalClicks - correctCount,
              wszystkie_kliki: totalClicks,
              wszystkie_cele_na_ekranie: appearances,
              skutecznosc_klikniec: accuracy,       // % dobrych kliknięć
              skutecznosc_wykrywania: detectionRate // % wyłapanych celów
          },
          
          wyniki: standardData,
          wyniki_szczegolowe: customData
      };
  
      console.log("Wysyłanie do Nous...", payload);
      window.electronTest.sendResults(payload);
  
  } else {
      console.log("Tryb przeglądarki - standardowy zapis CSV.");
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
