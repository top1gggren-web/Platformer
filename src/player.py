import pygame
import time


class Player:
    def __init__(self, x, y, scale_y):
        self.image = pygame.image.load("assets/images/Player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.accel = 0.5
        self.max_speed = 4
        self.jump_force = -10
        self.friction_ground = 0.5
        self.on_ground = False
        self.friction_air = 1
        self.max_fall = 3.5
        self.coyote_time = 0.08
        self.jump_buffer = 0.08
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 1
        self.jump = -16
        self.gravity = 0.4
        self.rect.height = 20
        self.rect.width = 10

        scaled_image_width = self.image.get_width() * scale_y
        scaled_image_height = self.image.get_height() * scale_y
        self.image = pygame.transform.scale(
            self.image, 
            (int(scaled_image_width), int(scaled_image_height))
        )

    def draw(self, surface):
        if self.image:
            surface.blit(
                self.image,
                (int(self.rect.x),
                int(self.rect.y))
            )
        
    def create_hitbox(self, surface, scale_y):
        self.rect.height = 32 * scale_y
        self.rect.width = 16 * scale_y
        pygame.draw.rect(surface, (255,0,0), self.rect, 2, 1)
        


    def update(self, keys, collision_rects):
        # ===== INPUT =====
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1

        # ===== ACCELERATION =====
        self.vel_x += move * self.accel

        # clamp speed
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        if self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed

        # ===== FRICTION =====
        if move == 0:
            if self.on_ground:
                self.vel_x *= self.friction_ground
            else:
                self.vel_x *= self.friction_air

            if abs(self.vel_x) < 0.05:
                self.vel_x = 0

        # ===== GRAVITY =====
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall:
            self.vel_y = self.max_fall

        # ===== TIMERS =====
        dt = time.clock.tick(60) / 1000
        if self.on_ground:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer -= dt

        self.jump_buffer_timer -= dt

        # jump press
        if keys[pygame.K_SPACE]:
            self.jump_buffer_timer = self.jump_buffer

        # ===== JUMP =====
        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jump_buffer_timer = 0
            self.coyote_timer = 0

        # variable jump (короткий стрибок)
        if not keys[pygame.K_SPACE] and self.vel_y < -3:
            self.vel_y *= 0.5

        # ===== MOVE X =====
        self.rect.x += self.vel_x
        for r in collision_rects:
            if self.rect.colliderect(r):
                if self.vel_x > 0:
                    self.rect.right = r.left
                elif self.vel_x < 0:
                    self.rect.left = r.right
                self.vel_x = 0

        # ===== MOVE Y =====
        self.rect.y += self.vel_y
        self.on_ground = False

        for r in collision_rects:
            if self.rect.colliderect(r):
                if self.vel_y > 0:
                    self.rect.bottom = r.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = r.bottom
                    self.vel_y = 0

        # перевірка зіткнення з землею
        self.on_ground = False
        for tile in collision_rects:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:  # падаємо вниз
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True