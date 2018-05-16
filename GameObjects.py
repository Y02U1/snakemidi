class Player:
    x = []
    y = []
    speed = 16
    length = 16
    direction = 0

    updateCountMax = 2
    updateCount = 0

    def __init__(self):
        for i in range(0, self.length):
            self.x.append(0)
            self.y.append(0)

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