import pygame
class TransformationGroup(pygame.sprite.Group):
    def draw(self, surface, offset_x, offset_y):
        for sprite in self.sprites():
            moved_rect = pygame.Rect(sprite.rect.x - offset_x, sprite.rect.y - offset_y, sprite.rect.width, sprite.rect.height)
            x = moved_rect.centerx - sprite.image.get_width()//2
            y = moved_rect.bottom - sprite.image.get_height()
            surface.blit(
                sprite.image,(x, y))