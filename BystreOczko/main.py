# -*- coding: utf-8 -*-
"""
BystreOczko – wersja PsychoPy (HPM / Nous).
Siatka sygnalizatorów: jedno światło zapala się na zielono w losowym momencie;
zadaniem jest jak najszybsze naciśnięcie na zielone.
"""
import os
import json
import random
from datetime import datetime
from pathlib import Path

from psychopy import visual, core, event

# --- Konfiguracja Nous (HPM) ---
NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES = SCRIPT_DIR / 'resources'

ROWS, COLS = 3, 6
TRIAL_TIMEOUT_SEC = 10.0
FEEDBACK_TIME = 0.5
N_TRIALS = 5 if NOUS_TRAINING else 10

INSTRUCTION = (
    'Przed tobą pojawi się plansza z sygnalizatorami. W losowym interwale czasu '
    'jeden z nich zapali się na zielono. Twoim zadaniem jest naciśnięcie na sygnalizator '
    'z zielonym światłem. W przypadku poprawnego trafienia wszystkie zapalą się na zielono. '
    'W przypadku błędnego trafienia, wszystkie zgasną. Powodzenia!'
)


def _write_results(script_dir, trials_data, correct_count, wrong_count, total_clicks, avg_rt_ms):
    n_trials = len(trials_data)
    results = {
        'testId': 'bystreOczko',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': correct_count,
        'ilosc_blednych_nacisniec': wrong_count,
        'ogolna_ilosc_nacisniec': total_clicks,
        'sredni_czas_reakcji': avg_rt_ms,
        'czas_reakcji': avg_rt_ms,
        'score': f'Poprawne: {correct_count} | Błędne: {wrong_count} | Łącznie: {total_clicks} | Śr. RT: {avg_rt_ms} ms',
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(-1, -1, -1),
        allowGUI=False,
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    # Ekran instrukcji
    instr = visual.TextStim(
        win, text=INSTRUCTION,
        color='white', height=0.05,
        wrapWidth=1.8, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'return', 'y', 'n', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0)
        return

    # Siatka sygnalizatorów (współrzędne jak w JS)
    x_coords = [(i - (COLS - 1) / 2) * 0.18 for i in range(COLS)]
    y_coords = [0.2, 0.0, -0.2]
    size = [0.12, 0.12]

    lights = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            stim = visual.ImageStim(
                win,
                image=str(RESOURCES / 'sygCzer.png'),
                size=size,
                pos=(x_coords[c], y_coords[r]),
            )
            row.append(stim)
        lights.append(row)

    trials_data = []
    trial_clock = core.Clock()
    rt_clock = core.Clock()

    for trial_idx in range(N_TRIALS):
        # Sprawdź ESC
        if event.getKeys(keyList=['escape']):
            break

        # Wszystkie na czerwono
        for r in range(ROWS):
            for c in range(COLS):
                lights[r][c].setImage(str(RESOURCES / 'sygCzer.png'))
                lights[r][c].draw()

        green_onset = 1.0 + random.random() * 3.0
        target_row = random.randint(0, ROWS - 1)
        target_col = random.randint(0, COLS - 1)

        responded = False
        rt = None
        correct = 0
        green_on = False
        prev_pressed = mouse.getPressed()
        escaped = False

        trial_clock.reset()
        rt_clock.reset()

        while trial_clock.getTime() < TRIAL_TIMEOUT_SEC:
            t = trial_clock.getTime()

            if event.getKeys(keyList=['escape']):
                escaped = True
                break

            # Włączenie zielonego
            if not green_on and t >= green_onset:
                green_on = True
                lights[target_row][target_col].setImage(str(RESOURCES / 'sygZiel.png'))
                rt_clock.reset()

            # Rysuj siatkę
            for r in range(ROWS):
                for c in range(COLS):
                    lights[r][c].draw()

            # Kliknięcie myszy
            pressed = mouse.getPressed()
            is_new_click = (pressed[0] or pressed[1] or pressed[2]) and not (prev_pressed[0] or prev_pressed[1] or prev_pressed[2])
            prev_pressed = pressed

            if green_on and not responded and is_new_click:
                pos = mouse.getPos()
                for r in range(ROWS):
                    for c in range(COLS):
                        if lights[r][c].contains(pos):
                            responded = True
                            rt = rt_clock.getTime()
                            correct = 1 if (r == target_row and c == target_col) else 0
                            feedback_img = RESOURCES / 'sygZiel.png' if correct == 1 else RESOURCES / 'syg.png'
                            for rr in range(ROWS):
                                for cc in range(COLS):
                                    lights[rr][cc].setImage(str(feedback_img))
                            break
                    if responded:
                        break
                if responded:
                    break

            win.flip()

        # Feedback przez krótką chwilę
        if responded:
            for r in range(ROWS):
                for c in range(COLS):
                    lights[r][c].draw()
            win.flip()
            core.wait(FEEDBACK_TIME)

        trials_data.append({
            'greenOnset': green_onset,
            'target_row': target_row,
            'target_col': target_col,
            'rt': rt,
            'correct': correct,
        })

        if escaped:
            break

    win.close()

    # Podsumowanie wyników (zgodne z wersją JS)
    correct_count = sum(1 for t in trials_data if t['correct'] == 1)
    wrong_count = sum(1 for t in trials_data if t['rt'] is not None and t['correct'] == 0)
    total_clicks = correct_count + wrong_count
    n_trials = len(trials_data)
    sum_rt = sum(
        t['rt'] if t['rt'] is not None and t['rt'] >= 0 else TRIAL_TIMEOUT_SEC
        for t in trials_data
    )
    avg_rt_ms = round((sum_rt / n_trials) * 1000) if n_trials else 0

    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, trials_data, correct_count, wrong_count, total_clicks, avg_rt_ms)


if __name__ == '__main__':
    main()
