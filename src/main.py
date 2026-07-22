#!/usr/bin/env python3

import pygame


WINDOW_SIZE = (640, 480)
FRAME_RATE  = 60

def main():
    pygame.init()
    display = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    running = True
    while running:
        # HANDLING INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # UPDATING


        # RENDERING
        display.fill("black")
        pygame.display.update()


        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == "__main__":
    main()

