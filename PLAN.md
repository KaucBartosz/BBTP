# Plan: poprawa dokładności pomiarów RT w testach JS (BBTP)

## Faza 0 — Diagnoza (DONE)
RT mierzone w: GoNoGo, GoNoGoBiegacze, NWstecz, BystreOczko, Corsi, Semafor, Stop, Stroop, Sygnalizacja, ZlapSygnal.
RT nie mierzone w: FabrykaFigur, PingPong, Samochodzik (czas wykonania zadania).

## Faza 1 — Stroop (DONE)
Poprawka: RT od `targetText.tStart` zamiast stałych 0.5 s. Przetestowane przed/po (CSV).

## Faza 2 — Samochodzik (DONE)
Problem: `Date.now()` (zegar ścienny) zamiast monotonicznego.
Poprawka: użyć `performance.now()` / PsychoJS `util.Clock`. Zastosowano (brak testu przed/po — test wymaga interakcji manualnej).

## Faza 3 — Semafor, Sygnalizacja, Stop, ZlapSygnal (DONE)
Problem: RT w sekundach, zaokrąglenia na końcu; JS mniej precyzyjny niż Python.
Poprawka: per-trial RT w ms, uśrednianie zaokrąglonych ms. Zastosowano (brak testu przed/po — testy wymagają interakcji manualnej).

## Faza 4 — GoNoGo, GoNoGoBiegacze, NWstecz, BystreOczko, Corsi (DONE)
RT mierzone i zbierane w wynikach. Poprawiono uśrednianie RT (per-trial ms) we wszystkich pięciu testach, zgodnie z Pythonem.

## Faza 5 — Brakujące pola w sendResults (DONE)
Dodano blok `statystyki` do JS sendResults w testach, które go nie miały: Stroop, BystreOczko, ZlapSygnal.

## Procedura dla każdej fazy
1. Uruchomić test (Playwright) → CSV przed.
2. Zastosować poprawkę.
3. Uruchomić test ponownie → CSV po.
4. Porównać RT.
5. Zaktualizować AGENTS.md.
"