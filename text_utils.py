import pygame
import pygame.freetype
from pygame import gfxdraw

def draw_smooth_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

def render_scaled_text(font, text, color, target_height, render_size=64):        
    surface, _ = font.render(text, fgcolor=color, size=render_size)
    glyph_height = font.get_sized_height(render_size)

    scale_ratio = target_height / glyph_height
    target_width = int(surface.get_width() * scale_ratio)
    target_height = int(surface.get_height() * scale_ratio)

    scaled_surface = pygame.transform.smoothscale(surface, (target_width, target_height))
    return scaled_surface

def draw_centered_text(font, surface, text, center_pos, color=(0, 0, 0), line_height=16):
    lines = text.splitlines()
    total_height = len(lines) * line_height
    start_y = center_pos[1] - total_height // 2

    for i, line in enumerate(lines):
        text_surface, _ = font.render(line, fgcolor=color)
        rect = text_surface.get_rect()
        rect.centerx = center_pos[0]
        rect.top = start_y + i * line_height
        surface.blit(text_surface, rect)

def draw_centered_text1(font, surface, text, center_pos, color = (0,0,0), line_height = 10):
        lines = text.splitlines()
        total_height = len(lines) * line_height
        start_y = center_pos[1] - total_height // 2

        for i, line in enumerate(lines):
            text_surface = render_scaled_text(font, line, color, line_height)
            rect = text_surface.get_rect()
            rect.center = (round(center_pos[0]), round(rect.centery))          
            rect.top = int(start_y + i * line_height)
            surface.blit(text_surface, rect)

def draw_centered_text2(font, surface, text, center_pos, line_height=10, color=(0, 0, 0)):
    lines = text.splitlines()
    total_height = len(lines) * line_height
    start_y = center_pos[1] - total_height // 2
    
    for i, line in enumerate(lines):
        # Render text directly at the desired size
        text_surface, text_rect = render_text(font, line, color, line_height)
        
        # Calculate position with proper pixel alignment
        rect = text_surface.get_rect()
        rect.center = (int(center_pos[0]), int(rect.centery))
        rect.top = int(start_y + i * line_height)
        
        # Make sure we're aligning to whole pixels
        rect.x = int(rect.x)
        rect.y = int(rect.y)
        
        surface.blit(text_surface, rect)
