"""
S to pause
V to toggle velocity vector
G to toggle grid
P to trace
T to switch tools
"""

import pygame
import physics
import time
import math


def ext_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def update_screen(trace=False):
    pygame.display.update()
    clock.tick(120)
    #(245,222,179)(224,255,255)(0,0,0)
    if not trace:
        screen.fill((245,222,179))


class Point:

    def __init__(self,x,y,locked:bool):
        self.pos = [x,y]
        self.prev_pos = [x,y]
        self.locked = locked
        self.color = (0,0,155) if locked else (255,255,255)
        self.vector = [0,0]


class Stick:

    def __init__(self,conn:list,length,isSpring:bool):
        #Conn is the list of indices
        self.connections = conn
        self.length = length
        self.isSpring = isSpring
        self.color = (128,128,0) if isSpring else (169,169,169)
    
    def __repr__(self):
        return str(self.connections)


class Objects:

    def __init__(self,pts:list=[],conn:list=[],ground=5000,bound:tuple=None):
        self.vertices = pts
        self.connections = conn
        self.g = 9.8
        #Damping factors
        self.bounce = -1
        self.sprCoeff = 0.9
        self.sprStiff = 1
        # -inf for springs
        self.sprExpLim = -math.inf
        self.dR = 0
        self.ground = ground
        self.bounds = bound
        #Vector drawing
        self.vecMag = 100
        self.vecScale = 10
    
    def addPoint(self,x,y,locked):
        self.vertices.append(Point(x,y,locked))
    
    def addConnection(self,indices:list,isSpring:bool):
        dist = physics.Vector(*physics.VectorSubtract(self.vertices[indices[0]].pos,self.vertices[indices[1]].pos))[0]
        self.connections.append(Stick(indices,dist,isSpring))
    
    def step(self,dt=0.01,dR=10):
        self.dR = dR
        #dt: precision
        #dR: steps in the future
        for _ in range(dR):
            for point in self.vertices:
                if not point.locked:
                    prevPos = point.pos

                    point.vector = list(physics.VectorSubtract(point.pos,point.prev_pos))
                    if point.pos[1] > self.ground:
                        point.pos[1] = self.ground
                        point.vector[1] *= self.bounce
                    if self.bounds:
                        if point.pos[0] < self.bounds[0]:
                            point.pos[0] = self.bounds[0]
                            point.vector[0] *= self.bounce
                        elif point.pos[0] > self.bounds[1]:
                            point.pos[0] = self.bounds[1]
                            point.vector[0] *= self.bounce
                    point.pos = list(physics.VectorAddition(point.vector,point.pos))
                    
                    #Gravity
                    point.pos[1] += self.g*(dt**2)
                    point.prev_pos = prevPos
            
            for stick in self.connections:
                if stick.isSpring:
                    connA,connB = stick.connections
                    connA = self.vertices[connA]
                    connB = self.vertices[connB]
                    nVec = physics.normalize(physics.VectorSubtract(connA.pos,connB.pos))
                    a = self.sprStiff*(physics.Vector(*physics.VectorSubtract(connA.pos,connB.pos))[0]-stick.length)
                    if a > self.sprExpLim:
                        if not connA.locked:
                            connA.pos[0] -= (nVec[0]*(a))*(dt**2)
                            connA.pos[1] -= (nVec[1]*(a))*(dt**2)
                        if not connB.locked:
                            connB.pos[0] += (nVec[0]*(a))*(dt**2)
                            connB.pos[1] += (nVec[1]*(a))*(dt**2)
                else:
                    connA,connB = stick.connections
                    connA = self.vertices[connA]
                    connB = self.vertices[connB]
                    stickCenter = list(physics.VectorAddition(connA.pos,connB.pos))
                    stickCenter[0] /= 2
                    stickCenter[1] /= 2
                    nVec = physics.normalize(physics.VectorSubtract(connA.pos,connB.pos))
                    if not connA.locked:
                        connA.pos = [stickCenter[0]+(stick.length/2)*nVec[0],stickCenter[1]+(stick.length/2)*nVec[1]]
                    if not connB.locked:
                        connB.pos = [stickCenter[0]-(stick.length/2)*nVec[0],stickCenter[1]-(stick.length/2)*nVec[1]]
    
    def draw(self,surf,trace=False):
        if trace:
            for point in self.vertices:
                pygame.draw.circle(surf,point.color,point.pos,1)
        else:
            for stick in self.connections:
                conn = stick.connections
                pygame.draw.line(surf,stick.color,self.vertices[conn[0]].pos,self.vertices[conn[1]].pos,width=2)
            for point in self.vertices:
                pygame.draw.circle(surf,point.color,point.pos,7)
    
    def drawVector(self,surf):
        for point in self.vertices:
            vec = physics.VectorAddition(point.pos,
            physics.Scale(point.vector,self.dR*self.vecScale))
            mag = physics.Vector(*physics.Scale(point.vector,self.dR*self.vecScale))[0]
            grad = mag/self.vecMag
            red = round(255*grad)
            if red > 255:
                red = 255
            elif red < 0:
                red = 0
            green = round(255*(1-grad))
            if green > 255:
                green = 255
            elif green < 0:
                green = 0
            pygame.draw.line(surf,(red,green,0),point.pos,vec,width=2)
    
    def check(self,x,y,lock=False,delete=False,moveTo=None):
        for i,pt in enumerate(self.vertices):
            dist = physics.Vector(*physics.VectorSubtract((x,y),pt.pos))[0]
            if abs(dist) <= 7:
                if lock:
                    if pt.locked:
                        pt.locked = False
                        pt.color = (255,255,255)
                    else:
                        pt.locked = True
                        pt.color = (0,0,155)
                if delete:
                    self.vertices.remove(pt)
                    pt_to_remove = []
                    for conn in self.connections:
                        if i in conn.connections:
                            pt_to_remove.append(conn)
                        else:
                            if conn.connections[0] > i:
                                conn.connections[0] -= 1
                            if conn.connections[1] > i:
                                conn.connections[1] -= 1
                    for pt in pt_to_remove:
                        self.connections.remove(pt)
                if moveTo:
                    pt.pos = moveTo
                    pt.prev_pos = moveTo
                return i
        return None


def drawCloth(nodesX,nodesY,sep):
    points = []
    for y in range(nodesY):
        for x in range(nodesX):
            points.append(Point(x*sep,y*sep,False))
    sticks = []
    for i in range(nodesY):
        for t in range(nodesX-1):
            sticks.append(Stick([t+i*nodesX,t+1+i*nodesX],sep))
    for i in range(nodesX):
        for t in range(nodesY-1):
            sticks.append(Stick([i+t*nodesX,i+(t+1)*nodesX],sep))
    return points,sticks


def main():
    #Tracing
    trace = False

    #Grid: 42 for 1 cm
    GRIDTICKS = 20
    drawGrid = False

    obj = Objects(ground=height,bound=(0,width))
    start = False
    drawPoint = 0
    connStart = None
    drawVector = True
    MAXTOOL = 4
    toolList = ['Place','Connect','Connect Spring','Delete','Move']
    while True:
        #draw grid
        if drawGrid:
            for x in range(math.floor(width/GRIDTICKS)):
                if x % 5 == 0:
                    pygame.draw.line(screen,(140,140,140),(x*GRIDTICKS,0),(x*GRIDTICKS,height),width=2)
                else:
                    pygame.draw.line(screen,(110,110,110),(x*GRIDTICKS,0),(x*GRIDTICKS,height))
            
            for y in range(math.floor(height/GRIDTICKS)):
                if y % 5 == 0:
                    pygame.draw.line(screen,(140,140,140),(0,y*GRIDTICKS),(width,y*GRIDTICKS),width=2)
                else:
                    pygame.draw.line(screen,(110,110,110),(0,y*GRIDTICKS),(width,y*GRIDTICKS))

        pygame.display.set_caption(f"Tool: {toolList[drawPoint]} [PAUSED]"if not start else f"Tool: {toolList[drawPoint]}")
        ext_game()
        if start:
            #choose dt and dR here
            #Cloth sim: dt=0.1, dR=5 1:1
            obj.step(dt=0.01,dR=10)
        obj.draw(screen,trace=trace if start else False)
        if drawVector:
            obj.drawVector(screen)

        key = pygame.key.get_pressed()
        #S toggle pause
        if key[pygame.K_s]:
            if start:
                start = False
                time.sleep(0.2)
            else:
                start = True
                time.sleep(0.2)
        
        #V toggle velocity vector
        if key[pygame.K_v]:
            if drawVector:
                drawVector = False
                time.sleep(0.2)
            else:
                drawVector = True
                time.sleep(0.2)    
        
        #G toggle grid
        if key[pygame.K_g]:
            if drawGrid:
                drawGrid = False
                time.sleep(0.2)
            else:
                drawGrid = True
                time.sleep(0.2)
        
        #P toggle trace
        if key[pygame.K_p]:
            if trace:
                trace = False
                time.sleep(0.2)
            else:
                trace = True
                time.sleep(0.2)
        
        #T switches tools
        if key[pygame.K_t]:
            time.sleep(0.2)
            drawPoint += 1
            connStart = None
            if drawPoint > MAXTOOL:
                drawPoint = 0
        
        if pygame.mouse.get_pressed()[0]:
            if drawPoint == 0:
                if obj.check(*pygame.mouse.get_pos(),lock=True) is None:
                    obj.addPoint(*pygame.mouse.get_pos(),False)
                time.sleep(0.2)
            elif drawPoint == 1 or drawPoint == 2:
                if connStart is not None:
                    connPoint = obj.check(*pygame.mouse.get_pos())
                    if connPoint is not None and connPoint != connStart:
                        obj.addConnection([connStart,connPoint],False if drawPoint==1 else True)
                        connStart = None
                    else:
                        connStart = None
                else:
                    connStart = obj.check(*pygame.mouse.get_pos())
                    time.sleep(0.05)
            elif drawPoint == 3:
                obj.check(*pygame.mouse.get_pos(),delete=True)
            elif drawPoint == 4:
                obj.check(*pygame.mouse.get_pos(),moveTo=pygame.mouse.get_pos())
        
        if connStart is not None:
            pygame.draw.line(screen,(0,155,0),obj.vertices[connStart].pos,pygame.mouse.get_pos())
        update_screen(trace=trace if start else False)


if __name__ == '__main__':
    pygame.init()
    width = 1000
    height = 600
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    main()



