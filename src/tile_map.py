import pygame
import os

class Tile():
    # TODO: make all tiles from the same tipe refer to the same object.
    # there is no reason to load one for each map position
    def __init__(self, id: int, image: pygame.Surface):
        self.id = id
        self.image = image

class Map():
    def __init__(self,
                 tile_size: int,
                 rows: int,
                 cols: int):
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols
        self.tiles: list[list[Tile]] = []

    def load_from_list(self, tiles: list[list[int]], tiles_path: str):
        assert self.rows == len(tiles)
        assert self.cols == len(tiles[0])

        loaded_tiles: dict[int, Tile] = {}
        for file in os.listdir(tiles_path):
            tile_img = pygame.image.load(tiles_path + "/" + file).convert()
            tile_img = pygame.transform.scale(tile_img,
                                              (self.tile_size, self.tile_size))
            tile_id = int(os.path.splitext(file)[0])
            loaded_tiles[tile_id] = Tile(tile_id, tile_img)

        for row in tiles:
            self.tiles.append([loaded_tiles[tile_id] for tile_id in row])

    def draw(self, surface: pygame.Surface):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                surface.blit(tile.image,
                             (j * self.tile_size, i * self.tile_size))

    def log_tiles(self):
        for row in self.tiles:
            print(row)

    def get_size(self):
        return (self.cols * self.tile_size, self.rows * self.tile_size)

    def check_pos(self, pos: pygame.Vector2):
        tile_y = int(pos.y / self.tile_size)
        tile_x = int(pos.x / self.tile_size)

        return self.tiles[tile_y][tile_x].id

    def get_tile(self, pos):
        tile_y = int(pos.y / self.tile_size)
        tile_x = int(pos.x / self.tile_size)

        return self.tiles[tile_y][tile_x]

