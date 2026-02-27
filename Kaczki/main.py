#!/usr/bin/env python3
"""
Test Kaczki - strzelanie do kul
Wersja Python dla Nous (HPM - High Precision Mode)
"""

import os
import json
import random
import math
from datetime import datetime
from pathlib import Path
from psychopy import visual, core, event, event, monitors
from psychopy.hardware import keyboard
from psychopy.core import quit as core_quit

# Sprawdzenie środowiska Nous
NOUS_LAUNCHER = os.environ.get('NOUS_LAUNCHER') == '1'
NOUS_TRAINING = os.environ.get('NOUS_TRAINING') == '1'
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES = SCRIPT_DIR / 'resources'

def _write_results(script_dir, score, czas_trwania, is_training=False):
    """Zapis wyników do pliku results.json"""
    if not NOUS_LAUNCHER:
        return
    
    results = {
        'testId': 'kaczki',
        'subjectId': f'{random.randint(0, 999999):06d}',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ilosc_poprawnych_nacisniec': score['trafione'],
        'ilosc_blednych_nacisniec': 0,  # nie ma błędnych naciśnięć w tym teście
        'ogolna_ilosc_nacisniec': score['ogolnie'],
        'czas_trwania_sek': round(czas_trwania),
        'trafione_kule': score['trafione'],
        'przeszly_kule': score['przeszly'],
        'wszystkie_kule': score['wszystkie'],
        'skutecznosc': score['wszystkie'] > 0 and round((score['trafione'] / score['wszystkie']) * 100) or 0,
        'score': f"Trafione: {score['trafione']} | Przeszły: {score['przeszly']} | Skuteczność: {score['wszystkie'] > 0 and round((score['trafione'] / score['wszystkie']) * 100) or 0}%"
    }
    
    out_path = script_dir / 'results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

class Ball:
    """Klasa reprezentująca kulę"""
    def __init__(self, win, start_x, start_y, target_x, target_y):
        self.win = win
        self.visible = True
        self.radius = 0.02 + random.random() * 0.01  # losowy rozmiar
        
        # Losowy kolor
        colors = [
            [1, 0, 0],  # czerwony
            [0, 1, 0],  # zielony
            [0, 0, 1],  # niebieski
            [1, 1, 0],  # żółty
            [1, 0, 1],  # magenta
            [0, 1, 1]   # cyjan
        ]
        self.color = random.choice(colors)
        
        # Obliczanie wektora ruchu
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Losowa prędkość (podstawowa + do 50%)
        base_speed = 0.005
        speed = base_speed + random.random() * (base_speed * 0.5)  # maksymalnie +50%
        
        # Normalizacja wektora
        self.vx = (dx / distance) * speed
        self.vy = (dy / distance) * speed
        
        # Pozycja początkowa
        self.x = start_x
        self.y = start_y
        
        # Wizualizacja kuli
        self.circle = visual.Circle(
            win=win,
            radius=self.radius,
            fillColor=self.color,
            lineColor=[1, 1, 1],
            lineWidth=2,
            pos=[self.x, self.y]
        )
    
    def update(self):
        """Aktualizacja pozycji kuli"""
        if not self.visible:
            return False
        
        self.x += self.vx
        self.y += self.vy
        
        # Sprawdzenie czy kula przeszła na drugą stronę
        if self.y > 1.0:
            self.visible = False
            return False
        
        self.circle.pos = [self.x, self.y]
        return True
    
    def draw(self):
        """Rysowanie kuli"""
        if self.visible:
            self.circle.draw()
    
    def check_collision(self, mouse_x, mouse_y):
        """Sprawdzenie kolizji z myszą"""
        if not self.visible:
            return False
        
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance <= self.radius:
            self.visible = False
            return True
        
        return False

def show_instructions(win):
    """Wyświetlenie instrukcji"""
    instr_text = visual.TextStim(
        win=win,
        text='Cel testu:\n\nZ losowego punktu dolnego ekranu wystrzeliwane są kule, które lecą w kierunku losowego punktu na górnej krawędzi ekranu.\n\nTwoim zadaniem jest naciskanie na pojawiające się kule.\n\nNa start ustawione jest 60 kul.\n\nNaciśnij spację, aby rozpocząć test.\nNaciśnij ESC, aby przerwać test.',
        color=[1, 1, 1],
        height=0.05,
        wrapWidth=1.8
    )
    
    instr_text.draw()
    win.flip()
    
    # Czekanie na spację lub ESC
    keys = event.waitKeys(keyList=['space', 'escape'])
    if keys and keys[0] == 'escape':
        return False
    return True

def shoot_ball(win, balls, current_balls, balls_to_shoot):
    """Wystrzelenie nowej kuli"""
    if current_balls >= balls_to_shoot:
        return
    
    # Losowanie punktu startowego (dolny ekran z marginesem 5%)
    margin = 0.9  # 90% szerokości ekranu (5% margines z każdej strony)
    start_x = (random.random() * margin - margin/2)
    start_y = -1.0  # dolna krawędź
    
    # Losowanie punktu docelowego (górny ekran z marginesem 5%)
    target_x = (random.random() * margin - margin/2)
    target_y = 1.0  # górna krawędź
    
    # Tworzenie kuli
    ball = Ball(win, start_x, start_y, target_x, target_y)
    balls.append(ball)

def main():
    """Główna funkcja testu"""
    # Ustawienia testu
    balls_to_shoot = 60  # około 1 minuta gry
    if NOUS_TRAINING:
        balls_to_shoot = 30  # tryb treningowy - mniej kul
    
    # Inicjalizacja okna
    win = visual.Window(
        fullscr=True,
        color=[0, 0, 0],
        units='height',
        allowGUI=False,
        monitor='testMonitor'
    )
    
    # Inicjalizacja myszy
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)  # WAŻNE: zawsze po utworzeniu mouse
    mouse.clickReset()  # reset stanu kliknięć
    
    # Inicjalizacja klawiatury
    kb = keyboard.Keyboard()
    
    # Zmienne gry
    balls = []
    score = {'trafione': 0, 'przeszly': 0, 'ogolnie': 0, 'wszystkie': balls_to_shoot}
    start_time = core.getTime()
    next_ball_time = start_time + 1.0  # pierwsza kula po 1s
    current_balls = 0
    is_completed = False
    escaped = False
    
    try:
        # Ekran instrukcji
        start_game = show_instructions(win)
        if not start_game:
            escaped = True
            core_quit()
        
        # Główna pętla gry
        while not is_completed:
            # Sprawdzanie ESC
            keys = kb.getKeys(['escape'], waitRelease=False)
            if keys:
                escaped = True
                core_quit()
            
            # Sprawdzanie czasu na nową kulę
            current_time = core.getTime()
            if current_time >= next_ball_time and current_balls < balls_to_shoot:
                # Losowanie liczby kul do wystrzelenia (1-3)
                num_balls = random.randint(1, 3)
                for _ in range(num_balls):
                    shoot_ball(win, balls, current_balls, balls_to_shoot)
                
                # Losowanie interwału (0.5-2.0 sekundy)
                next_ball_time = current_time + (0.5 + random.random() * 1.5)
            
            # Aktualizacja pozycji kul
            for ball in balls[:]:
                if not ball.update():
                    if not ball.visible:
                        score['przeszly'] += 1
                        balls.remove(ball)
            
            # Sprawdzanie kliknięć myszą
            if mouse.getPressed()[0]:  # lewy przycisk myszy
                mouse_pos = mouse.getPos()
                if mouse_pos is not None and len(mouse_pos) >= 2:
                    mouse_x, mouse_y = float(mouse_pos[0]), float(mouse_pos[1])
                
                    for ball in balls[:]:
                        if ball.check_collision(mouse_x, mouse_y):
                            score['trafione'] += 1
                            score['ogolnie'] += 1
                            balls.remove(ball)
                            break  # jedno kliknięcie = jedna kula
            
            # Rysowanie
            for ball in balls:
                ball.draw()
            win.flip()
            
            # Sprawdzanie końca gry - gdy suma trafionych i przelotek osiągnie limit
            total_processed = score['trafione'] + score['przeszly']
            if total_processed >= balls_to_shoot:
                is_completed = True
            
            # Ograniczenie FPS
            core.wait(1/60, hogCPUperiod=0)
    
    except Exception as e:
        print(f"Błąd w teście Kaczki: {e}")
    
    finally:
        # Obliczanie czasu trwania
        end_time = core.getTime()
        czas_trwania = end_time - start_time
        
        # Zapis wyników
        _write_results(SCRIPT_DIR, score, czas_trwania, NOUS_TRAINING)
        
        # Zamknięcie okna
        win.close()

if __name__ == '__main__':
    main()