import pygame
import subprocess

from GameObjects import *
import time
from MIDIUtils import MIDIRhythm
import matplotlib.pyplot as plt


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.size = self.width, self.height = 640, 400
        self.player = PlayerContinuous()
        self.apple = Apple(5, 5)
        self.musicFile = None
        self.musicProcess = None
        self.musicData = None
        self.seek = 0
        self.length = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snake")
        self._running = True
        self._image_surf = pygame.image.load("block.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()
        self.musicFile = 'everlasting_hymn.mid'
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
        # print("Seek:", self.seek)
        # print(self.musicData['x'])
        self.player.speed = self.musicData['y'][self.seek]
        self.player.update()
        if self.seek + 1 != self.length:
            self.seek = self.seek + 1
        else:
            self.seek = 0
            print("Ricomincia")
            print(time.time() - self.start)
            # self.on_cleanup()

    def on_render(self):
        self._display_surf.fill((202, 252, 121))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        fontdir = pygame.font.match_font("tekolight", False, False)
        myfont = pygame.font.Font(fontdir, 32)
        self._display_surf.blit(myfont.render(self.musicFile, True, (0, 0, 0)), (20, 360))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        self.musicProcess.kill()

    def start_music(self):
        self.start = time.time()
        if self.musicProcess is None:
            # self.musicProcess = subprocess.Popen(['java', '-jar', 'KISSMIDI.jar', self.musicFile])
            pass

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