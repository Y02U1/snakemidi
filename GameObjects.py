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

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


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