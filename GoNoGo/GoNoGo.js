/*************** 
 * Gonogo *
 ***************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2025.1.1.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'GoNoGo';  // from the Builder filename that created this script
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
flowScheduler.add(instructionsRoutineBegin());
flowScheduler.add(instructionsRoutineEachFrame());
flowScheduler.add(instructionsRoutineEnd());
flowScheduler.add(DifficultyRoutineBegin());
flowScheduler.add(DifficultyRoutineEachFrame());
flowScheduler.add(DifficultyRoutineEnd());
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


var instructionsClock;
var instrText;
var instrKey;
var DifficultyClock;
var text;
var key_diff;
var trialClock;
var key_resp;
var numberStim;
var feedbackClock;
var feedbackStim;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "instructions"
  instructionsClock = new util.Clock();
  instrText = new visual.TextStim({
    win: psychoJS.window,
    name: 'instrText',
    text: 'Witaj w teście Go/NoGo!\n\nTwoim zadaniem jest reagowanie na liczby:\n\nPARZYSTE (0, 2, 4, 6, 8)\n-> Naciśnij SPACJĘ (Szybko!)\n\nNIEPARZYSTE (1, 3, 5, 7, 9)\n-> Nic nie rób (Czekaj)\n\n\nNaciśnij SPACJĘ, aby rozpocząć.',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  instrKey = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "Difficulty"
  DifficultyClock = new util.Clock();
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: 'Wybierz poziom trudności:\n\n1 - ŁATWY (1.5 sekundy)\n2 - NORMALNY (1.0 sekunda)\n3 - TRUDNY (0.5 sekundy)\n\nNaciśnij 1, 2 lub 3.',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  key_diff = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // --- NOUS INTEGRATION: INIT ---
  if (typeof window.electronTest !== 'undefined') {
      console.log("Nous Launcher wykryty. Blokowanie zapisu CSV.");
      psychoJS.experiment.save = () => Promise.resolve(); 
  }
  
  // Inicjalizacja zmiennych globalnych (bezpieczniki)
  window.currentNumber = "Wait"; 
  window.trialCondition = "init";
  window.feedbackColor = "white";
  window.correctKey = undefined;
  
  // Domyślne wartości trudności
  window.decisionTime = 1.0; 
  window.difficultyName = "Normalny (Domyślny)";
  
  console.log("Eksperyment zainicjowany.");
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  // --- NOUS INTEGRATION: INIT ---
  if (typeof window.electronTest !== 'undefined') {
      psychoJS.experiment.save = () => Promise.resolve(); 
  }
  
  window.currentNumber = "Wait"; 
  window.trialCondition = "init";
  window.feedbackColor = "white"; // Nowa zmienna
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  numberStim = new visual.TextStim({
    win: psychoJS.window,
    name: 'numberStim',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.15,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -2.0 
  });
  
  // Initialize components for Routine "feedback"
  feedbackClock = new util.Clock();
  feedbackStim = new visual.TextStim({
    win: psychoJS.window,
    name: 'feedbackStim',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.15,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var routineForceEnded;
var instructionsMaxDurationReached;
var _instrKey_allKeys;
var instructionsMaxDuration;
var instructionsComponents;
function instructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    instructionsClock.reset();
    routineTimer.reset();
    instructionsMaxDurationReached = false;
    // update component parameters for each repeat
    instrKey.keys = undefined;
    instrKey.rt = undefined;
    _instrKey_allKeys = [];
    psychoJS.experiment.addData('instructions.started', globalClock.getTime());
    instructionsMaxDuration = null
    // keep track of which components have finished
    instructionsComponents = [];
    instructionsComponents.push(instrText);
    instructionsComponents.push(instrKey);
    
    for (const thisComponent of instructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function instructionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'instructions' ---
    // get current time
    t = instructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instrText* updates
    if (t >= 0.0 && instrText.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instrText.tStart = t;  // (not accounting for frame time here)
      instrText.frameNStart = frameN;  // exact frame index
      
      instrText.setAutoDraw(true);
    }
    
    
    // if instrText is active this frame...
    if (instrText.status === PsychoJS.Status.STARTED) {
    }
    
    
    // *instrKey* updates
    if (t >= 0.0 && instrKey.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instrKey.tStart = t;  // (not accounting for frame time here)
      instrKey.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { instrKey.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { instrKey.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { instrKey.clearEvents(); });
    }
    
    // if instrKey is active this frame...
    if (instrKey.status === PsychoJS.Status.STARTED) {
      let theseKeys = instrKey.getKeys({keyList: 'space', waitRelease: false});
      _instrKey_allKeys = _instrKey_allKeys.concat(theseKeys);
      if (_instrKey_allKeys.length > 0) {
        instrKey.keys = _instrKey_allKeys[_instrKey_allKeys.length - 1].name;  // just the last key pressed
        instrKey.rt = _instrKey_allKeys[_instrKey_allKeys.length - 1].rt;
        instrKey.duration = _instrKey_allKeys[_instrKey_allKeys.length - 1].duration;
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
    for (const thisComponent of instructionsComponents)
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


function instructionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'instructions' ---
    for (const thisComponent of instructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('instructions.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(instrKey.corr, level);
    }
    psychoJS.experiment.addData('instrKey.keys', instrKey.keys);
    if (typeof instrKey.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('instrKey.rt', instrKey.rt);
        psychoJS.experiment.addData('instrKey.duration', instrKey.duration);
        routineTimer.reset();
        }
    
    instrKey.stop();
    // the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var DifficultyMaxDurationReached;
var _key_diff_allKeys;
var DifficultyMaxDuration;
var DifficultyComponents;
function DifficultyRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Difficulty' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // keep track of whether this Routine was forcibly ended
    routineForceEnded = false;
    DifficultyClock.reset();
    routineTimer.reset();
    DifficultyMaxDurationReached = false;
    // update component parameters for each repeat
    key_diff.keys = undefined;
    key_diff.rt = undefined;
    _key_diff_allKeys = [];
    psychoJS.experiment.addData('Difficulty.started', globalClock.getTime());
    DifficultyMaxDuration = null
    // keep track of which components have finished
    DifficultyComponents = [];
    DifficultyComponents.push(text);
    DifficultyComponents.push(key_diff);
    
    for (const thisComponent of DifficultyComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function DifficultyRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Difficulty' ---
    // get current time
    t = DifficultyClock.getTime();
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
    
    
    // *key_diff* updates
    if (t >= 0.0 && key_diff.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_diff.tStart = t;  // (not accounting for frame time here)
      key_diff.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_diff.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_diff.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_diff.clearEvents(); });
    }
    
    // if key_diff is active this frame...
    if (key_diff.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_diff.getKeys({keyList: ['1','2','3'], waitRelease: false});
      _key_diff_allKeys = _key_diff_allKeys.concat(theseKeys);
      if (_key_diff_allKeys.length > 0) {
        key_diff.keys = _key_diff_allKeys[_key_diff_allKeys.length - 1].name;  // just the last key pressed
        key_diff.rt = _key_diff_allKeys[_key_diff_allKeys.length - 1].rt;
        key_diff.duration = _key_diff_allKeys[_key_diff_allKeys.length - 1].duration;
        // was this correct?
        if (key_diff.keys == '') {
            key_diff.corr = 1;
        } else {
            key_diff.corr = 0;
        }
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
    for (const thisComponent of DifficultyComponents)
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


var choice;
function DifficultyRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Difficulty' ---
    for (const thisComponent of DifficultyComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Difficulty.stopped', globalClock.getTime());
    // was no response the correct answer?!
    if (key_diff.keys === undefined) {
      if (['None','none',undefined].includes('')) {
         key_diff.corr = 1;  // correct non-response
      } else {
         key_diff.corr = 0;  // failed to respond (incorrectly)
      }
    }
    // store data for current loop
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_diff.corr, level);
    }
    psychoJS.experiment.addData('key_diff.keys', key_diff.keys);
    psychoJS.experiment.addData('key_diff.corr', key_diff.corr);
    if (typeof key_diff.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_diff.rt', key_diff.rt);
        psychoJS.experiment.addData('key_diff.duration', key_diff.duration);
        routineTimer.reset();
        }
    
    key_diff.stop();
    // --- OBSŁUGA WYBORU TRUDNOŚCI ---
    // Zakładamy, że masz komponent klawiatury o nazwie 'key_diff'
    
    let choice = '2'; // Domyślny fallback
    
    if (typeof key_diff !== 'undefined' && key_diff.keys) {
        // PsychoJS może zwrócić tablicę ['1'] lub string '1'
        if (Array.isArray(key_diff.keys)) {
            choice = key_diff.keys[0]; 
        } else {
            choice = key_diff.keys;
        }
    }
    
    // Ustawienie parametrów w zależności od klawisza
    if (choice === '1') {
        window.decisionTime = 1.5;
        window.difficultyName = "Łatwy (1.5s)";
    } else if (choice === '3') {
        window.decisionTime = 0.5;
        window.difficultyName = "Trudny (0.5s)";
    } else {
        window.decisionTime = 1.0;
        window.difficultyName = "Normalny (1.0s)";
    }
    
    console.log(`Wybrano poziom: ${window.difficultyName}`);
    
    // Zapisz wybór do danych (dla pewności)
    psychoJS.experiment.addData('difficulty_level', window.difficultyName);
    psychoJS.experiment.addData('decision_time_setting', window.decisionTime);
    // the Routine "Difficulty" was not non-slip safe, so reset the non-slip timer
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
      trialsLoopScheduler.add(feedbackRoutineBegin(snapshot));
      trialsLoopScheduler.add(feedbackRoutineEachFrame());
      trialsLoopScheduler.add(feedbackRoutineEnd(snapshot));
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
var _key_resp_allKeys;
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
    // --- LOGIKA PRÓBY ---
    
    // 1. Losowanie liczby 0-9
    let num = Math.floor(Math.random() * 10);
    window.currentNumber = num.toString(); 
    
    // 2. Logika: Parzyste (0,2,4,6,8) = GO, Nieparzyste = NOGO
    if (num % 2 === 0) {
        window.trialCondition = 'go';
        window.correctKey = 'space';
    } else {
        window.trialCondition = 'nogo';
        window.correctKey = undefined; 
    }
    
    // 3. Aktualizacja tekstu na ekranie
    // (Wymagane, jeśli Builder nie odświeża zmiennej $window.currentNumber automatycznie w JS)
    if (typeof numberStim !== 'undefined') {
        numberStim.setText(window.currentNumber);
    }
    
    // Resetowanie zmiennych pomocniczych (opcjonalne, ale dobre dla porządku)
    window.feedbackColor = 'white';
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    numberStim.setText(currentNumber);
    psychoJS.experiment.addData('trial.started', globalClock.getTime());
    trialMaxDuration = null
    // keep track of which components have finished
    trialComponents = [];
    trialComponents.push(key_resp);
    trialComponents.push(numberStim);
    
    for (const thisComponent of trialComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function trialRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'trial' ---
    // get current time
    t = trialClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *key_resp* updates
    if (t >= 0 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp.tStart = t;  // (not accounting for frame time here)
      key_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp.clearEvents(); });
    }
    frameRemains = 0 + window.decisionTime - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (key_resp.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      // keep track of stop time/frame for later
      key_resp.tStop = t;  // not accounting for scr refresh
      key_resp.frameNStop = frameN;  // exact frame index
      // update status
      key_resp.status = PsychoJS.Status.FINISHED;
      frameRemains = 0 + window.decisionTime - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
      if (key_resp.status === PsychoJS.Status.STARTED && t >= frameRemains) {
        // keep track of stop time/frame for later
        key_resp.tStop = t;  // not accounting for scr refresh
        key_resp.frameNStop = frameN;  // exact frame index
        // update status
        key_resp.status = PsychoJS.Status.FINISHED;
        key_resp.status = PsychoJS.Status.FINISHED;
          }
        
      }
      
      // if key_resp is active this frame...
      if (key_resp.status === PsychoJS.Status.STARTED) {
        let theseKeys = key_resp.getKeys({keyList: 'space', waitRelease: false});
        _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
        if (_key_resp_allKeys.length > 0) {
          key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
          key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
          key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
          // was this correct?
          if (key_resp.keys == '') {
              key_resp.corr = 1;
          } else {
              key_resp.corr = 0;
          }
          // a response ends the routine
          continueRoutine = false;
        }
      }
      
      
      // *numberStim* updates
      if (t >= 0.0 && numberStim.status === PsychoJS.Status.NOT_STARTED) {
        // keep track of start time/frame for later
        numberStim.tStart = t;  // (not accounting for frame time here)
        numberStim.frameNStart = frameN;  // exact frame index
        
        numberStim.setAutoDraw(true);
      }
      
      
      // if numberStim is active this frame...
      if (numberStim.status === PsychoJS.Status.STARTED) {
      }
      
      frameRemains = 0.0 + window.decisionTime - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
      if (numberStim.status === PsychoJS.Status.STARTED && t >= frameRemains) {
        // keep track of stop time/frame for later
        numberStim.tStop = t;  // not accounting for scr refresh
        numberStim.frameNStop = frameN;  // exact frame index
        // update status
        numberStim.status = PsychoJS.Status.FINISHED;
        numberStim.setAutoDraw(false);
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
  
  
var pressed;
var wasCorrect;
function trialRoutineEnd(snapshot) {
    return async function () {
      //--- Ending Routine 'trial' ---
      for (const thisComponent of trialComponents) {
        if (typeof thisComponent.setAutoDraw === 'function') {
          thisComponent.setAutoDraw(false);
        }
      }
      psychoJS.experiment.addData('trial.stopped', globalClock.getTime());
      // --- OCENA WYNIKU I PRZYGOTOWANIE FEEDBACKU ---
      
      // 1. Sprawdź czy użytkownik nacisnął klawisz (zakładamy nazwę 'key_resp')
      let pressed = false;
      
      if (typeof key_resp !== 'undefined' && key_resp.keys) {
          if (Array.isArray(key_resp.keys) && key_resp.keys.length > 0) {
              pressed = true;
          } else if (typeof key_resp.keys === 'string' && key_resp.keys.length > 0) {
              pressed = true;
          }
      }
      
      // 2. Porównaj reakcję z warunkiem (Go/NoGo)
      let wasCorrect = false;
      
      if (window.trialCondition === 'go') {
          // Warunek GO: Musi być reakcja
          if (pressed) {
              wasCorrect = true; 
          } else {
              wasCorrect = false; 
          }
      } else {
          // Warunek NOGO: Musi być BRAK reakcji
          if (!pressed) {
              wasCorrect = true; 
          } else {
              wasCorrect = false; 
          }
      }
      
      // 3. Ustaw kolor dla następnej rutyny (feedback)
      if (wasCorrect) {
          window.feedbackColor = 'green';
      } else {
          window.feedbackColor = 'red';
      }
      
      // 4. Zapisz kluczowe dane do analizy
      psychoJS.experiment.addData('number_shown', window.currentNumber);
      psychoJS.experiment.addData('condition', window.trialCondition);
      psychoJS.experiment.addData('was_correct', wasCorrect);
      // was no response the correct answer?!
      if (key_resp.keys === undefined) {
        if (['None','none',undefined].includes('')) {
           key_resp.corr = 1;  // correct non-response
        } else {
           key_resp.corr = 0;  // failed to respond (incorrectly)
        }
      }
      // store data for current loop
      // update the trial handler
      if (currentLoop instanceof MultiStairHandler) {
        currentLoop.addResponse(key_resp.corr, level);
      }
      psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
      psychoJS.experiment.addData('key_resp.corr', key_resp.corr);
      if (typeof key_resp.keys !== 'undefined') {  // we had a response
          psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
          psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
          routineTimer.reset();
          }
      
      key_resp.stop();
      // the Routine "trial" was not non-slip safe, so reset the non-slip timer
      routineTimer.reset();
      
      // Routines running outside a loop should always advance the datafile row
      if (currentLoop === psychoJS.experiment) {
        psychoJS.experiment.nextEntry(snapshot);
      }
      return Scheduler.Event.NEXT;
    }
  }
  
  
var feedbackMaxDurationReached;
var feedbackMaxDuration;
var feedbackComponents;
function feedbackRoutineBegin(snapshot) {
    return async function () {
      TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
      
      //--- Prepare to start Routine 'feedback' ---
      t = 0;
      frameN = -1;
      continueRoutine = true; // until we're told otherwise
      // keep track of whether this Routine was forcibly ended
      routineForceEnded = false;
      feedbackClock.reset(routineTimer.getTime());
      routineTimer.add(1.500000);
      feedbackMaxDurationReached = false;
      // update component parameters for each repeat
      feedbackStim.setColor(new util.Color(window.feedbackColor));
      feedbackStim.setText(window.currentNumber);
      psychoJS.experiment.addData('feedback.started', globalClock.getTime());
      feedbackMaxDuration = null
      // keep track of which components have finished
      feedbackComponents = [];
      feedbackComponents.push(feedbackStim);
      
      for (const thisComponent of feedbackComponents)
        if ('status' in thisComponent)
          thisComponent.status = PsychoJS.Status.NOT_STARTED;
      return Scheduler.Event.NEXT;
    }
  }
  
  
function feedbackRoutineEachFrame() {
    return async function () {
      //--- Loop for each frame of Routine 'feedback' ---
      // get current time
      t = feedbackClock.getTime();
      frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
      // update/draw components on each frame
      
      // *feedbackStim* updates
      if (t >= 0.0 && feedbackStim.status === PsychoJS.Status.NOT_STARTED) {
        // keep track of start time/frame for later
        feedbackStim.tStart = t;  // (not accounting for frame time here)
        feedbackStim.frameNStart = frameN;  // exact frame index
        
        feedbackStim.setAutoDraw(true);
      }
      
      
      // if feedbackStim is active this frame...
      if (feedbackStim.status === PsychoJS.Status.STARTED) {
      }
      
      frameRemains = 0.0 + 1.5 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
      if (feedbackStim.status === PsychoJS.Status.STARTED && t >= frameRemains) {
        // keep track of stop time/frame for later
        feedbackStim.tStop = t;  // not accounting for scr refresh
        feedbackStim.frameNStop = frameN;  // exact frame index
        // update status
        feedbackStim.status = PsychoJS.Status.FINISHED;
        feedbackStim.setAutoDraw(false);
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
      for (const thisComponent of feedbackComponents)
        if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
          continueRoutine = true;
          break;
        }
      
      // refresh the screen if continuing
      if (continueRoutine && routineTimer.getTime() > 0) {
        return Scheduler.Event.FLIP_REPEAT;
      } else {
        return Scheduler.Event.NEXT;
      }
    };
  }
  
  
function feedbackRoutineEnd(snapshot) {
    return async function () {
      //--- Ending Routine 'feedback' ---
      for (const thisComponent of feedbackComponents) {
        if (typeof thisComponent.setAutoDraw === 'function') {
          thisComponent.setAutoDraw(false);
        }
      }
      psychoJS.experiment.addData('feedback.stopped', globalClock.getTime());
      if (routineForceEnded) {
          routineTimer.reset();} else if (feedbackMaxDurationReached) {
          feedbackClock.add(feedbackMaxDuration);
      } else {
          feedbackClock.add(1.500000);
      }
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
        
        let rawData = psychoJS.experiment._trialsData;
        // Filtrujemy tylko te wiersze, które są faktycznymi próbami (mają ocenę poprawności)
        let allData = rawData.filter(trial => trial.hasOwnProperty('was_correct')); 
        
        let goTrials = 0;
        let nogoTrials = 0;
        let hits = 0;
        let misses = 0;
        let correctRejects = 0;
        let falseAlarms = 0;
        let totalRT = 0;
        let hitRTCount = 0;
    
        for (let trial of allData) {
            // Bezpieczne pobieranie RT
            let currentRT = 0;
            let hasRT = false;
            
            if (trial.key_resp && trial.key_resp.rt) {
                 if (Array.isArray(trial.key_resp.rt)) currentRT = trial.key_resp.rt[0];
                 else currentRT = trial.key_resp.rt;
                 
                 if (currentRT > 0) hasRT = true;
            }
    
            if (trial.condition === 'go') {
                goTrials++;
                if (trial.was_correct) {
                    hits++;
                    if (hasRT) {
                        totalRT += currentRT;
                        hitRTCount++;
                    }
                } else {
                    misses++;
                }
            } else if (trial.condition === 'nogo') {
                nogoTrials++;
                if (trial.was_correct) {
                    correctRejects++;
                } else {
                    falseAlarms++;
                }
            }
        }
    
        // Obliczenia statystyczne
        let avgRT = hitRTCount > 0 ? Math.round((totalRT / hitRTCount) * 1000) : 0;
        let totalTrials = goTrials + nogoTrials;
        let totalCorrect = hits + correctRejects;
        let accuracy = totalTrials > 0 ? Math.round((totalCorrect / totalTrials) * 100) : 0;
        let faRate = nogoTrials > 0 ? Math.round((falseAlarms / nogoTrials) * 100) : 0;
    
        // Budowa paczki danych
        let payload = {
            testId: "GoNoGo_Numbers",
            subjectId: expInfo['participant'],
            timestamp: new Date().toISOString(),
            
            // GŁÓWNY WYNIK
            czas_reakcji: avgRT,
            
            // POZIOM TRUDNOŚCI (DODANE)
            poziom_trudnosci: window.difficultyName || "Nieznany",
            
            // OPIS
            score: `Poziom: ${window.difficultyName} | Celność: ${accuracy}% | Czas: ${avgRT}ms`,
            
            // SZCZEGÓŁY
            statystyki: {
                poprawne: totalCorrect,
                wszystkie: totalTrials,
                hits: hits,
                misses: misses,
                false_alarms: falseAlarms,
                correct_rejections: correctRejects,
                fa_rate_percent: faRate,
                ustawiony_czas: window.decisionTime
            },
            
            // SUROWE DANE
            wyniki: allData
        };
    
        console.log("Wysyłanie do Nous...", payload);
        window.electronTest.sendResults(payload);
    }
    psychoJS.window.close();
    psychoJS.quit({message: message, isCompleted: isCompleted});
    
    return Scheduler.Event.QUIT;
  }
