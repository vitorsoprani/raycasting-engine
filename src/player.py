import pygame


class Player():

    def __init__(self,
                 pos: pygame.Vector2 = pygame.Vector2(0, 0),
                 dir: pygame.Vector2 = pygame.Vector2(1, 0)):
        self.pos = pos
        self.dir = dir

        self.angular_vel = 0.1
        self.linear_vel = 5

    def draw(self, surface: pygame.Surface):
        color = "red"
        pygame.draw.circle(surface, color, self.pos, 10)
        pygame.draw.line(surface, color, self.pos, self.pos + (self.dir * 20))

    def update_dir(self, rotation_sign: int):
        self.dir.rotate_rad_ip(self.angular_vel * rotation_sign)

    def update_pos(self, movement_sign: int):
        self.pos += self.dir * self.linear_vel * movement_sign
