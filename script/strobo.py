import pygame
import time
import colorsys
import sys

# --- CONFIG ---
FREQUENCY_HZ = 20.0   # vitesse de rotation des couleurs
FPS = 120             # fluidité
DURATION_SEC = 0      # 0 = illimité
	# ---------------

pygame.init()
try:
	# Plein écran
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	pygame.mouse.set_visible(False)
	clock = pygame.time.Clock()

	start_time = time.time()
	running = True

	while running:
		# Intercepter et ignorer tous les événements clavier/souris
		for event in pygame.event.get():
			if event.type in (
				pygame.QUIT,
				pygame.KEYUP,
				pygame.MOUSEBUTTONDOWN,
				pygame.MOUSEBUTTONUP,
				pygame.MOUSEMOTION
			):
				continue
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					running = False

		# Arc-en-ciel fluide (HSV → RGB)
		t = time.time() - start_time
		hue = (t * FREQUENCY_HZ) % 1.0
		r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
		color = (int(r * 255), int(g * 255), int(b * 255))

		screen.fill(color)
		pygame.display.flip()

		# Fin après durée donnée (si > 0)
		if DURATION_SEC > 0 and t >= DURATION_SEC:
			running = False

		clock.tick(FPS)

finally:
	pygame.quit()
