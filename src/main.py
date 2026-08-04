#!/usr/bin/env python3

import pygame
from player import Player
from tile_map import Map
from ray import Ray


WINDOW_SIZE = (750, 750)
FRAME_RATE  = 60
TILE_MAP = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def main():
    pygame.init()
    display = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    tile_map = Map(50, 15, 15)
    tile_map.load_from_list(TILE_MAP)
    tile_map.log_tiles()

    player = Player(pygame.Vector2(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
    ray = Ray(player.pos, player.dir)

    # command design pattern wannabe...
    # TODO: Better implementation of the pattern
    movement = {"linear": 0, "angular": 0}

    running = True
    while running:
        # HANDLING INPUT
        movement["linear"] = 0
        movement["angular"] = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement["linear"] += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement["angular"] -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement["linear"] -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement["angular"] += 1


        # UPDATING
        player.update_dir(movement["angular"])
        player.update_pos(movement["linear"])
        ray.cast(tile_map)


        # RENDERING
        display.fill("black")
        tile_map.draw(display)
        player.draw(display)
        ray.draw(display)
        pygame.display.update()


        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == "__main__":
    main()

