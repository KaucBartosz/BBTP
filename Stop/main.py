# -*- coding: utf-8 -*-
"""
Stop – wersja PsychoPy (HPM).
Samochód jedzie w tę i z powrotem; po 2–5 s pojawia się znak STOP.
Kliknięcie w auto lub w znak STOP po jego pojawieniu się = poprawna reakcja (RT).
Integracja z Nous: NOUS_LAUNCHER, results.json, ESC bez zapisu.
"""
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

N_TRIALS = 10 if not NOUS_TRAINING else 5
TRIAL_TIMEOUT = 10.0
CAR_SPEED = 0.3
CAR_Y = -0.3


def _write_results(script_dir, trials_data, poprawne, bledne, wszystkie, avg_rt_ms, score_text=''):
    results = {
        'testId': 'Stop',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        'sredni_czas_reakcji': avg_rt_ms,
        'score': score_text or f'Poprawne: {poprawne} | Błędne: {bledne} | Łącznie: {wszystkie} | Śr. RT: {avg_rt_ms} ms',
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    tlo_path = RESOURCES / 'tlo.png'
    car_path = RESOURCES / 'car.png'
    stop_path = RESOURCES / 'stop.png'
    if not tlo_path.exists():
        tlo_path = SCRIPT_DIR / 'resources' / 'tlo.png'
    if not car_path.exists():
        car_path = SCRIPT_DIR / 'resources' / 'car.png'
    if not stop_path.exists():
        stop_path = SCRIPT_DIR / 'resources' / 'stop.png'

    win = visual.Window(fullscr=True, units='height', color=(0, 0, 0), allowGUI=False)

    # Instrukcja
    instr = visual.TextStim(
        win,
        text='Witaj!\n\nNa ekranie porusza się samochodzik.\n'
             'Twoim zadaniem jest naciśnięcie na niego (lub na znak STOP), gdy gdzieś na ekranie pojawi się znak stop.\n\n'
             'Naciśnij SPACJĘ, aby rozpocząć.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys and keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, score_text='')
        return

    # Stimuli
    tlo = visual.ImageStim(win, image=str(tlo_path), size=(2, 1), pos=(0, 0))
    car = visual.ImageStim(win, image=str(car_path), size=(0.28, 0.28), pos=(0, CAR_Y))
    stop_sign = visual.ImageStim(win, image=str(stop_path), size=(0.2, 0.2), pos=(0, 0.2))
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    trials_data = []
    escaped = False

    for _ in range(N_TRIALS):
        stop_onset = 2.0 + random.random() * 3.0
        stop_x = -0.6 + random.random() * 1.2
        stop_sign.pos = (stop_x, 0.2)
        stop_sign.opacity = 0

        car_x = -0.5
        car_direction = 1
        trial_clock = core.Clock()
        stop_clock = None
        responded = False
        rt_sec = None
        correct = 0

        while trial_clock.getTime() < TRIAL_TIMEOUT:
            t = trial_clock.getTime()

            # Pojawienie się STOP
            if not responded and t >= stop_onset and stop_clock is None:
                stop_sign.opacity = 1
                stop_clock = core.Clock()

            # Ruch auta
            car_x += car_direction * CAR_SPEED * (1.0 / 60.0)
            if car_x >= 0.5:
                car_x = 0.5
                car_direction = -1
            elif car_x <= -0.5:
                car_x = -0.5
                car_direction = 1
            car.pos = (car_x, CAR_Y)

            tlo.draw()
            car.draw()
            stop_sign.draw()
            win.flip()

            # ESC
            if event.getKeys(keyList=['escape']):
                escaped = True
                break

            # Klik w auto lub znak STOP (po pojawieniu się znaku)
            if stop_clock is not None and not responded:
                if mouse.isPressedIn(car) or mouse.isPressedIn(stop_sign):
                    responded = True
                    rt_sec = stop_clock.getTime()
                    correct = 1
                    break

        if escaped:
            break

        trials_data.append({
            'stopOnset': stop_onset,
            'responded': responded,
            'rt': rt_sec,
            'correct': correct,
        })

    win.close()

    if not NOUS_LAUNCHER:
        return

    correct_count = sum(t['correct'] for t in trials_data)
    responded_count = sum(1 for t in trials_data if t['responded'])
    incorrect_count = max(0, responded_count - correct_count)
    rts = [t['rt'] for t in trials_data if t.get('rt') is not None and t['rt'] >= 0]
    avg_rt_ms = round((sum(rts) / len(rts)) * 1000) if rts else 0
    total = len(trials_data)
    accuracy = round((correct_count / total) * 100) if total else 0
    score_text = f'Poprawne: {correct_count} | Błędne: {incorrect_count} | Łącznie: {responded_count} | Skuteczność: {accuracy}% | Śr. RT: {avg_rt_ms} ms'

    _write_results(SCRIPT_DIR, trials_data, correct_count, incorrect_count, responded_count, avg_rt_ms, score_text=score_text)


if __name__ == '__main__':
    main()
