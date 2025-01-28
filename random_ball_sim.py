import pygame
import numpy as np

#basic ball class
class Ball:

    def __init__(self,x,y,radius,dx,dy,state):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.state=state
        self.rad=radius
        self.mass=np.pi*(self.rad**2)
        if self.state=='S':
            self.color=uninfected
        elif self.state=='I':
            self.color=infected
        elif self.state=='R':
            self.color=uninfected
    
    def setvelo(self,newdx,newdy):
        self.dx=newdx
        self.dy=newdy

    def getdist(self,x,y):
        return np.sqrt((self.x-x)**2+(self.y-y)**2)
    
    def checkwallcollisions(self):
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

    def checkballcollisions(self,balls):
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

        if self.state=='S':
            self.color=uninfected
        elif self.state=='I':
            self.color=infected
        elif self.state=='R':
            self.color=uninfected
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.rad)


class InfectiousBall(Ball):
    def infect(self,prob):
        if np.random.rand()<prob:
            return 'I'
        return 'S'

    def checkballcollisions(self,balls):
        #ball-to-ball collisions
        for ball in balls:
            if ball!=self:
                d=self.getdist(ball.x,ball.y)
                if d<=self.rad+ball.rad-1:
                    #changing color if ball touches red ball
                    if ball.state=='I' and self.state=='S':
                        self.state=self.infect(infectionprob)
                    elif ball.state=='S' and self.state=='I':
                        ball.state=ball.infect(infectionprob)
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

                   



pygame.init()

width,height=900,600
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Interacting Balls")
white=(255,255,255)
blue=(173,216,230)
red=(255,0,59)

uninfected=blue
infected=red
infectionprob=0.8

balls=[]
radius=10
velomag=4
ballcount=20


while len(balls)<ballcount:
    x=np.random.randint(radius,width-radius)
    y=np.random.randint(radius,height-radius)
    spaced=True
    for ball in balls:
        if ball.getdist(x,y)<radius:
            spaced=False
    if spaced:
        balls.append(InfectiousBall(x,y,radius,np.random.choice([-velomag,velomag])*np.random.rand(),np.random.choice([-velomag,velomag])*np.random.rand(),'S'))
while len(balls)<ballcount+1:
    x=np.random.randint(radius,width-radius)
    y=np.random.randint(radius,height-radius)
    spaced=True
    for ball in balls:
        if ball.getdist(x,y)<radius:
            spaced=False
    if spaced:
        balls.append(InfectiousBall(x,y,radius,np.random.choice([-velomag,velomag])*np.random.rand(),np.random.choice([-velomag,velomag])*np.random.rand(),'I'))

    
#main pygame loop
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill(white)

    for ball in balls:
        ball.checkwallcollisions()
        ball.checkballcollisions(balls)
    
    for ball in balls:
        ball.display()

    #constantly updating
    pygame.display.flip()

    pygame.time.Clock().tick(100)

pygame.quit()
