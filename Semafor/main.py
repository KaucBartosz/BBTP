# -*- coding: utf-8 -*-
"""
Semafor – wersja PsychoPy.
Zgodna z semafor.js: menu (Test / Prezentacja), animacja demo,
mouseWasReleased fix, dane RT w ms, pola błędów rozdzielone.
"""

import json
import math
import os
import random
from datetime import datetime
from pathlib import Path

from psychopy import core, event, visual

# ── Konfiguracja ───────────────────────────────────────────────────────────────
NOUS_LAUNCHER = os.environ.get("NOUS_LAUNCHER") == "1"
NOUS_TRAINING = os.environ.get("NOUS_TRAINING") == "1"
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES = SCRIPT_DIR / "resources"

N = 8
TRIAL_TIMEOUT = 15.0  # s
FEEDBACK_TIME = 0.5  # s
N_TRIALS = 20
CORNER_COORDS = {(0, 0), (0, N - 1), (N - 1, 0), (N - 1, N - 1)}

# Lampki demo dla ekranu Prezentacji (indeksy siatki)
DEMO_XIX, DEMO_XIY = 3, 0  # x-lampka (górna krawędź, kolumna 3)
DEMO_YIX, DEMO_YIY = 0, 5  # y-lampka (lewa krawędź,  wiersz  5)
# Cel demo: lamp_grid[DEMO_XIX][DEMO_YIY] = lamp_grid[3][5]

INSTRUCTION = (
    "Za chwilę zobaczysz planszę z lampkami. Twoim zadaniem będzie, "
    "za pomocą MYSZY, wskazać tę lampkę, która znajduje się na przecięciu "
    "prostych dwóch lampek zapalonych na zielono. Staraj się klikać "
    "najszybciej jak potrafisz. Aby rozpocząć zadanie, wciśnij SPACJĘ."
)

# Kolory w przestrzeni PsychoPy rgb (-1..1); konwersja: v_01*2-1
_GREEN = (-0.70, 0.90, -0.70)  # linie przecięcia
_YELLOW = (1.00, 0.76, -1.00)  # kółko na przecięciu (fill)
_ORANGE = (1.00, 0.30, -1.00)  # kółko na przecięciu (line)
_CURSOR = (0.90, 0.90, 0.90)  # kursor (fill)
_CURSOR_BORDER = (-0.50, -0.50, -0.50)
_INFO_YELLOW = (1.00, 1.00, -0.10)  # tekst info w prezentacji
_GRAY_HINT = (0.00, 0.00, 0.00)  # podpowiedź klawiszowa
_GRAY_PREZ_TITLE = (0.30, 0.30, 0.30)  # nagłówek prezentacji
_GRAY_BACK = (0.10, 0.10, 0.10)  # przycisk powrotu (normalny)
_GOLD_BACK = (1.00, 0.50, -0.60)  # przycisk powrotu (hover)
_HOVER_GREEN = (-0.30, 1.00, -0.10)  # opcja 1 – hover
_HOVER_BLUE = (-0.10, 0.50, 1.00)  # opcja 2 – hover


# ── Funkcje pomocnicze ─────────────────────────────────────────────────────────


def _grid_coords():
    return [(i - (N - 1) / 2) * 0.08 for i in range(N)]


def _over(mpos, cx, cy, hw, hh):
    """Czy kursor mieści się w prostokącie (cx±hw, cy±hh)?"""
    return abs(mpos[0] - cx) <= hw and abs(mpos[1] - cy) <= hh


def _clamp01(x):
    return max(0.0, min(1.0, x))


def _smooth_step(x):
    s = _clamp01(x)
    return s * s * (3.0 - 2.0 * s)


def _reset_grid(lamp_grid):
    """Przywraca siatkę do stanu domyślnego (przed próbą)."""
    for ix in range(N):
        for iy in range(N):
            if (ix, iy) in CORNER_COORDS:
                lamp_grid[ix][iy].opacity = 0.0
                lamp_grid[ix][iy].setImage(str(RESOURCES / "lampkaOFF.png"))
            elif ix == 0 or ix == N - 1 or iy == 0 or iy == N - 1:
                lamp_grid[ix][iy].opacity = 1.0
                lamp_grid[ix][iy].setImage(str(RESOURCES / "lampkaZielOFF.png"))
            else:
                lamp_grid[ix][iy].opacity = 1.0
                lamp_grid[ix][iy].setImage(str(RESOURCES / "lampkaOFF.png"))


def _setup_demo_lamps(lamp_grid):
    """Ustawia siatkę w stan demo (dla ekranu Prezentacji)."""
    _reset_grid(lamp_grid)
    lamp_grid[DEMO_XIX][DEMO_XIY].setImage(str(RESOURCES / "lampkaZielON.png"))
    lamp_grid[DEMO_YIX][DEMO_YIY].setImage(str(RESOURCES / "lampkaZielON.png"))


def _draw_grid(lamp_grid):
    for ix in range(N):
        for iy in range(N):
            if lamp_grid[ix][iy].opacity > 0:
                lamp_grid[ix][iy].draw()


# ── main() ─────────────────────────────────────────────────────────────────────


def main():
    win = visual.Window(
        fullscr=True,
        units="height",
        color=(-1, -1, -1),
        allowGUI=False,
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    gc = _grid_coords()

    # ── Siatka lampek ──────────────────────────────────────────────────────────
    lamp_grid = []
    for ix in range(N):
        row = []
        for iy in range(N):
            is_corner = (ix, iy) in CORNER_COORDS
            is_outer = ix == 0 or ix == N - 1 or iy == 0 or iy == N - 1
            if is_corner:
                img, opacity = str(RESOURCES / "lampkaOFF.png"), 0.0
            elif is_outer:
                img, opacity = str(RESOURCES / "lampkaZielOFF.png"), 1.0
            else:
                img, opacity = str(RESOURCES / "lampkaOFF.png"), 1.0
            stim = visual.ImageStim(
                win, image=img, size=(0.08, 0.08), pos=(gc[ix], gc[iy])
            )
            stim.opacity = opacity
            row.append(stim)
        lamp_grid.append(row)

    demo_tx = gc[DEMO_XIX]  # -0.04  (pozycja X celu demo)
    demo_ty = gc[DEMO_YIY]  #  0.12  (pozycja Y celu demo)

    # ── Elementy MENU ──────────────────────────────────────────────────────────
    menu_title = visual.TextStim(
        win, text="Semafor", height=0.09, pos=(0, 0.28), color="white"
    )
    menu_opt1 = visual.TextStim(
        win, text="1.  Test", height=0.055, pos=(0, 0.06), color="white"
    )
    menu_opt2 = visual.TextStim(
        win, text="2.  Prezentacja", height=0.055, pos=(0, -0.10), color="white"
    )
    menu_hint = visual.TextStim(
        win,
        text="[ klawisze:  1  lub  2 ]",
        height=0.032,
        pos=(0, -0.28),
        color=_GRAY_HINT,
    )

    # ── Elementy PREZENTACJI ───────────────────────────────────────────────────
    prez_title = visual.TextStim(
        win, text="— Prezentacja —", height=0.04, pos=(0, 0.44), color=_GRAY_PREZ_TITLE
    )
    prez_h_line = visual.Rect(
        win, size=(0.68, 0.006), pos=(0.0, demo_ty), fillColor=_GREEN, lineColor=_GREEN
    )
    prez_v_line = visual.Rect(
        win, size=(0.006, 0.68), pos=(demo_tx, 0.0), fillColor=_GREEN, lineColor=_GREEN
    )
    prez_circle = visual.Circle(
        win, radius=0.048, pos=(demo_tx, demo_ty), fillColor=_YELLOW, lineColor=_ORANGE
    )
    prez_cursor = visual.Circle(
        win, radius=0.026, pos=(0.38, 0.36), fillColor=_CURSOR, lineColor=_CURSOR_BORDER
    )
    prez_info = visual.TextStim(
        win, text="", height=0.038, pos=(0, -0.40), color=_INFO_YELLOW, wrapWidth=1.2
    )
    prez_back = visual.TextStim(
        win, text="← Wróć do menu", height=0.031, pos=(0, -0.462), color=_GRAY_BACK
    )

    prez_h_line.opacity = 0.0
    prez_v_line.opacity = 0.0
    prez_circle.opacity = 0.0
    prez_cursor.opacity = 0.0

    # ══════════════════════════════════════════════════════════════════════════
    # MENU
    # ══════════════════════════════════════════════════════════════════════════
    menu_state = "choice"  # 'choice' | 'prezentacja'
    menu_mouse_released = False
    menu_choice = None  # ustawiane na 'test' po wyborze

    anim_clock = core.Clock()
    loop_count = 0
    lamp_on = False

    while menu_choice is None:
        keys = event.getKeys(keyList=["escape", "1", "2", "space", "backspace"])
        pressed = mouse.getPressed()
        if not any(pressed):
            menu_mouse_released = True

        # ── WYBÓR ─────────────────────────────────────────────────────────────
        if menu_state == "choice":
            if "escape" in keys:
                win.close()
                return

            mp = mouse.getPos()
            over1 = _over(mp, 0, 0.06, 0.30, 0.05)
            over2 = _over(mp, 0, -0.10, 0.30, 0.05)

            menu_opt1.setColor(_HOVER_GREEN if over1 else "white")
            menu_opt2.setColor(_HOVER_BLUE if over2 else "white")

            menu_title.draw()
            menu_opt1.draw()
            menu_opt2.draw()
            menu_hint.draw()

            if menu_mouse_released and pressed[0]:
                if over1:
                    menu_choice = "test"
                elif over2:
                    menu_opt1.setColor("white")
                    menu_opt2.setColor("white")
                    menu_state = "prezentacja"
                    anim_clock.reset()
                    loop_count = 0
                    _setup_demo_lamps(lamp_grid)
                    lamp_on = False
                    menu_mouse_released = False

            if "1" in keys or "space" in keys:
                menu_choice = "test"
            if "2" in keys:
                menu_opt1.setColor("white")
                menu_opt2.setColor("white")
                menu_state = "prezentacja"
                anim_clock.reset()
                loop_count = 0
                _setup_demo_lamps(lamp_grid)
                lamp_on = False
                menu_mouse_released = False

        # ── PREZENTACJA ───────────────────────────────────────────────────────
        elif menu_state == "prezentacja":
            if "escape" in keys or "backspace" in keys:
                menu_state = "choice"
                menu_mouse_released = False
                menu_opt1.setColor("white")
                menu_opt2.setColor("white")
            else:
                ANIM_T = 7.5
                raw_at = anim_clock.getTime()
                at = raw_at % ANIM_T

                # Nowa pętla → reset demo
                loop_n = int(raw_at / ANIM_T)
                if loop_n > loop_count:
                    loop_count = loop_n
                    _setup_demo_lamps(lamp_grid)
                    lamp_on = False

                # Linie (1.0–2.5 s fade-in, 7.0–7.5 s fade-out)
                line_a = (
                    _clamp01((at - 1.0) / 1.5) * 0.85 * _clamp01(1.0 - (at - 7.0) / 0.5)
                )
                prez_h_line.opacity = line_a
                prez_v_line.opacity = line_a

                # Pulsujące kółko (2.5–4.6 s)
                if 2.5 <= at < 4.6:
                    prez_circle.opacity = max(
                        0.0, 0.6 + 0.4 * math.sin(at * math.pi * 3.0)
                    )
                else:
                    prez_circle.opacity = 0.0

                # Kursor (4.5–6.2 s) – leci do celu, miga przy kliknięciu
                if 4.5 <= at < 6.2:
                    move_t = _smooth_step(_clamp01((at - 4.5) / 1.3))
                    prez_cursor.setPos(
                        (
                            0.38 + (demo_tx - 0.38) * move_t,
                            0.36 + (demo_ty - 0.36) * move_t,
                        )
                    )
                    click_fade = _clamp01((at - 5.80) / 0.15)
                    click_return = _clamp01((at - 5.95) / 0.15)
                    prez_cursor.opacity = 1.0 - click_fade * 0.85 + click_return * 0.85
                else:
                    prez_cursor.opacity = 0.0

                # Zapalenie lampki docelowej (5.9 s)
                if at >= 5.9 and not lamp_on:
                    lamp_grid[DEMO_XIX][DEMO_YIY].setImage(
                        str(RESOURCES / "lampkaON.png")
                    )
                    lamp_on = True

                # Tekst fazy
                if at < 1.0:
                    info = "Dwie lampki zapalają się na zielono..."
                elif at < 2.5:
                    info = "Każda wyznacza linię przez całą siatkę..."
                elif at < 4.5:
                    info = "Wskaż lampkę na przecięciu tych linii!"
                elif at < 5.9:
                    info = "Kliknij myszką w to miejsce!"
                else:
                    info = "✓  To jest prawidłowa odpowiedź!"
                prez_info.setText(info)

                # Rysowanie
                prez_title.draw()
                _draw_grid(lamp_grid)
                prez_h_line.draw()
                prez_v_line.draw()
                prez_circle.draw()
                prez_cursor.draw()
                prez_info.draw()

                # Przycisk powrotu
                mp = mouse.getPos()
                over_back = _over(mp, 0, -0.462, 0.22, 0.025)
                prez_back.setColor(_GOLD_BACK if over_back else _GRAY_BACK)
                prez_back.draw()

                if menu_mouse_released and pressed[0] and over_back:
                    menu_state = "choice"
                    menu_mouse_released = False
                    menu_opt1.setColor("white")
                    menu_opt2.setColor("white")

        win.flip()

    # ══════════════════════════════════════════════════════════════════════════
    # INSTRUKCJA (Welcome)
    # ══════════════════════════════════════════════════════════════════════════
    instr = visual.TextStim(
        win,
        text=INSTRUCTION,
        color="white",
        height=0.05,
        wrapWidth=1.2,
        alignText="center",
    )
    instr.draw()
    win.flip()

    keys = event.waitKeys(keyList=["space", "return", "escape"])
    if keys and "escape" in keys:
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0)
        return

    # ══════════════════════════════════════════════════════════════════════════
    # PĘTLA PRÓB
    # ══════════════════════════════════════════════════════════════════════════
    _reset_grid(lamp_grid)

    trials_data = []
    trial_clock = core.Clock()
    feedback_clock = core.Clock()
    escaped = False

    for _trial_idx in range(N_TRIALS):
        if event.getKeys(keyList=["escape"]):
            escaped = True
            break

        # ── Reset siatki ──────────────────────────────────────────────────────
        _reset_grid(lamp_grid)

        # ── Losowanie ─────────────────────────────────────────────────────────
        x_edge = "top" if random.random() < 0.5 else "bottom"
        y_edge = "left" if random.random() < 0.5 else "right"
        y_edge_row = 0 if x_edge == "top" else N - 1
        x_edge_col = 0 if y_edge == "left" else N - 1

        while True:
            x_index = random.randrange(N)
            while x_index == x_edge_col:
                x_index = random.randrange(N)
            y_index = random.randrange(N)
            while y_index == y_edge_row:
                y_index = random.randrange(N)
            if (x_index, y_edge_row) not in CORNER_COORDS and (
                x_edge_col,
                y_index,
            ) not in CORNER_COORDS:
                break

        lamp_grid[x_index][y_edge_row].setImage(str(RESOURCES / "lampkaZielON.png"))
        lamp_grid[x_edge_col][y_index].setImage(str(RESOURCES / "lampkaZielON.png"))

        target_x = x_index
        target_y = y_index

        clicked_x = None
        clicked_y = None
        rt = None
        correct = 0
        show_feedback = False
        # Musi nastąpić puszczenie przycisku przed akceptacją kliknięcia
        mouse_was_released = False

        trial_clock.reset()
        feedback_clock.reset()

        # ── Pętla klatek ──────────────────────────────────────────────────────
        while True:
            if event.getKeys(keyList=["escape"]):
                escaped = True
                break

            elapsed = trial_clock.getTime()
            pressed = mouse.getPressed()

            # Śledź puszczenie przycisku
            if not any(pressed):
                mouse_was_released = True

            # Rysowanie siatki
            _draw_grid(lamp_grid)

            # Kliknięcie lampki (tylko po puszczeniu przycisku)
            if mouse_was_released and pressed[0] and not show_feedback:
                click_pos = mouse.getPos()
                for ix in range(N):
                    for iy in range(N):
                        if lamp_grid[ix][iy].opacity == 0:
                            continue
                        if lamp_grid[ix][iy].contains(click_pos):
                            clicked_x = ix
                            clicked_y = iy
                            rt = elapsed
                            correct = 1 if (ix == target_x and iy == target_y) else 0
                            if correct == 1:
                                lamp_grid[ix][iy].setImage(
                                    str(RESOURCES / "lampkaON.png")
                                )
                            show_feedback = True
                            mouse_was_released = False
                            feedback_clock.reset()
                            break
                    if show_feedback:
                        break

            if show_feedback and feedback_clock.getTime() >= FEEDBACK_TIME:
                break
            if elapsed >= TRIAL_TIMEOUT:
                break

            win.flip()

        # rt w milisekundach (None dla braku odpowiedzi)
        trials_data.append(
            {
                "x_edge": x_edge,
                "y_edge": y_edge,
                "x_index": x_index,
                "y_index": y_index,
                "target_x": target_x,
                "target_y": target_y,
                "clicked_x": clicked_x,
                "clicked_y": clicked_y,
                "rt": round(rt * 1000) if rt is not None else None,
                "correct": correct,
            }
        )

        if escaped:
            break

    win.close()

    # ══════════════════════════════════════════════════════════════════════════
    # AGREGACJA WYNIKÓW
    # ══════════════════════════════════════════════════════════════════════════
    ilosc_klikniec_ogolem = sum(1 for t in trials_data if t["clicked_x"] is not None)
    poprawne_trafienia = sum(1 for t in trials_data if t["correct"] == 1)
    no_answer = sum(1 for t in trials_data if t["clicked_x"] is None)
    bledne_klikniecia = max(0, ilosc_klikniec_ogolem - poprawne_trafienia)
    bledne_trafienia = bledne_klikniecia + no_answer  # suma: błędne + braki
    total_trials = ilosc_klikniec_ogolem + no_answer
    accuracy = round((poprawne_trafienia / total_trials) * 100) if total_trials else 0

    # Średni RT (ms) – tylko próby z kliknięciem, braki wykluczone
    rts = [t["rt"] for t in trials_data if t["rt"] is not None]
    avg_rt = round(sum(rts) / len(rts)) if rts else 0

    if NOUS_LAUNCHER:
        _write_results(
            SCRIPT_DIR,
            trials_data,
            poprawne_trafienia,
            bledne_klikniecia,
            bledne_trafienia,
            ilosc_klikniec_ogolem,
            no_answer,
            accuracy,
            avg_rt,
        )


# ── Zapis wyników ──────────────────────────────────────────────────────────────


def _write_results(
    script_dir,
    trials_data,
    poprawne_trafienia,
    bledne_klikniecia,
    bledne_trafienia,
    ilosc_klikniec_ogolem,
    no_answer,
    accuracy,
    avg_rt,
):
    results = {
        "testId": "semafor",
        "subjectId": f"{random.randint(0, 999999):06d}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ilosc_poprawnych_nacisniec": poprawne_trafienia,
        "ilosc_blednych_nacisniec": bledne_trafienia,  # suma: błędne + braki
        "ilosc_blednych_klikniec": bledne_klikniecia,  # tylko błędne kliknięcia
        "ogolna_ilosc_nacisniec": ilosc_klikniec_ogolem,
        "ilosc_brakow_nacisniec": no_answer,  # tylko braki odpowiedzi
        "sredni_czas_reakcji": avg_rt,
        "score": (
            f"Kliknięć: {ilosc_klikniec_ogolem} | "
            f"Poprawne: {poprawne_trafienia} | "
            f"Błędne (w tym brak odp.): {bledne_trafienia} | "
            f"Brak odp.: {no_answer} | "
            f"Skuteczność: {accuracy}% | "
            f"Śr. RT: {avg_rt} ms"
        ),
        "statystyki": {
            "poprawne": poprawne_trafienia,
            "bledne_lacznie": bledne_trafienia,
            "bledne_klikniecia": bledne_klikniecia,
            "brak_odpowiedzi": no_answer,
            "wszystkie_kliki": ilosc_klikniec_ogolem,
            "proby": len(trials_data),
            "skutecznosc_proc": accuracy,
        },
        "wyniki": trials_data,  # rt już w ms, None dla braku odpowiedzi
    }
    out_path = script_dir / "results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
