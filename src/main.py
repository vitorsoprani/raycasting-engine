#!/usr/bin/env python3

import pygame
from player import Player



WINDOW_SIZE = (640, 480)
FRAME_RATE  = 60

def main():
    pygame.init()
    display = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    player = Player(pygame.Vector2(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

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
        print(movement)


        # UPDATING
        player.update_dir(movement["angular"])
        player.update_pos(movement["linear"])


        # RENDERING
        display.fill("black")
        player.draw(display)
        pygame.display.update()


        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == "__main__":
    main()

