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
        self.rel_x = 0.0

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

            # Can't use tile_map.check_pos() because map_y and map_x are NOT
            # relative to the player coordinates (self.pos)
            if tile_map.tiles[map_y][map_x].id != 0:
                self.hit = True
                break

        if self.side == "x":
            self.length = (x_length - scaling_x) * tile_size
            self.rel_x = (self.pos + (self.dir * self.length)).x % tile_size
        else:
            self.length = (y_length - scaling_y) * tile_size
            self.rel_x = (self.pos + (self.dir * self.length)).y % tile_size

        self.rel_x = self.rel_x / tile_size
        print(self.length)

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface,
                         "white",
                         self.pos,
                         self.pos + self.dir * self.length)


class RayCaster():
    def __init__(self, tile_map: Map, fov: float, n_rays: int):
        self.tile_map = tile_map
        self.fov = fov
        self.n_rays = n_rays
        self.rays = [Ray(pygame.Vector2(), pygame.Vector2()) for _ in range(n_rays)]

    def cast_all(self, pos: pygame.Vector2, dir: pygame.Vector2):
        angle_step = self.fov / self.n_rays
        ray_dir = dir.rotate(-self.fov / 2)

        for ray in self.rays:
            ray.pos.update(pos)
            ray.dir.update(ray_dir)
            ray.cast(self.tile_map)

            ray_dir.rotate_ip(angle_step)

    def draw_all(self, surface: pygame.Surface):
        for ray in self.rays:
            ray.draw(surface)

    def render_3d(self, surface: pygame.Surface, horizon: int):
        h = surface.get_height()
        # TODO: better calculation for the rectangles width
        w = int((surface.get_width() + self.n_rays - 1) / self.n_rays) # round up
        max_depth = 200

        tile_size = self.tile_map.tile_size

        for i, ray in enumerate(self.rays):
            if not ray.hit:
                continue

            if ray.length == 0:
                continue

            color = pygame.Color("red") if ray.side == "x" else pygame.Color("darkred")
            color = color.lerp((0, 0, 0), min(1, ray.length / max_depth))

            end_pos = ray.pos + ray.dir * ray.length


            ray_h = (h / ray.length) * tile_size
            rect = pygame.Rect(w * i, horizon - (ray_h / 2), w, ray_h)

            map_y = int(end_pos.y / tile_size)
            map_x = int(end_pos.x / tile_size)
            tile = self.tile_map.tiles[map_y][map_x]
            texture = tile.get_texture(ray.rel_x)
            texture = pygame.transform.scale(texture, (rect.width, rect.height))

            surface.blit(texture, (rect.x, rect.y))




