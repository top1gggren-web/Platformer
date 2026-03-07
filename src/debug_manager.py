import pygame
from src.player import Player
from src.camera import Camera

class DebugManager:
    """DebugManager is responsible for managing debug information and rendering it on the screen."""  
    START_POS: tuple[int, int] = (10, 10)

    def __init__(self, debug_mode: bool = False, text_color: pygame.Color = None):
        if text_color is None:
            text_color = pygame.Color(0, 50, 0)
        self._font = pygame.font.SysFont("Arial", 16)
        self._enabled = debug_mode
        self._text_color = text_color

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @enabled.setter
    def text_color(self, value: pygame.Color):
        self._text_color = value

    def draw_info(self, screen: pygame.Surface, camera: Camera, player: Player, detailed: bool = False):
        """Draws debug information on the screen if debug mode is enabled."""
        if not self._enabled:
            return

        self._draw_camera_info(screen, camera)
        self._draw_player_info(screen, player, detailed=detailed)

    def _draw_camera_info(self, screen: pygame.Surface, camera: Camera):
        """Draws the camera's offset on the screen."""
        info_text = f"Camera Offset (x, y): ({camera.offset_x:.2f}, {camera.offset_y:.2f})"
        debug_text = self._font.render(info_text, True, self._text_color)
        screen.blit(debug_text, (self.START_POS[0], self.START_POS[1] + 20))

    def _draw_player_info(self, screen: pygame.Surface, player: Player, detailed: bool = False):
        """Draws the player's velocity and ground status on the screen."""
        info_text = (
            f"Position (x, y): ({player.rect.x:.2f}, {player.rect.y:.2f}) "
            f"| Velocity (x, y): ({player.vel_x:.2f}, {player.vel_y:.2f}) "
            f"| On Ground: {player.on_ground} | State: {player.state} "
        )
        if detailed:
            info_text += (
                f"| Animation Timer: {player.animation_timer:.2f} "
                f"| Current Frame Index: {player.curent_frame_i}"
            )
        debug_text = self._font.render(info_text, True, self._text_color)
        screen.blit(debug_text, self.START_POS)
