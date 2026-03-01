import pygame

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(None, 60)
        self.small = pygame.font.SysFont(None, 40)

        self.start_rect = pygame.Rect(width//2-100, 380, 200, 60)
        self.exit_rect = pygame.Rect(width//2-100, 460, 200, 60)

    def draw(self, screen):
        screen.fill((20, 20, 30))

        title = self.font.render("PLATFORMER", True, (240,240,240))
        screen.blit(title, (self.width//2 - title.get_width()//2, 280))

        pygame.draw.rect(screen, (70,160,70), self.start_rect)
        pygame.draw.rect(screen, (160,70,70), self.exit_rect)

        start_txt = self.small.render("START", True, (255,255,255))
        exit_txt = self.small.render("EXIT", True, (255,255,255))

        screen.blit(start_txt, (self.start_rect.centerx - start_txt.get_width()//2,
                                self.start_rect.centery - start_txt.get_height()//2))

        screen.blit(exit_txt, (self.exit_rect.centerx - exit_txt.get_width()//2,
                               self.exit_rect.centery - exit_txt.get_height()//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                return "game"
            if self.exit_rect.collidepoint(event.pos):
                return "exit"
        return "menu"