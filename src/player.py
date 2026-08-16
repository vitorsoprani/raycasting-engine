import pygame
from tile_map import Map


class Player():

    def __init__(self,
                 pos: pygame.Vector2 = pygame.Vector2(0, 0),
                 dir: pygame.Vector2 = pygame.Vector2(1, 0)):
        self.pos = pos
        self.dir = dir

        self.angular_vel = 0.05
        self.linear_vel = 1.5

    def draw(self, surface: pygame.Surface):
        color = "white"
        pygame.draw.circle(surface, color, self.pos, 2)
        pygame.draw.line(surface, color, self.pos, self.pos + self.dir * 10)

    def update_dir(self, rotation_sign: int):
        self.dir.rotate_rad_ip(self.angular_vel * rotation_sign)

    def update_pos(self, vertical_mov: int, horizontal_mov: int, tile_map: Map):
        mov_dir = (self.dir * vertical_mov)
        mov_dir += (self.dir.rotate(90) * horizontal_mov)

        if mov_dir.length_squared() != 0:
            mov_dir.normalize_ip()

        movement = mov_dir * self.linear_vel

        self.pos.y += movement.y
        if tile_map.check_pos(self.pos) > 0:
            self.pos.y -= movement.y

        self.pos.x += movement.x
        if tile_map.check_pos(self.pos) > 0:
            self.pos.x -= movement.x

        if tile_map.check_pos(self.pos) == -1:
            event = pygame.event.Event(pygame.USEREVENT)
            pygame.event.post(event)
