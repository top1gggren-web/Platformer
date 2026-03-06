import pytmx
import pygame
import math
from settings import get_screen_info

class Level:
    def __init__(self, id):
        self.id = id
        self.blocks = []
        self.textures = []
        self.old_offset = {"x":None,"y":None}
        self.level = pytmx.load_pygame(f"levels/map{self.id}.tmx", pixelalpha = True)
        screen_info = get_screen_info()
        WIDTH = screen_info["WIDTH"]
        HEIGHT = screen_info["HEIGHT"]
        rel_block_size = HEIGHT/20
        self.scale_y = rel_block_size/self.level.tileheight
        self.scaled_tile_width = math.ceil(self.level.tilewidth * self.scale_y)
        self.scaled_tile_height = math.ceil(self.level.tileheight * self.scale_y)
        self.new_x = 0 # int((WIDTH - self.scaled_tile_width * self.level.width)/2)
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
                    self.textures.append((x * self.scaled_tile_width, y * self.scaled_tile_height, tile))

    def draw(self, surface, offset_x, offset_y):
        for x, y, tile in self.textures:
            surface.blit(
                tile,
                (int(x - offset_x),
                int(y - offset_y))
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

    def draw_hitbox(self, screen, offset_x, offset_y):
        for block in self.blocks:
            moved_block = pygame.Rect(block.x - offset_x - self.new_x, block.y - offset_y, block.width, block.height)
            pygame.draw.rect(screen, (0,0,255), moved_block, 2)
        print(offset_x, offset_y)
