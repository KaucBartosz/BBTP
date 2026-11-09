# Graph Report - BBTP  (2026-11-09)

## Corpus Check
- Large corpus: 129 files · ~1,024,123 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 527 nodes · 787 edges · 16 communities
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 54 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Python Launchers (main.py)
- GoNoGoBiegacze Task
- FabrykaFigur Task
- NWstecz Task
- GoNoGo Task
- Corsi Task
- PingPong Task
- Semafor Task
- BystreOczko Task
- Sygnalizacja Task
- Stop Task
- Stroop Task
- ZlapSygnal Task
- Samochodzik Task
- Shared Experiment Scaffold
- Semafor Python Launcher

## God Nodes (most connected - your core abstractions)
1. `PsychoJS 2025.1.1 Runtime Bundle` - 13 edges
2. `main()` - 11 edges
3. `trainingLoopBegin()` - 10 edges
4. `trialsLoopBegin()` - 9 edges
5. `trialsLoopBegin()` - 9 edges
6. `testLoopBegin()` - 8 edges
7. `quitPsychoJS()` - 8 edges
8. `blocksLoopBegin()` - 7 edges
9. `quitPsychoJS()` - 7 edges
10. `trialsLoopBegin()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Corsi Experiment Page` --semantically_similar_to--> `NWstecz Experiment Page`  [INFERRED] [semantically similar]
  Corsi/index.html → NWstecz/index.html
- `Stroop Experiment Page` --semantically_similar_to--> `Fabryka Figur Experiment Page`  [INFERRED] [semantically similar]
  Stroop/index.html → FabrykaFigur/index.html
- `GoNoGo Biegacze Experiment Page` --semantically_similar_to--> `GoNoGo Experiment Page`  [INFERRED] [semantically similar]
  GoNoGoBiegacze/index.html → GoNoGo/index.html
- `Semafor Experiment Page` --semantically_similar_to--> `Sygnalizacja Experiment Page`  [INFERRED] [semantically similar]
  Semafor/index.html → Sygnalizacja/index.html
- `Stop Signal Experiment Page` --semantically_similar_to--> `Zlap Sygnal Experiment Page`  [INFERRED] [semantically similar]
  Stop/index.html → ZlapSygnal/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Tasks Sharing The PsychoPy Page Scaffold** — bystreoczko_index, corsi_index, fabrykafigur_index, gonogobiegacze_index, gonogo_index, nwstecz_index, pingpong_index, samochodzik_index, semafor_index, stop_index, stroop_index, sygnalizacja_index, zlapsygnal_index, bbtp_experiment_page_scaffold, bbtp_psychojs_runtime [EXTRACTED 1.00]
- **BBTP Cognitive Test Battery Tasks** — bystreoczko_index, corsi_index, fabrykafigur_index, gonogo_index, nwstecz_index, semafor_index, stop_index, stroop_index, sygnalizacja_index, zlapsygnal_index, bbtp_cognitive_test_battery [INFERRED 0.85]

## Communities (16 total, 0 thin omitted)

### Community 0 - "Python Launchers (main.py)"
Cohesion: 0.07
Nodes (35): main(), _write_results(), generate_sequence(), main(), point_in_circle(), _write_results(), build_pool(), main() (+27 more)

### Community 1 - "GoNoGoBiegacze Task"
Cohesion: 0.07
Nodes (27): blocksLoopBegin(), blocksLoopScheduler, breakRoutineBegin(), breakRoutineEachFrame(), breakRoutineEnd(), dialogCancelScheduler, experimentInit(), expInfo (+19 more)

### Community 2 - "FabrykaFigur Task"
Cohesion: 0.06
Nodes (21): ALL_COLORS, ALL_SHAPES, buildPool(), dialogCancelScheduler, DIFFICULTY_CONFIG, difficultyRoutineEachFrame(), difficultyRoutineEnd(), DURATION_OPTIONS (+13 more)

### Community 3 - "NWstecz Task"
Cohesion: 0.07
Nodes (20): dialogCancelScheduler, difficultyRoutineEachFrame(), expInfo, feedbackRoutineBegin(), feedbackRoutineEachFrame(), feedbackRoutineEnd(), flowScheduler, importConditions() (+12 more)

### Community 4 - "GoNoGo Task"
Cohesion: 0.07
Nodes (20): dialogCancelScheduler, DifficultyRoutineEachFrame(), experimentInit(), expInfo, feedbackRoutineBegin(), feedbackRoutineEachFrame(), feedbackRoutineEnd(), flowScheduler (+12 more)

### Community 5 - "Corsi Task"
Cohesion: 0.07
Nodes (19): BLOCK_DEFAULT_COLOR, BLOCK_PLAYER_COLOR, BLOCK_SYSTEM_COLOR, dialogCancelScheduler, DIFFICULTY_CONFIG, difficultyRoutineEachFrame(), experimentInit(), expInfo (+11 more)

### Community 6 - "PingPong Task"
Cohesion: 0.07
Nodes (16): ballVelocity, dialogCancelScheduler, DIFFICULTY_SETTINGS, difficultyRoutineEachFrame(), expInfo, flowScheduler, gameRoutineBegin(), gameRoutineEachFrame() (+8 more)

### Community 7 - "Semafor Task"
Cohesion: 0.08
Nodes (17): dialogCancelScheduler, experimentInit(), expInfo, flowScheduler, importConditions(), menuRoutineEachFrame(), n_trialsLoopBegin(), n_trialsLoopEndIteration() (+9 more)

### Community 8 - "BystreOczko Task"
Cohesion: 0.08
Nodes (15): dialogCancelScheduler, expInfo, flowScheduler, importConditions(), PILOTING, psychoJS, quitPsychoJS(), selectionRoutineEachFrame() (+7 more)

### Community 9 - "Sygnalizacja Task"
Cohesion: 0.09
Nodes (15): dialogCancelScheduler, experimentInit(), expInfo, flowScheduler, importConditions(), PILOTING, psychoJS, quitPsychoJS() (+7 more)

### Community 10 - "Stop Task"
Cohesion: 0.09
Nodes (14): dialogCancelScheduler, driveRoutineBegin(), driveRoutineEachFrame(), driveRoutineEnd(), experimentInit(), expInfo, flowScheduler, importConditions() (+6 more)

### Community 11 - "Stroop Task"
Cohesion: 0.09
Nodes (14): COLORS, dialogCancelScheduler, expInfo, flowScheduler, HINT_DATA, KEYS_MAP, NAMES, quitPsychoJS() (+6 more)

### Community 12 - "ZlapSygnal Task"
Cohesion: 0.08
Nodes (10): dialogCancelScheduler, DURATION_OPTIONS, durationSelectionRoutineEachFrame(), experimentInit(), expInfo, flowScheduler, psychoJS, quitPsychoJS() (+2 more)

### Community 13 - "Samochodzik Task"
Cohesion: 0.13
Nodes (11): activeKeys, dialogCancelScheduler, difficultyRoutine(), expInfo, finishRoutine(), flowScheduler, gameRoutine(), loadTrackResources() (+3 more)

### Community 14 - "Shared Experiment Scaffold"
Cohesion: 0.21
Nodes (15): BBTP Cognitive Test Battery, PsychoJS 2025.1.1 Runtime Bundle, BystreOczko Experiment Page, Corsi Experiment Page, Fabryka Figur Experiment Page, GoNoGo Experiment Page, GoNoGo Biegacze Experiment Page, NWstecz Experiment Page (+7 more)

### Community 15 - "Semafor Python Launcher"
Cohesion: 0.25
Nodes (9): _clamp01(), _draw_grid(), _grid_coords(), main(), _over(), _reset_grid(), _setup_demo_lamps(), _smooth_step() (+1 more)

## Knowledge Gaps
- **1 isolated node(s):** `BystreOczko Experiment Page`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 299 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Semafor Python Launcher` to `Python Launchers (main.py)`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `BystreOczko Experiment Page` to the rest of the system?**
  _1 weakly-connected nodes found - possible missing edges._
- **Should `Python Launchers (main.py)` be split into smaller, more focused modules?**
  _Cohesion score 0.07145501666049611 - nodes in this community are weakly interconnected._
- **Should `GoNoGoBiegacze Task` be split into smaller, more focused modules?**
  _Cohesion score 0.07399577167019028 - nodes in this community are weakly interconnected._
- **Should `FabrykaFigur Task` be split into smaller, more focused modules?**
  _Cohesion score 0.0641025641025641 - nodes in this community are weakly interconnected._
- **Should `NWstecz Task` be split into smaller, more focused modules?**
  _Cohesion score 0.07017543859649122 - nodes in this community are weakly interconnected._
- **Should `GoNoGo Task` be split into smaller, more focused modules?**
  _Cohesion score 0.07357357357357357 - nodes in this community are weakly interconnected._

---

## Scope & Exclusions (graf objął 41 z 129 wykrytych plików)

Wykluczone świadomie, żeby graf nie utonął w 12 identycznych kopiach biblioteki:

| Wykluczone | Pliki | Rozmiar | Powód |
|---|---|---|---|
| `*/lib/psychojs-2025.1.1.js` + `.iife.js` | 24 | 2,46 MB każdy (tylko 2 unikalne hashe) | vendored PsychoJS, 12 identycznych kopii |
| `*/lib/psychojs-2025.1.1.js.LEGAL.txt` | 13 | 25 KB każdy (identyczne) | tekst licencji |
| `*/resources/*.png` | 49 | sprite'y | zasoby graficzne, brak struktury kodu |

W grafie są natomiast węzły importów do PsychoJS (`*_lib_psychojs_2025_1_1[_core|_data|...]`) — AST tworzy je z samych ścieżek `import`, więc powiązanie z biblioteką jest widoczne, ale bez jej wnętrza.

Uwaga o jakości: 215 krawędzi surowego ekstraktu wskazuje na encje spoza grafu — to importy Pythona (`random`, `json`, `os`, `datetime`, `pathlib`, `math`, `psychopy`). To nie uszkodzenie grafu, tylko brak węzłów dla zależności zewnętrznych (build dorobił dla nich placeholdery).
