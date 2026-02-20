/******************** 
 * Bystreoczko *
 ********************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.1.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'bystreOczko';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};
let PILOTING = util.getUrlParameters().has('__pilotToken');
const TRIAL_TIMEOUT_SEC = 10.0;  // limit czasu na próbę; przy minięciu dodawany do średniego RT

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([(- 1.0), (- 1.0), (- 1.0)]),
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
flowScheduler.add(welcomeRoutineBegin());
flowScheduler.add(welcomeRoutineEachFrame());
flowScheduler.add(welcomeRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);


flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'resources/syg.png', 'path': 'resources/syg.png'},
    {'name': 'resources/sygCzer.png', 'path': 'resources/sygCzer.png'},
    {'name': 'resources/sygZiel.png', 'path': 'resources/sygZiel.png'},
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


var welcomeClock;
var text;
var key_resp;
var trialClock;
var mouse;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "welcome"
  welcomeClock = new util.Clock();
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: 'Przed tobą pojawi się plansza z sygnalizatorami. W losowym interwale czasu jeden z nich zapali się na zielono. Twoim zadaniem jest naciśnięcie na sygnalizator z zielonym światłem. W przypadku poprawnego trafienia wszystkie zapalą się na zielono. W przypadku błędnego trafienia, wszystkie zgasną. Powodzenia!',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  // --- NOUS INTEGRATION: INIT ---
  if (typeof window.electronTest !== 'undefined') {
      psychoJS.experiment.save = function() { return Promise.resolve(); };
  }
  
  // --- KONFIGURACJA SIATKI ---
  window.ROWS = 3;
  window.COLS = 6;
  
  // Współrzędne
  let x_coords = [];
  for (let i = 0; i < window.COLS; i++) {
      x_coords.push((i - (window.COLS - 1) / 2) * 0.18);
  }
  let y_coords = [0.2, 0.0, -0.2];
  
  // FIZYCZNE TWORZENIE OBIEKTÓW (Tego brakowało!)
  window.lights = [];
  for (let r = 0; r < window.ROWS; r++) {
      let rowStims = [];
      for (let c = 0; c < window.COLS; c++) {
          let stim = new visual.ImageStim({
              win: psychoJS.window,
              image: 'resources/sygCzer.png',
              size: [0.12, 0.12],
              pos: [x_coords[c], y_coords[r]]
          });
          rowStims.push(stim);
      }
      window.lights.push(rowStims);
  }
  
  // Inicjalizacja zmiennych stanu
  window.clicked_row = null;
  window.clicked_col = null;
  window.target_row = 0;
  window.target_col = 0;
  window.green_is_on = false;
  window.responded = false;
  window.rt = null;
  window.correct = 0;
  window.greenOnset = 0;
  window.feedbackTime = 0.5;
  window.prevMouseState = false;
  
  window.rtClock = new util.Clock();
  window.feedbackClock = new util.Clock();
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine

  // --- EKRAN DOTYKOWY: konwersja touch -> PsychoJS "height" units ---
  window._touchJustStarted = false;
  window._touchPsychoX = null;
  window._touchPsychoY = null;
  window._touchCanvas = null;
  let canvas = (psychoJS.window._renderer && psychoJS.window._renderer.view) || document.querySelector('canvas');
  if (canvas) {
    window._touchCanvas = canvas;
    function touchToPsycho(clientX, clientY) {
      let r = canvas.getBoundingClientRect();
      let aspect = r.width / r.height;
      return {
        x: (2 * (clientX - r.left) / r.width - 1) * aspect,
        y: 1 - 2 * (clientY - r.top) / r.height
      };
    }
    canvas.addEventListener('touchstart', function (e) {
      e.preventDefault();
      if (e.touches.length > 0) {
        let p = touchToPsycho(e.touches[0].clientX, e.touches[0].clientY);
        window._touchJustStarted = true;
        window._touchPsychoX = p.x;
        window._touchPsychoY = p.y;
      }
    }, { passive: false });
    canvas.addEventListener('touchend', function (e) { e.preventDefault(); }, { passive: false });
    canvas.addEventListener('touchmove', function (e) { e.preventDefault(); }, { passive: false });
  }

  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var welcomeMaxDurationReached;
var _key_resp_allKeys;
var welcomeMaxDuration;
var welcomeComponents;
function welcomeRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'welcome' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    welcomeClock.reset();
    routineTimer.reset();
    welcomeMaxDurationReached = false;
    // update component parameters for each repeat
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    psychoJS.experiment.addData('welcome.started', globalClock.getTime());
    welcomeMaxDuration = null
    // keep track of which components have finished
    welcomeComponents = [];
    welcomeComponents.push(text);
    welcomeComponents.push(key_resp);
    
    for (const thisComponent of welcomeComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function welcomeRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'welcome' ---
    // get current time
    t = welcomeClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *text* updates
    if (t >= 0.0 && text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      text.tStart = t;  // (not accounting for frame time here)
      text.frameNStart = frameN;  // exact frame index
      
      text.setAutoDraw(true);
    }
    
    
    // if text is active this frame...
    if (text.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *key_resp* updates
    if (t >= 0.0 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp.tStart = t;  // (not accounting for frame time here)
      key_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp.clearEvents(); });
    }
    
    // if key_resp is active this frame...
    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: ['y','n','left','right','space'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
        key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
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
    for (const thisComponent of welcomeComponents)
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


function welcomeRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'welcome' ---
    for (const thisComponent of welcomeComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('welcome.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp.corr, level);
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
        routineTimer.reset();
        }
    
    key_resp.stop();
    // the Routine "welcome" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var trials;
function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 10, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(trialRoutineBegin(snapshot));
      trialsLoopScheduler.add(trialRoutineEachFrame());
      trialsLoopScheduler.add(trialRoutineEnd(snapshot));
      trialsLoopScheduler.add(trialsLoopEndIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}


var trialMaxDurationReached;
var gotValidClick;
var trialMaxDuration;
var trialComponents;
function trialRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'trial' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    trialClock.reset();
    routineTimer.reset();
    trialMaxDurationReached = false;
    // update component parameters for each repeat
    // Reset stanu przed nową próbą
    window.clicked_row = null;
    window.clicked_col = null;
    window.green_is_on = false;
    window.responded = false;
    window.rt = null;
    window.correct = 0;
    
    // Przywrócenie czerwonego koloru wszystkim światłom
    for (let r = 0; r < window.ROWS; r++) {
        for (let c = 0; c < window.COLS; c++) {
            window.lights[r][c].setImage('resources/sygCzer.png');
            window.lights[r][c].setOpacity(1.0);
        }
    }
    
    // Losowanie momentu zapalenia i pozycji celu
    window.greenOnset = 1.0 + Math.random() * 3.0; 
    window.target_row = Math.floor(Math.random() * window.ROWS);
    window.target_col = Math.floor(Math.random() * window.COLS);
    
    window.rtClock.reset();
    window.feedbackClock.reset();
    
    // Zabezpieczenie przed trzymaniem przycisku myszy
    let currentButtons = mouse.getPressed();
    window.prevMouseState = (currentButtons[0] || currentButtons[1] || currentButtons[2]);
    // setup some python lists for storing info about the mouse
    gotValidClick = false; // until a click is received
    mouse.mouseClock.reset();
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(mouse);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var prevButtonState;
var _mouseButtons;
function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    let currentTime = trialClock.getTime();
    
    // 1. Włączanie zielonego światła
    if (!window.green_is_on && currentTime >= window.greenOnset) {
        window.green_is_on = true;
        window.lights[window.target_row][window.target_col].setImage('resources/sygZiel.png');
        window.rtClock.reset();
    }
    
    // 2. Rysowanie siatki
    for (let r = 0; r < window.ROWS; r++) {
        for (let c = 0; c < window.COLS; c++) {
            window.lights[r][c].draw();
        }
    }
    
    // 3. Obsługa kliknięcia (mysz) lub dotknięcia (ekran dotykowy)
    let buttons = mouse.getPressed();
    let isPressedNow = (buttons[0] || buttons[1] || buttons[2]);
    let isNewClick = isPressedNow && !window.prevMouseState;
    window.prevMouseState = isPressedNow;

    function pointInStim(px, py, stim) {
      let pos = stim.pos || stim._pos;
      let size = stim.size || stim._size || [0.12, 0.12];
      if (!pos || (typeof pos[0] !== 'number') || (typeof pos[1] !== 'number')) return false;
      let hx = (Array.isArray(size) ? size[0] : size) / 2;
      let hy = (Array.isArray(size) ? size[1] : size) / 2;
      return Math.abs(px - pos[0]) <= hx && Math.abs(py - pos[1]) <= hy;
    }

    if (window.green_is_on && !window.responded && isNewClick) {
        for (let r = 0; r < window.ROWS; r++) {
            for (let c = 0; c < window.COLS; c++) {
                if (mouse.isPressedIn(window.lights[r][c])) {
                    window.responded = true;
                    window.clicked_row = r;
                    window.clicked_col = c;
                    window.rt = window.rtClock.getTime();
                    window.correct = (r === window.target_row && c === window.target_col) ? 1 : 0;
                    // Feedback wizualny
                    let feedbackImg = (window.correct === 1) ? 'resources/sygZiel.png' : 'resources/syg.png';
                    for (let rr = 0; rr < window.ROWS; rr++) {
                        for (let cc = 0; cc < window.COLS; cc++) {
                            window.lights[rr][cc].setImage(feedbackImg);
                        }
                    }
                    window.feedbackClock.reset();
                    break;
                }
            }
            if (window.responded) break;
        }
    }
    // Ekran dotykowy: traktuj dotknięcie jak kliknięcie
    if (window.green_is_on && !window.responded && window._touchJustStarted && window._touchPsychoX != null && window._touchCanvas) {
        for (let r = 0; r < window.ROWS; r++) {
            for (let c = 0; c < window.COLS; c++) {
                if (pointInStim(window._touchPsychoX, window._touchPsychoY, window.lights[r][c])) {
                    window.responded = true;
                    window.clicked_row = r;
                    window.clicked_col = c;
                    window.rt = window.rtClock.getTime();
                    window.correct = (r === window.target_row && c === window.target_col) ? 1 : 0;
                    let feedbackImg = (window.correct === 1) ? 'resources/sygZiel.png' : 'resources/syg.png';
                    for (let rr = 0; rr < window.ROWS; rr++) {
                        for (let cc = 0; cc < window.COLS; cc++) {
                            window.lights[rr][cc].setImage(feedbackImg);
                        }
                    }
                    window.feedbackClock.reset();
                    break;
                }
            }
            if (window.responded) break;
        }
        window._touchJustStarted = false;
        window._touchPsychoX = null;
        window._touchPsychoY = null;
    } else if (window._touchJustStarted) {
        window._touchJustStarted = false;
        window._touchPsychoX = null;
        window._touchPsychoY = null;
    }
    
    // 4. Koniec próby (po feedbacku lub po timeout)
    if (window.responded && window.feedbackClock.getTime() >= window.feedbackTime) {
        continueRoutine = false;
    }
    
    if (currentTime >= TRIAL_TIMEOUT_SEC) {
        continueRoutine = false;
    }
    // *mouse* updates
    if (t >= 0.0 && mouse.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      mouse.tStart = t;  // (not accounting for frame time here)
      mouse.frameNStart = frameN;  // exact frame index
      
      mouse.status = PsychoJS.Status.STARTED;
      prevButtonState = mouse.getPressed();  // if button is down already this ISN'T a new click
    }
    
    // if mouse is active this frame...
    if (mouse.status === PsychoJS.Status.STARTED) {
      _mouseButtons = mouse.getPressed();
      if (!_mouseButtons.every( (e,i,) => (e == prevButtonState[i]) )) { // button state changed?
        prevButtonState = _mouseButtons;
        if (_mouseButtons.reduce( (e, acc) => (e+acc) ) > 0) { // state changed to a new click
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
    for (const thisComponent of trialComponents)
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


var _mouseXYs;
function trialRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'trial' ---
    for (const thisComponent of trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('trial.stopped', globalClock.getTime());
    psychoJS.experiment.addData('greenOnset', window.greenOnset);
    psychoJS.experiment.addData('target_row', window.target_row);
    psychoJS.experiment.addData('target_col', window.target_col);
    psychoJS.experiment.addData('rt', window.rt);
    psychoJS.experiment.addData('correct', window.correct);
    // store data for psychoJS.experiment (ExperimentHandler)
    _mouseXYs = mouse.getPos();
    _mouseButtons = mouse.getPressed();
    psychoJS.experiment.addData('mouse.x', _mouseXYs[0]);
    psychoJS.experiment.addData('mouse.y', _mouseXYs[1]);
    psychoJS.experiment.addData('mouse.leftButton', _mouseButtons[0]);
    psychoJS.experiment.addData('mouse.midButton', _mouseButtons[1]);
    psychoJS.experiment.addData('mouse.rightButton', _mouseButtons[2]);
    // the Routine "trial" was not non-slip safe, so reset the non-slip timer
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
  if (typeof window.electronTest !== 'undefined') {
      if (isCompleted) {
          // Tylko wiersze z prób (pomijamy np. wiersz z rutyny welcome)
          let allData = (psychoJS.experiment._trialsData || []).filter(function (t) { return typeof t.correct !== 'undefined'; });
          let correctCount = 0;   // naciśnięcie na zielone
          let wrongCount = 0;     // naciśnięcie na czerwone
          let sumRT = 0;          // suma czasów reakcji (s); przy timeout +TRIAL_TIMEOUT_SEC

          for (let trial of allData) {
              if (trial.correct === 1) {
                  correctCount++;
              } else if (typeof trial.rt === 'number' && trial.rt >= 0) {
                  wrongCount++;
              }
              let rtSec = (typeof trial.rt === 'number' && trial.rt >= 0) ? trial.rt : TRIAL_TIMEOUT_SEC;
              sumRT += rtSec;
          }

          let totalClicks = correctCount + wrongCount;
          let nTrials = allData.length;
          let avgRTms = nTrials > 0 ? Math.round((sumRT / nTrials) * 1000) : 0;

          window.electronTest.sendResults({
              testId: expInfo['expName'],
              subjectId: expInfo['participant'],
              timestamp: new Date().toISOString(),
              ilosc_poprawnych_nacisniec: correctCount,
              ilosc_blednych_nacisniec: wrongCount,
              ogolna_ilosc_nacisniec: totalClicks,
              sredni_czas_reakcji: avgRTms,
              czas_reakcji: avgRTms,
              score: `Poprawne: ${correctCount} | Błędne: ${wrongCount} | Łącznie: ${totalClicks} | Śr. RT: ${avgRTms} ms`,
              wyniki: allData
          });
      } else {
          window.electronTest.close();
      }
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
