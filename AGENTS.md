## Codebase Navigation — MANDATORY

You MUST use codebase-index MCP tools FIRST when exploring or navigating the codebase. This is not optional.

- ALWAYS start with: get_project_summary, find_symbol, get_function_source, get_class_source, get_structure_summary, get_dependencies, get_dependents, get_change_impact, get_call_chain, search_codebase
- Only fall back to Read/Glob/Grep when codebase-index tools genuinely don't have what you need.
- If you catch yourself reaching for Glob/Grep/Read to find or understand code, STOP and use codebase-index instead.

## Codebase Indexing

- When the user requests to "index the codebase", "scan the codebase", "build the index", or similar, you MUST call codebase-index.index_project.
- Do NOT ask questions. Do NOT suggest manual indexing. Just call the tool.
- If the index already exists, you may ask the user if they want to re-index or skip, but only after calling codebase-index.get_project_summary to check the current state.
- If the user says "update", "refresh", or "sync", call codebase-index.index_project.
- If the user says "clear", "reset", or "delete index", call codebase-index.clear_index.
- If the user says "status", "what's indexed", or "show index", call codebase-index.get_project_summary.
- If the user says "search", "find", or "look for", use codebase-index.search_codebase first. Only use Glob/Grep/Read if codebase-index returns no results and you're sure the code exists.
- If the user says "dependencies", "dependents", or "call graph", use codebase-index.get_dependencies, codebase-index.get_dependents, or codebase-index.get_call_chain. Do NOT try to infer this from file names or directory structure.
- If the user says "diff", "changes", or "compare", use codebase-index.get_change_impact. Do NOT try to infer this from file names or directory structure.
- If the user says "structure", "outline", or "hierarchy", use codebase-index.get_structure_summary. Do NOT try to infer this from file names or directory structure.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **BBTP** (336 symbols, 659 relationships, 18 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/BBTP/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/BBTP/context` | Codebase overview, check index freshness |
| `gitnexus://repo/BBTP/clusters` | All functional areas |
| `gitnexus://repo/BBTP/processes` | All execution flows |
| `gitnexus://repo/BBTP/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:

1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

# Code Index MCP — Intelligent Code Search

This project uses Code Index MCP for intelligent code indexing and search. Use these tools to search code, analyze files, and navigate the codebase efficiently.

## Available Tools

### Project Management

| Tool | Description |
|------|-------------|
| **`set_project_path`** | Initialize indexing for a project directory |
| **`refresh_index`** | Rebuild the shallow file index after file changes |
| **`build_deep_index`** | Generate the full symbol index used by deep analysis |
| **`get_settings_info`** | View current project configuration and status |

### Search & Discovery

| Tool | Description |
|------|-------------|
| **`search_code_advanced`** | Smart search with regex, fuzzy matching, file filtering, and paginated results (10 per page by default) |
| **`find_files`** | Locate files using glob patterns (e.g., `**/*.py`) |
| **`get_file_summary`** | Analyze file structure, functions, imports, and complexity (requires deep index) |

### Monitoring & Auto-refresh

| Tool | Description |
|------|-------------|
| **`get_file_watcher_status`** | Check file watcher status and configuration |
| **`configure_file_watcher`** | Enable/disable auto-refresh and configure settings |

## Usage Guidelines

- **Use Code Index MCP FIRST** when searching for code, analyzing files, or navigating the codebase
- **Cache is automatic** - indexes are loaded from persistent cache on startup
- **File watcher is automatic** - indexes refresh automatically when files change
- **Search patterns**: Use `search_code_advanced` with regex or fuzzy matching
- **File discovery**: Use `find_files` with glob patterns like `src/**/*.tsx`
- **File analysis**: Use `get_file_summary` to understand structure and complexity (run `build_deep_index` first if needed)

## Quick Start

1. **Initialize project**: `set_project_path` with path to repository
2. **Search code**: `search_code_advanced` with query like "authentication function"
3. **Find files**: `find_files` with pattern like `**/*.py`
4. **Analyze file**: `get_file_summary` with file path (after `build_deep_index`)

## Cache & Auto-refresh

- **Persistent cache** in msgpack format stored locally
- **File watcher** monitors changes and refreshes index automatically
- **Smart processing** batches rapid changes to prevent excessive rebuilds
- No manual intervention needed - cache and indexing are managed automatically

## PsychoJS Testy — WYMAGANIA

Przy tworzeniu nowych testów psychometrycznych w PsychoJS, MUSISZ spełnić następujące wymagania:

### index.html

Każdy test MUSI mieć `index.html` z dokładnie taką strukturą (kopiuj z istniejących działających testów):

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <title>NazwaTestu [PsychoPy]</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jquery-ui-dist@1.12.1/jquery-ui.min.css">
    <link rel="stylesheet" href="./lib/psychojs-2025.1.1.css">
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery-ui-dist@1.12.1/jquery-ui.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/preloadjs@1.0.1/lib/preloadjs.min.js"></script>
    <script src="./nazwatestu.js" type="module"></script>
    <script src="./lib/psychojs-2025.1.1.iife.js" nomodule></script>
  </body>
</html>
```

**WAŻNE**: Brak CDN linków (jQuery, jQuery UI, PreloadJS) lub `<div id="root">` spowoduje czarny/biały ekran!

### Struktura plików

```
NazwaTestu/
├── index.html          # Z CDN linkami (PATRZ WYŻEJ)
├── nazwatestu.js       # Główny plik JS (wzoruj na GoNoGo.js)
├── main.py             # Wersja Python (HPM)
└── lib/                # Biblioteki PsychoJS (kopiuj z BystreOczko/lib/)
    ├── psychojs-2025.1.1.css
    ├── psychojs-2025.1.1.iife.js
    ├── psychojs-2025.1.1.js
    └── ...
```

### Kod JavaScript

Wzoruj się na **GoNoGo.js** lub **Stroop/stroop.js**:

- Każda routine ma `Begin/EachFrame/End` functions
- Components array z proper status tracking (`NOT_STARTED` → `STARTED` → `FINISHED`)
- `continueRoutine` properly managed w eachFrame
- Keyboard z `callOnFlip` dla clock reset, start, clearEvents
- Mouse z proper initialization
- `psychoJS.experiment.save = function() { return Promise.resolve(); }` dla Nous integration

### NIGDY NIE RÓB

- NIE twórz minimalistycznego index.html bez CDN linków
- NIE używaj `visual.Polygon` - używaj `visual.Rect` (bardziej niezawodne)
- NIE pomijaj `<div id="root"></div>` w body
- NIE pomijaj CSS link
- NIE twórz kodu od zera - kopiuje strukturę z działających testów

<!-- gitnexus:end -->
# Poradnik Agenta Testów – Projekt Nous

## 1. Architektura Nous

**Nous** (v1.1.8) to launcher (Electron) do badań psychologicznych i klinicznych:

- Zarządza biblioteką testów z GitHub (paczki ZIP)
- Obsługuje metryczki badanych (demografię)
- Przechowuje wyniki: IndexedDB lokalnie + synchronizacja Firebase

### Rodzaje testów

#### A. Testy Webowe (JS/HTML) – Standardowe

- **Plik startowy**: `index.html` (w głównym folderze lub podfolderze)
- **Komunikacja**: `window.electronTest` (bridge)
- **Zakończenie**: `window.electronTest.sendResults(data)` – zapis wyników
- **Wyjście bez zapisu**: `window.electronTest.close()` – ESC/przerwanie
- Uruchamiane w pełnoekranowym oknie Electrona

#### B. Testy Natywne (HPM - High Precision Mode) – Python

- **Plik startowy**: `main.py`
- **Zmienne środowiskowe**:
  - `NOUS_LAUNCHER='1'` – informacja, że test działa pod kontrolą Nous
  - `NOUS_TRAINING='1'` lub `'0'` – tryb treningowy
- **Wyniki**: Po zakończeniu skrypt zapisuje `results.json` w folderze roboczym
- Launcher odczytuje plik automatycznie po zamknięciu procesu
- **WAŻNE**: `_write_results()` wywoływać TYLKO gdy `NOUS_LAUNCHER == True`
- **WAŻNE**: Przy ESC lub wyjściu bez ukończenia: zapisz pusty wynik jeśli `NOUS_LAUNCHER`

---

## 2. Standardowe Nazewnictwo Wyników (OBOWIĄZKOWE)

Wszystkie testy muszą zwracać te same pola w `sendResults()` / `results.json`:

### Główne pola (używane w podsumowaniu zaraz po teście)

```javascript
{
  "testId": "nazwa_testu",              // string, bez spacji
  "subjectId": "opcjonalny_id",         // jeśli test sam nadaje ID
  "timestamp": "2025-02-20T12:00:00Z",   // ISO string
  "ilosc_poprawnych_nacisniec": 5,      // liczba poprawnych kliknięć/naciśnięć
  "ilosc_blednych_nacisniec": 3,        // liczba błędnych kliknięć/naciśnięć
  "ogolna_ilosc_nacisniec": 8,          // łączna liczba kliknięć/naciśnięć
  "sredni_czas_reakcji": 450            // średni RT w ms (TYLKO jeśli test mierzy RT)
}
```

### Dodatkowe pola (opcjonalne, widoczne w pliku wynikowym)

- `score`: tekst podsumowania (np. `"Poprawne: 5 | Błędne: 3 | Skuteczność: 62%"`)
- `statystyki`: obiekt ze szczegółowymi statystykami
- `wyniki`: surowe dane prób (lista obiektów)
- `poziom_trudnosci`: dla testów z wyborem poziomu (GoNoGo, PingPong, Samochodzik itp.)

**WAŻNE:**

- Jeśli test **NIE mierzy czasu reakcji**, **NIE umieszczaj** `sredni_czas_reakcji` w wynikach
- Jeśli test mierzy RT, zawsze licz średni RT dla **wszystkich odpowiedzi** (poprawnych i błędnych), chyba że specyfika testu wymaga inaczej
- Niektóre testy mają dodatkowe pola specyficzne dla testu – to jest dopuszczalne (patrz sekcja 10)

---

## 3. Checklista dla Nowych/Przeglądanych Testów

### Integracja z Nous (JS)

- [ ] Sprawdzenie `window.electronTest` przed zapisem CSV: `psychoJS.experiment.save = function() { return Promise.resolve(); }`
- [ ] ESC = wyjście bez zapisu: `if (!isCompleted) window.electronTest.close()`
- [ ] Normalne zakończenie: `window.electronTest.sendResults({...})` z ujednoliconymi polami
- [ ] Filtrowanie `_trialsData`: tylko wiersze z `typeof t.correct !== 'undefined'` (pomijamy welcome)

### Integracja z Nous (Python)

- [ ] Sprawdzenie `NOUS_LAUNCHER` i `NOUS_TRAINING` z `os.environ`
- [ ] ESC na ekranie instrukcji: zapis pustych wyników jeśli `NOUS_LAUNCHER`
- [ ] ESC w trakcie prób: flaga `escaped`, przerwanie zewnętrznej pętli
- [ ] Zapis `results.json` tylko gdy `NOUS_LAUNCHER == True`
- [ ] Ścieżki względne: `Path(__file__).resolve().parent / 'resources'`
- [ ] Widoczność kursora: po utworzeniu `event.Mouse(win=win)` wywołać `mouse.setVisible(True)` (pełny ekran z `allowGUI=False` może domyślnie ukrywać kursor)
- [ ] **NIE używać** `gui.Dlg` ani `core.quit()` – zakłócają integrację z Nous (patrz: problem PingPong)

### Nazewnictwo wyników

- [ ] `ilosc_poprawnych_nacisniec` (nie: trafień, kliknięć, odpowiedzi)
- [ ] `ilosc_blednych_nacisniec` (nie: błędów, pomyłek)
- [ ] `ogolna_ilosc_nacisniec` (nie: wszystkie_kliki, total_clicks)
- [ ] `sredni_czas_reakcji` tylko jeśli test mierzy RT

### Ekran wprowadzający

- [ ] Tekst instrukcji wyjaśniający zadanie
- [ ] Wyjście przez ESC (bez zapisu lub pusty wynik)
- [ ] Kontynuacja przez klawisz (spacja/Enter)

### Obsługa ekranu dotykowego (JS)

- [ ] Pobranie canvas: `psychoJS.window._renderer.view` lub `document.querySelector('canvas')`
- [ ] Event listeners: `touchstart`, `touchend`, `touchmove` z `preventDefault()`
- [ ] Konwersja współrzędnych: `touchToPsycho(clientX, clientY)` → jednostki PsychoJS
- [ ] Funkcja `pointInStim(px, py, stim)` z zabezpieczeniem na `pos`/`size`
- [ ] Czyszczenie stanu dotyku po obsłużeniu (`_touchJustStarted = false`)

### Inne

- [ ] Usunięcie referencji do legacy scripts z `index.html`
- [ ] Brak zduplikowanego kodu (np. podwójne sprawdzanie ESC)
- [ ] Poprawne liczenie statystyk (np. średni RT dla wszystkich odpowiedzi, nie tylko poprawnych)

---

## 4. Typowe Problemy i Rozwiązania

### Problem: Zafałszowana średnia RT / liczba prób

**Przyczyna**: `_trialsData` zawiera wiersz z rutyny welcome (bez `correct`)
**Rozwiązanie**: Filtrowanie przed pętlą wyników:

```javascript
let allData = (psychoJS.experiment._trialsData || []).filter(
  function (t) { return typeof t.correct !== 'undefined'; }
);
```

### Problem: W testach Python (PsychoPy) nie widać kursora myszy

**Przyczyna**: W pełnym ekranie z `allowGUI=False` PsychoPy na niektórych systemach domyślnie ukrywa kursor.
**Rozwiązanie**: Zaraz po utworzeniu obiektu myszy wywołać `mouse.setVisible(True)`:

```python
mouse = event.Mouse(win=win)
mouse.setVisible(True)
```

### Problem: ESC nie przerywa całej serii prób

**Przyczyna**: `break` tylko w wewnętrznej pętli `while`
**Rozwiązanie**: Flaga `escaped`, sprawdzenie po zakończeniu próby:

```python
escaped = False
for trial_idx in range(N_TRIALS):
    while trial_clock.getTime() < TIMEOUT:
        if event.getKeys(['escape']):
            escaped = True
            break
        # ... logika próby
    if escaped:
        break
```

### Problem: Dotyk nie działa

**Przyczyna**: Brak konwersji współrzędnych lub błędne sprawdzanie `contains`
**Rozwiązanie**:

- Konwersja `touchToPsycho()` z aspect ratio
- Funkcja `pointInStim()` z zabezpieczeniem na `pos`/`size`
- Sprawdzanie `opacity > 0` przed hit-testem

### Problem: Niezgodne nazwy wyników

**Przyczyna**: Różne testy używają różnych nazw
**Rozwiązanie**: Zawsze używać:

- `ilosc_poprawnych_nacisniec`
- `ilosc_blednych_nacisniec`
- `ogolna_ilosc_nacisniec`
- `sredni_czas_reakcji` (tylko jeśli mierzy RT)

### Problem: Test Python nie zapisuje wyników do Nous

**Przyczyna**: Użycie `gui.Dlg` lub `core.quit()` powoduje zamknięcie procesu przed zapisem
**Rozwiązanie**:

- Zastąp `gui.Dlg` ekranami `visual.TextStim` z `event.waitKeys()`
- Zastąp `core.quit()` wyjściem przez `return` z funkcji `main()`
- Upewnij się, że `_write_results()` jest wywoływane **przed** `win.close()`
- **Przykład złego kodu** (PingPong): `core.quit()` po ESC – test nie zapisuje wyników
- **Poprawna struktura**: `if NOUS_LAUNCHER: _write_results(...); win.close(); return`

### Problem: HPM nie startuje testu / wyniki się nie pokazują

**Przyczyna**: Launcher uruchamia `main.py` i czeka na `results.json` po zamknięciu procesu. Jeśli `core.quit()` jest wywoływane zamiast naturalnego powrotu, plik może nie zostać zapisany.
**Rozwiązanie**: Upewnij się, że kod Pythona zawsze zapisuje `results.json` przed zakończeniem, gdy `NOUS_LAUNCHER == True`.

---

## 5. Przykłady Poprawnego Kodu

### JS: quitPsychoJS z ujednoliconymi polami

```javascript
async function quitPsychoJS(message, isCompleted) {
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  if (typeof window.electronTest !== 'undefined') {
      if (isCompleted) {
          let allData = (psychoJS.experiment._trialsData || []).filter(
              function (t) { return typeof t.correct !== 'undefined'; }
          );
          let poprawneNacisniecia = 0;
          let wszystkieNacisniecia = 0;
          let sumRT = 0;
          let validRTCount = 0;

          for (let trial of allData) {
              wszystkieNacisniecia++;
              if (trial.correct === 1) poprawneNacisniecia++;
              if (typeof trial.rt === 'number' && trial.rt >= 0) {
                  sumRT += trial.rt;
                  validRTCount++;
              }
          }

          let bledneNacisniecia = Math.max(0, wszystkieNacisniecia - poprawneNacisniecia);
          let sredniCzasReakcji = validRTCount > 0 ? Math.round((sumRT / validRTCount) * 1000) : 0;

          window.electronTest.sendResults({
              testId: expInfo['expName'],
              subjectId: expInfo['participant'],
              timestamp: new Date().toISOString(),
              ilosc_poprawnych_nacisniec: poprawneNacisniecia,
              ilosc_blednych_nacisniec: bledneNacisniecia,
              ogolna_ilosc_nacisniec: wszystkieNacisniecia,
              sredni_czas_reakcji: sredniCzasReakcji, // TYLKO jeśli test mierzy RT
              score: `Poprawne: ${poprawneNacisniecia} | Błędne: ${bledneNacisniecia} | ...`,
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
```

### Python: main.py z Nous HPM (wzorcowy szablon)

```python
import os
import json
import random
from datetime import datetime
from pathlib import Path
from psychopy import visual, core, event

NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES = SCRIPT_DIR / 'resources'

def _write_results(script_dir, trials_data, poprawne, bledne, wszystkie, avg_rt_ms):
    results = {
        'testId': 'nazwa_testu',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        # 'sredni_czas_reakcji': avg_rt_ms,  # TYLKO jeśli mierzy RT
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    win = visual.Window(fullscr=True, units='height', color=(0,0,0), allowGUI=False)
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)  # WAŻNE: zawsze po utworzeniu mouse
    
    # Instrukcja z ESC
    instr = visual.TextStim(win, text='...', color='white', height=0.05)
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'return', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0)  # pusty wynik
        return
    
    # ... logika testu ...
    
    # Wyniki
    poprawne = sum(1 for t in trials_data if t['correct'] == 1)
    wszystkie = len(trials_data)
    bledne = max(0, wszystkie - poprawne)
    avg_rt_ms = ... # jeśli mierzy RT
    
    win.close()  # zamknij okno PRZED zapisem wyników
    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, trials_data, poprawne, bledne, wszystkie, avg_rt_ms)

if __name__ == '__main__':
    main()
```

### JS: Obsługa dotyku

```javascript
// W experimentInit:
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

// W trialRoutineEachFrame:
function pointInStim(px, py, stim) {
  let pos = stim.pos || stim._pos;
  let size = stim.size || stim._size || [0.08, 0.08];
  if (!pos || (typeof pos[0] !== 'number') || (typeof pos[1] !== 'number')) return false;
  let hx = (Array.isArray(size) ? size[0] : size) / 2;
  let hy = (Array.isArray(size) ? size[1] : size) / 2;
  return Math.abs(px - pos[0]) <= hx && Math.abs(py - pos[1]) <= hy;
}

if (show_feedback === false && window._touchJustStarted && window._touchPsychoX != null && window._touchCanvas) {
  for (let ix = 0; ix < lamp_grid.length; ix++) {
    for (let iy = 0; iy < lamp_grid[ix].length; iy++) {
      if (lamp_grid[ix][iy].opacity === 0) continue;
      if (pointInStim(window._touchPsychoX, window._touchPsychoY, lamp_grid[ix][iy])) {
        // ... obsługa kliknięcia ...
        break;
      }
    }
    if (show_feedback) break;
  }
  window._touchJustStarted = false;
  window._touchPsychoX = null;
  window._touchPsychoY = null;
} else if (window._touchJustStarted) {
  window._touchJustStarted = false;
  window._touchPsychoX = null;
  window._touchPsychoY = null;
}
```

---

## 6. Struktura Plików Testu

```
NazwaTestu/
├── index.html              # Entry point (tylko dla JS)
├── NazwaTestu.js           # Główny plik JS (lub semafor.js, Poppelv2.js itd.)
├── main.py                 # Główny plik Python (HPM)
├── resources/              # Zasoby (obrazy, dźwięki)
│   ├── obraz1.png
│   └── obraz2.png
├── lib/                    # Biblioteki PsychoJS (opcjonalne)
│   └── psychojs-2025.1.1.js
└── data/                   # Zapis CSV (jeśli nie Nous)
```

---

## 7. Tryb Treningowy

### Python (HPM)

- Sprawdzanie: `NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'`
- Można użyć do zmniejszenia liczby prób (np. 5 zamiast 10)
- Przykład: `N_TRIALS = 10 if not NOUS_TRAINING else 5`

### JS (Standard)

- **Obecnie**: Tryb treningowy jest obsługiwany przez launcher **po zakończeniu testu**
- Launcher sprawdza `isTraining` i blokuje zapis do bazy
- Test JS **nie otrzymuje** informacji o trybie treningowym
- Jeśli w przyszłości launcher zacznie przekazywać `window.electronTest.isTraining`, można użyć do zmiany liczby prób

---

## 8. Ważne Uwagi

- **Nie tworzyć** dokumentacji/README chyba że użytkownik wyraźnie poprosi
- **Nie zmieniać** logiki testu bez wyraźnej prośby użytkownika
- **Zachowywać** oryginalne działanie testu przy dodawaniu funkcji
- **Sprawdzać** czy test działa zarówno z myszą jak i dotykiem (jeśli dotyk jest dodany)
- **Ujednolicać** nazewnictwo wyników we wszystkich testach
- **Filtrować** `_trialsData` aby pominąć wiersze bez `correct` (welcome itp.)
- **ESC zawsze** = `window.electronTest.close()` (bez zapisu) gdy `isCompleted === false`
- **Nie używać** `gui.Dlg` ani `core.quit()` w testach HPM – powodują problemy z Nous
- **HPM toggle** – domyślnie wyłączony przy każdym uruchomieniu aplikacji (niezależnie od poprzedniego stanu)

---

## 9. Przykładowe Zadania

### "Przeanalizuj test X i popraw..."

1. Przeczytaj główny plik JS/Python
2. Sprawdź `quitPsychoJS` / `_write_results` pod kątem nazewnictwa
3. Sprawdź obsługę ESC
4. Sprawdź czy są referencje do legacy scripts
5. Sprawdź czy test mierzy RT (jeśli tak, czy `sredni_czas_reakcji` jest w wynikach)
6. Wprowadź poprawki zgodnie z checklistą

### "Dodaj obsługę ekranu dotykowego"

1. W `experimentInit`: pobierz canvas, dodaj touch listeners
2. W `trialRoutineEachFrame`: dodaj funkcję `pointInStim` i blok obsługi dotyku
3. Pamiętaj o czyszczeniu stanu dotyku po obsłużeniu

### "Stwórz wersję Python/PsychoPy"

1. Skopiuj logikę z JS do Pythona
2. Użyj `psychopy.visual`, `psychopy.core`, `psychopy.event`
3. Dodaj `NOUS_LAUNCHER` i `NOUS_TRAINING` z `os.environ`
4. Zapis `results.json` tylko gdy `NOUS_LAUNCHER == True`
5. ESC na instrukcji: zapis pustych wyników
6. ESC w próbach: flaga `escaped`, przerwanie zewnętrznej pętli
7. Dostępne biblioteki HPM: `PsychoPy, NumPy, SciPy, Pandas, Pyglet, Pillow (PIL), wxPython`
8. **NIE używaj** `gui.Dlg` (dialog GUI) ani `core.quit()` – użyj `visual.TextStim` + `event.waitKeys()` i `return`

### "Napraw integrację testu Python z Nous"

1. Usuń wszystkie wywołania `core.quit()` – zastąp `return` lub naturalnym końcem `main()`
2. Usuń `gui.Dlg` – zastąp ekranami tekstowymi
3. Dodaj `NOUS_LAUNCHER` i `NOUS_TRAINING` jeśli ich brakuje
4. Przenieś `_write_results()` przed `win.close()` lub zaraz po pętli głównej
5. Sprawdź, czy ESC zapisuje pusty wynik zamiast po prostu kończyć

---

## 10. Testy w Projekcie

| Test | Typ | RT | Dotyk | Specyfika |
|------|-----|----|-------|-----------|
| **BystreOczko** | JS + HPM (Python) | ✅ tak | ✅ JS | Siatka sygnalizatorów; `ilosc_obiektow_do_klikniecia` (HPM) |
| **Poppel** | JS + HPM (Python) | ❌ nie | ✅ JS | Obiekty przesuwające się; `ilosc_obiektow_do_klikniecia` |
| **Semafor** | JS + HPM (Python) | ❌ nie | ✅ JS | Matryce logiczne; `ilosc_obiektow_do_klikniecia` |
| **Raven** | JS | ✅ tak | ❌ | Test matryc logicznych |
| **GoNoGo** | JS + HPM (Python) | ✅ tak | ❌ | Go/NoGo; `poziom_trudnosci`; parzyste=GO |
| **Stop** | JS + HPM (Python) | ✅ tak | ❌ | Samochód + znak STOP; kliknięcie myszą |
| **Sygnalizacja** | JS + HPM (Python) | ✅ tak | ❌ | Dwa auta, dwa światła; klawisze A/D lub strzałki; "falstart" = błąd |
| **Samochodzik** | JS + HPM (Python) | ❌ nie | ❌ | Nawigacja autem; `czas_pokonania_trasy_sek`; kolizje=błędy; używa PIL + Pyglet |
| **Piórkowski** | JS + HPM (Python) | ✅ tak | ❌ | Kółka losowo; kliknięcie w auto; `klikniecia_bez_kolka`; wybór czasu trwania |
| **PingPong** | JS + HPM (Python) | ❌ nie | ❌ | Odbijanie piłki 2 paletkami; `ilosc_poprawnych_nacisniec` = odbicia paletką, `ilosc_blednych_nacisniec` = przepuszczone; `poziom_trudnosci`; tryb Trudny ma progresję prędkości |

### Uwagi o specyficznych polach wynikowych

- **Samochodzik**: `ilosc_poprawnych_nacisniec` = 1 jeśli trasa ukończona, `ilosc_blednych_nacisniec` = liczba kolizji, `czas_pokonania_trasy_sek` = czas przejazdu
- **Piórkowski**: `ogolna_ilosc_nacisniec` = łączna liczba kółek (trafione + pominięte), `klikniecia_bez_kolka` = kliknięcia bez aktywnego kółka
- **GoNoGo**: `ogolna_ilosc_nacisniec` = liczba naciśnięć spacji (nie łączna liczba prób), `poziom_trudnosci` = nazwa wybranego poziomu
- **Sygnalizacja**: `ogolna_ilosc_nacisniec` = tylko aktywne kliknięcia (bez `too_slow`), RT liczone tylko od momentu pojawienia się zielonego światła
- **PingPong**: ⚠️ wymaga refaktoryzacji – brak integracji z Nous HPM

---

## 11. Biblioteki Dostępne w HPM

Silnik HPM zawiera skompilowane środowisko Python z następującymi bibliotekami:

| Biblioteka | Zastosowanie |
|-----------|-------------|
| `psychopy` | Główna biblioteka: `visual`, `core`, `event`, `hardware.keyboard` |
| `numpy` | Operacje matematyczne, tablice |
| `scipy` | Statystyki, przetwarzanie sygnałów |
| `pandas` | Analiza danych tabelarycznych |
| `pyglet` | System okienkowy niższego poziomu (używany przez PsychoPy; `pyglet.window.key` do ciągłego śledzenia klawiszy) |
| `pillow (PIL)` | Przetwarzanie obrazów (np. detekcja koloru pikseli – Samochodzik) |
| `wxPython` | GUI toolkit (odradzany – zamiast tego użyj TextStim) |

---

**Ostatnia aktualizacja**: 2026-03-21
**Wersja Nous**: 1.2.0
