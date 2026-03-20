#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Corsi - Test pamięci przestrzennej (PsychoPy / HPM)
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

from psychopy import visual, core, event

NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent

BLOCK_DEFAULT_COLOR = [0.2, 0.05, 0.05]
BLOCK_LIT_COLOR = [0.1, 0.8, 0.1]
BLOCK_SIZE = 0.08
GAP = 0.02
RESPONSE_TIMEOUT = 30
MAX_SEQUENCE_LENGTH = 20
MAX_CONSECUTIVE_ERRORS = 1

DIFFICULTY_CONFIG = {
    1: {'label': 'Łatwy (3x3)', 'gridSize': 3},
    2: {'label': 'Średni (4x4)', 'gridSize': 4},
    3: {'label': 'Trudny (5x5)', 'gridSize': 5},
    4: {'label': 'Bardzo trudny (6x6)', 'gridSize': 6},
    5: {'label': 'Ekspert (7x7)', 'gridSize': 7},
    6: {'label': 'Mistrz (8x8)', 'gridSize': 8},
    7: {'label': 'Arcymistrz (9x9)', 'gridSize': 9},
    8: {'label': 'Legenda (10x10)', 'gridSize': 10}
}

FLASH_SPEED_CONFIG = {
    1: {'label': 'Łatwy (1.0s)', 'flashDuration': 1.0, 'flashGap': 0.3},
    2: {'label': 'Normalny (0.5s)', 'flashDuration': 0.5, 'flashGap': 0.2},
    3: {'label': 'Trudny (0.3s)', 'flashDuration': 0.3, 'flashGap': 0.15}
}


def generate_sequence(grid_size, length):
    total_blocks = grid_size * grid_size
    seq = []
    used = set()
    while len(seq) < length:
        idx = random.randint(0, total_blocks - 1)
        if idx not in used:
            seq.append(idx)
            used.add(idx)
            if len(used) >= total_blocks * 0.8:
                used.clear()
    return seq


def point_in_circle(px, py, cx, cy, radius):
    dx = px - cx
    dy = py - cy
    return (dx * dx + dy * dy) <= (radius * radius)


def _write_results(script_dir, trial_data, total_trials, correct_trials, max_correct_length,
                   avg_rt_ms, chosen_difficulty, grid_size, chosen_flash_speed):
    accuracy = round((correct_trials / total_trials) * 100) if total_trials > 0 else 0
    results = {
        'testId': 'Corsi',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': correct_trials,
        'ilosc_blednych_nacisniec': total_trials - correct_trials,
        'ogolna_ilosc_nacisniec': total_trials,
        'sredni_czas_reakcji': avg_rt_ms,
        'max_dlugosc_sekwencji': max_correct_length,
        'poziom_trudnosci': DIFFICULTY_CONFIG[chosen_difficulty]['label'],
        'rozmiar_siatki': f'{grid_size}x{grid_size}',
        'szybkosc_swiecenia': FLASH_SPEED_CONFIG[chosen_flash_speed]['label'],
        'score': f'Max: {max_correct_length} | Poprawne: {correct_trials}/{total_trials} | Skuteczność: {accuracy}% | Śr. RT: {avg_rt_ms}ms',
        'statystyki': {
            'poprawne': correct_trials,
            'bledne': total_trials - correct_trials,
            'wszystkie_proby': total_trials,
            'skutecznosc': accuracy,
            'max_sekwencja': max_correct_length,
            'sredni_czas_ms': avg_rt_ms,
            'poziom': chosen_difficulty,
            'rozmiar_siatki': grid_size,
            'szybkosc_swiecenia': chosen_flash_speed
        },
        'wyniki_szczegolowe': trial_data
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    win = visual.Window(fullscr=True, units='height', color=[0, 0, 0], allowGUI=False)
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)
    
    # Welcome - POPRAWNY POLSKI TEKST BEZ CHIŃSKICH ZNAKÓW
    welcome_text = visual.TextStim(
        win,
        text='TEST CORSI - Pamięć przestrzenna\n\nNa ekranie pojawią się koła w siatce.\nKilka kół zapali się na zielono.\nZapamiętaj kolejność i kliknij na koła.\nKażda poprawna odpowiedź wydłuży sekwencję.\nTest kończy się po błędnej odpowiedzi.\n\nNaciśnij SPACJĘ, aby kontynuować.\nESC - wyjście',
        color='white', height=0.04, wrapWidth=1.6
    )
    welcome_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 1, 3)
        return

    # Difficulty
    difficulty_text = visual.TextStim(
        win,
        text='Wybierz rozmiar siatki:\n\n1 - 3x3 (Łatwy)\n2 - 4x4 (Średni)\n3 - 5x5 (Trudny)\n4 - 6x6\n5 - 7x7\n6 - 8x8\n7 - 9x9\n8 - 10x10 (Legenda)\n\nNaciśnij 1-8\nESC - wyjście',
        color='white', height=0.04, wrapWidth=1.6
    )
    difficulty_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1','2','3','4','5','6','7','8','escape'])
    if keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, 1, 3, 2)
        return
    chosen_difficulty = int(keys[0])
    grid_size = DIFFICULTY_CONFIG[chosen_difficulty]['gridSize']

    # Flash speed
    flash_speed_text = visual.TextStim(
        win,
        text='Wybierz szybkość świecenia:\n\n1 - Łatwy (1.0s - długo)\n2 - Normalny (0.5s)\n3 - Trudny (0.3s - szybko)\n\nNaciśnij 1, 2 lub 3\nESC - wyjście',
        color='white', height=0.04, wrapWidth=1.6
    )
    flash_speed_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1','2','3','escape'])
    if keys[0] == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, chosen_difficulty, grid_size, 2)
        return
    chosen_flash_speed = int(keys[0])
    flash_duration = FLASH_SPEED_CONFIG[chosen_flash_speed]['flashDuration']
    flash_gap = FLASH_SPEED_CONFIG[chosen_flash_speed]['flashGap']

    # Create grid
    grid_blocks = []
    block_positions = []
    total_width = grid_size * BLOCK_SIZE + (grid_size - 1) * GAP
    start_x = -total_width / 2 + BLOCK_SIZE / 2
    start_y = total_width / 2 - BLOCK_SIZE / 2
    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * (BLOCK_SIZE + GAP)
            y = start_y - row * (BLOCK_SIZE + GAP)
            block = visual.Polygon(win, edges=60, radius=BLOCK_SIZE / 2, pos=[x, y],
                                   fillColor=BLOCK_DEFAULT_COLOR, lineColor=[1,1,1], lineWidth=2)
            grid_blocks.append(block)
            block_positions.append((x, y))

    instruction_text = visual.TextStim(win, text='Obserwuj sekwencję...', pos=[0, 0.45], height=0.035, color='white')
    feedback_text = visual.TextStim(win, text='', pos=[0, -0.45], height=0.04, color='white')

    # Game loop
    current_sequence_length = 2
    total_trials = 0
    correct_trials = 0
    max_correct_length = 0
    trial_data = []
    escaped = False
    clock = core.Clock()

    while not escaped:
        sequence = generate_sequence(grid_size, current_sequence_length)
        player_sequence = []
        for block in grid_blocks:
            block.fillColor = BLOCK_DEFAULT_COLOR

        # Show sequence
        instruction_text.text = f'Obserwuj sekwencję... (długość: {current_sequence_length})'
        for seq_idx, block_idx in enumerate(sequence):
            if event.getKeys(['escape']):
                escaped = True
                break
            grid_blocks[block_idx].fillColor = BLOCK_LIT_COLOR
            for block in grid_blocks:
                block.draw()
            instruction_text.draw()
            win.flip()
            core.wait(flash_duration)
            grid_blocks[block_idx].fillColor = BLOCK_DEFAULT_COLOR
            for block in grid_blocks:
                block.draw()
            instruction_text.draw()
            win.flip()
            core.wait(flash_gap)
        if escaped:
            break

        # Player turn
        instruction_text.text = 'Powtórz sekwencję klikając na kółka.'
        feedback_text.text = ''
        for block in grid_blocks:
            block.draw()
        instruction_text.draw()
        feedback_text.draw()
        win.flip()

        clock.reset()
        response_start = clock.getTime()
        mouse.clickReset()
        prev_buttons = mouse.getPressed()
        response_complete = False

        while not response_complete and not escaped:
            if event.getKeys(['escape']):
                escaped = True
                break

            if clock.getTime() - response_start > RESPONSE_TIMEOUT:
                total_trials += 1
                trial_data.append({'trial': total_trials, 'sequenceLength': current_sequence_length, 'result': 'timeout', 'responseTime': RESPONSE_TIMEOUT})
                feedback_text.text = 'Czas minął!'
                feedback_text.color = 'orange'
                for block_idx in sequence:
                    grid_blocks[block_idx].fillColor = BLOCK_LIT_COLOR
                    for block in grid_blocks:
                        block.draw()
                    instruction_text.draw()
                    feedback_text.draw()
                    win.flip()
                    core.wait(0.3)
                    grid_blocks[block_idx].fillColor = BLOCK_DEFAULT_COLOR
                core.wait(1.0)
                response_complete = True
                break

            buttons = mouse.getPressed()
            is_new_click = buttons[0] and not prev_buttons[0]
            prev_buttons = buttons[:]

            if is_new_click:
                click_pos = mouse.getPos()
                clicked_block_idx = None
                for i, (bx, by) in enumerate(block_positions):
                    if point_in_circle(click_pos[0], click_pos[1], bx, by, BLOCK_SIZE / 2):
                        clicked_block_idx = i
                        break

                if clicked_block_idx is not None:
                    player_sequence.append(clicked_block_idx)
                    grid_blocks[clicked_block_idx].fillColor = BLOCK_LIT_COLOR
                    for block in grid_blocks:
                        block.draw()
                    instruction_text.draw()
                    feedback_text.draw()
                    win.flip()
                    core.wait(0.1)
                    grid_blocks[clicked_block_idx].fillColor = BLOCK_DEFAULT_COLOR

                    current_idx = len(player_sequence) - 1
                    if player_sequence[current_idx] != sequence[current_idx]:
                        total_trials += 1
                        trial_data.append({'trial': total_trials, 'sequenceLength': current_sequence_length, 'result': 'incorrect', 'responseTime': clock.getTime() - response_start})
                        feedback_text.text = 'BŁĄD!'
                        feedback_text.color = 'red'
                        for block_idx in sequence:
                            grid_blocks[block_idx].fillColor = BLOCK_LIT_COLOR
                            for block in grid_blocks:
                                block.draw()
                            instruction_text.draw()
                            feedback_text.draw()
                            win.flip()
                            core.wait(0.3)
                            grid_blocks[block_idx].fillColor = BLOCK_DEFAULT_COLOR
                        core.wait(1.0)
                        response_complete = True
                        break

                    if len(player_sequence) == len(sequence):
                        total_trials += 1
                        correct_trials += 1
                        max_correct_length = max(max_correct_length, current_sequence_length)
                        trial_data.append({'trial': total_trials, 'sequenceLength': current_sequence_length, 'result': 'correct', 'responseTime': clock.getTime() - response_start})
                        feedback_text.text = 'POPRAWNIE!'
                        feedback_text.color = 'green'
                        if current_sequence_length < MAX_SEQUENCE_LENGTH:
                            current_sequence_length += 1
                        for block in grid_blocks:
                            block.draw()
                        instruction_text.draw()
                        feedback_text.draw()
                        win.flip()
                        core.wait(1.5)
                        response_complete = True
                        break

            for block in grid_blocks:
                block.draw()
            instruction_text.draw()
            feedback_text.draw()
            win.flip()

    # Calculate stats before closing
    correct_times = [t['responseTime'] for t in trial_data if t['result'] == 'correct']
    avg_rt_ms = round((sum(correct_times) / len(correct_times)) * 1000) if correct_times else 0
    accuracy = round((correct_trials / total_trials) * 100) if total_trials > 0 else 0

    win.close()

    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, trial_data, total_trials, correct_trials,
                       max_correct_length, avg_rt_ms, chosen_difficulty, grid_size, chosen_flash_speed)


if __name__ == '__main__':
    main()