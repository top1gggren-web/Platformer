import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_y, group):
        super().__init__(group)
        
        self.images = {}
        for file_path in os.listdir("assets/images/"):
            if file_path.startswith("Mushroom"):
                image = pygame.image.load(f"assets/images/{file_path}")
                scaled_image_width = (image.get_width() * scale_y)/2
                scaled_image_height = (image.get_height() * scale_y)/2
                image_name = os.path.splitext(file_path)[0]
                self.images[image_name] = pygame.transform.scale(
                    image,
                    (int(scaled_image_width), int(scaled_image_height))
                )
                
        self.image = self.images["Mushroom_stay"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.curent_frame_i = 1
        self.animation_speed = 250
        self.animation_timer = 0
        self.state = "stay"

        self.accel = 0.5
        self.max_speed = 4
        self.jump_force = -13
        self.friction_ground = 0.5
        self.on_ground = False
        self.friction_air = 0.95
        self.max_fall = 12
        self.coyote_time = 0.08
        self.coyote_timer = 0
        self.jump_buffer = 0.08
        self.jump_buffer_timer = 0
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 1
        self.jump = -16
        self.gravity = 0.5
        self.rect.height = self.rect.height * 0.82

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (0,50,255), self.rect, 2, 1)

    def update(self, keys, collision_rects, dt):
        move = self.handle_input(keys)
        self.apply_horizontal_movement(move)
        self.apply_gravity()
        self.apply_timers(dt, keys)
        self.handle_jump(keys)
        self.handle_collisions(collision_rects)
        if self.animation_timer == self.animation_speed:
            self.animation_timer = 0
        self.handle_animation_states(dt)
        # print(self.animation_timer)
        print(self.vel_x)

    def handle_animation_states(self, dt):
        if self.state == "walking":
            self.animation_timer = min(dt*1000 + self.animation_timer, self.animation_speed)
            if self.vel_x > 0:
                if self.animation_speed == self.animation_timer:
                    self.curent_frame_i += 1
                if self.curent_frame_i > 2:
                    self.curent_frame_i = 1
                self.image = self.images[f"Mushroom_right_walking_{self.curent_frame_i}"]
            if self.vel_x < 0:
                if self.animation_speed == self.animation_timer:
                    self.curent_frame_i += 1
                if self.curent_frame_i > 2:
                    self.curent_frame_i = 1
                self.image = self.images[f"Mushroom_left_walking_{self.curent_frame_i}"]
        if self.state == "fall":
            self.image = self.images["Mushroom_fall"]
        if self.state == "fall_left":
            self.image = self.images["Mushroom_left_fall"]
        if self.state == "fall_right":
            self.image = self.images["Mushroom_right_fall"]
        if self.state == "stay":
            self.image = self.images["Mushroom_stay"]


    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall:
            self.vel_y = self.max_fall

    def handle_input(self, keys):
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.state = "walking"
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.state = "walking"
            move += 1
        if keys[pygame.K_SPACE]:
            self.state = "jump"
            self.jump_buffer_timer = self.jump_buffer
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.on_ground == False:
            self.state = "fall_left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.on_ground == False:
            self.state = "fall_right"
        if self.vel_x == 0 and self.on_ground == False:
            self.state = "fall"
        if not any(keys) and self.on_ground == True:
            self.state = "stay"

        return move

    def handle_collisions(self, collision_rects):
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
                    

    def handle_jump(self, keys):
        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jump_buffer_timer = 0
            self.coyote_timer = 0

        # variable jump (короткий стрибок)
        if not keys[pygame.K_SPACE] and self.vel_y < -3:
            self.vel_y *= 0.5

    def apply_horizontal_movement(self, move):
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

    def apply_timers(self, dt, keys):
        if self.on_ground:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer -= dt

        self.jump_buffer_timer -= dt

        
