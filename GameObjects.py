from random import randint
from pygame import draw


class Player:
    x = [0]
    y = [0]
    speed = 16
    direction = 0

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)
        self.x[1] = 1 * 16
        self.x[2] = 2 * 16

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]
            if self.direction == 0:
                self.x[0] = self.x[0] + self.speed
            elif self.direction == 1:
                self.x[0] = self.x[0] - self.speed
            elif self.direction == 2:
                self.y[0] = self.y[0] - self.speed
            elif self.direction == 3:
                self.y[0] = self.y[0] + self.speed
            self.updateCount = 0

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

    def right(self):
        self.direction = 0

    def left(self):
        self.direction = 1

    def up(self):
        self.direction = 2

    def down(self):
        self.direction = 3


class Apple:
    x = 0
    y = 0
    step = 16

    def __init__(self, x, y, width, height):
        self.x = x * self.step
        self.y = y * self.step
        self.width = width
        self.height = height

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def is_partial_collision(self, x2, y2, w2, h2):
        """
        Controlla una collisione parziale con 1 altro oggetto
        :param x2: x del secondo oggetto
        :param y2: y del secondo oggetto
        :param w2: larghezza del secondo oggetto
        :param h2: altezza del secondo oggetto
        :return: True - collisione. False - niente
        """
        if x2 <= self.x <= x2+w2 and y2 <= self.y <= y2 + h2:
            return True
        if x2 <= self.x+self.width <= x2+w2 and y2 <= self.y <= y2 + h2:
            return True
        if x2 <= self.x <= x2+w2 and y2 <= self.y + self.height <= y2 + h2:
            return True
        if x2 <= self.x+self.width <= x2+w2 and y2 <= self.y + self.height <= y2 + h2:
            return True
        return False

    def move(self, window_width, window_height):
        self.x = randint(0, window_width-self.width)
        self.y = randint(0, window_height-self.height)


class PlayerContinuous:
    x = 0
    y = 0
    speed = 0
    direction = 0

    def __init__(self):
        pass

    def update(self):
        if self.direction == 0:
            self.x = self.x + self.speed
        elif self.direction == 1:
            self.x = self.x - self.speed
        elif self.direction == 2:
            self.y = self.y - self.speed
        elif self.direction == 3:
            self.y = self.y + self.speed

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def right(self):
        self.direction = 0

    def left(self):
        self.direction = 1

    def up(self):
        self.direction = 2

    def down(self):
        self.direction = 3


class PolySnake:
    speed = 0
    direction = 0

    def __init__(self, width=16, height=16):
        self.pointlist = [[0, 0], [width, 0], [width, height], [0, height]]

    def update(self):
        if self.direction == 0:
            # Destra
            for point in self.pointlist:
                point[0] = point[0] + self.speed
        elif self.direction == 1:
            # Sinistra
            for point in self.pointlist:
                point[0] = point[0] - self.speed
        elif self.direction == 2:
            # Su
            for point in self.pointlist:
                point[1] = point[1] - self.speed
        elif self.direction == 3:
            # Giu
            for point in self.pointlist:
                point[1] = point[1] + self.speed

    def draw(self, surface):
        draw.polygon(surface, (0, 0, 0), self.pointlist)

    def right(self):
        self.direction = 0

    def left(self):
        self.direction = 1

    def up(self):
        self.direction = 2

    def down(self):
        self.direction = 3