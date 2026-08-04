import math
import pygame
from tile_map import Map

class Ray():
    def __init__(self, pos: pygame.Vector2, dir: pygame.Vector2):
        self.pos = pos
        self.dir = dir
        self.length = 0.0
        self.hit = False
        self.side = None

    def cast(self, tile_map: Map):
        tile_size = tile_map.tile_size

        scaling_x = abs(1 / self.dir.x) if self.dir.x != 0 else math.inf
        scaling_y = abs(1 / self.dir.y) if self.dir.y != 0 else math.inf

        map_x = int(self.pos.x / tile_size)
        map_y = int(self.pos.y / tile_size)

        if self.dir.x < 0:
            x_step = -1
            x_length = (self.pos.x / tile_size - map_x) * scaling_x
        else:
            x_step = 1
            x_length = (map_x + 1 - self.pos.x / tile_size) * scaling_x

        if self.dir.y < 0:
            y_step = -1
            y_length = (self.pos.y / tile_size - map_y) * scaling_y
        else:
            y_step = 1
            y_length = (map_y + 1 - self.pos.y / tile_size) * scaling_y

        while True:
            if y_length < x_length:
                y_length += scaling_y
                map_y += y_step
                self.side = "y"
            else:
                x_length += scaling_x
                map_x += x_step
                self.side = "x"

            if not (0 <= map_y < tile_map.rows and 0 <= map_x < tile_map.cols):
                self.hit = False
                break

            if tile_map.tiles[map_y][map_x] != 0:
                self.hit = True
                break

        if self.side == "x":
            self.length = (x_length - scaling_x) * tile_size
        else:
            self.length = (y_length - scaling_y) * tile_size

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface,
                         "green",
                         self.pos,
                         self.pos + self.dir * self.length)

