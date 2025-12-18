import os
import pygame
import subprocess
import random
import multiprocessing
import time

IMG = "/sgoinfre/goinfre/Perso/zcadinot/script/Lauvray/img/lauvray.jpg"
SND = "/sgoinfre/goinfre/Perso/zcadinot/script/Lauvray/mp3/wow.mp3"

VOLUME = 0.3
MIN_SCALE = 1
MAX_SCALE = 60

# config cascade
CASCADE_COUNT = 10
CASCADE_DELAY = 0.1


def enable_sound():
    subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ 0", shell=True)
    subprocess.run("pactl set-sink-volume @DEFAULT_SINK@ 40%", shell=True)


def cascade(n, delay):
    while n > 0:
        multiprocessing.Process(target=launch).start()
        time.sleep(delay)
        n -= 1


class MediaPlayer:
    def __init__(self):
        pygame.init()

    def _pos(self, iw, ih):
        sw = pygame.display.Info().current_w
        sh = pygame.display.Info().current_h
        if iw > sw:
            iw = sw
        if ih > sh:
            ih = sh
        x = random.randint(0, sw - iw)
        y = random.randint(0, sh - ih)
        return x, y, iw, ih

    def show(self, img_path, snd_path):
        img = pygame.image.load(img_path)
        iw, ih = img.get_size()

        scale = random.randint(MIN_SCALE, MAX_SCALE) / 100
        iw = int(iw * scale)
        ih = int(ih * scale)

        x, y, iw, ih = self._pos(iw, ih)
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"

        win = pygame.display.set_mode((iw, ih))
        win.blit(pygame.transform.scale(img, (iw, ih)), (0, 0))
        pygame.display.update()

        pygame.mixer.init()
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.load(snd_path)
        pygame.mixer.music.play()

        run = True
        while run:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                cascade(CASCADE_COUNT, CASCADE_DELAY)
                run = False


def launch():
    enable_sound()
    MediaPlayer().show(IMG, SND)


if __name__ == "__main__":
    cascade(CASCADE_COUNT, CASCADE_DELAY)
