import time
import pygame
from src.camera import Camera
from src.transformation_group import TransformationGroup
from settings import get_screen_info, FPS, HITBOX_VISIBLE
from src.menu import Menu
from src.level import Level
from src.player import Player

def main():
    pygame.init()
    screen_info = get_screen_info()
    WIDTH = screen_info["WIDTH"]
    HEIGHT = screen_info["HEIGHT"]
    camera = Camera(WIDTH, HEIGHT)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    sprites = TransformationGroup()
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()
    menu = Menu(WIDTH, HEIGHT)
    level = Level(id=1)
    player = Player(WIDTH//2,HEIGHT//2, level.scale_y, sprites)
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
                if new_state == "exit":
                    running = False

        if state == "menu":
            menu.draw(screen)

        elif state == "game":
            screen.fill((30,30,40))
            start_time = time.time()
            dt = clock.tick(FPS) / 1000

            player.update(keys, level.blocks, dt)
            camera.update(player)
            level.draw(screen, camera.offset_x, camera.offset_y)
            sprites.draw(screen, camera.offset_x, camera.offset_y)

            if HITBOX_VISIBLE:
                player.draw_hitbox(screen, camera.offset_x, camera.offset_y)
                level.draw_hitbox(screen, camera.offset_x, camera.offset_y)

            end_time = time.time()
            # print("Delay: ", round(end_time - start_time, 4))

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
