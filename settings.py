import pygame

def get_screen_info():
    screen_info = pygame.display.Info()
    return{
        "WIDTH": screen_info.current_w,
        "HEIGHT": screen_info.current_h
    }
HITBOX_VISIBLE = False
FPS = 60

GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_POWER = -10