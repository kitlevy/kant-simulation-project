import pygame
import numpy as np

#Ball class w/ wall collisions, other ball collisions
class Ball:

    def __init__(self,x,y,radius,dx,dy,color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.rad = radius
    
    def display(self):
        self.x+=self.dx
        self.y+=self.dy

        if self.x - self.rad <= 0 or self.x + self.rad >= width:
            self.dx = -self.dx
        if self.y - self.rad <= 0 or self.y + self.rad >= height:
            self.dy = -self.dy
        
        for ball in balls:
            if ball != self:
                d = np.sqrt((self.x-ball.x)**2+(self.y-ball.y)**2)
                if d<=self.rad+ball.rad:
                    self.dx = -self.dx
                    self.dy = -self.dy
        
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)


pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
white = (255, 255, 255)
blue = (173, 216, 230)

balls=[]
balls.append(Ball(100,100,20,np.random.choice([-4,4]),np.random.choice([-4,4]),blue))
balls.append(Ball(150,150,20,np.random.choice([-4,4]),np.random.choice([-4,4]),blue))
balls.append(Ball(200,200,20,np.random.choice([-4,4]),np.random.choice([-4,4]),blue))

#main pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    for ball in balls:
        ball.display()

    #constantly updating
    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
