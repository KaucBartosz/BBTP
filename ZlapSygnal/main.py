# -*- coding: utf-8 -*-
"""
Złap Sygnał – wersja PsychoPy (HPM / Nous).
Test Aparatu Piórkowskiego: Ocena koordynacji wzrokowo-ruchowej.
Na ekranie pojawiają się czerwone kółka - zadaniem jest kliknięcie na samochód.
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

# --- KONFIGURACJA ZMIENNYCH ---
APPEARANCE_RATE = 107  # Częstotliwość pojawiania się znaków na minutę
TIME_BETWEEN_CIRCLES = 60.0 / APPEARANCE_RATE  # Czas między znakami w sekundach
CIRCLE_SIZE = 0.15  # Rozmiar kółka w jednostkach height

# Opcje czasu trwania testu (w sekundach)
DURATION_OPTIONS = [30, 60, 90, 120]
DEFAULT_DURATION = 60

INSTRUCTION = 'Na ekranie w krótkich odstępach czasu pojawiać się będzie czerwone kółko. \nTwoim zadaniem jest, za pomocą MYSZY, kliknąć na samochód za każdym razem, gdy pojawi się nowe kółko. \nStaraj się reagować najszybciej jak potrafisz. \nAby rozpocząć zadanie, wciśnij SPACJĘ.'

DURATION_SELECTION_TEXT = (
    'Wybierz czas trwania testu:\n\n'
    '1 - 30 sekund\n'
    '2 - 60 sekund\n'
    '3 - 90 sekund\n'
    '4 - 120 sekund'
)


def _write_results(script_dir, trials_data, correct_count, miss_count, total_circles, avg_rt_ms, selected_duration, clicks_without_circle):
    results = {
        'testId': 'ZlapSygnal',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': correct_count,
        'ilosc_blednych_nacisniec': miss_count,
        'ogolna_ilosc_nacisniec': total_circles,
        'sredni_czas_reakcji': avg_rt_ms,
        'klikniecia_bez_kolka': clicks_without_circle,
        'score': f'Poprawne: {correct_count} | Misses: {miss_count} | Bez kółka: {clicks_without_circle} | Łącznie: {total_circles} | Śr. RT: {avg_rt_ms} ms',
        'wyniki': trials_data,
        'selectedDuration': selected_duration,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def select_duration(win):
    """Pozwala użytkownikowi wybrać czas trwania testu."""
    duration_text = visual.TextStim(
        win, text=DURATION_SELECTION_TEXT,
        color='white', height=0.06,
        wrapWidth=1.4, alignText='center',
    )
    duration_text.draw()
    win.flip()
    
    keys = event.waitKeys(keyList=['1', '2', '3', '4', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    
    if keyname == 'escape':
        return None
    elif keyname == '1':
        return 30
    elif keyname == '2':
        return 60
    elif keyname == '3':
        return 90
    elif keyname == '4':
        return 120
    else:
        return DEFAULT_DURATION


def main():
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(-1, -1, -1),
        allowGUI=False,
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    # Wybór czasu trwania testu
    selected_duration = select_duration(win)
    if selected_duration is None:
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, DEFAULT_DURATION, 0)
        return

    # Ekran instrukcji
    instr = visual.TextStim(
        win, text=INSTRUCTION,
        color='white', height=0.05,
        wrapWidth=1.4, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'return', 'y', 'n', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0, 0, 0, selected_duration, 0)
        return

    # Samochód - statyczny na środku na dole ekranu
    car = visual.ImageStim(
        win,
        image=str(RESOURCES / 'car.png'),
        size=[0.3, 0.15],
        pos=[0, -0.35]
    )

    trials_data = []
    trial_clock = core.Clock()
    
    # Zmienne do śledzenia
    correct_count = 0
    miss_count = 0
    total_responses = 0
    rt_sum = 0.0
    circle_id = 0
    current_circle = None
    circle_onset_time = None
    next_circle_time = TIME_BETWEEN_CIRCLES
    responded = False
    waiting_for_release = False
    circle_timeout = 0
    clicks_without_circle = 0  # Kliknięcia bez widocznego kółka
    
    prev_pressed = mouse.getPressed() or [0, 0, 0]
    escaped = False
    
    trial_clock.reset()
    
    while trial_clock.getTime() < selected_duration:
        t = trial_clock.getTime()
        
        if event.getKeys(keyList=['escape']):
            escaped = True
            break
        
        # Odczyt myszy
        pressed = mouse.getPressed()
        if pressed is not None and len(pressed) >= 3:
            is_pressed_now = pressed[0] or pressed[1] or pressed[2]
            is_new_click = is_pressed_now and not (prev_pressed[0] or prev_pressed[1] or prev_pressed[2])
            prev_pressed = pressed
        else:
            is_pressed_now = False
            is_new_click = False

        # Jeśli gracz puścił przycisk, zaczynamy liczyć czas do kolejnego kółka
        if waiting_for_release and not is_pressed_now:
            waiting_for_release = False
            next_circle_time = t + TIME_BETWEEN_CIRCLES

        # Sprawdzenie timeoutu dla widocznego kółka (miss)
        if current_circle is not None and not responded:
            if t >= circle_timeout:
                miss_count += 1
                trials_data.append({
                    'circleId': circle_id,
                    'correct': 0,
                    'miss': 1,
                    'rt': None
                })
                current_circle = None
                # Po missie od razu odliczamy do następnego kółka
                next_circle_time = t + TIME_BETWEEN_CIRCLES

        # Tworzenie nowego kółka
        if current_circle is None and not waiting_for_release and t >= next_circle_time:
            circle_id += 1
            random_x = (random.random() - 0.5) * 1.0  # Losowa pozycja X (±0.50, bez obrzeży)
            random_y = -0.10 + random.random() * 0.53  # Losowa pozycja Y (od -0.10 do 0.43)
            
            current_circle = visual.Circle(
                win,
                radius=CIRCLE_SIZE / 2,
                pos=(random_x, random_y),
                fillColor='red',
                lineColor='red',
                units='height'
            )
            circle_onset_time = t
            responded = False
            
            # Timeout kółka (ile czasu badany ma na kliknięcie)
            circle_timeout = t + TIME_BETWEEN_CIRCLES * 1.5
        
        # Rysowanie kółka
        if current_circle is not None and not responded:
            current_circle.draw()
        
        # Rysowanie samochodu
        car.draw()
        
        # Obsługa kliknięcia mychy
        if current_circle is not None and not responded and is_new_click and circle_onset_time is not None:
            if car.contains(mouse.getPos()):
                responded = True
                rt = t - circle_onset_time
                correct_count += 1
                total_responses += 1
                rt_sum += rt
                
                trials_data.append({
                    'circleId': circle_id,
                    'correct': 1,
                    'miss': 0,
                    'rt': rt
                })
                
                # Znika kółko i zaczynamy czekać na puszczenie
                current_circle = None
                waiting_for_release = True
        
        # Kliknięcie bez widocznego kółka
        if is_new_click and (current_circle is None or responded):
            if car.contains(mouse.getPos()):
                clicks_without_circle += 1
        
        win.flip()
    
    # Zapis ostatniego kółka jeśli był miss
    if current_circle is not None and not responded:
        miss_count += 1
        trials_data.append({
            'circleId': circle_id,
            'correct': 0,
            'miss': 1,
            'rt': None
        })
    
    win.close()

    # Podsumowanie wyników
    total_circles = correct_count + miss_count
    avg_rt_ms = round((rt_sum / total_responses) * 1000) if total_responses > 0 else 0

    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, trials_data, correct_count, miss_count, total_circles, avg_rt_ms, selected_duration, clicks_without_circle)


if __name__ == '__main__':
    main()
