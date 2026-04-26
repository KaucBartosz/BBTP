# -*- coding: utf-8 -*-
"""
GoNoGo Cyfry – wersja PsychoPy (HPM).
Cyfry nieparzyste (1, 3, 7, 9) = GO (naciśnij spację), 
parzyste (2, 4, 6, 8) = NOGO (czekaj).
Integracja z Nous: NOUS_LAUNCHER, results.json, ESC bez zapisu.
"""
import os
import json
import random
import math
from datetime import datetime
from pathlib import Path
from psychopy import visual, core, event

NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent

def _write_results(script_dir, trials_data, hits, fa, go_trials, nogo_trials, avg_hit_rt_ms, avg_fa_rt_ms, d_prime, accuracy, score_text=''):
    wszystkie_nacisniecia = sum(1 for t in trials_data if t.get('pressed') and not t.get('anticipatory', False))
    results = {
        'testId': 'GoNoGoCyfry',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': hits,
        'ilosc_blednych_nacisniec': fa,
        'ogolna_ilosc_nacisniec': wszystkie_nacisniecia,
        'sredni_czas_reakcji': avg_hit_rt_ms,
        'poziom_trudnosci': "Standard",
        'score': score_text,
        'statystyki': {
            'go_trials': go_trials,
            'nogo_trials': nogo_trials,
            'hits': hits,
            'misses': go_trials - hits,
            'false_alarms': fa,
            'correct_rejections': nogo_trials - fa,
            'd_prime': float(d_prime),
            'avg_hit_rt_ms': avg_hit_rt_ms,
            'avg_fa_rt_ms': avg_fa_rt_ms,
            'accuracy_percent': accuracy
        },
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def generate_block(num_go, num_nogo, max_consecutive_nogo=3):
    while True:
        seq = []
        go, nogo = num_go, num_nogo
        for _ in range(num_go + num_nogo):
            if go == 0:
                seq.append('nogo')
                nogo -= 1
            elif nogo == 0:
                seq.append('go')
                go -= 1
            else:
                if random.random() < go / (go + nogo):
                    seq.append('go')
                    go -= 1
                else:
                    seq.append('nogo')
                    nogo -= 1
        
        # Check max consecutive nogo
        max_cons = 0
        current_cons = 0
        for cond in seq:
            if cond == 'nogo':
                current_cons += 1
                if current_cons > max_cons:
                    max_cons = current_cons
            else:
                current_cons = 0
        if max_cons <= max_consecutive_nogo:
            break

    go_stims = [1, 3, 7, 9]
    nogo_stims = [2, 4, 6, 8]
    block = []
    for cond in seq:
        if cond == 'go':
            digit = str(random.choice(go_stims))
        else:
            digit = str(random.choice(nogo_stims))
        soa = random.uniform(1.3, 1.6)
        block.append({'condition': cond, 'digit': digit, 'soa': soa})
    return block

def pnorm(p):
    # Approximation of inverse normal CDF
    p = min(max(p, 0.00001), 0.99999)
    t = math.sqrt(-2.0 * math.log(p if p < 0.5 else 1.0 - p))
    num = 2.515517 + 0.802853 * t + 0.010328 * t * t
    den = 1.0 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t
    z = t - num / den
    return -z if p < 0.5 else z

def main():
    win = visual.Window(fullscr=True, units='height', color='black', allowGUI=False)
    mouse = event.Mouse(win=win)
    mouse.setVisible(False)

    # --- Instrukcja ---
    instr = visual.TextStim(
        win,
        text='Zadanie Go/No-Go\n\nNaciśnij SPACJĘ, gdy zobaczysz cyfrę NIEPARZYSTĄ (1, 3, 7, 9).\nNIE naciskaj niczego, gdy zobaczysz cyfrę PARZYSTĄ (2, 4, 6, 8).\n\nNaciśnij SPACJĘ, aby rozpocząć.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys and keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0.0, 0, score_text='')
        return

    # --- Wybór trybu ---
    mode_text = visual.TextStim(
        win,
        text='Wybierz tryb:\n\n1 - Badanie\n2 - Trening + Badanie\n\nNaciśnij 1 lub 2.',
        color='white', height=0.05, wrapWidth=1.8, alignText='center',
    )
    mode_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', 'escape'])
    if keys and keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0.0, 0, score_text='')
        return
    
    is_training_mode = (keys[0] == '2') if keys else False

    trial_text = visual.TextStim(win, text='', color='white', height=0.15, alignText='center')
    feedback_text = visual.TextStim(win, text='', color='white', height=0.10, alignText='center')
    break_text = visual.TextStim(win, text='Przerwa. Naciśnij SPACJĘ, aby kontynuować.', color='white', height=0.05, alignText='center')

    def run_trial(trial, is_training):
        digit = trial['digit']
        condition = trial['condition']
        soa = trial['soa']
        
        trial_text.setText(digit)
        
        clock = core.Clock()
        event.clearEvents()
        
        pressed = False
        rt_sec = None
        
        # Bodziec widoczny 500ms
        while clock.getTime() < 0.5:
            trial_text.draw()
            win.flip()
            keys = event.getKeys(keyList=['space', 'escape'], timeStamped=clock)
            for k, t in keys:
                if k == 'escape':
                    return 'escape', None
                if k == 'space' and not pressed:
                    pressed = True
                    rt_sec = t
        
        # Okno reakcji do 1000ms
        while clock.getTime() < 1.0:
            win.flip()
            if not pressed:
                keys = event.getKeys(keyList=['space', 'escape'], timeStamped=clock)
                for k, t in keys:
                    if k == 'escape':
                        return 'escape', None
                    if k == 'space' and not pressed:
                        pressed = True
                        rt_sec = t

        # Czekaj resztę SOA (blank)
        while clock.getTime() < soa:
            win.flip()

        anticipatory = pressed and rt_sec < 0.150
        valid_response = pressed and not anticipatory
        
        is_go = (condition == 'go')
        if is_go:
            was_correct = valid_response
        else:
            was_correct = not valid_response
            
        trial_data = {
            'condition': condition,
            'digit': digit,
            'pressed': pressed,
            'rt': rt_sec,
            'anticipatory': anticipatory,
            'was_correct': was_correct
        }

        if is_training:
            if anticipatory:
                feedback_text.setText('Zbyt szybko!')
                feedback_text.setColor('orange')
            elif was_correct:
                feedback_text.setText('Dobrze!')
                feedback_text.setColor('green')
            else:
                feedback_text.setText('Źle!')
                feedback_text.setColor('red')
                
            f_clock = core.Clock()
            while f_clock.getTime() < 0.5:
                feedback_text.draw()
                win.flip()

        return 'ok', trial_data

    # --- Pętle testu ---
    trials_data = []
    
    if is_training_mode:
        training_trials = generate_block(10, 10, 3)
        for t in training_trials:
            status, _ = run_trial(t, is_training=True)
            if status == 'escape':
                win.close()
                if NOUS_LAUNCHER:
                    _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0.0, 0, score_text='')
                return

    blocks = 4 if not NOUS_TRAINING else 1
    trials_per_block = 50 if not NOUS_TRAINING else 10

    for b in range(blocks):
        if NOUS_TRAINING:
            test_trials = generate_block(8, 2, 3)
        else:
            test_trials = generate_block(40, 10, 3)
            
        for t in test_trials:
            status, trial_res = run_trial(t, is_training=False)
            if status == 'escape':
                win.close()
                if NOUS_LAUNCHER:
                    _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0.0, 0, score_text='')
                return
            trials_data.append(trial_res)
            
        if b < blocks - 1:
            break_text.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'escape'])
            if keys and keys[0] == 'escape':
                win.close()
                if NOUS_LAUNCHER:
                    _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 0.0, 0, score_text='')
                return

    win.close()

    if not NOUS_LAUNCHER:
        return

    # --- Wyniki ---
    go_trials = 0
    nogo_trials = 0
    hits = 0
    misses = 0
    cr = 0
    fa = 0
    sum_hit_rt = 0
    count_hit_rt = 0
    sum_fa_rt = 0
    count_fa_rt = 0

    for t in trials_data:
        if t.get('anticipatory'):
            continue
        if t['condition'] == 'go':
            go_trials += 1
            if t['pressed']:
                hits += 1
                sum_hit_rt += t['rt']
                count_hit_rt += 1
            else:
                misses += 1
        else:
            nogo_trials += 1
            if t['pressed']:
                fa += 1
                sum_fa_rt += t['rt']
                count_fa_rt += 1
            else:
                cr += 1

    hr = count_hit_rt / max(go_trials, 1)
    far = count_fa_rt / max(nogo_trials, 1)

    # d-prime adjustments
    hr_adj = hr
    far_adj = far
    if hr_adj == 1: hr_adj = 1 - 1 / (2 * max(go_trials, 1))
    if hr_adj == 0: hr_adj = 1 / (2 * max(go_trials, 1))
    if far_adj == 1: far_adj = 1 - 1 / (2 * max(nogo_trials, 1))
    if far_adj == 0: far_adj = 1 / (2 * max(nogo_trials, 1))

    d_prime = f"{(pnorm(hr_adj) - pnorm(far_adj)):.2f}"
    
    avg_hit_rt_ms = round((sum_hit_rt / count_hit_rt) * 1000) if count_hit_rt > 0 else 0
    avg_fa_rt_ms = round((sum_fa_rt / count_fa_rt) * 1000) if count_fa_rt > 0 else 0

    total_correct = hits + cr
    total_trials = go_trials + nogo_trials
    accuracy = round((total_correct / max(total_trials, 1)) * 100)

    score_text = f"Hits: {hits}/{go_trials} | FA: {fa}/{nogo_trials} | Skut: {accuracy}% | d': {d_prime} | RT Hits: {avg_hit_rt_ms} ms | RT FA: {avg_fa_rt_ms} ms"

    _write_results(SCRIPT_DIR, trials_data, hits, fa, go_trials, nogo_trials, avg_hit_rt_ms, avg_fa_rt_ms, d_prime, accuracy, score_text=score_text)


if __name__ == '__main__':
    main()
