# -*- coding: utf-8 -*-
"""
Poppel – wersja PsychoPy (HPM / Nous).
Dwa cele na górze; obiekty przesuwają się w dwóch rzędach na dole.
Zadanie: klikać w obiekty pasujące do celów. W połowie (30 s) cele się zmieniają. Próba 60 s.
Czas reakcji nie jest zbierany.
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
IMAGE_PATH = RESOURCES

# Parametry układu (jak w JS)
N_PER_ROW = 6
SIZE_TOP = 0.22
SIZE_BOTTOM = 0.14
TOP_Y = 0.32
ROW1_Y = -0.10
ROW2_Y = -0.30
GAP = 0.07
SPEED = 0.25
TRIAL_DURATION = 60.0
TARGET_CHANGE_TIME = 30.0
APPEAR_X = 0.0

POOL = [
    'gwBLA.png', 'gwBLU.png', 'gwGRE.png', 'gwRED.png', 'gwYEL.png',
    'koBLA.png', 'koBLU.png', 'koGRE.png', 'koRED.png', 'koYEL.png',
    'kwBLA.png', 'kwBLU.png', 'kwGRE.png', 'kwRED.png', 'kwYEL.png',
    'pkBLA.png', 'pkBLU.png', 'pkGRE.png', 'pkRED.png', 'pkYEL.png',
    'trBLA.png', 'trBLU.png', 'trGRE.png', 'trRED.png', 'trYEL.png',
]


def safe_sample(arr, n):
    a = arr.copy()
    out = []
    while len(out) < n and a:
        idx = random.randrange(len(a))
        out.append(a.pop(idx))
    return out


def make_sequence(pool, n):
    return [random.choice(pool) for _ in range(n)]


def main():
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(0, 0, 0),
        allowGUI=False,
    )
    mouse = event.Mouse(win=win)
    trial_clock = core.Clock()
    frame_clock = core.Clock()

    X_STEP = SIZE_BOTTOM + GAP
    X_START = -((N_PER_ROW - 1) / 2) * X_STEP
    WRAP_DISTANCE = N_PER_ROW * X_STEP
    items_per_sec = SPEED / X_STEP
    items_needed = int(items_per_sec * 35) + (N_PER_ROW * 2)

    # Losowanie celów i sekwencji dolnej
    targets = safe_sample(POOL, 2)
    base_seq = make_sequence(POOL, items_needed * 2)
    base_seq.insert(4, targets[0])
    base_seq.insert(8, targets[1])
    bottom_sequence = base_seq.copy()

    # Stimuly górne (cele)
    top_stims = []
    for i, name in enumerate(targets):
        x_pos = -0.25 if i == 0 else 0.25
        stim = visual.ImageStim(
            win,
            image=str(IMAGE_PATH / name),
            pos=(x_pos, TOP_Y),
            size=(SIZE_TOP, SIZE_TOP),
        )
        top_stims.append({'stim': stim, 'imgName': name})

    # Stimuly dolne (start poza ekranem)
    bottom_stims = []
    prev_x = []
    for idx in range(N_PER_ROW * 2):
        col = idx % N_PER_ROW
        row = idx // N_PER_ROW
        standard_x = X_START + col * X_STEP
        x = standard_x - 1.8
        y = ROW1_Y if row == 0 else ROW2_Y
        img_file = bottom_sequence.pop(0)
        stim = visual.ImageStim(
            win,
            image=str(IMAGE_PATH / img_file),
            pos=(x, y),
            size=(SIZE_BOTTOM, SIZE_BOTTOM),
        )
        stim.opacity = 1.0
        bottom_stims.append({
            'stim': stim,
            'imgName': img_file,
            'clicked': False,
            'counted': False,
            'x': x,
            'y': y,
        })
        prev_x.append(x)

    # Liczniki
    total_presses = 0
    target_presses = 0
    target_appearances = 0
    clicked_records = []
    change_done = False
    prev_pressed = mouse.getPressed()
    hit_box_half = (SIZE_BOTTOM * 1.3) / 2

    # Tekst licznika
    counter_text = visual.TextStim(
        win, text='Poprawne: 0',
        pos=(0.6, 0.45), height=0.035, color='white',
    )

    escaped = False
    frame_clock.reset()
    while trial_clock.getTime() < TRIAL_DURATION:
        if event.getKeys(keyList=['escape']):
            escaped = True
            break

        elapsed = trial_clock.getTime()
        dt = frame_clock.getTime()
        frame_clock.reset()
        if dt <= 0 or dt > 0.5:
            dt = 1.0 / 60.0

        # Kliknięcie
        pressed = mouse.getPressed()
        is_new_click = pressed[0] and not prev_pressed[0]
        prev_pressed = pressed

        if is_new_click:
            total_presses += 1
            click_pos = mouse.getPos()
            candidates = []
            for b in bottom_stims:
                if b['clicked']:
                    continue
                dx = abs(click_pos[0] - b['x'])
                dy = abs(click_pos[1] - b['y'])
                if dx < hit_box_half and dy < hit_box_half:
                    dist_sq = dx * dx + dy * dy
                    candidates.append((dist_sq, b))
            if candidates:
                candidates.sort(key=lambda c: c[0])
                selected = candidates[0][1]
                is_correct = selected['imgName'] in targets
                if is_correct:
                    target_presses += 1
                selected['stim'].opacity = 0.0 if is_correct else 0.2
                selected['clicked'] = True
                clicked_records.append({
                    'time': elapsed,
                    'stim_image': selected['imgName'],
                    'is_correct': 1 if is_correct else 0,
                    'x': click_pos[0],
                    'y': click_pos[1],
                })
                counter_text.text = f'Poprawne: {target_presses}'

        # Ruch dolnych figur
        for i, b in enumerate(bottom_stims):
            new_x = b['x'] + SPEED * dt
            if prev_x[i] < APPEAR_X <= new_x and not b['counted']:
                if b['imgName'] in targets:
                    target_appearances += 1
                b['counted'] = True

            if new_x > X_START + WRAP_DISTANCE:
                new_x -= WRAP_DISTANCE
                next_img = bottom_sequence.pop(0) if bottom_sequence else random.choice(POOL)
                b['stim'].setImage(str(IMAGE_PATH / next_img))
                b['imgName'] = next_img
                b['clicked'] = False
                b['counted'] = False
                b['stim'].opacity = 1.0

            b['x'] = new_x
            prev_x[i] = new_x
            b['stim'].pos = (new_x, b['y'])
            if b['stim'].opacity > 0:
                b['stim'].draw()

        # Zmiana celów w połowie
        if not change_done and elapsed >= TARGET_CHANGE_TIME:
            targets = safe_sample(POOL, 2)
            for j, t in enumerate(top_stims):
                t['stim'].setImage(str(IMAGE_PATH / targets[j]))
                t['imgName'] = targets[j]
            injection = make_sequence(targets, 4)
            bottom_sequence = injection + bottom_sequence
            change_done = True

        if len(bottom_sequence) < 20:
            bottom_sequence.extend(make_sequence(POOL, 20))

        for t in top_stims:
            t['stim'].draw()
        counter_text.draw()
        win.flip()

    win.close()

    # Wyniki (zgodne z JS)
    bledne_trafienia = max(0, total_presses - target_presses)
    poprawne_trafienia = target_presses
    obiekty_do_klikniecia = target_appearances
    accuracy = round((poprawne_trafienia / total_presses) * 100) if total_presses else 0
    detection_rate = round((poprawne_trafienia / obiekty_do_klikniecia) * 100) if obiekty_do_klikniecia else 0

    results = {
        'testId': 'Poppelv2',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne_trafienia,
        'ilosc_blednych_nacisniec': bledne_trafienia,
        'ogolna_ilosc_nacisniec': total_presses,
        'ilosc_obiektow_do_klikniecia': obiekty_do_klikniecia,
        'score': f'Poprawne: {poprawne_trafienia} | Błędne: {bledne_trafienia} | Obiektów do kliknięcia: {obiekty_do_klikniecia} | Skuteczność: {accuracy}%',
        'statystyki': {
            'poprawne': poprawne_trafienia,
            'bledne': bledne_trafienia,
            'wszystkie_kliki': total_presses,
            'obiekty_do_klikniecia': obiekty_do_klikniecia,
            'skutecznosc_klikniec': accuracy,
            'skutecznosc_wykrywania': detection_rate,
        },
        'wyniki_szczegolowe': clicked_records,
    }

    if NOUS_LAUNCHER:
        out_path = SCRIPT_DIR / 'results.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
