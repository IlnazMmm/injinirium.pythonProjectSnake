import pygame as pg
import sys
from random import randrange

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.range_height = (self.size // 2, self.game.screen_height - self.size // 2, self.size)
        self.range_width = (self.size // 2, self.game.screen_width - self.size // 2, self.size)
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_s and self.directions[pg.K_s]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_a and self.directions[pg.K_a]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

            if event.key == pg.K_d and self.directions[pg.K_d]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(*self.range_width), randrange(*self.range_height)]

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.screen_width:
            self.game.input_name()
            self.game.input_score(self.length)
            self.game.show_results()
            pg.quit()
            sys.exit()
        if self.rect.top < 0 or self.rect.bottom > self.game.screen_height:
            self.game.input_name()
            self.game.input_score(self.length)
            self.game.show_results()
            pg.quit()
            sys.exit()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.input_name()
            self.game.input_score(self.length)
            self.game.show_results()
            pg.quit()
            sys.exit()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)

class Score:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE

    def draw(self, length):
        font = pg.font.Font(None, 42)
        color= pg.Color('lightskyblue3')
        txt_score = font.render("Очки: ", True, color)
        self.game.screen.blit(txt_score, (10, 10))

        txt_length = font.render(str(length), True, color)
        self.game.screen.blit(txt_length, (100, 10))
