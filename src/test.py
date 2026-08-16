import pygame
from tile_map import Tile

img = pygame.image.load("./data/images/tiles/1.png")
tile = Tile(1, img)

for i in range(tile.image.get_width()):
    print(i)
    print(i/32)
    texture = tile.get_texture(i / 32)
    pygame.image.save(texture, "test_images/" + str(i) + ".png")
