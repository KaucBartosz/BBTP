/************** 
 * Raven *
 **************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.1.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'Raven';  // from the Builder filename that created this script
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
  backgroundImage: 'resources/tlo.png',
  backgroundFit: 'fill',
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
    {'name': 'resources/bike.png', 'path': 'resources/bike.png'},
    {'name': 'resources/car.png', 'path': 'resources/car.png'},
    {'name': 'resources/train.png', 'path': 'resources/train.png'},
    {'name': 'resources/tram.png', 'path': 'resources/tram.png'},
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
    text: 'Witaj w teście matryc logicznych.\n\nTwoim zadaniem jest uzupełnienie brakującego fragmentu wzoru.\n\n1. W górnej części ekranu zobaczysz układ obrazków z jednym pustym polem.\n\n2. Spośród czterech obrazków na dole wybierz ten, który Twoim zdaniem najlepiej pasuje do całości.\n\nW tym badaniu liczy się przede wszystkim poprawność Twoich odpowiedzi.\n\nNaciśnij SPACJĘ, aby rozpocząć',
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
  
  // Inicjalizacja punktacji
  window.score = 0;
  window.lastAnswerIndex = -1;
  
  // --- OPTYMALIZACJA: TWORZENIE OBIEKTÓW RAZ ---
  window.matrixStimuli = [];
  for (let i = 0; i < 3; i++) {
      window.matrixStimuli.push(new visual.ImageStim({
          win: psychoJS.window,
          size: [0.15, 0.15],
          opacity: 0 // ukryte na starcie
      }));
  }
  
  window.choiceStimuli = [];
  for (let i = 0; i < 4; i++) {
      window.choiceStimuli.push(new visual.ImageStim({
          win: psychoJS.window,
          size: [0.15, 0.15],
          opacity: 0 // ukryte na starcie
      }));
  }
  mouse = new core.Mouse({
    win: psychoJS.window,
  });
  mouse.mouseClock = new util.Clock();
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine

  // --- Obsługa ekranu dotykowego (NOUS) ---
  window._touchJustStarted = false;
  window._touchPsychoX = null;
  window._touchPsychoY = null;
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
    // Resetujemy punkty przed startem testu
    window.score = 0;
    
    // Upewniamy się, że mysz jest widoczna
    psychoJS.window.mouseVisible = true;
    
    // Czyścimy bufor klawiatury
    psychoJS.eventManager.clearEvents();
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
    
    // Sprawdzamy naciśnięcie spacji
    let keys = psychoJS.eventManager.getKeys({keyList: ['space']});
    
    if (keys.length > 0) {
        continueRoutine = false; // Kończymy powitanie i zaczynamy test
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
    // Możemy zresetować zegar globalny, aby czas testu liczony był od zakończenia instrukcji
    globalClock.reset();
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
var possibleIndices;
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
    // 1. Zabezpieczenie myszy
    window.mouseLock = mouse.getPressed()[0] === 1;
    
    // 2. Logika losowania (bez powtórzeń)
    let allImages = ['resources/bike.png', 'resources/car.png', 'resources/train.png', 'resources/tram.png'];
    let possibleIndices = [0, 1, 2, 3];
    if (window.lastAnswerIndex !== -1) {
        possibleIndices = possibleIndices.filter(idx => idx !== window.lastAnswerIndex);
    }
    let finalIndex = possibleIndices[Math.floor(Math.random() * possibleIndices.length)];
    window.lastAnswerIndex = finalIndex;
    window.correctAnswer = allImages[finalIndex];
    
    // 3. Aktualizacja Matrycy (Góra)
    let matrixPositions = [[-0.15, 0.25], [0.15, 0.25], [-0.15, 0.05]];
    for (let i = 0; i < 3; i++) {
        window.matrixStimuli[i].setImage(window.correctAnswer);
        window.matrixStimuli[i].setPos(matrixPositions[i]);
        window.matrixStimuli[i].setOpacity(1);
        window.matrixStimuli[i].setAutoDraw(true);
    }
    
    // 4. Aktualizacja Wyborów (Dół)
    let choicePositions = [[-0.3, -0.35], [-0.1, -0.35], [0.1, -0.35], [0.3, -0.35]];
    for (let i = 0; i < 4; i++) {
        window.choiceStimuli[i].setImage(allImages[i]);
        window.choiceStimuli[i].setPos(choicePositions[i]);
        window.choiceStimuli[i].setOpacity(1);
        window.choiceStimuli[i].setAutoDraw(true);
    }
    
    window.responseGiven = false;
    // setup some python lists for storing info about the mouse
    // current position of the mouse:
    mouse.x = [];
    mouse.y = [];
    mouse.leftButton = [];
    mouse.midButton = [];
    mouse.rightButton = [];
    mouse.time = [];
    gotValidClick = false; // until a click is received
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
var _mouseXYs;
function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    // --- Each Frame ---
    
    // 1. Zarządzanie blokadą myszy (Anti-Cheat / Fast-Forward)
    // Jeśli użytkownik trzymał przycisk z poprzedniej rundy, 
    // czekamy aż go puści, zanim pozwolimy na wybór.
    if (window.mouseLock) {
        if (mouse.getPressed()[0] === 0) {
            window.mouseLock = false; 
        }
    }
    

    function pointInStim(px, py, stim) {
      let pos = stim.pos || stim._pos;
      let size = stim.size || stim._size || [0.15, 0.15];
      if (!pos || (typeof pos[0] !== 'number') || (typeof pos[1] !== 'number')) return false;
      let hx = (Array.isArray(size) ? size[0] : size) / 2;
      let hy = (Array.isArray(size) ? size[1] : size) / 2;
      return Math.abs(px - pos[0]) <= hx && Math.abs(py - pos[1]) <= hy;
    }

    // 2. Sprawdzanie kliknięcia w opcje odpowiedzi (mysz)
    if (!window.mouseLock && !window.responseGiven) {
        
        for (let i = 0; i < window.choiceStimuli.length; i++) {
            let stim = window.choiceStimuli[i];
            
            // Sprawdzamy, czy lewy przycisk myszy jest wciśnięty nad danym obrazkiem
            if (mouse.getPressed()[0] === 1 && stim.contains(mouse)) {
                
                window.responseGiven = true;
                let reactionTime = trialClock.getTime(); // Czas namysłu nad matrycą
                
                // Tablica nazw obrazków (musi być w tej samej kolejności co w Begin Routine)
                let allImages = [
                    'resources/bike.png', 
                    'resources/car.png', 
                    'resources/train.png', 
                    'resources/tram.png'
                ];
                
                let clickedImageName = allImages[i];
                let isCorrect = (clickedImageName === window.correctAnswer) ? 1 : 0;
    
                // --- Logika zapisu i punktacji ---
                window.score += isCorrect;
                
                // Rejestrujemy dane w PsychoPy (dla statystyk w End Experiment)
                psychoJS.experiment.addData('rt', reactionTime);
                psychoJS.experiment.addData('selected_image', clickedImageName);
                psychoJS.experiment.addData('target_image', window.correctAnswer);
                psychoJS.experiment.addData('correct', isCorrect);
                
                // Koniec rutyny - przejście do następnego zadania
                continueRoutine = false;
            }
        }
    }

    // 2b. Sprawdzanie dotyku w opcje odpowiedzi
    if (!window.responseGiven && window._touchJustStarted && window._touchPsychoX != null && window._touchCanvas) {
      for (let i = 0; i < window.choiceStimuli.length; i++) {
        let stim = window.choiceStimuli[i];
        if (stim.opacity === 0) continue;
        if (pointInStim(window._touchPsychoX, window._touchPsychoY, stim)) {
          window.responseGiven = true;
          let reactionTime = trialClock.getTime();
          let allImages = [
            'resources/bike.png',
            'resources/car.png',
            'resources/train.png',
            'resources/tram.png'
          ];
          let clickedImageName = allImages[i];
          let isCorrect = (clickedImageName === window.correctAnswer) ? 1 : 0;
          window.score += isCorrect;
          psychoJS.experiment.addData('rt', reactionTime);
          psychoJS.experiment.addData('selected_image', clickedImageName);
          psychoJS.experiment.addData('target_image', window.correctAnswer);
          psychoJS.experiment.addData('correct', isCorrect);
          continueRoutine = false;
          break;
        }
      }
      window._touchJustStarted = false;
      window._touchPsychoX = null;
      window._touchPsychoY = null;
    } else if (window._touchJustStarted) {
      window._touchJustStarted = false;
      window._touchPsychoX = null;
      window._touchPsychoY = null;
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


function trialRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'trial' ---
    for (const thisComponent of trialComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('trial.stopped', globalClock.getTime());
    // Sprzątanie (ukrywanie)
    for (let stim of window.matrixStimuli) stim.setAutoDraw(false);
    for (let stim of window.choiceStimuli) stim.setAutoDraw(false);
    
    // Zapis punktacji do PsychoPy
    psychoJS.experiment.addData('total_score', window.score);
    // store data for psychoJS.experiment (ExperimentHandler)
    psychoJS.experiment.addData('mouse.x', mouse.x);
    psychoJS.experiment.addData('mouse.y', mouse.y);
    psychoJS.experiment.addData('mouse.leftButton', mouse.leftButton);
    psychoJS.experiment.addData('mouse.midButton', mouse.midButton);
    psychoJS.experiment.addData('mouse.rightButton', mouse.rightButton);
    psychoJS.experiment.addData('mouse.time', mouse.time);
    
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
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  if (typeof window.electronTest !== 'undefined') {
      if (isCompleted) {
          let allData = (psychoJS.experiment._trialsData || []).filter(function (t) { return typeof t.correct !== 'undefined'; });
          let poprawneNacisniecia = 0;
          let wszystkieNacisniecia = 0;
          let sumRT = 0;
          let validRTCount = 0;

          for (let trial of allData) {
              if (typeof trial.correct !== 'undefined') {
                  wszystkieNacisniecia++;
                  if (trial.correct === 1) {
                      poprawneNacisniecia++;
                  }
                  if (typeof trial.rt === 'number' && trial.rt >= 0) {
                      sumRT += trial.rt;
                      validRTCount++;
                  }
              }
          }

          let bledneNacisniecia = Math.max(0, wszystkieNacisniecia - poprawneNacisniecia);
          let sredniCzasReakcji = validRTCount > 0 ? Math.round((sumRT / validRTCount) * 1000) : 0;
          let accuracy = wszystkieNacisniecia > 0 ? Math.round((poprawneNacisniecia / wszystkieNacisniecia) * 100) : 0;

          window.electronTest.sendResults({
              testId: expInfo['expName'] || 'Raven',
              subjectId: expInfo['participant'],
              timestamp: new Date().toISOString(),
              ilosc_poprawnych_nacisniec: poprawneNacisniecia,
              ilosc_blednych_nacisniec: bledneNacisniecia,
              ogolna_ilosc_nacisniec: wszystkieNacisniecia,
              sredni_czas_reakcji: sredniCzasReakcji,
              score: `Poprawne: ${poprawneNacisniecia} | Błędne: ${bledneNacisniecia} | Łącznie: ${wszystkieNacisniecia} | Skuteczność: ${accuracy}% | Śr. RT: ${sredniCzasReakcji} ms`,
              statystyki: {
                  poprawne: poprawneNacisniecia,
                  bledne: bledneNacisniecia,
                  wszystkie: wszystkieNacisniecia,
                  skutecznosc_proc: accuracy,
                  sredni_czas_ms: sredniCzasReakcji
              },
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
