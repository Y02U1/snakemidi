import pygame
import subprocess

from GameObjects import *
import time
from MIDIUtils import MIDIRhythm
import matplotlib.pyplot as plt


class App:
    def __init__(self):
        self._running = False
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.size = self.width, self.height = 640, 400
        self.player = None
        self.apple = None
        self.musicFile = None
        self.musicProcess = None
        self.musicData = None
        self.seek = 0
        self.length = 0
        # 1 - facile
        # 3 - medio
        # 5 - difficile?
        self.speed = 3

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snake")
        self._running = True
        self._image_surf = pygame.image.load("img/block.png").convert()
        self._apple_surf = pygame.image.load("img/newapple.png").convert()
        self.player = PolySnake(width=32)
        self.apple = Apple(5, 5, 8, 8)  # FIXME non si può migliorare il passaggio della size?
        self.musicFile = 'mid/everlasting_hymn.mid'
        # self.musicFile = 'test.mid'
        staves = MIDIRhythm(self.musicFile).proto()
        self.start_music()
        x, y = staves[0][0], staves[0][1]
        self.musicData = {'x': x, 'y': y}
        self.length = len(self.musicData['x'])

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
        self.player.speed = self.musicData['y'][self.seek]*self.speed
        self.player.update()
        if self.seek + 1 != self.length:
            self.seek = self.seek + 1
        else:
            self.seek = 0
            print("Ricomincia")
            print(time.time() - self.start)
            self.on_cleanup()

        # FIXME non si può evitare il passaggio della size?
#        if self.apple.is_partial_collision(self.player.x, self.player.y, 16, 16):
#            self.apple.move(self.width, self.height)

    def on_render(self):
        # Sfondo
        self._display_surf.fill((202, 252, 121))

        # GameObjects
        self.player.draw(self._display_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        # Testo
        fontdir = pygame.font.match_font("tekolight", False, False)
        myfont = pygame.font.Font(fontdir, 32)
        self._display_surf.blit(myfont.render(self.musicFile, True, (0, 0, 0)), (20, 360))

        pygame.display.flip()  # Aggiorna

    def on_cleanup(self):
        pygame.quit()
        self.musicProcess.kill()

    def start_music(self):
        self.start = time.time()
        if self.musicProcess is None:
            # self.musicProcess = subprocess.Popen(['java', '-jar', 'KISSMIDI.jar', self.musicFile])
            pass

    def is_full_collision(self, x1, y1, x2, y2, bsize):
        if x2 <= x1 <= x2 + bsize:
            if y2 <= y1 <= y2 + bsize:
                return True
        return False

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        # plt.plot(self.musicData['x'], self.musicData['y'])
        # plt.show()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            time.sleep(1 / 100.0)
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()