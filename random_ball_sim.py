import pygame
import numpy as np

#Ball class w/ wall collisions,other ball collisions
class Ball:

    def __init__(self,x,y,radius,dx,dy,color):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.color=color
        self.rad=radius
        self.mass=np.pi*(self.rad**2)
    
    def setvelo(self,newdx,newdy):
        self.dx=newdx
        self.dy=newdy

    def getdist(self,x,y):
        return np.sqrt((self.x-x)**2+(self.y-y)**2)
    
    def checkcollisions(self,balls):
        #wall collisions
        if self.x-self.rad<=1:
            self.x=self.rad+1
            self.dx=-self.dx
        if self.x+self.rad>=width-1:
            self.x=width-self.rad-1
            self.dx=-self.dx
        if self.y-self.rad<=1:
            self.y=self.rad+1
            self.dy=-self.dy
        if self.y+self.rad>=height-1:
            self.y=height-self.rad-1
            self.dy=-self.dy

        #ball-to-ball collisions
        for ball in balls:
            if ball!=self:
                d=self.getdist(ball.x,ball.y)
                if d<=self.rad+ball.rad-1:
                    #fixing the overlap glitch
                    overlap=(self.rad+ball.rad-d+1)/2
                    tempdx=(self.x-ball.x)/d
                    tempdy=(self.y-ball.y)/d
                    self.x+=tempdx*overlap
                    self.y+=tempdy*overlap
                    ball.x-=tempdx*overlap
                    ball.y-=tempdy*overlap
                    #using that calc 3 + high school physics knowledge
                    p1=np.array([self.x,self.y])
                    p2=np.array([ball.x,ball.y])
                    v1=np.array([self.dx,self.dy])
                    v2=np.array([ball.dx,ball.dy])

                    r=p1-p2
                    n=r/np.sqrt(r.dot(r))
                    
                    relv=v1-v2
                    imp=2*(relv.dot(n))*(self.mass*ball.mass)/(self.mass+ball.mass)
                    
                    newv1=v1-(imp/self.mass)*n
                    newv2=v2+(imp/ball.mass)*n

                    self.setvelo(newv1[0],newv1[1])
                    ball.setvelo(newv2[0],newv2[1])

    
    def display(self):
        self.x+=self.dx
        self.y+=self.dy
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.rad)


pygame.init()

width,height=900,600
screen=pygame.display.set_mode((width,height))
white=(255,255,255)
blue=(173,216,230)

balls=[]
radius=20
velomag=4
while len(balls)<10:
    x=np.random.randint(radius,width-radius)
    y=np.random.randint(radius,height-radius)
    spaced=True
    for ball in balls:
        if ball.getdist(x,y)<radius:
            spaced=False
    if spaced:
        balls.append(Ball(x,y,radius,np.random.choice([-velomag,velomag])*np.random.rand(),np.random.choice([-velomag,velomag])*np.random.rand(),blue))
    
#main pygame loop
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill(white)

    for ball in balls:
        ball.checkcollisions(balls)
    
    for ball in balls:
        ball.display()

    #constantly updating
    pygame.display.flip()

    pygame.time.Clock().tick(100)

pygame.quit()
