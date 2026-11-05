# Plan: poprawa dokładności pomiarów RT w testach JS (BBTP)

## Faza 0 — Diagnoza (DONE)
RT mierzone w: GoNoGo, GoNoGoBiegacze, NWstecz, BystreOczko, Corsi, Semafor, Stop, Stroop, Sygnalizacja, ZlapSygnal.
RT nie mierzone w: FabrykaFigur, PingPong, Samochodzik (czas wykonania zadania).

## Faza 1 — Stroop (DONE)
Poprawka: RT od `targetText.tStart` zamiast stałych 0.5 s. Przetestowane przed/po (CSV).

## Faza 2 — Samochodzik
Problem: `Date.now()` (zegar ścienny) zamiast monotonicznego.
Poprawka: użyć `performance.now()` / PsychoJS `util.Clock`. Przetestować przed/po (czas_ms w CSV).

## Faza 3 — Semafor, Sygnalizacja, Stop, ZlapSygnal
Problem: RT w sekundach, zaokrąglenia na końcu; JS mniej precyzyjny niż Python.
Poprawka: per-trial RT w ms, uśrednianie zaokrąglonych ms. Przetestować przed/po.

## Faza 4 — GoNoGo, GoNoGoBiegacze, NWstecz, BystreOczko, Corsi
Sprawdzić czy RT jest zbierane w wynikach (JS rt_refs niskie). Uzupełnić jeśli brakuje. Przetestować.

## Faza 5 — Brakujące pola w sendResults
Dodać blok `statystyki` i `pominiete` do JS sendResults (wszystkie testy).

## Procedura dla każdej fazy
1. Uruchomić test (Playwright) → CSV przed.
2. Zastosować poprawkę.
3. Uruchomić test ponownie → CSV po.
4. Porównać RT.
5. Zaktualizować AGENTS.md.
"