# -*- coding: utf-8 -*-
"""
GoNoGo – wersja PsychoPy (HPM).
Parzyste (0,2,4,6,8) = GO (naciśnij spację), nieparzyste = NOGO (czekaj).
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
DIFFICULTY_MAP = {
    '1': (1.5, 'Łatwy (1.5s)'),
    '2': (1.0, 'Normalny (1.0s)'),
    '3': (0.5, 'Trudny (0.5s)'),
}


def _write_results(script_dir, trials_data, poprawne, bledne, wszystkie, avg_rt_ms,
                   difficulty_name='Nieznany', score_text=''):
    results = {
        'testId': 'GoNoGo',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        'sredni_czas_reakcji': avg_rt_ms,
        'poziom_trudnosci': difficulty_name,
        'score': score_text or f'Poprawne: {poprawne} | Błędne: {bledne} | Łącznie: {wszystkie} | Śr. RT: {avg_rt_ms} ms | Poziom: {difficulty_name}',
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    win = visual.Window(fullscr=True, units='height', color=(0, 0, 0), allowGUI=False)

    # --- Instrukcja ---
    instr = visual.TextStim(
        win,
        text='Witaj w teście Go/NoGo!\n\nTwoim zadaniem jest reagowanie na liczby:\n\n'
             'PARZYSTE (0, 2, 4, 6, 8)\n-> Naciśnij SPACJĘ (Szybko!)\n\n'
             'NIEPARZYSTE (1, 3, 5, 7, 9)\n-> Nic nie rób (Czekaj)\n\n\nNaciśnij SPACJĘ, aby rozpocząć.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    keyname = keys[0] if keys else None
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, score_text='')
        return

    # --- Wybór trudności ---
    diff_text = visual.TextStim(
        win,
        text='Wybierz poziom trudności:\n\n1 - ŁATWY (1.5 s)\n2 - NORMALNY (1.0 s)\n3 - TRUDNY (0.5 s)\n\nNaciśnij 1, 2 lub 3.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    diff_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', 'escape'])
    keyname = keys[0] if keys else None
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, score_text='')
        return
    decision_time, difficulty_name = DIFFICULTY_MAP.get(keyname, (1.0, 'Normalny (1.0s)'))

    # Komponenty próby
    number_stim = visual.TextStim(win, text='', color='white', height=0.15, alignText='center')
    feedback_stim = visual.TextStim(win, text='', color='white', height=0.15, alignText='center')
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    trials_data = []
    escaped = False

    for trial_idx in range(N_TRIALS):
        num = random.randint(0, 9)
        current_number = str(num)
        is_go = (num % 2) == 0

        number_stim.setText(current_number)
        number_stim.draw()
        win.flip()

        clock = core.Clock()
        pressed = False
        rt_sec = None
        while clock.getTime() < decision_time:
            keys = event.getKeys(keyList=['space', 'escape'], timeStamped=clock)
            for k, t in keys:
                if k == 'escape':
                    escaped = True
                    break
                if k == 'space':
                    pressed = True
                    rt_sec = t
                    break
            if escaped:
                break
            if pressed:
                break
        if escaped:
            break

        # Ocena
        if is_go:
            was_correct = pressed
        else:
            was_correct = not pressed

        trials_data.append({
            'number_shown': current_number,
            'condition': 'go' if is_go else 'nogo',
            'was_correct': was_correct,
            'pressed': pressed,
            'rt': rt_sec if pressed else None,
        })

        # Feedback
        feedback_stim.setText(current_number)
        feedback_stim.setColor('green' if was_correct else 'red')
        feedback_stim.draw()
        win.flip()
        core.wait(1.5)

    win.close()

    # Wyniki
    if not NOUS_LAUNCHER:
        return

    wszystkie = sum(1 for t in trials_data if t.get('pressed'))
    poprawne = sum(1 for t in trials_data if t.get('pressed') and t.get('was_correct'))
    bledne = max(0, wszystkie - poprawne)
    rts = [t['rt'] for t in trials_data if t.get('rt') is not None and t['rt'] >= 0]
    avg_rt_ms = round((sum(rts) / len(rts)) * 1000) if rts else 0
    accuracy = round((poprawne / len(trials_data)) * 100) if trials_data else 0
    score_text = f'Poprawne: {poprawne} | Błędne: {bledne} | Łącznie: {wszystkie} | Skuteczność: {accuracy}% | Śr. RT: {avg_rt_ms} ms | Poziom: {difficulty_name}'

    _write_results(SCRIPT_DIR, trials_data, poprawne, bledne, wszystkie, avg_rt_ms,
                   difficulty_name=difficulty_name, score_text=score_text)


if __name__ == '__main__':
    main()
