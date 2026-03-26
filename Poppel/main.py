# -*- coding: utf-8 -*-
"""
Poppel – wersja PsychoPy (HPM / Nous).
Dwa cele na górze; obiekty przesuwają się w dwóch rzędach na dole.
Zadanie: klikać w obiekty pasujące do celów.
Cele zmieniają się co 20 s. Czas reakcji nie jest zbierany.
3 poziomy trudności, 3 opcje czasu trwania.
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

# --- Stałe ---
ALL_SHAPES = ['kw', 'ko', 'tr', 'gw', 'pk']
ALL_COLORS = ['RED', 'BLU', 'GRE', 'YEL', 'BLA']
BASE_SPEED = 0.25

DIFFICULTY_CONFIG = {
    'easy':   {'label': 'Łatwy',  'shapes': 3, 'colors': 3, 'speed_mult': 1.0},
    'medium': {'label': 'Średni', 'shapes': 4, 'colors': 4, 'speed_mult': 1.2},
    'hard':   {'label': 'Trudny', 'shapes': 5, 'colors': 5, 'speed_mult': 1.35},
}

DURATION_OPTIONS = [40, 120, 300]
TARGET_CHANGE_INTERVAL = 20.0  # seconds
TARGET_RATIO = 0.4  # 40% minimum good figures
N_TARGETS = 2
APPEAR_X = -0.7  # count appearance when figure enters visible area

# Layout
N_PER_ROW = 6
SIZE_TOP = 0.22
SIZE_BOTTOM = 0.14
TOP_Y = 0.32
ROW1_Y = -0.10
ROW2_Y = -0.30
GAP = 0.07
APPEAR_X = 0.0


# --- Helpers ---
def build_pool(n_shapes, n_colors):
    pool = []
    for s in range(n_shapes):
        for c in range(n_colors):
            pool.append(ALL_SHAPES[s] + ALL_COLORS[c] + '.png')
    return pool


def safe_sample(arr, n):
    a = arr.copy()
    out = []
    while len(out) < n and a:
        idx = random.randrange(len(a))
        out.append(a.pop(idx))
    return out


def make_sequence_with_target_ratio(pool, targets, n):
    """Build a sequence of n items with at least TARGET_RATIO of them being targets."""
    seq = []
    batch_size = 10
    target_count = int(batch_size * TARGET_RATIO)  # 4
    random_count = batch_size - target_count        # 6
    while len(seq) < n:
        batch = []
        for _ in range(target_count):
            batch.append(random.choice(targets))
        for _ in range(random_count):
            batch.append(random.choice(pool))
        random.shuffle(batch)
        seq.extend(batch)
    return seq[:n]


def _write_results(script_dir, clicked_records, poprawne, bledne, wszystkie,
                   obiekty, accuracy, detection_rate, diff_label, duration, pominiete=0):
    results = {
        'testId': 'Poppelv2',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': poprawne,
        'ilosc_blednych_nacisniec': bledne,
        'ogolna_ilosc_nacisniec': wszystkie,
        'ilosc_obiektow_do_klikniecia': obiekty,
        'pominiete_cele': pominiete,
        'poziom_trudnosci': diff_label,
        'czas_trwania': duration,
        'score': (f'Poziom: {diff_label} | Czas: {duration}s | '
                  f'Poprawne: {poprawne} | Błędne: {bledne} | '
                  f'Pominięte: {pominiete} | '
                  f'Obiektów: {obiekty} | Skuteczność: {accuracy}%'),
        'statystyki': {
            'poprawne': poprawne,
            'bledne': bledne,
            'wszystkie_kliki': wszystkie,
            'obiekty_do_klikniecia': obiekty,
            'pominiete_cele': pominiete,
            'skutecznosc_klikniec': accuracy,
            'skutecznosc_wykrywania': detection_rate,
            'poziom_trudnosci': diff_label,
            'czas_trwania_sek': duration,
        },
        'wyniki_szczegolowe': clicked_records,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(0, 0, 0),
    )
    win.mouseVisible = True
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    # ================= WELCOME SCREEN =================
    instr_text = (
        "Za chwilę na ekranie zobaczysz serię różnych figur. Za pomocą MYSZY, klikaj na te figury, "
        "których kształt i kolor odpowiada wzorcowi przedstawionemu u góry ekranu. "
        "Wzorzec, co jakiś czas będzie się zmieniał. Zawsze należy klikać na te figury, "
        "których kształt i kolor odpowiada aktualnemu wzorcowi. "
        "Staraj się reagować najszybciej jak potrafisz. Aby rozpocząć zadanie, wciśnij SPACJĘ."
    )
    instr = visual.TextStim(
        win,
        text=instr_text,
        color='white', height=0.045, wrapWidth=1.6, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'return', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 'nieznany', 0)
        return

    # ================= DIFFICULTY SELECTION =================
    diff_text = visual.TextStim(
        win,
        text=('Wybierz poziom trudności:\n\n'
              '1 – Łatwy (3 figury, 3 kolory)\n'
              '2 – Średni (4 figury, 4 kolory, +20% prędkości)\n'
              '3 – Trudny (5 figur, 5 kolorów, +35% prędkości)\n\n'
              'Naciśnij 1, 2 lub 3.'),
        color='white', height=0.045, wrapWidth=1.6, alignText='center',
    )
    diff_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', 'num_1', 'num_2', 'num_3', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, 'nieznany', 0)
        return

    diff_map = {'1': 'easy', '2': 'medium', '3': 'hard',
                'num_1': 'easy', 'num_2': 'medium', 'num_3': 'hard'}
    chosen_difficulty = diff_map.get(keyname, 'easy')
    cfg = DIFFICULTY_CONFIG[chosen_difficulty]
    diff_label = cfg['label']
    active_pool = build_pool(cfg['shapes'], cfg['colors'])
    active_speed = BASE_SPEED * cfg['speed_mult']

    # ================= DURATION SELECTION =================
    dur_text = visual.TextStim(
        win,
        text=('Wybierz czas trwania testu:\n\n'
              '1 – 40 sekund\n'
              '2 – 120 sekund\n'
              '3 – 300 sekund\n\n'
              'Naciśnij 1, 2 lub 3.'),
        color='white', height=0.045, wrapWidth=1.6, alignText='center',
    )
    dur_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', 'num_1', 'num_2', 'num_3', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 0, 0, diff_label, 0)
        return

    dur_map = {'1': DURATION_OPTIONS[0], '2': DURATION_OPTIONS[1], '3': DURATION_OPTIONS[2],
               'num_1': DURATION_OPTIONS[0], 'num_2': DURATION_OPTIONS[1], 'num_3': DURATION_OPTIONS[2]}
    chosen_duration = dur_map.get(keyname, DURATION_OPTIONS[0])

    # ================= SETUP =================

    X_STEP = SIZE_BOTTOM + GAP
    X_START = -((N_PER_ROW - 1) / 2) * X_STEP
    WRAP_DISTANCE = N_PER_ROW * X_STEP

    # Initial targets
    targets = safe_sample(active_pool, N_TARGETS)

    # Top stims
    top_stims = []
    for i, name in enumerate(targets):
        x_pos = -0.25 if i == 0 else 0.25
        stim = visual.ImageStim(
            win,
            image=str(RESOURCES / name),
            pos=(x_pos, TOP_Y),
            size=(SIZE_TOP, SIZE_TOP),
        )
        top_stims.append({'stim': stim, 'imgName': name})

    # Build initial sequence with 40% target ratio
    items_per_sec = active_speed / X_STEP
    items_needed = int(items_per_sec * (chosen_duration + 10)) + (N_PER_ROW * 2)
    bottom_sequence = make_sequence_with_target_ratio(active_pool, targets, items_needed)

    # Bottom stims
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
            image=str(RESOURCES / img_file),
            pos=(x, y),
            size=(SIZE_BOTTOM, SIZE_BOTTOM),
        )
        stim.opacity = 1.0
        bottom_stims.append({
            'stim': stim,
            'imgName': img_file,
            'clicked': False,
            'counted': False,
            'drained': False,
            'x': x,
            'y': y,
        })
        prev_x.append(x)

    # Counters
    total_presses = 0
    target_presses = 0
    target_appearances = 0
    missed_targets = 0
    clicked_records = []
    last_change_time = 0.0
    target_change_flash_time = -1.0
    game_phase = 'RUNNING'  # 'RUNNING' | 'DRAINING'
    drain_mode = 'CHANGE'   # 'CHANGE' | 'END'
    drained_count = 0
    prev_pressed = mouse.getPressed()
    hit_box_half = (SIZE_BOTTOM * 1.3) / 2

    counter_text = visual.TextStim(
        win, text='Poprawne: 0',
        pos=(0.6, 0.45), height=0.035, color='white',
    )

    # Highlight rectangle for target change flash
    highlight_rect = visual.Rect(
        win,
        width=1.2, height=SIZE_TOP + 0.08,
        pos=(0, TOP_Y),
        lineColor='yellow',
        lineWidth=4,
        fillColor=None,
    )
    highlight_rect.opacity = 0.0

    trial_clock = core.Clock()
    frame_clock = core.Clock()
    escaped = False

    # ================= MAIN LOOP =================
    frame_clock.reset()
    while True:
        if event.getKeys(keyList=['escape']):
            escaped = True
            break

        elapsed = trial_clock.getTime()
        dt = frame_clock.getTime()
        frame_clock.reset()
        if dt <= 0 or dt > 0.5:
            dt = 1.0 / 60.0

        # --- Click handling ---
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
                    'x': float(click_pos[0]),
                    'y': float(click_pos[1]),
                })
                counter_text.text = f'Poprawne: {target_presses}'

        # --- Move bottom figures ---
        for i, b in enumerate(bottom_stims):
            new_x = b['x'] + active_speed * dt

            if prev_x[i] < APPEAR_X <= new_x and not b['counted']:
                if b['imgName'] in targets:
                    target_appearances += 1
                b['counted'] = True

            if new_x > X_START + WRAP_DISTANCE:
                # Track missed targets (only if not already drained)
                if not b['drained'] and not b['clicked'] and b['counted'] and b['imgName'] in targets:
                    missed_targets += 1

                if game_phase == 'DRAINING':
                    if not b['drained']:
                        b['stim'].opacity = 0.0
                        b['imgName'] = '__blank__'
                        b['clicked'] = True
                        b['counted'] = True
                        b['drained'] = True
                        drained_count += 1
                    # Park far off-screen to prevent re-wrap during drain
                    new_x = -10.0
                else:
                    new_x -= WRAP_DISTANCE
                    next_img = bottom_sequence.pop(0) if bottom_sequence else random.choice(active_pool)
                    b['stim'].setImage(str(RESOURCES / next_img))
                    b['imgName'] = next_img
                    b['clicked'] = False
                    b['counted'] = False
                    b['drained'] = False
                    b['stim'].opacity = 1.0

            b['x'] = new_x
            prev_x[i] = new_x
            b['stim'].pos = (new_x, b['y'])
            if b['stim'].opacity > 0:
                b['stim'].draw()

        # --- Check drain completion ---
        if game_phase == 'DRAINING' and drained_count >= len(bottom_stims):
            if drain_mode == 'END':
                break  # screen is empty – exit cleanly
            else:
                targets = safe_sample(active_pool, N_TARGETS)
                for j, t_s in enumerate(top_stims):
                    t_s['stim'].setImage(str(RESOURCES / targets[j]))
                    t_s['imgName'] = targets[j]
                target_change_flash_time = elapsed
                last_change_time = elapsed

                # Rebuild sequence for remaining duration
                remaining = max(chosen_duration - elapsed + 10, 60)
                items = int(active_speed / X_STEP * remaining) + N_PER_ROW * 2
                bottom_sequence = make_sequence_with_target_ratio(active_pool, targets, max(items, 60))

                # Re-spawn all stims from off-screen left
                for i, b in enumerate(bottom_stims):
                    col = i % N_PER_ROW
                    row = i // N_PER_ROW
                    standard_x = X_START + col * X_STEP
                    spawn_x = standard_x - 1.8
                    y = ROW1_Y if row == 0 else ROW2_Y
                    next_img = bottom_sequence.pop(0)
                    b['stim'].setImage(str(RESOURCES / next_img))
                    b['imgName'] = next_img
                    b['clicked'] = False
                    b['counted'] = False
                    b['drained'] = False
                    b['stim'].opacity = 1.0
                    b['stim'].pos = (spawn_x, y)
                    b['x'] = spawn_x
                    prev_x[i] = spawn_x

                drained_count = 0
                game_phase = 'RUNNING'

        # --- Enter DRAINING when target change time arrives ---
        if game_phase == 'RUNNING' and elapsed - last_change_time >= TARGET_CHANGE_INTERVAL and elapsed > 1:
            game_phase = 'DRAINING'
            drain_mode = 'CHANGE'
            drained_count = 0
            for b in bottom_stims:
                b['drained'] = False
            bottom_sequence = []  # clear – nothing new spawns during drain

        # --- End-of-test drain ---
        if elapsed >= chosen_duration and game_phase == 'RUNNING':
            game_phase = 'DRAINING'
            drain_mode = 'END'
            drained_count = 0
            for b in bottom_stims:
                b['drained'] = False
            bottom_sequence = []

        # Replenish (only during RUNNING phase)
        if game_phase == 'RUNNING' and len(bottom_sequence) < 30:
            bottom_sequence.extend(
                make_sequence_with_target_ratio(active_pool, targets, 40)
            )

        for t_s in top_stims:
            t_s['stim'].draw()
        counter_text.draw()

        # Draw target change flash (yellow border for 1.5s)
        if target_change_flash_time >= 0 and (elapsed - target_change_flash_time) < 1.5:
            flash_opacity = max(0.0, 1.0 - ((elapsed - target_change_flash_time) / 1.5))
            highlight_rect.opacity = flash_opacity
            highlight_rect.draw()
        else:
            highlight_rect.opacity = 0.0

        win.flip()

    win.close()

    # ================= RESULTS =================
    bledne_trafienia = max(0, total_presses - target_presses)
    poprawne_trafienia = target_presses
    obiekty_do_klikniecia = target_appearances
    accuracy = round((poprawne_trafienia / total_presses) * 100) if total_presses else 0
    detection_rate = round((poprawne_trafienia / obiekty_do_klikniecia) * 100) if obiekty_do_klikniecia else 0


    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, clicked_records, poprawne_trafienia,
                       bledne_trafienia, total_presses, obiekty_do_klikniecia,
                       accuracy, detection_rate, diff_label, chosen_duration,
                       missed_targets)


if __name__ == '__main__':
    main()
