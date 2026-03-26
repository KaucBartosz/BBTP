#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PingPong – Test Koordynacji (PsychoPy / HPM).
Dwie paletki (W/S i strzałki) odbijają piłkę.
Integracja z Nous: NOUS_LAUNCHER, results.json, ESC bez zapisu.
"""

import os
import json
import math
import random
from datetime import datetime
from pathlib import Path
from psychopy import visual, core, event
from psychopy.hardware import keyboard

# ==================== KONFIGURACJA NOUS ====================

NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent

# ==================== KONFIGURACJA GRY ====================

TEST_DURATION = 120 if not NOUS_TRAINING else 60  # 2 minuty (1 minuta w trybie treningowym)

DIFFICULTY_SETTINGS = {
    'Easy':     {'base_speed': 0.005,  'paddle_height': 0.25},
    'Normal':   {'base_speed': 0.0096, 'paddle_height': 0.20},
    'Hard':     {'base_speed': 0.0096, 'paddle_height': 0.18},
    'Survival': {'base_speed': 0.0096, 'paddle_height': 0.18},
}
DIFFICULTY_NAMES = {
    '1': ('Easy',     'Łatwy'),
    '2': ('Normal',   'Normalny'),
    '3': ('Hard',     'Trudny'),
    '4': ('Survival', 'Przetrwanie'),
}

# Tryb Trudny – progresja prędkości
MAX_SPEED_MULTIPLIER   = 4
SPEED_INCREASE_INTERVAL = 1.5  # sekund między wzrostami
SPEED_INCREASE_AMOUNT   = 0.2


# ==================== ZAPIS WYNIKÓW ====================

def _write_results(script_dir, game_state, difficulty_label, duration_s, paddle_hits, survival_time=None):
    wall_hits = game_state['total_wall_hits']
    
    if survival_time is not None:
        score_text = (
            f'Poziom: {difficulty_label} | '
            f'Czas: {round(survival_time, 1)}s | '
            f'Odbicia paletką: {paddle_hits}'
        )
        total = paddle_hits
        czas_trwania_str = f"{round(survival_time, 1)}s"
    else:
        total = paddle_hits + wall_hits
        score_text = (
            f'Poziom: {difficulty_label} | '
            f'Odbicia paletką: {paddle_hits} | '
            f'Przepuszczone: {wall_hits} | '
            f'Czas: {round(duration_s)}s'
        )
        czas_trwania_str = f"{round(duration_s)}s"

    results = {
        'testId':                    'PingPong',
        'subjectId':                 f'{random.randint(0, 999999):06d}',
        'timestamp':                 datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': paddle_hits,
        'ilosc_blednych_nacisniec':   0 if survival_time is not None else wall_hits,
        'ogolna_ilosc_nacisniec':     total,
        'poziom_trudnosci':           difficulty_label,
        'czas_trwania_sek':           round(survival_time) if survival_time is not None else round(duration_s),
        'score':                      score_text,
        'statystyki': {
            'lewa_sciana':       game_state['left_wall_hits'],
            'prawa_sciana':      game_state['right_wall_hits'],
            'odbicia_paletka':   paddle_hits,
            'max_predkosc_x':    round(game_state['max_speed_reached'], 2),
            'zmiany_predkosci':  game_state['speed_changes'],
        },
    }
    
    if survival_time is not None:
        results['statystyki']['czas_przezycia_sek'] = round(survival_time)
        
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


# ==================== GŁÓWNA FUNKCJA ====================

def main():
    win = visual.Window(
        size=[1920, 1080],
        fullscr=True,
        color=[-1, -1, -1],
        units='height',
        allowGUI=False,
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(False)

    # --- Ekran powitalny ---
    welcome_text = visual.TextStim(
        win,
        text=(
            'PING PONG – Test Koordynacji\n\n'
            'Twoim zadaniem jest odbijanie piłki za pomocą dwóch paletek.\n\n'
            'LEWA PALETKA:  klawisze W (góra) i S (dół)\n'
            'PRAWA PALETKA: strzałki góra i dół lub klawisze O i L\n\n'
            f'Test trwa {TEST_DURATION // 60} minutę/y (lub bez limitu w trybie Przetrwania). Odbijaj piłkę jak najdłużej!\n\n'
            'Naciśnij SPACJĘ, aby wybrać poziom trudności\n'
            'ESC – wyjście bez zapisu'
        ),
        font='Arial', height=0.04, color='white', wrapWidth=1.5,
    )
    welcome_text.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys and keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, {
                'left_wall_hits': 0, 'right_wall_hits': 0,
                'total_wall_hits': 0, 'speed_changes': 0, 'max_speed_reached': 1.0,
            }, 'Brak', 0, 0)
        return

    # --- Wybór poziomu trudności ---
    difficulty_text = visual.TextStim(
        win,
        text=(
            'WYBIERZ POZIOM TRUDNOŚCI\n\n'
            '1 – ŁATWY       (wolniejsza piłka, większe paletki)\n'
            '2 – NORMALNY    (standardowa prędkość)\n'
            '3 – TRUDNY      (prędkość rośnie z czasem)\n'
            '4 – PRZETRWANIE (jeden błąd = koniec, bez limitu czasu)\n\n'
            'Naciśnij 1, 2, 3 lub 4'
        ),
        font='Arial', height=0.04, color='white', wrapWidth=1.5,
    )
    difficulty_text.draw()
    win.flip()

    diff_keys = event.waitKeys(keyList=['1', '2', '3', '4', 'escape'])
    if diff_keys and diff_keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, {
                'left_wall_hits': 0, 'right_wall_hits': 0,
                'total_wall_hits': 0, 'speed_changes': 0, 'max_speed_reached': 1.0,
            }, 'Brak', 0, 0)
        return

    diff_key = diff_keys[0] if diff_keys else '2'
    difficulty, difficulty_label = DIFFICULTY_NAMES.get(diff_key, ('Normal', 'Normalny'))
    settings     = DIFFICULTY_SETTINGS[difficulty]
    base_speed   = settings['base_speed']
    paddle_height = settings['paddle_height']

    # --- Stan gry ---
    game_state = {
        'left_wall_hits':  0,
        'right_wall_hits': 0,
        'total_wall_hits': 0,
        'speed_multiplier': 1.0,
        'speed_changes':   0,
        'max_speed_reached': 1.0,
    }
    ball_vel = {'x': 0.0, 'y': 0.0}
    last_paddle_hit_time = 0.0
    paddle_hits = 0  # licznik udanych odbić paletką
    survival_time = None

    # --- Obiekty gry ---
    left_paddle = visual.Rect(
        win, width=0.02, height=paddle_height,
        fillColor='white', lineColor='white', pos=(-0.45, 0),
    )
    right_paddle = visual.Rect(
        win, width=0.02, height=paddle_height,
        fillColor='white', lineColor='white', pos=(0.45, 0),
    )
    ball = visual.Polygon(
        win, edges=100, radius=0.015,
        fillColor='white', lineColor='white', pos=(0, 0),
    )
    left_wall = visual.Rect(
        win, width=0.005, height=1.0,
        fillColor='red', lineColor='red', pos=(-0.5, 0),
    )
    right_wall = visual.Rect(
        win, width=0.005, height=1.0,
        fillColor='red', lineColor='red', pos=(0.5, 0),
    )
    timer_text = visual.TextStim(
        win, text='02:00', font='Arial',
        height=0.03, color='white', pos=(0, 0.45),
    )

    # --- Resetowanie piłki ---
    def reset_ball():
        ball.pos = (0, 0)
        h_dir = 1 if random.random() > 0.5 else -1
        v_angle = (random.random() - 0.5) * 0.5
        speed = base_speed * game_state['speed_multiplier']
        ball_vel['x'] = h_dir * speed * math.cos(v_angle)
        ball_vel['y'] = speed * math.sin(v_angle)

    def update_ball_speed():
        current = math.sqrt(ball_vel['x'] ** 2 + ball_vel['y'] ** 2)
        new_speed = base_speed * game_state['speed_multiplier']
        if current > 0:
            ball_vel['x'] = (ball_vel['x'] / current) * new_speed
            ball_vel['y'] = (ball_vel['y'] / current) * new_speed

    # --- Klawiatura (ciągłe śledzenie) ---
    kb = keyboard.Keyboard()
    frame_dur = win.getActualFrameRate()
    frame_dur = 1.0 / frame_dur if frame_dur else 1.0 / 60.0
    paddle_speed = 0.5

    reset_ball()
    game_clock = core.Clock()
    start_time = core.getTime()
    escaped = False

    # ==================== PĘTLA GŁÓWNA GRY ====================
    while True:
        t = game_clock.getTime()

        if t >= TEST_DURATION and difficulty != 'Survival':
            break

        # ESC – przerwanie
        if event.getKeys(keyList=['escape']):
            escaped = True
            break

        # --- Ruch paletek ---
        paddle_half_h = paddle_height / 2

        keys_w  = kb.getKeys(['w'],    waitRelease=False, clear=False)
        keys_s  = kb.getKeys(['s'],    waitRelease=False, clear=False)
        keys_up = kb.getKeys(['up', 'o'],   waitRelease=False, clear=False)
        keys_dn = kb.getKeys(['down', 'l'], waitRelease=False, clear=False)

        lp = left_paddle.pos
        rp = right_paddle.pos

        if any(k.duration is None for k in keys_w):
            left_paddle.pos = (lp[0], min(lp[1] + paddle_speed * frame_dur, 0.5 - paddle_half_h))
        if any(k.duration is None for k in keys_s):
            left_paddle.pos = (lp[0], max(lp[1] - paddle_speed * frame_dur, -0.5 + paddle_half_h))
        if any(k.duration is None for k in keys_up):
            right_paddle.pos = (rp[0], min(rp[1] + paddle_speed * frame_dur, 0.5 - paddle_half_h))
        if any(k.duration is None for k in keys_dn):
            right_paddle.pos = (rp[0], max(rp[1] - paddle_speed * frame_dur, -0.5 + paddle_half_h))

        # --- Ruch piłki ---
        bx, by = ball.pos
        ball.pos = (bx + ball_vel['x'], by + ball_vel['y'])
        bx, by = ball.pos
        br = 0.015
        pw = 0.02

        lp = left_paddle.pos
        rp = right_paddle.pos

        # Góra / dół
        if by + br >= 0.5:
            ball.pos = (bx, 0.5 - br)
            ball_vel['y'] = -abs(ball_vel['y'])
            bx, by = ball.pos
        if by - br <= -0.5:
            ball.pos = (bx, -0.5 + br)
            ball_vel['y'] = abs(ball_vel['y'])
            bx, by = ball.pos

        # Kolizja – lewa paletka
        if (bx - br <= lp[0] + pw / 2 and
                bx + br >= lp[0] - pw / 2 and
                lp[1] - paddle_half_h <= by <= lp[1] + paddle_half_h and
                ball_vel['x'] < 0):
            ball.pos = (lp[0] + pw / 2 + br, by)
            ball_vel['x'] = abs(ball_vel['x'])
            hit_pos = (by - lp[1]) / paddle_half_h
            ball_vel['y'] += hit_pos * 0.003
            paddle_hits += 1
            if difficulty == 'Hard':
                game_state['speed_multiplier'] = 1.0
                last_paddle_hit_time = t
                update_ball_speed()

        # Kolizja – prawa paletka
        bx, by = ball.pos
        if (bx + br >= rp[0] - pw / 2 and
                bx - br <= rp[0] + pw / 2 and
                rp[1] - paddle_half_h <= by <= rp[1] + paddle_half_h and
                ball_vel['x'] > 0):
            ball.pos = (rp[0] - pw / 2 - br, by)
            ball_vel['x'] = -abs(ball_vel['x'])
            hit_pos = (by - rp[1]) / paddle_half_h
            ball_vel['y'] += hit_pos * 0.003
            paddle_hits += 1
            if difficulty == 'Hard':
                game_state['speed_multiplier'] = 1.0
                last_paddle_hit_time = t
                update_ball_speed()

        # Uderzenie w lewą ścianę
        bx, by = ball.pos
        if bx - br <= -0.5:
            game_state['left_wall_hits']  += 1
            game_state['total_wall_hits'] += 1
            if difficulty == 'Survival':
                survival_time = t
                break
            if difficulty == 'Hard':
                game_state['speed_multiplier'] = 1.0
                last_paddle_hit_time = t
            reset_ball()

        # Uderzenie w prawą ścianę
        bx, by = ball.pos
        if bx + br >= 0.5:
            game_state['right_wall_hits'] += 1
            game_state['total_wall_hits'] += 1
            if difficulty == 'Survival':
                survival_time = t
                break
            if difficulty == 'Hard':
                game_state['speed_multiplier'] = 1.0
                last_paddle_hit_time = t
            reset_ball()

        # Tryb Trudny / Survival – przyspieszenie
        if difficulty == 'Hard':
            time_since = t - last_paddle_hit_time
            if time_since >= SPEED_INCREASE_INTERVAL:
                new_mult = min(game_state['speed_multiplier'] + SPEED_INCREASE_AMOUNT, MAX_SPEED_MULTIPLIER)
                if new_mult != game_state['speed_multiplier']:
                    game_state['speed_multiplier'] = new_mult
                    game_state['speed_changes'] += 1
                    game_state['max_speed_reached'] = max(game_state['max_speed_reached'], game_state['speed_multiplier'])
                    last_paddle_hit_time = t
                    update_ball_speed()
        elif difficulty == 'Survival':
            # Gładsza krzywa przyrostu, bo rośnie w nieskończoność
            time_since = t - last_paddle_hit_time
            if time_since >= 3.0: # Co 3 sekundy
                game_state['speed_multiplier'] += 0.1 # +10% prędkości
                game_state['speed_changes'] += 1
                game_state['max_speed_reached'] = max(game_state['max_speed_reached'], game_state['speed_multiplier'])
                last_paddle_hit_time = t
                update_ball_speed()

        # --- Timer ---
        if difficulty == 'Survival':
            display_time = t
        else:
            display_time = TEST_DURATION - t
            
        mins = int(display_time // 60)
        secs = int(display_time % 60)
        timer_text.text = f'{mins:02d}:{secs:02d}'

        # --- Rysowanie ---
        left_wall.draw()
        right_wall.draw()
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()
        timer_text.draw()
        win.flip()

    # ==================== PO ZAKOŃCZENIU GRY ====================

    duration_s = core.getTime() - start_time

    if not escaped:
        # Ekran wyników końcowych
        wall_hits = game_state['total_wall_hits']
        
        if difficulty == 'Survival':
            if survival_time is not None:
                st = float(survival_time)
                surv_mins = int(st // 60)
                surv_secs = int(st % 60)
            else:
                surv_mins = 0
                surv_secs = 0
            res_text = (
                'KONIEC TESTU – TRYB PRZETRWANIA\n\n'
                f'Czas przeżycia: {surv_mins:02d}:{surv_secs:02d}\n'
                f'Odbicia paletką: {paddle_hits}\n\n'
                'Naciśnij SPACJĘ, aby zakończyć'
            )
        else:
            res_text = (
                'KONIEC TESTU\n\n'
                f'Poziom: {difficulty_label}\n'
                f'Odbicia paletką: {paddle_hits}\n'
                f'Przepuszczone (lewa): {game_state["left_wall_hits"]}\n'
                f'Przepuszczone (prawa): {game_state["right_wall_hits"]}\n'
                f'Przepuszczone razem: {wall_hits}\n\n'
                'Naciśnij SPACJĘ, aby zakończyć'
            )
            
        results_text = visual.TextStim(
            win,
            text=res_text,
            font='Arial', height=0.04, color='white', wrapWidth=1.5,
        )
        results_text.draw()
        win.flip()
        event.waitKeys(keyList=['space', 'escape'])

    win.close()

    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, game_state, difficulty_label, duration_s, paddle_hits, survival_time)


if __name__ == '__main__':
    main()