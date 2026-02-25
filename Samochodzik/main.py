"""
Samochodzik - Test nawigacji (wersja PsychoPy)
Sterowanie: strzałki klawiatury
Mechanika: wykrywanie kolizji z białą trasą, reset na start po wyjechaniu poza trasę
"""

import os
import json
import random
import math
from datetime import datetime
from pathlib import Path
from psychopy import visual, core, event
from PIL import Image

# --- Konfiguracja Nous (HPM) ---
NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES = SCRIPT_DIR / 'resources'

# Konfiguracja testu
REACTION_TIME_LIMIT_SEC = 3.0
FEEDBACK_TIME = 0.5
N_TRIALS = 5 if NOUS_TRAINING else 10

# Skalowanie mapy i auta
MAP_SCALE = 1.6
MAP_ASPECT = 0.555
CAR_SIZE = (0.03, 0.05)

# Współrzędne startowe (z analizy obrazu 800x444)
# Zielone pole środek: x=232, y=383 (w pikselach)
# Mapowanie na jednostki 'height' z uwzględnieniem MAP_SCALE:
start_x = (232 / 800 - 0.5) * MAP_SCALE
start_y = (0.2775 - 383 / 800) * MAP_SCALE
START_AREA = (start_x, start_y)

INSTRUCTION = (
    'TEST NAWIGACJI SAMOCHODZIKIEM\n\n'
    'Sterowanie:\n'
    'Strzałka w górę - jazda do przodu\n'
    'Strzałka w dół - jazda do tyłu\n'
    'Strzałka w lewo - skręt w lewo\n'
    'Strzałka w prawo - skręt w prawo\n\n'
    'Cel: poruszaj się po białej trasie\n'
    'Jeśli wyjedziesz poza trasę - reset do pozycji startowej\n\n'
    'Naciśnij SPACJĘ aby rozpocząć\n'
    'Naciśnij ESC aby wyjść'
)

def _write_results(script_dir, trials_data, collision_count, duration):
    results = {
        'testId': 'samochodzik', # małe litery jak w JS
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': 1 if collision_count > 0 or duration > 0 else 0,
        'ilosc_blednych_nacisniec': collision_count,
        'ogolna_ilosc_nacisniec': (1 if collision_count > 0 or duration > 0 else 0) + collision_count,
        'czas_pokonania_trasy_sek': round(duration),
        'score': f'Meta osiągnięta! Kolizje: {collision_count} | Czas: {round(duration)}s',
        'statystyki': {
            'liczba_kolizji': collision_count,
            'czas_trwania_ms': round(duration * 1000)
        },
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def is_on_track(x, y, track_pixels):
    """Sprawdzenie czy punkt jest na białej/zielonej/czerwonej trasie"""
    # Mapowanie z powrotem na piksele obrazu 800x444
    rel_x = x / MAP_SCALE
    rel_y = y / MAP_SCALE
    
    pixel_x = int((rel_x + 0.5) * 800)
    pixel_y = int((0.2775 - rel_y) * 800)

    if pixel_x < 0 or pixel_x >= 800 or pixel_y < 0 or pixel_y >= 444:
        return False

    try:
        pixel = track_pixels.getpixel((pixel_x, pixel_y))
        if isinstance(pixel, int):
            return pixel > 200
        # Akceptujemy biały, zielony i czerwony
        return any(c > 200 for c in pixel)
    except Exception:
        return False

def is_at_finish(x, y, track_pixels):
    """Sprawdzenie czy punkt jest na czerwonym polu mety (R > 200)"""
    rel_x = x / MAP_SCALE
    rel_y = y / MAP_SCALE
    pixel_x = int((rel_x + 0.5) * 800)
    pixel_y = int((0.2775 - rel_y) * 800)

    if pixel_x < 0 or pixel_x >= 800 or pixel_y < 0 or pixel_y >= 444:
        return False

    try:
        pixel = track_pixels.getpixel((pixel_x, pixel_y))
        if isinstance(pixel, int): return False
        # Czerwony kolor mety
        return pixel[0] > 200 and pixel[1] < 100 and pixel[2] < 100
    except Exception:
        return False

def main():
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(-1, -1, -1),
        allowGUI=False
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    instr = visual.TextStim(
        win, text=INSTRUCTION,
        color='white', height=0.04,
        wrapWidth=1.5, alignText='center',
    )
    instr.draw()
    win.flip()
    
    keys = event.waitKeys(keyList=['space', 'return', 'escape'])
    if not keys or 'escape' in keys:
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0)
        return

    track_image = visual.ImageStim(
        win=win,
        image=str(RESOURCES / 'trasa.png'),
        pos=[0, 0],
        size=[MAP_SCALE, MAP_SCALE * MAP_ASPECT],
        opacity=1.0
    )

    car = visual.ImageStim(
        win=win,
        image=str(RESOURCES / 'sam.png'),
        pos=[START_AREA[0], START_AREA[1]],
        size=CAR_SIZE,
        opacity=1.0
    )

    try:
        track_pixels = Image.open(str(RESOURCES / 'trasa.png')).convert('RGB')
    except Exception as e:
        print(f"Błąd zasobów: {e}")
        win.close()
        return

    # Używamy KeyStateHandler dla idealnie płynnego sterowania na Windows
    from pyglet.window import key
    key_handler = key.KeyStateHandler()
    win.winHandle.push_handlers(key_handler)

    car_x, car_y = START_AREA
    car_rotation_rad = 0.0
    car_speed = 0.007 # Prędkość na klatkę
    collision_count = 0
    start_time = core.getTime()
    finished = False

    while not finished:
        if event.getKeys(keyList=['escape']):
            break
        
        dx, dy = 0, 0
        if key_handler[key.LEFT]: dx -= 1
        if key_handler[key.RIGHT]: dx += 1
        if key_handler[key.UP]: dy += 1
        if key_handler[key.DOWN]: dy -= 1
        
        if dx != 0 or dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            car_x += (dx / length) * car_speed
            car_y += (dy / length) * car_speed
            car_rotation_rad = math.atan2(dx, dy)

        # Detekcja kolizji i mety
        half_w = CAR_SIZE[0] / 2
        half_h = CAR_SIZE[1] / 2
        corners_rel = [(-half_w, -half_h), (half_w, -half_h), (-half_w, half_h), (half_w, half_h)]
        
        collision = False
        on_finish = False
        
        for cx, cy in corners_rel:
            rx = car_x + cx * math.cos(car_rotation_rad) + cy * math.sin(car_rotation_rad)
            ry = car_y - cx * math.sin(car_rotation_rad) + cy * math.cos(car_rotation_rad)
            
            # Najpierw sprawdzamy metę
            if is_at_finish(rx, ry, track_pixels):
                on_finish = True
                break
                
            # Potem sprawdzamy kolizję z czarnym tłem
            if not is_on_track(rx, ry, track_pixels):
                collision = True
                break

        if on_finish:
            finished = True
            break

        if collision:
            car_x, car_y = START_AREA
            car_rotation_rad = 0.0
            collision_count += 1

        car.pos = [car_x, car_y]
        car.ori = math.degrees(car_rotation_rad)

        track_image.draw()
        car.draw()
        win.flip()

    duration = core.getTime() - start_time
    
    if finished:
        finish_text = visual.TextStim(win, text="Brawo! Meta osiągnięta!", color='green', height=0.08)
        finish_text.draw()
        win.flip()
        core.wait(2.0)

    win.close()

    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, [], collision_count, duration)

if __name__ == '__main__':
    main()
