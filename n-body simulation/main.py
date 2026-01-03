import pygame
import math
import random
import time

G = 6.6743*(10**-11)
#A small number to dampen forces
EPSILON = 0
#A small number to do something
EPSISILON = 0.0000000000000000000001

def graviF(x1,y1,x2,y2,m1,m2):
    return G*m1*m2*(x2-x1)/(math.sqrt((x2-x1)**2+(y2-y1)**2+EPSILON**2)**3), G*m1*m2*(y2-y1)/(math.sqrt((x2-x1)**2+(y2-y1)**2+EPSILON**2)**3)


def fx(v):
    return v[0]


def fy(v):
    return v[1]


class Node:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.m = 0
        self.width = 0
        self.child = []
    
    def __repr__(self):
        return str(self.child)


class BarnesHut:

    def __init__(self,particles:list,field_length,field_height,alpha,beta):
        #Note: Anything outside the field length and field height will not be included in the calculation
        self.particles = particles
        self.l = field_length
        self.h = field_height
        self.theta = 0.7
        self.alpha = alpha
        self.beta = beta
    
    def update(self,screen):
        BHtree = Node()
        for particle in self.particles:
            BHtree = self.BHconstruct(BHtree,particle,0,0,self.l,self.h,screen)
        for particle in self.particles:
            gx,gy = self.upt_force(particle,BHtree)
            pygame.draw.circle(screen,(255,255,250),(particle.x*alpha,particle.y*alpha),2)
            particle.vx += gx/particle.m
            particle.vy += gy/particle.m
            particle.x += particle.vx
            particle.y += particle.vy

    def upt_force(self,p,t):
        if t != p:
            if type(t) == Particle:
                return graviF(p.x*self.beta,p.y*self.beta,t.x*self.beta,t.y*self.beta,p.m,t.m)
            else:
                d = math.sqrt((t.x-p.x)**2+(t.y-p.y)**2)
                s = t.width
                if s/(d+EPSISILON) < self.theta or len(t.child)==0:
                    return graviF(p.x*self.beta,p.y*self.beta,t.x*self.beta,t.y*self.beta,p.m,t.m)
                else:
                    tgx = 0
                    tgy = 0
                    for i in range(4):
                        gx,gy = self.upt_force(p,t.child[i])
                        tgx += gx
                        tgy += gy
                    return (tgx,tgy)
        return (0,0)

    def BHconstruct(self,node,particle,x,y,l,w,screen):
        
        #TODO: quadtree visualization
        #pygame.draw.rect(screen,(0,220,0),(x,y,l,w),width=1)

        newNode = Node()

        #If there is a particle in node, subdivide
        if type(node) == Particle and self.contains(particle.x,particle.y,(x,y,l,w)):
            #Subdivide
            #Inserts an already existing particle into one of the quadrants
            nw = self.BHconstruct(Node(),node,x,y,l/2,w/2,screen)
            ne = self.BHconstruct(Node(),node,x+l/2,y,l/2,w/2,screen)
            sw = self.BHconstruct(Node(),node,x,y+w/2,l/2,w/2,screen)
            se = self.BHconstruct(Node(),node,x+l/2,y+w/2,l/2,w/2,screen)

            #Removes old particle
            node.child = [nw,ne,sw,se]

            #Inserts b
            nw = self.BHconstruct(node.child[0],particle,x,y,l/2,w/2,screen)
            ne = self.BHconstruct(node.child[1],particle,x+l/2,y,l/2,w/2,screen)
            sw = self.BHconstruct(node.child[2],particle,x,y+w/2,l/2,w/2,screen)
            se = self.BHconstruct(node.child[3],particle,x+l/2,y+w/2,l/2,w/2,screen)

            m = nw.m+ne.m+sw.m+se.m
            cgx = (nw.x*nw.m+ne.x*ne.m+sw.x*sw.m+se.x*se.m)/(m+EPSISILON)
            cgy = (nw.y*nw.m+ne.y*ne.m+sw.y*sw.m+se.y*se.m)/(m+EPSISILON)
            newNode.x = cgx
            newNode.y = cgy
            newNode.m = m
            newNode.width = max(l,w)
            newNode.child = [nw,ne,sw,se]
            return newNode
        #If this is an internal node
        elif type(node) != Particle and len(node.child) != 0:
            nw = self.BHconstruct(node.child[0],particle,x,y,l/2,w/2,screen)
            ne = self.BHconstruct(node.child[1],particle,x+l/2,y,l/2,w/2,screen)
            sw = self.BHconstruct(node.child[2],particle,x,y+w/2,l/2,w/2,screen)
            se = self.BHconstruct(node.child[3],particle,x+l/2,y+w/2,l/2,w/2,screen)
        
            m = nw.m+ne.m+sw.m+se.m
            cgx = (nw.x*nw.m+ne.x*ne.m+sw.x*sw.m+se.x*se.m)/(m+EPSISILON)
            cgy = (nw.y*nw.m+ne.y*ne.m+sw.y*sw.m+se.y*se.m)/(m+EPSISILON)
            newNode.x = cgx
            newNode.y = cgy
            newNode.m = m
            newNode.width = max(l,w)
            newNode.child = [nw,ne,sw,se]
            return newNode
        #If the node is empty and node contains particle
        elif self.contains(particle.x,particle.y,(x,y,l,w)) and len(node.child)==0:
            return particle
        return node
    
    @staticmethod
    def contains(x,y,rect:tuple):
        #Rect:(x,y,l,w)
        if rect[0] <= x < rect[0]+rect[2]:
            if rect[1] <= y < rect[1]+rect[3]:
                return True
        return False


class Particle:

    def __init__(self,x,y,m,vx=0,vy=0):
        self.x = x
        self.y = y
        self.m = m
        self.vx = vx
        self.vy = vy
    
    def __repr__(self):
        return str(f"particle at: {self.x,self.y} with mass: {self.m}")
    
    def fg(self,particles):
        return map(self.graviF2,particles)
    
    def graviF2(self,p2):
        if p2 is not self:
            return G*self.m*p2.m*(p2.x-self.x)/(math.sqrt((p2.x-self.x)**2+(p2.y-self.y)**2+EPSILON**2)**3), G*self.m*p2.m*(p2.y-self.y)/(math.sqrt((p2.x-self.x)**2+(p2.y-self.y)**2+EPSILON**2)**3)
        else:
            return 0,0


def galaxy(star:Particle,min_weight,max_weight,radius,num_of_particles,clockwise=True,vix=0,viy=0,mindist=10):
    #Use beta=1 and episilon=0
    star.vx = vix
    star.vy = viy
    g = [star]
    rot = 1
    if clockwise:
        rot = -1
    for _ in range(num_of_particles):
        r = random.uniform(mindist,radius)
        phi = random.uniform(0,2*math.pi)
        v = math.sqrt((G*star.m)/r)
        vx = v*math.cos(phi+(math.pi*rot/2))+vix
        vy = v*math.sin(phi+(math.pi*rot/2))+viy
        g.append(Particle(star.x+r*math.cos(phi),star.y+r*math.sin(phi),random.uniform(min_weight,max_weight),vx,vy))
    return g


def ringWithNBodies(c:tuple,n,m,r):
    bodies = []
    mass = m/(n-1)
    dTheta = 2*math.pi/n
    cx,cy = c
    for t in range(n):
        x = r*math.cos(dTheta*t)
        y = r*math.sin(dTheta*t)
        v = math.sqrt((G*m)/(4*r))
        vx = v*math.cos(dTheta*t+(math.pi/2))
        vy = v*math.sin(dTheta*t+(math.pi/2))
        bodies.append(Particle(x+cx,y+cy,mass,vx,vy))
    return bodies


def ext_app():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def update_screen():
    pygame.display.update()
    clock.tick(15)
    screen.fill((0,0,0))


#Main loop
#Logging files
logFile = "GalaxyFormation.txt"
isLogFile = False
logFileLine = ''
logStart = time.time()
numLogLines = 0

width = 800
height = 800

if isLogFile:
    if input(f"Logging in the file named: {logFile}? (Y or N)") == "Y":
        with open(logFile,'w') as f:
            f.write(f"!config {width} {height} \n")
    else:
        raise ValueError("Logging in file was not allowed")

maxsize = 800
alpha = height/maxsize
#distance multiplier
beta = 1

pygame.init()
pygame.display.set_caption('Aperture Science Gravity Simulator 2.0')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))

#testing
particles = ringWithNBodies((400,400),100,10**12,150)
BHparticles = BarnesHut(particles,width*(1/alpha),height*(1/alpha),alpha,beta)
while True:
    ext_app()
    pygame.draw.line(screen,(136,136,136),(width/2,0),(width/2,height))
    pygame.draw.line(screen,(136,136,136),(0,height/2),(width,height/2))
    #Unapproximated Euler integration (brute force)
    #'''
    for particle in particles:
        Fx = 0
        Fy = 0

        fog = list(particle.fg(particles))
        fog2 = fog[:]
        Fx = math.fsum(map(fx,fog))
        Fy = math.fsum(map(fy,fog2))

        drawX = round(particle.x*alpha)
        drawY = round(particle.y*alpha)
        pygame.draw.circle(screen,(255,255,255),(drawX,drawY),1)
        
        #Log file
        if 0<drawX<width and 0<drawY<height:
            logFileLine += f'{drawX},{drawY}|'
        
        particle.vx += Fx/particle.m
        particle.vy += Fy/particle.m
        particle.x += particle.vx
        particle.y += particle.vy
    #'''
    pygame.display.set_caption(str(clock.get_fps()))
    #BHparticles.update(screen)

    #TODO: logfiles only works with brute force
    if isLogFile:
        t2 = time.time()
        with open(logFile,'a') as f:
            if len(logFileLine) != 0:
                numLogLines += 1
                f.write(logFileLine+"\n")
                print(f'[PARTICLE POS LOGGED SUCCESSFULLY] Time elapsed: {t2-logStart} s, video length(30fps): {numLogLines/30}.')
            else:
                print(f'[ERROR LOGGING POS] Time elapsed: {t2-logStart}, No position to log.')
    
    logFileLine = ''
    update_screen()
