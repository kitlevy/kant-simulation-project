import pygame
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

white = (255, 255, 255)
blue = (173, 216, 230)

ball_radius = 20
ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = random.randint(ball_radius, height - ball_radius)
ball_dx = random.choice([-5, 5])
ball_dy = random.choice([-5, 5])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
        ball_dx = -ball_dx
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
        ball_dy = -ball_dy
    
    if pygame.mouse.get_pressed()[0]==1:
        (ball_x,ball_y)=pygame.mouse.get_pos()
        ball_dx = random.choice([-5, 5])
        ball_dy = random.choice([-5, 5])

    screen.fill(white)

    pygame.draw.circle(screen, blue, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
