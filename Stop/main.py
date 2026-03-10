# -*- coding: utf-8 -*-
"""
Stop – wersja PsychoPy (HPM).
Samochód stoi w miejscu; po 1–3 s pojawia się znak STOP.
Kliknięcie w auto, w znak STOP lub naciśnięcie SPACJI po pojawieniu się znaku = poprawna reakcja.
Reakcja przed znakiem = falstart (błąd).
Maksymalny czas reakcji = 5s.
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

N_TRIALS = 50 if not NOUS_TRAINING else 5
CAR_Y = -0.3
CAR_X = 0.25 # Zaktualizowana pozycja (zgodnie z manualną poprawką użytkownika w JS)


def _write_results(script_dir, trials_data, poprawne, bledne, wszystkie, avg_rt_ms, total_clicks, falstarty, score_text=''):
    results = {
        'testId': 'Stop',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        'sredni_czas_reakcji': avg_rt_ms,
        'totalClicks': total_clicks,
        'score': score_text,
        'statystyki': {
            'sredni_czas_ms': avg_rt_ms,
            'poprawne_reakcje': poprawne,
            'wszystkie_proby': len(trials_data),
            'skutecznosc': round((poprawne / len(trials_data)) * 100) if trials_data else 0,
            'reakcje': wszystkie,
            'bledne_reakcje': bledne,
            'totalClicks': total_clicks,
            'falstarty': falstarty
        },
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    tlo_path = RESOURCES / 'tlo.png'
    car_path = RESOURCES / 'car.png'
    stop_path = RESOURCES / 'stop.png'
    
    if not tlo_path.exists(): tlo_path = SCRIPT_DIR / 'resources' / 'tlo.png'
    if not car_path.exists(): car_path = SCRIPT_DIR / 'resources' / 'car.png'
    if not stop_path.exists(): stop_path = SCRIPT_DIR / 'resources' / 'stop.png'

    win = visual.Window(fullscr=True, units='height', color=(0, 0, 0), allowGUI=False)

    # Instrukcja
    instr = visual.TextStim(
        win,
        text='Witaj!\n\nNa ekranie znajduje się samochód.\n'
             'Twoim zadaniem jest go zatrzymać, gdy zobaczysz znak STOP.\n\n'
             'Aby to zrobić, naciśnij na samochód lub naciśnij klawisz SPACJA.\n\n'
             'Naciśnij SPACJĘ, aby rozpocząć.',
        color='white', height=0.05, wrapWidth=1.5, alignText='center',
    )
    instr.draw()
    win.flip()
    
    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys and 'escape' in keys:
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, score_text='')
        return

    # Stimuli
    tlo = visual.ImageStim(win, image=str(tlo_path), size=(2, 1), pos=(0, 0))
    car = visual.ImageStim(win, image=str(car_path), size=(0.28, 0.28), pos=(CAR_X, CAR_Y))
    stop_sign = visual.ImageStim(win, image=str(stop_path), size=(0.2, 0.2), pos=(0, 0.2))
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    trials_data = []
    escaped = False

    for _ in range(N_TRIALS):
        stop_onset = 1.0 + random.random() * 2.0 # 1-3 s
        stop_x = -0.6 + random.random() * 1.2
        stop_sign.pos = (stop_x, 0.2)
        stop_sign.opacity = 0

        trial_clock = core.Clock()
        stop_clock = None
        responded = False
        rt_sec = None
        correct = 0
        is_falstart = False

        while trial_clock.getTime() < 10.0: # Ogólny timeout
            t = trial_clock.getTime()

            # Pojawienie się STOP
            if not responded and t >= stop_onset and stop_clock is None:
                stop_sign.opacity = 1
                stop_clock = core.Clock()

            # Limit czasu 5s od pojawienia się STOP
            if stop_clock and stop_clock.getTime() >= 5.0:
                break

            tlo.draw()
            car.draw()
            stop_sign.draw()
            win.flip()

            # ESC
            if event.getKeys(keyList=['escape']):
                escaped = True
                break

            # Reakcja (Mysz lub SPACJA)
            keys = event.getKeys(keyList=['space'])
            buttons = mouse.getPressed()
            
            # REAKCJA PRZED ZNAKIEM STOP (Falstart)
            if not stop_sign.opacity and not responded:
                if any(buttons) or 'space' in keys:
                    responded = True
                    correct = 0
                    is_falstart = True
                    break

            # POPRAWNA REAKCJA (po pojawieniu się STOP)
            if stop_sign.opacity and not responded:
                if (any(buttons) and (mouse.isPressedIn(car) or mouse.isPressedIn(stop_sign))) or 'space' in keys:
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
            'isFalstart': is_falstart
        })

    win.close()

    if not NOUS_LAUNCHER:
        return

    correct_count = sum(t['correct'] for t in trials_data)
    responded_count = sum(1 for t in trials_data if t['responded'])
    incorrect_count = max(0, responded_count - correct_count)
    falstart_count = sum(1 for t in trials_data if t.get('is_falstart', False) or (t['responded'] and t['correct'] == 0 and not t.get('rt')))
    
    # Fix falstart count logic to be explicit
    falstart_count = sum(1 for t in trials_data if t.get('isFalstart'))
    
    rts = [t['rt'] for t in trials_data if t.get('rt') is not None and t['rt'] >= 0]
    avg_rt_ms = round((sum(rts) / len(rts)) * 1000) if rts else 0
    total_trials = len(trials_data)
    accuracy = round((correct_count / total_trials) * 100) if total_trials else 0
    
    total_clicks = responded_count # Zgodnie z logiką w JS
    
    score_text = f'Poprawne: {correct_count} | Błędne: {incorrect_count} | Łącznie: {responded_count} | Kliknięcia: {total_clicks} | Skuteczność: {accuracy}% | Śr. RT: {avg_rt_ms} ms'

    _write_results(SCRIPT_DIR, trials_data, correct_count, incorrect_count, responded_count, avg_rt_ms, total_clicks, falstart_count, score_text=score_text)


if __name__ == '__main__':
    main()
