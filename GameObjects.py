class Player:
    x = 10
    y = 10
    speed = 8
    direction = 0

    def right(self):
        self.direction = 0

    def left(self):
        self.direction = 1

    def up(self):
        self.direction = 2

    def down(self):
        self.direction = 3

    def update(self):
        if self.direction == 0:
            self.x = self.x + self.speed
        elif self.direction == 1:
            self.x = self.x - self.speed
        elif self.direction == 2:
            self.y = self.y - self.speed
        elif self.direction == 3:
            self.y = self.y + self.speed
