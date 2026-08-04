import pygame

class Map():
    def __init__(self,
                 tile_size: int,
                 rows: int,
                 cols: int):
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols
        self.tiles: list[list[int]]

    def load_from_list(self, tiles: list[list[int]]):
        assert self.rows == len(tiles)
        assert self.cols == len(tiles[0])

        self.tiles = tiles.copy()

    def draw(self, surface: pygame.Surface):
        y_offset = 0
        for i in self.tiles:
            x_offset = 0

            for j in i:
                tile_rect = pygame.rect.Rect(x_offset,
                                             y_offset,
                                             self.tile_size,
                                             self.tile_size)
                if j == 0:
                    pygame.draw.rect(surface, "white", tile_rect)
                elif j == 1:
                    pygame.draw.rect(surface, "blue", tile_rect)
                pygame.draw.rect(surface, "black", tile_rect, 1)

                x_offset += self.tile_size

            y_offset += self.tile_size


    def log_tiles(self):
        for row in self.tiles:
            print(row)

