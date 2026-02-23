#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PingPong - Test Koordynacji
PsychoPy Implementation
"""

from psychopy import visual, core, event, gui, hardware
import math
import random

# ==================== CONFIGURATION ====================

TEST_DURATION = 120  # 2 minutes in seconds

DIFFICULTY_SETTINGS = {
    'Easy': {'base_speed': 0.005, 'paddle_height': 0.25},
    'Normal': {'base_speed': 0.0096, 'paddle_height': 0.20},  # 20% faster
    'Hard': {'base_speed': 0.0096, 'paddle_height': 0.18}     # 20% faster
}

# Hard mode speed progression
MAX_SPEED_MULTIPLIER = 4  # x4 max speed
SPEED_INCREASE_INTERVAL = 1.5  # seconds
SPEED_INCREASE_AMOUNT = 0.2

# ==================== DIALOG ====================

dlg = gui.Dlg(title="PingPong - Test Koordynacji")
dlg.addField("Participant:", "000001")
dlg.addField("Session:", "001")
dlg.show()

if dlg.OK:
    exp_info = {'participant': dlg.data[0], 'session': dlg.data[1]}
else:
    core.quit()

# ==================== WINDOW SETUP ====================

win = visual.Window(
    size=[1920, 1080],
    fullscr=True,
    color=[-1, -1, -1],  # Black background
    units='height',
    allowGUI=False
)

# Get frame rate
frame_dur = win.getActualFrameRate()
if frame_dur is None:
    frame_dur = 1/60.0
else:
    frame_dur = 1.0 / frame_dur

# ==================== WELCOME SCREEN ====================

welcome_text = visual.TextStim(
    win,
    text='PING PONG - Test Koordynacji\n\n' +
         'Twoim zadaniem jest odbijanie piłki za pomocą dwóch paletek.\n\n' +
         'LEWA PALETKA: klawisze W (góra) i S (dół)\n' +
         'PRAWA PALETKA: strzałki góra i dół\n\n' +
         'Test trwa 2 minuty. Odbijaj piłkę jak najdłużej!\n\n' +
         'Naciśnij SPACJĘ, aby wybrać poziom trudności\n' +
         'ESC - wyjście bez zapisu',
    font='Arial',
    height=0.04,
    color='white',
    wrapWidth=1.5
)

welcome_text.draw()
win.flip()

# Wait for space key
event.waitKeys(keyList=['space', 'escape'])
if 'escape' in event.getKeys(['escape']):
    win.close()
    core.quit()

# ==================== DIFFICULTY SELECTION ====================

difficulty_text = visual.TextStim(
    win,
    text='WYBIERZ POZIOM TRUDNOŚCI\n\n' +
         '1 - ŁATWY (wolniejsza piłka, większe paletki)\n' +
         '2 - NORMALNY (standardowa prędkość)\n' +
         '3 - TRUDNY (prędkość rośnie z czasem)\n\n' +
         'Naciśnij 1, 2 lub 3',
    font='Arial',
    height=0.04,
    color='white',
    wrapWidth=1.5
)

difficulty_text.draw()
win.flip()

# Wait for difficulty selection
difficulty_keys = event.waitKeys(keyList=['1', '2', '3', 'escape'])
if 'escape' in difficulty_keys:
    win.close()
    core.quit()

if '1' in difficulty_keys:
    difficulty = 'Easy'
elif '2' in difficulty_keys:
    difficulty = 'Normal'
else:
    difficulty = 'Hard'

# ==================== GAME VARIABLES ====================

settings = DIFFICULTY_SETTINGS[difficulty]
base_speed = settings['base_speed']
paddle_height = settings['paddle_height']

# Game state
game_state = {
    'left_wall_hits': 0,
    'right_wall_hits': 0,
    'total_wall_hits': 0,
    'speed_multiplier': 1.0,
    'speed_changes': 0,
    'max_speed_reached': 1.0
}

# Ball velocity
ball_vel = {'x': 0, 'y': 0}
last_paddle_hit_time = 0.0

# ==================== CREATE GAME OBJECTS ====================

# Left paddle
left_paddle = visual.Rect(
    win,
    width=0.02,
    height=paddle_height,
    fillColor='white',
    lineColor='white',
    pos=(-0.45, 0)
)

# Right paddle
right_paddle = visual.Rect(
    win,
    width=0.02,
    height=paddle_height,
    fillColor='white',
    lineColor='white',
    pos=(0.45, 0)
)

# Ball (circle using Polygon)
ball = visual.Polygon(
    win,
    edges=100,
    radius=0.015,
    fillColor='white',
    lineColor='white',
    pos=(0, 0)
)

# Left wall (red)
left_wall = visual.Rect(
    win,
    width=0.005,
    height=1.0,
    fillColor='red',
    lineColor='red',
    pos=(-0.5, 0)
)

# Right wall (red)
right_wall = visual.Rect(
    win,
    width=0.005,
    height=1.0,
    fillColor='red',
    lineColor='red',
    pos=(0.5, 0)
)

# Timer text
timer_text = visual.TextStim(
    win,
    text='02:00',
    font='Arial',
    height=0.03,
    color='white',
    pos=(0, 0.45)
)

# ==================== HELPER FUNCTIONS ====================

def reset_ball():
    """Reset ball to center with random direction"""
    ball.pos = (0, 0)
    
    # Random initial direction
    horizontal_dir = 1 if random.random() > 0.5 else -1
    vertical_angle = (random.random() - 0.5) * 0.5  # ±15°
    
    speed = base_speed * game_state['speed_multiplier']
    ball_vel['x'] = horizontal_dir * speed * math.cos(vertical_angle)
    ball_vel['y'] = speed * math.sin(vertical_angle)

def update_ball_speed():
    """Update ball velocity based on current speed multiplier"""
    current_speed = math.sqrt(ball_vel['x']**2 + ball_vel['y']**2)
    new_speed = base_speed * game_state['speed_multiplier']
    
    if current_speed > 0:
        ball_vel['x'] = (ball_vel['x'] / current_speed) * new_speed
        ball_vel['y'] = (ball_vel['y'] / current_speed) * new_speed

# ==================== KEYBOARD SETUP ====================

# Use keyboard component for continuous key tracking
from psychopy.hardware import keyboard
kb = keyboard.Keyboard()

# ==================== MAIN GAME LOOP ====================

# Initialize ball
reset_ball()

# Create clock
game_clock = core.Clock()

# Paddle speed per second
paddle_speed = 0.5

while True:
    # Get current time
    t = game_clock.getTime()
    
    # Check if 2 minutes passed
    if t >= TEST_DURATION:
        break
    
    # Check for escape
    keys = kb.getKeys(['escape'])
    if 'escape' in keys:
        win.close()
        core.quit()
    
    # Get current key states
    keys_w = kb.getKeys(['w'], waitRelease=False, clear=False)
    keys_s = kb.getKeys(['s'], waitRelease=False, clear=False)
    keys_up = kb.getKeys(['up'], waitRelease=False, clear=False)
    keys_down = kb.getKeys(['down'], waitRelease=False, clear=False)
    
    # Update paddle positions
    paddle_half_height = paddle_height / 2
    
    left_pos = left_paddle.pos
    right_pos = right_paddle.pos
    
    # Left paddle (W/S)
    if keys_w:  # W pressed
        for k in keys_w:
            if k.duration is None:  # Still pressed
                left_paddle.pos = (left_pos[0], min(left_pos[1] + paddle_speed * frame_dur, 0.5 - paddle_half_height))
                break
    if keys_s:  # S pressed
        for k in keys_s:
            if k.duration is None:  # Still pressed
                left_paddle.pos = (left_pos[0], max(left_pos[1] - paddle_speed * frame_dur, -0.5 + paddle_half_height))
                break
    
    # Right paddle (arrows)
    if keys_up:  # Up pressed
        for k in keys_up:
            if k.duration is None:  # Still pressed
                right_paddle.pos = (right_pos[0], min(right_pos[1] + paddle_speed * frame_dur, 0.5 - paddle_half_height))
                break
    if keys_down:  # Down pressed
        for k in keys_down:
            if k.duration is None:  # Still pressed
                right_paddle.pos = (right_pos[0], max(right_pos[1] - paddle_speed * frame_dur, -0.5 + paddle_half_height))
                break
    
    # Update ball position
    ball_pos = ball.pos
    ball.pos = (ball_pos[0] + ball_vel['x'], ball_pos[1] + ball_vel['y'])
    ball_pos = ball.pos
    
    # Handle collisions
    paddle_width = 0.02
    ball_radius = 0.015
    left_pos = left_paddle.pos
    right_pos = right_paddle.pos
    
    # Top and bottom walls
    if ball_pos[1] + ball_radius >= 0.5:
        ball.pos = (ball_pos[0], 0.5 - ball_radius)
        ball_vel['y'] = -abs(ball_vel['y'])
        ball_pos = ball.pos
    if ball_pos[1] - ball_radius <= -0.5:
        ball.pos = (ball_pos[0], -0.5 + ball_radius)
        ball_vel['y'] = abs(ball_vel['y'])
        ball_pos = ball.pos
    
    # Left paddle collision
    if (ball_pos[0] - ball_radius <= left_pos[0] + paddle_width / 2 and
        ball_pos[0] + ball_radius >= left_pos[0] - paddle_width / 2 and
        ball_pos[1] >= left_pos[1] - paddle_half_height and
        ball_pos[1] <= left_pos[1] + paddle_half_height and
        ball_vel['x'] < 0):
        
        ball.pos = (left_pos[0] + paddle_width / 2 + ball_radius, ball_pos[1])
        ball_vel['x'] = abs(ball_vel['x'])
        
        # Add angle based on hit position
        hit_position = (ball_pos[1] - left_pos[1]) / paddle_half_height
        ball_vel['y'] += hit_position * 0.003
        
        # Hard mode speed reset
        if difficulty == 'Hard':
            game_state['speed_multiplier'] = 1.0
            last_paddle_hit_time = t
            update_ball_speed()
    
    # Right paddle collision
    if (ball_pos[0] + ball_radius >= right_pos[0] - paddle_width / 2 and
        ball_pos[0] - ball_radius <= right_pos[0] + paddle_width / 2 and
        ball_pos[1] >= right_pos[1] - paddle_half_height and
        ball_pos[1] <= right_pos[1] + paddle_half_height and
        ball_vel['x'] > 0):
        
        ball.pos = (right_pos[0] - paddle_width / 2 - ball_radius, ball_pos[1])
        ball_vel['x'] = -abs(ball_vel['x'])
        
        hit_position = (ball_pos[1] - right_pos[1]) / paddle_half_height
        ball_vel['y'] += hit_position * 0.003
        
        if difficulty == 'Hard':
            game_state['speed_multiplier'] = 1.0
            last_paddle_hit_time = t
            update_ball_speed()
    
    ball_pos = ball.pos
    
    # Left wall hit
    if ball_pos[0] - ball_radius <= -0.5:
        game_state['left_wall_hits'] += 1
        game_state['total_wall_hits'] += 1
        
        if difficulty == 'Hard':
            game_state['speed_multiplier'] = 1.0
            last_paddle_hit_time = t
        
        reset_ball()
    
    # Right wall hit
    if ball_pos[0] + ball_radius >= 0.5:
        game_state['right_wall_hits'] += 1
        game_state['total_wall_hits'] += 1
        
        if difficulty == 'Hard':
            game_state['speed_multiplier'] = 1.0
            last_paddle_hit_time = t
        
        reset_ball()
    
    # Hard mode speed increase
    if difficulty == 'Hard':
        time_since_hit = t - last_paddle_hit_time
        if (time_since_hit >= SPEED_INCREASE_INTERVAL and 
            game_state['speed_multiplier'] < MAX_SPEED_MULTIPLIER):
            
            game_state['speed_multiplier'] = min(
                game_state['speed_multiplier'] + SPEED_INCREASE_AMOUNT,
                MAX_SPEED_MULTIPLIER
            )
            game_state['speed_changes'] += 1
            game_state['max_speed_reached'] = max(
                game_state['max_speed_reached'],
                game_state['speed_multiplier']
            )
            last_paddle_hit_time = t
            update_ball_speed()
    
    # Update timer
    remaining = TEST_DURATION - t
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    timer_text.text = f'{minutes:02d}:{seconds:02d}'
    
    # Draw everything
    left_wall.draw()
    right_wall.draw()
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()
    timer_text.draw()
    
    win.flip()

# ==================== RESULTS SCREEN ====================

results_text = visual.TextStim(
    win,
    text='KONIEC TESTU\n\n' +
         f'Lewa strona: {game_state["left_wall_hits"]} uderzeń\n' +
         f'Prawa strona: {game_state["right_wall_hits"]} uderzeń\n' +
         f'Razem: {game_state["total_wall_hits"]} uderzeń\n\n' +
         'Naciśnij SPACJĘ, aby zakończyć',
    font='Arial',
    height=0.05,
    color='white',
    wrapWidth=1.5
)

results_text.draw()
win.flip()

# Wait for space
event.waitKeys(keyList=['space', 'escape'])

# ==================== CLEANUP ====================

win.close()
core.quit()