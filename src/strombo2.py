# stroboscope_confirm_silent.py
# pip install pygame
import pygame
import time
import sys
import random

# --- CONFIG ---
FREQUENCY_HZ = 100   # ajuste prudemment (Hz)
DURATION_SEC = 0    # 0 = illimité
COLOR_A = (255,255,255)
COLOR_B = (0,0,0)
# ---------------

if FREQUENCY_HZ <= 0:
    sys.exit(1)

half_period = 0.5 / FREQUENCY_HZ

pygame.init()
try:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    start = time.time()
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) if random.randint(0, 5) < 3 else COLOR_A
    running = True
    showing_confirm = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing_confirm = True
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_F4 and (mods & pygame.KMOD_ALT):
                    showing_confirm = True
                elif event.key == pygame.K_y:
                    if showing_confirm:
                        running = False
                elif event.key == pygame.K_n:
                    showing_confirm = False
                elif event.key == pygame.K_ESCAPE:
                    showing_confirm = True

        if not showing_confirm:
            screen.fill(color)
            pygame.display.flip()
            pygame.time.delay(int(half_period * 1000))
            color = COLOR_B if color == COLOR_A else COLOR_A
        else:
            draw_confirmation()
            pygame.display.flip()
            pygame.time.delay(50)

        if DURATION_SEC > 0 and (time.time() - start) >= DURATION_SEC:
            running = False

        clock.tick(1000)
finally:
    pygame.quit()
