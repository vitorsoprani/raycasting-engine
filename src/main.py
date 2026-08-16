#!/usr/bin/env python3

import os
import pygame
from player import Player
from tile_map import Map
from raycaster import RayCaster

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = MAIN_DIR + "/../data/"
print(f"Data: {DATA_DIR}")

WINDOW_SIZE = (1280, 720)
FRAME_RATE  = 60

TILE_MAP = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

MOUSE_X_SENSITIVITY = 0.08
MOUSE_Y_SENSITIVITY = 1

MIN_HORIZON = int(WINDOW_SIZE[1] / 8)
MAX_HORIZON = WINDOW_SIZE[1] - MIN_HORIZON

FOV = 75
RESOLUTION = 400

def main():
    # pygame initializations:
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN | pygame.SCALED)
    display = pygame.display.get_surface()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # loadind resources:
    jumpscare_img = pygame.image.load(DATA_DIR + "images/scary.jpeg").convert()
    jumpscare_img = pygame.transform.scale(jumpscare_img, display.get_size())
    jumpscare_sound = pygame.mixer.Sound(DATA_DIR + "sounds/scary_scream.mp3")
    pygame.mixer.music.load(DATA_DIR + "sounds/scary_music.mp3")
    pygame.mixer.music.play(loops = -1)


    # engine initialization:
    tile_map = Map(50, 20, 20)
    tile_map.load_from_list(TILE_MAP)
    tile_map.log_tiles()
    minimap = pygame.Surface(tile_map.get_size())
    horizon = int(WINDOW_SIZE[1] / 2)

    player = Player(pygame.Vector2(75, 75))
    raycaster = RayCaster(tile_map, FOV, RESOLUTION)

    # command design pattern wannabe...
    # TODO: Better implementation of the pattern
    movement = {"horizontal": 0, "vertical": 0, "angular": 0}

    # flags
    show_map = False
    running = True
    jumpscare = False

    while running:
        # HANDLING INPUT
        movement["vertical"] = 0
        movement["horizontal"] = 0
        movement["angular"] = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_m:
                    if pygame.key.get_pressed()[pygame.K_RCTRL]:
                        show_map = not show_map
            if event.type == pygame.USEREVENT:
                jumpscare = True

        if jumpscare:
            print("SUSTO MUITO ASSUSTADOR")
            display.blit(jumpscare_img, (0, 0))
            pygame.display.update()
            jumpscare_sound.play()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement["vertical"] += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement["vertical"] -= 1
        if keys[pygame.K_a]:
            movement["horizontal"] -= 1
        if keys[pygame.K_d]:
            movement["horizontal"] += 1
        if keys[pygame.K_LEFT]:
            movement["angular"] -= 1
        if keys[pygame.K_RIGHT]:
            movement["angular"] += 1

        mouse_rel_mov = pygame.mouse.get_rel()
        movement["angular"] = int(mouse_rel_mov[0] * MOUSE_X_SENSITIVITY)
        horizon -= int(mouse_rel_mov[1] * MOUSE_Y_SENSITIVITY)
        if horizon > MAX_HORIZON:
            horizon = MAX_HORIZON

        if horizon < MIN_HORIZON:
            horizon = MIN_HORIZON

        # UPDATING
        player.update_dir(movement["angular"])
        player.update_pos(movement["vertical"], movement["horizontal"], tile_map)
        raycaster.cast_all(player.pos, player.dir)


        # RENDERING
        display.fill("black")
        raycaster.render_3d(display, horizon)

        if show_map:
            tile_map.draw(minimap)
            player.draw(minimap)
            raycaster.draw_all(minimap)
            display.blit(pygame.transform.scale(minimap, (200, 200)), (0, 0))

        pygame.display.update()


        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == "__main__":
    main()

