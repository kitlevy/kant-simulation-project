import pygame
import pygame.freetype

def render_scaled_text(font, text, color, target_height):
        render_size = 208  #rendering large then scaling down for quality
        surface, _ = font.render(text, fgcolor=color, size=render_size)

        scale_ratio = target_height / surface.get_height()
        target_width = int(surface.get_width() * scale_ratio)

        scaled_surface = pygame.transform.smoothscale(surface, (target_width, target_height))
        return scaled_surface

def draw_centered_text(font, surface, text, center_pos, color = (0,0,0), line_height = 10):
        lines = text.splitlines()
        total_height = len(lines) * line_height
        start_y = center_pos[1] - total_height // 2

        for i, line in enumerate(lines):
            text_surface = render_scaled_text(font, line, color, line_height)
            rect = text_surface.get_rect()
            rect.centerx = center_pos[0]
            rect.top = start_y + i * line_height
            surface.blit(text_surface, rect)
