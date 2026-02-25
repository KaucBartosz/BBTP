"""
Samochodzik - Test nawigacji (wersja PsychoPy)
Sterowanie: strzałki klawiatury
Mechanika: wykrywanie kolizji z białą trasą, reset na start po wyjechaniu poza trasę
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

# Konfiguracja testu
REACTION_TIME_LIMIT_SEC = 3.0  # limit czasu na reakcję (nie używany w tym teście)
FEEDBACK_TIME = 0.5
N_TRIALS = 5 if NOUS_TRAINING else 10

# Współrzędne startowe (z analizy obrazu)
START_AREA = (0.232, 0.383)  # x, y w jednostkach 'height'
CAR_SIZE = (0.05, 0.08)  # szerokość, wysokość w jednostkach 'height'

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
        'testId': 'Samochodzik',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': 0,
        'ilosc_blednych_nacisniec': collision_count,
        'ogolna_ilosc_nacisniec': 0,
        'czas_trwania': duration,
        'liczba_kolizji': collision_count,
        'wyniki': trials_data,
    }
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def load_track_pixels():
    """Wczytanie pikseli tła dla detekcji kolizji"""
    img = visual.ImageStim(
        win=None,
        image=str(RESOURCES / 'trasa.png'),
        size=[1.0, 0.555]  # proporcje obrazu 800x444
    )
    # Utworzenie canvas do analizy pikseli
    canvas = visual.Window(
        size=(800, 444),
        units='pix',
        color=(0, 0, 0),
        fullscr=False,
        winType='pyglet'
    )
    track_image = visual.ImageStim(
        win=canvas,
        image=str(RESOURCES / 'trasa.png'),
        size=[800, 444]
    )
    track_image.draw()
    canvas.flip()
    # Pobranie danych pikseli
    pixels = canvas.getMovieFrame(buffer='back')
    canvas.close()
    return pixels

def is_on_track(win, x, y, track_pixels):
    """Sprawdzenie czy punkt jest na białej trasie"""
    # Konwersja współrzędnych PsychoPy na piksele
    # PsychoPy: środek (0,0), zakres x: -0.5 do 0.5, y: -0.2775 do 0.2775 (units: 'height')
    # Obraz: 800x444, środek (400, 222)
    pixel_x = int((x + 0.5) * 800)
    pixel_y = int((0.2775 - y) * 444)

    # Sprawdzenie granic obrazu
    if pixel_x < 0 or pixel_x >= 800 or pixel_y < 0 or pixel_y >= 444:
        return False

    # Sprawdzenie czy piksel jest biały (trasą)
    # Piksele w formacie RGBA, biały: R=255, G=255, B=255
    r = track_pixels.getpixel((pixel_x, pixel_y))[0]
    return r > 200  # Sprawdzenie tylko kanału czerwonego (obrazy w skali szarości)

def main():
    # Inicjalizacja okna
    win = visual.Window(
        fullscr=True,
        units='height',
        color=(-1, -1, -1),
        allowGUI=False
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    # Ekran instrukcji
    instr = visual.TextStim(
        win, text=INSTRUCTION,
        color='white', height=0.05,
        wrapWidth=1.8, alignText='center',
    )
    instr.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space', 'return', 'escape'])
    first = keys[0] if keys else None
    keyname = first[0] if first and isinstance(first, (list, tuple)) else first
    if keyname == 'escape':
        win.close()
        if NOUS_LAUNCHER:
            _write_results(SCRIPT_DIR, [], 0, 0)
        return

    # Wczytanie obrazu tła i przygotowanie do detekcji kolizji
    track_image = visual.ImageStim(
        win=win,
        image=str(RESOURCES / 'trasa.png'),
        pos=[0, 0],
        size=[1.0, 0.555],  # proporcje obrazu 800x444
        opacity=1.0
    )

    # Samochód
    car = visual.ImageStim(
        win=win,
        image=str(RESOURCES / 'sam.png'),
        pos=[START_AREA[0], START_AREA[1]],
        size=CAR_SIZE,
        opacity=1.0
    )

    # Wczytanie pikseli tła dla detekcji kolizji
    # (używamy tymczasowego okna do pobrania pikseli)
    temp_win = visual.Window(
        size=(800, 444),
        units='pix',
        color=(0, 0, 0),
        fullscr=False,
        winType='pyglet'
    )
    track_stim = visual.ImageStim(
        win=temp_win,
        image=str(RESOURCES / 'trasa.png'),
        size=[800, 444]
    )
    track_stim.draw()
    temp_win.flip()
    track_pixels = temp_win.getMovieFrame(buffer='back')
    temp_win.close()

    # Zmienne stanu
    car_x, car_y = START_AREA
    car_rotation = 0.0
    car_speed = 0.005
    collision_count = 0
    start_time = core.getTime()
    is_game_over = False

    # Główna pętla gry
    while not is_game_over:
        # Obsługa klawiatury
        keys = event.getKeys()

        # Sprawdzenie klawiszy
        up_pressed = 'up' in keys or 'up arrow' in keys
        down_pressed = 'down' in keys or 'down arrow' in keys
        left_pressed = 'left' in keys or 'left arrow' in keys
        right_pressed = 'right' in keys or 'right arrow' in keys
        escape_pressed = 'escape' in keys

        # Wyjście z gry
        if escape_pressed:
            break

        # Sterowanie
        if up_pressed:
            # Jazda do przodu
            car_x += car_speed * core.sin(car_rotation)
            car_y += car_speed * core.cos(car_rotation)
        if down_pressed:
            # Jazda do tyłu
            car_x -= car_speed * core.sin(car_rotation) * 0.5
            car_y -= car_speed * core.cos(car_rotation) * 0.5
        if left_pressed:
            # Skręt w lewo
            car_rotation += 0.1
        if right_pressed:
            # Skręt w prawo
            car_rotation -= 0.1

        # Sprawdzenie kolizji
        # Sprawdzenie czterech rogów samochodu
        half_w = CAR_SIZE[0] / 2
        half_h = CAR_SIZE[1] / 2

        # Punkty rogów w przestrzeni PsychoPy
        corners = [
            (car_x - half_w, car_y - half_h),  # lewy dolny
            (car_x + half_w, car_y - half_h),  # prawy dolny
            (car_x - half_w, car_y + half_h),  # lewy górny
            (car_x + half_w, car_y + half_h)   # prawy górny
        ]

        # Sprawdzenie każdego rogu
        collision = False
        for corner in corners:
            if not is_on_track(win, corner[0], corner[1], track_pixels):
                collision = True
                break

        if collision:
            # Reset do pozycji startowej
            car_x, car_y = START_AREA
            car_rotation = 0.0
            collision_count += 1
            print(f'Kolizja! Reset do pozycji startowej. Licznik: {collision_count}')

        # Aktualizacja pozycji samochodu
        car.setPos([car_x, car_y])
        car.setOri(car_rotation * (180 / 3.14159))

        # Rysowanie
        track_image.draw()
        car.draw()

        # Aktualizacja ekranu
        win.flip()

        # Sprawdzenie czy okno zostało zamknięte
        if not win.mouseVisibile:
            break

    # Zakończenie
    win.close()

    # Obliczenie czasu trwania
    duration = core.getTime() - start_time

    # Zapis wyników
    if NOUS_LAUNCHER:
        _write_results(SCRIPT_DIR, [], collision_count, duration)

if __name__ == '__main__':
    main()