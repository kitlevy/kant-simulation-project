import pygame
import pygame.freetype

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

font = pygame.freetype.Font("assets/FreightMicro.ttf", 8)
font.pad = True
font.strong = True
font.origin = True

running = True
while running:
    screen.fill((255, 255, 255))
    font.render_to(screen, (100, 100), "Visualizing Kant’s Categorical Imperative", (0, 0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(30)
pygame.quit()
