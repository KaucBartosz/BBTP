# -*- coding: utf-8 -*-
"""
NWstecz – wersja PsychoPy (HPM).
Test pamięci roboczej N-Back.
Badany widzi kolejne cyfry i musi ocenić, czy aktualna cyfra jest taka sama jak N miejsc temu.
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

TARGET_CORRECT = 50
DIFFICULTY_MAP = {
    '1': (5.0, 'Łatwy (5s)'),
    '2': (2.0, 'Normalny (2s)'),
    '3': (1.0, 'Trudny (1s)'),
}
NBACK_MAP = {
    '1': (1, '1 wstecz'),
    '2': (2, '2 wstecz'),
    '3': (3, '3 wstecz'),
    '4': (4, '4 wstecz'),
    '5': (5, '5 wstecz'),
}


def _write_results(script_dir, trials_data, poprawne, bledne, wszystkie, avg_rt_ms,
                   nback_level=1, nback_name='1 wstecz', difficulty_name='Nieznany',
                   decision_time=2.0, test_ended_reason='', score_text=''):
    results = {
        'testId': 'NWstecz',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        'sredni_czas_reakcji': avg_rt_ms,
        'poziom_trudnosci': f'{nback_name} | {difficulty_name}',
        'nback_level': nback_level,
        'decision_time': decision_time,
        'total_correct': poprawne,
        'test_ended_reason': test_ended_reason,
        'score': score_text or f'Poprawne: {poprawne} | Błędne: {bledne} | N-Back: {nback_name} | Poziom: {difficulty_name} | Śr. RT: {avg_rt_ms} ms',
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    win = visual.Window(fullscr=True, units='height', color=(0, 0, 0), allowGUI=False)
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    # --- Instrukcja ---
    instr = visual.TextStim(
        win,
        text='W tym teście będziesz widzieć kolejne cyfry.\n\nPo wyświetleniu pierwszych 5 cyfr, Twoim zadaniem będzie ocenić, czy aktualna cyfra jest TAKA SAMA jak cyfra zapisana N miejsc wcześniej.\n\nNaciśnij TAK (Y) jeśli cyfra jest taka sama, NIE (N) jeśli jest inna.\nBrak reakcji oznacza automatycznie odpowiedź "Nie".\n\nNaciśnij SPACJĘ, aby kontynuować.',
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

    # --- Wybór N-Back ---
    nback_text = visual.TextStim(
        win,
        text='Wybierz ile miejsc wstecz chcesz zapamiętywać:\n\n1 - 1 miejsce wstecz\n2 - 2 miejsca wstecz\n3 - 3 miejsca wstecz\n4 - 4 miejsca wstecz\n5 - 5 miejsc wstecz\n\nNaciśnij 1, 2, 3, 4 lub 5.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    nback_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
    keyname = keys[0] if keys else None
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, score_text='')
        return
    nback_level, nback_name = NBACK_MAP.get(keyname, (1, '1 wstecz'))

    # --- Wybór trudności ---
    diff_text = visual.TextStim(
        win,
        text='Wybierz czas na odpowiedź:\n\n1 - ŁATWY (5 sekund)\n2 - NORMALNY (2 sekundy)\n3 - TRUDNY (1 sekunda)\n\nNaciśnij 1, 2 lub 3.',
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
    decision_time, difficulty_name = DIFFICULTY_MAP.get(keyname, (2.0, 'Normalny (2s)'))

    # Komponenty
    number_stim = visual.TextStim(win, text='', color='white', height=0.15, alignText='center')
    question_stim = visual.TextStim(
        win,
        text=f'Czy ta cyfra pojawiła się {nback_level} miejsc temu? (TAK/NIE)',
        color='white', height=0.04, pos=[0, 0.15], alignText='center', wrapWidth=1.8,
    )
    feedback_stim = visual.TextStim(win, text='...', color='darkgrey', height=0.1, alignText='center')
    progress_stim = visual.TextStim(win, text='', color='grey', height=0.03, pos=[0, -0.25], alignText='center')

    # --- Początkowa sekwencja 5 liczb ---
    sequence = []
    for i in range(5):
        sequence.append(random.randint(0, 9))

    # Wyświetl sekwencję z odliczaniem
    for i, num in enumerate(sequence):
        number_stim.setText(str(num))
        # Odliczanie w lewym górnym rogu: 5, 4, 3, 2, 1
        progress_stim = visual.TextStim(
            win,
            text=str(5 - i),
            color='grey',
            height=0.06,
            pos=[-0.85, 0.45],  # lewy górny róg
            alignText='left',
        )
        number_stim.draw()
        progress_stim.draw()
        win.flip()

        clock = core.Clock()
        escaped = False
        while clock.getTime() < 2.0:
            k = event.getKeys(keyList=['escape'])
            if k:
                escaped = True
                break
            core.wait(0.01)
        if escaped:
            win.close()
            if NOUS_LAUNCHER:
                _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, score_text='')
            return

    # --- Główna pętla testowa ---
    trials_data = []
    total_correct = 0
    test_ended = False
    test_ended_reason = ''
    escaped = False

    while not test_ended:
        # Generuj nową liczbę
        new_num = random.randint(0, 10) % 10
        sequence.append(new_num)
        current_index = len(sequence) - 1

        # Sprawdź czy to dopasowanie
        is_match = False
        if current_index >= nback_level:
            is_match = (sequence[current_index] == sequence[current_index - nback_level])

        # Wyświetl liczbę i pytanie
        number_stim.setText(str(new_num))
        question_stim.setText(f'Czy ta cyfra pojawiła się {nback_level} miejsc temu? (TAK/NIE)')
        question_stim.draw()
        number_stim.draw()
        win.flip()

        # Oczekuj odpowiedzi
        clock = core.Clock()
        pressed = False
        user_said_yes = False
        rt_sec = None

        while clock.getTime() < decision_time:
            keys = event.getKeys(keyList=['y', 'n', 't', 'Y', 'N', 'T', 'escape'], timeStamped=True)
            for k, t in keys:
                if k == 'escape':
                    escaped = True
                    break
                pressed = True
                rt_sec = t
                user_said_yes = (k.lower() in ['y', 't'])
                break
            if escaped or pressed:
                break
            core.wait(0.01)

        if escaped:
            break

        # Oceń poprawność
        was_correct = False
        if is_match and user_said_yes:
            was_correct = True
        elif not is_match and pressed and not user_said_yes:
            was_correct = True
        elif not is_match and not pressed:
            was_correct = True

        if was_correct:
            total_correct += 1
            feedback_stim.setText('✓ Poprawnie!')
            feedback_stim.setColor('green')
        else:
            feedback_stim.setColor('red')
            if is_match:
                feedback_stim.setText(f'✗ Błąd! Ta cyfra była taka sama jak {nback_level} miejsc temu.')
            else:
                feedback_stim.setText('✗ Błąd!')
            test_ended = True
            test_ended_reason = 'wrong_answer'

        # Sprawdź czy osiągnięto 50 poprawnych
        if total_correct >= TARGET_CORRECT:
            test_ended = True
            test_ended_reason = '50_correct'
            feedback_stim.setText('🎉 Gratulacje! Osiągnięto 50 poprawnych odpowiedzi!')
            feedback_stim.setColor('green')

        # Zapisz dane próby
        trials_data.append({
            'trial_number': current_index - 9,
            'current_number': str(new_num),
            'is_match': is_match,
            'user_response': 'TAK' if user_said_yes else ('NIE' if pressed else 'BRAK'),
            'was_correct': was_correct,
            'rt': rt_sec if pressed else None,
            'total_correct': total_correct,
        })

        # Feedback
        feedback_stim.draw()
        win.flip()
        core.wait(1.5)

    if escaped:
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, trials_data, total_correct, 0, len(trials_data), 0,
                           nback_level=nback_level, nback_name=nback_name,
                           difficulty_name=difficulty_name, decision_time=decision_time,
                           test_ended_reason='escape', score_text='')
        return

    win.close()

    # Wyniki
    if not NOUS_LAUNCHER:
        return

    wszystkie = sum(1 for t in trials_data if t.get('user_response') != 'BRAK')
    poprawne = total_correct
    bledne = sum(1 for t in trials_data if not t.get('was_correct'))
    rts = [t['rt'] for t in trials_data if t.get('rt') is not None and t['rt'] >= 0]
    avg_rt_ms = round((sum(rts) / len(rts)) * 1000) if rts else 0
    score_text = f'Poprawne: {poprawne} | Błędne: {bledne} | N-Back: {nback_name} | Poziom: {difficulty_name} | Śr. RT: {avg_rt_ms} ms'

    _write_results(SCRIPT_DIR, trials_data, poprawne, bledne, wszystkie, avg_rt_ms,
                   nback_level=nback_level, nback_name=nback_name,
                   difficulty_name=difficulty_name, decision_time=decision_time,
                   test_ended_reason=test_ended_reason, score_text=score_text)


if __name__ == '__main__':
    main()