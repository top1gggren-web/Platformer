import pygame
class TransformationGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            x = sprite.rect.centerx - sprite.image.get_width()//2
            y = sprite.rect.bottom - sprite.image.get_height()
            surface.blit(
                sprite.image,(x, y))