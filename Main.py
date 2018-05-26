import pygame
import subprocess

from GameObjects import *
import time
from random import randint
from MIDIUtils import *


def is_collision(x1, y1, x2, y2, bsize):
    if x1 >= x2 and x1 <= x2 + bsize:
        if y1 >= y2 and y1 <= y2 + bsize:
            return True
    return False


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.size = self.width, self.height = 640, 400
        self.player = Player(5)
        self.apple = Apple(5, 5)
        self.music = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snake")
        self._running = True
        self._image_surf = pygame.image.load("mid/block.png").convert()
        self._apple_surf = pygame.image.load("mid/apple.png").convert()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.player.down()
            elif event.key == pygame.K_UP:
                self.player.up()
            elif event.key == pygame.K_LEFT:
                self.player.left()
            elif event.key == pygame.K_RIGHT:
                self.player.right()

    def on_loop(self):
        self.player.update()

        for i in range(0, self.player.length):
            if is_collision(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], 8):
                self.apple.x = randint(2, 9) * 16
                self.apple.y = randint(2, 9) * 16
                self.player.length = self.player.length + 1

        for i in range(2, self.player.length):
            if is_collision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 8):
                self.music.kill()
                exit(0)

    def on_render(self):
        self._display_surf.fill((202, 252, 121))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        fontdir = pygame.font.match_font("tekolight", False, False)
        myfont = pygame.font.Font(fontdir, 32)
        self._display_surf.blit(myfont.render("Highscore: "+str(self.player.length), True, (0, 0, 0)), (20, 360))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        self.music.kill()

    def on_execute(self):
        self.music = subprocess.Popen(['java', '-jar', 'KISSMIDI.jar', 'mid/Super Mario Bros - Ground Theme.mid'])
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            time.sleep(50.0/(1000.0+self.player.length*100))
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()