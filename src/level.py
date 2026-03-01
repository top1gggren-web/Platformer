import pytmx
import pygame
import math
from settings import get_screen_info

class Level:
    TILE_SIDE = 16

    def __init__(self, id):
        self.id = id
        self.blocks = []
        self.textures = []
        self.level = pytmx.load_pygame(f"levels/level{self.id}.tmx", pixelalpha = True)
        screen_info = get_screen_info()
        WIDTH = screen_info["WIDTH"]
        HEIGHT = screen_info["HEIGHT"]
        self.scale_y = HEIGHT/(self.level.height*self.level.tileheight)
        self.scaled_tile_width = math.ceil(self.level.tilewidth * self.scale_y)
        self.scaled_tile_height = math.ceil(self.level.tileheight * self.scale_y)
        self.new_x = int((WIDTH - self.scaled_tile_width * self.level.width)/2)
        print("new_x:", self.new_x)
        self.init_tiles()
        self.init_hitboxes()

    def init_tiles(self):
        for layer in self.level.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    tile = self.level.get_tile_image_by_gid(gid)
                    tile = pygame.transform.scale(
                        tile,
                        (int(self.scaled_tile_width), int(self.scaled_tile_height))
                    )
                    self.textures.append((x * self.scaled_tile_width + self.new_x, y * self.scaled_tile_height, tile))

    def draw(self, surface):
        for x, y, tile in self.textures:
            surface.blit(
                tile,
                (int(x),
                int(y))
            )

    def init_hitboxes(self):
        for layer in self.level.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    tile = self.level.get_tile_image_by_gid(gid)
                    if tile:
                        if self.level.get_tile_properties_by_gid(gid)["has_collision"]:
                            block_rect = pygame.Rect(x * self.scaled_tile_width + self.new_x, y * self.scaled_tile_height, self.scaled_tile_width, self.scaled_tile_height)
                            self.blocks.append(block_rect)

    def draw_hitbox(self, screen):
        for block in self.blocks:
            pygame.draw.rect(screen, (0,0,255), block, 2)