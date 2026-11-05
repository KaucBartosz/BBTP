# BBTP — Psychometric tests: JS vs Python accuracy notes

## Cel
Porównanie dokładności zbierania wyników (zwłaszcza czasu reakcji RT) pomiędzy wersją Python (PsychoPy, `main.py`) a wersją JS (PsychoJS, `*.js`, uruchamiana przez Electron/Nous).

## Testy mierzące czas reakcji (RT)
RT jest mierzone w: GoNoGo, GoNoGoBiegacze, NWstecz, BystreOczko, Corsi, Semafor, Stop, Stroop, Sygnalizacja, ZlapSygnal.

RT NIE jest mierzone w: FabrykaFigur, PingPong, Samochodzik (tam mierzony jest czas wykonania zadania / przejazdu, nie RT per próba).

## Zidentyfikowane różnice wpływające na dokładność RT

1. **Stroop (stroop.js)** — RT liczony jako `theseKeys[0].rt - 0.5` (stała). Poprawka: `theseKeys[0].rt - targetText.tStart` (rzeczywisty onset stimulusu). Zmiana wprowadzona. Różnica ~15–30 ms/próbę.

2. **Samochodzik (samochodzik.js)** — czas przejazdu liczony przez `Date.now()` (zegar ścienny). Rekomendacja: użyć `performance.now()` / `util.Clock` (zegar monotoniczny), jak w Pythonie (`core.getTime()`).

3. **Semafor / Sygnalizacja / Stop / ZlapSygnal** — RT mierzony w sekundach zmiennoprzecinkowych (PsychoJS `util.Clock`, ~0.1–1 ms rozdzielczości) vs Python `core.Clock` (~1 µs). Rekomendacja: ujednolicić zaokrąglenia (per-trial ms → średnia) zgodnie z Pythonem; w `wyniki` zapisywać RT w ms.

4. **Zaokrąglenia** — Python zaokrągla RT do ms per próba, potem uśrednia zaokrąglone. JS uśrednia pełne sekundy i zaokrągla na końcu. Rekomendacja: w JS zaokrąglać per-trial RT do ms przed uśrednieniem, dla spójności z Pythonem.

5. **Brakujące pola w sendResults (JS)** — Python zapisuje blok `statystyki` (sredni_czas_ms, poprawne_reakcje, wszystkie_proby, bledne_reakcje, skutecznosc) i `pominiete`. JS często pomija te pola. Rekomendacja: dodać je do `sendResults`.

## Zastosowane poprawki
- Stroop: `rt_val` liczony od `targetText.tStart` (zamiast stałych 0.5 s).
- Samochodzik: `Date.now()` → `performance.now()` (zegar monotoniczny).
- Semafor, Sygnalizacja, Stop, ZlapSygnal: uśrednianie RT w ms (per-trial ms → średnia), zamiast sekund zmiennoprzecinkowych.

## Procedura testowania JS
- Serwer HTTP w folderze testu: `python -m http.server 8765`
- Automatyzacja przez Playwright (node_modules z Nous): naciśnięcia klawiszy, przechwycenie pobranego CSV.
- Punkt odniesienia przed/po: porównanie rt_ms w CSV.
"