import pygame
import time
from settings import *
from src.menu import Menu
from src.level import Level
from src.player import Player

def main():
    pygame.init()
    screen_info = get_screen_info()
    WIDTH = screen_info["WIDTH"]
    HEIGHT = screen_info["HEIGHT"]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()
    menu = Menu(WIDTH, HEIGHT)
    level = Level(id=1)
    player = Player(WIDTH//2,HEIGHT//2, level.scale_y)
    state = "menu"
    
    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if state == "menu":
                new_state = menu.handle_event(event)
                if new_state == "game":
                    state = "game"
                    level.create_hitbox()
                if new_state == "exit":
                    running = False
        
        if state == "menu":
            menu.draw(screen)
        
        elif state == "game":
            start_time = time.time()
            player.update(keys, level.blocks)
            screen.fill((30,30,40))
            level.draw(screen)
            player.draw(screen)
            player.create_hitbox(screen, level.scale_y)
            level.draw_hitbox(screen)
            end_time = time.time()
            print("Delay: ", end_time - start_time)
            
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()