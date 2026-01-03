import math
import pygame
import random
import time


def gradientInterpolation(c0, c1, t) -> tuple:
    # t is in [0,1]
    # linear interpolation between two points c0 and c1
    final = []
    for v,w in zip(c0,c1):
        s = t*v + (1-t)*w
        final.append(s)
    return tuple(final)


#z_n+1=z_n^2 + c where c is any real number and z is any complex number
def mandelbrot():
    pass


def buildTree(surface,a,l,k,c0,a0=0,f0=1,b=4,c=4):
    #Angle,initial length, depth, initial coordinates, a0=0, f0 is a coefficient
    if k > 0 and l > 3:
        x,y = c0
        phi1 = a0
        c1fx = l*math.cos(phi1-math.pi/2)+x
        c1fy = l*math.sin(phi1-math.pi/2)+y
        if l > 10:
            pygame.draw.line(surface,(128,0,0),c0,(c1fx,c1fy),width=k//2)
        else:
            pygame.draw.line(surface,(0,240,0),c0,(c1fx,c1fy),width=k//2)
        buildTree(surface,a,l-b,k-1,(c1fx,c1fy),a0+a,b=b,c=c)
        buildTree(surface,a,l-c,k-1,(c1fx,c1fy),a0-a,b=b,c=c)
        #buildTree(surface,a,f0*l,k-1,(c1fx,c1fy),a0+a,f0=f0)
        #buildTree(surface,a,f0*l,k-1,(c1fx,c1fy),a0-a,f0=f0)


def sTriangle(surface,x,y,l,k,illum=False):
    
    def drawTriangle(c,l,k):
        if k > 0:
            x,y = c
            coordinates = list((l*math.cos(i*math.pi*2/n+t)+x,l*math.sin(i*math.pi*2/n+t)+y) for i in range(n))
            cTriangles = list((l*math.cos(i*math.pi*2/n-t)+x,l*math.sin(i*math.pi*2/n-t)+y) for i in range(n))
            pygame.draw.polygon(surface,(0,0,0),coordinates)
            if illum:
                pygame.draw.ellipse(surface,(0,220,0),(c[0]-l/2,c[1]-l/4,l,l/2),width=2)
                pygame.draw.circle(surface,(0,220,0),c,l/6,width=2)
                pygame.draw.circle(surface,(0,220,0),c,l/12)
            for triangle in cTriangles:
                drawTriangle(triangle,l/2,k-1)

    n = 3
    t = math.pi/2
    coordinates = list((l*math.cos(i*math.pi*2/n-t)+x,l*math.sin(i*math.pi*2/n-t)+y) for i in range(n))
    pygame.draw.polygon(surface,(255,255,255),coordinates)
    drawTriangle((x,y),l/2,k)


def collatzGrapher(upper, surface):
    # number upper bound
    visited = []
    graph = {}
    graphWeights = {}
    computedSegments = []
    graphLength = 0.7
    zoomFactor = 1
    MAX = 100000000000
    MAX_TRAVERSAL_DEPTH = 200
    depth = 0
    speed = 1
    unstable = []

    pointsOfInterest = [(3,1),
                        (3,7),
                        (5,7),
                        (8,8),
                        (6,10),
                        (3,11),
                        (5,11),
                        (3,13),
                        (11,13),
                        (6,14),
                        (10,14),
                        (3,17),
                        (10,18),
                        (3,23),
                        (8,24),
                        (6,34)]

    # Collatz conjecture uses a=3, b=1
    a = 3
    b = 1

    def construtGraphHelper(n,n0,d) -> None:
        if n in visited or n > MAX or d == 0:
            if n < MAX and d != 0:
                graph[n].append(n0)
            if n > MAX:
                if (a,b) not in unstable:
                    unstable.append((a,b))
                    print(unstable)
            return
        
        visited.append(n)
        graph[n] = [n0]
        construtGraphHelper(colFunc(n), n, d-1)

    def constructGraph():
        graph.clear()
        visited.clear()
        for i in range(1, upper+1):
            graph[0] = []
            construtGraphHelper(i,0,990)

    def computeSegment(n, c0, a0, cmod):
        mx, my = cmod
        cx = 0
        cy = 0
        x,y = c0
        a1 = a0

        if n % 2 == 0:
            a1 = a0 + 8.65
            cx = graphLength*math.log(n) * math.cos(math.radians(a1)) + x
            cy = graphLength*math.log(n) * math.sin(math.radians(a1)) + y
        else:
            a1 = a0 - 16
            cx = graphLength*math.log(n) * math.cos(math.radians(a1)) + x
            cy = graphLength*math.log(n) * math.sin(math.radians(a1)) + y
        
        if len(graphWeights.keys()) > 0:
            weight = graphWeights[n]
            t = weight / max(graphWeights.values())
            color = gradientInterpolation((10,10,10),(155,47,47),t)
            computedSegments.append(((x,y),(cx,cy),color,round(math.log(graphWeights[n]))))
            #pygame.draw.line(surface,color,(x+mx, y+my),(cx+mx, cy+my),width=round(math.log(graphWeights[n])))
        else:
            computedSegments.append(((x,y),(cx,cy),color,round(math.log(graphWeights[n]))))
            #pygame.draw.line(surface,(0,240,0),(x+mx, y+my),(cx+mx, cy+my))
        return (cx, cy, a1)

    def traverseGraph(n, c0, a0, d, visited2, cmod=(0,0)):
        if n in visited2 or d == 0:
            return
        
        nextNodes = graph[n]
        visited2.append(n)
        
        for node in nextNodes:
            if node != 0:
                nx, ny, a1 = computeSegment(node,c0,a0,cmod)
                traverseGraph(node, (nx, ny), a1, d-1, visited2, cmod)
    
    def traverseWeight(n, d, visited2):
        if n in visited2 or d == 0:
            graphWeights[n] = 1
            return 1
        
        nextNodes = graph[n]
        visited2.append(n)
        
        weight = 0
        for node in nextNodes:
            if node != 0:
                weight += traverseWeight(node, d-1, visited2)
        graphWeights[n] = max(weight,2)
        return max(weight,2)

    def drawGraph(depth):
        for i in range(min(depth,len(computedSegments))):
            c1,c0,color,w = computedSegments[i]
            x1,y1 = c1
            x0,y0 = c0
            pygame.draw.line(surface,color,((x1-cx)*zoomFactor+width/2, (y1-cy)*zoomFactor+height/2),((x0-cx)*zoomFactor+width/2, (y0-cy)*zoomFactor+height/2),width=w)

    def colFunc(n):
        if n % 2 == 0:
            return n / 2
        else:
            return a*n + b

    constructGraph()
    traverseWeight(1, MAX_TRAVERSAL_DEPTH+1, [])
    traverseGraph(1, (0,0), -90, MAX_TRAVERSAL_DEPTH, [])

    # For only displaying the points of interest and to look around
    index = 0
    paused = False
    cx = 0
    cy = 0
    while True:
        a,b = pointsOfInterest[index]
        ext_app()
        pygame.display.set_caption(f'Fractals: max = {len(computedSegments)}, drawn = {depth}, a = {a}, b = {b}')

        drawGraph(depth)

        if depth > len(computedSegments):
            depth = 0
            a,b = pointsOfInterest[index]
            constructGraph()
            traverseWeight(1, MAX_TRAVERSAL_DEPTH+1, [])
            computedSegments = []
            traverseGraph(1, (0,0), -90, MAX_TRAVERSAL_DEPTH, [])
            index += 1
            if index >= len(pointsOfInterest):
                index = 0
        
        pygame.display.update()
        clock.tick(300)
        screen.fill((0,0,0))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            paused = False if paused else True
            time.sleep(0.5)
        if not paused:
            depth += 1
        
        if keys[pygame.K_w]:
            cy -= speed
        elif keys[pygame.K_s]:
            cy += speed
        if keys[pygame.K_a]:
            cx -= speed
        elif keys[pygame.K_d]:
            cx += speed
        if keys[pygame.K_r]:
            zoomFactor += 0.01
        elif keys[pygame.K_f]:
            zoomFactor -= 0.01


def fern():
    a = 0.85
    b = 0.04

    f1 = [[0,0],
          [0,0.16]]
    
    f2 = [[a,b],
          [-b,a]]
    
    f3 = [[0.20,-0.26],
          [0.23,0.22]]
    
    f4 = [[-0.15,0.28],
          [0.26,0.24]]

    f1t = [0,0]
    f2t = [0,1.6]
    f3t = [0,1.6]
    f4t = [0,0.44]

    p1 = 0.01
    p2 = 0.85
    p3 = 0.07
    p4 = 0.07

    v = [0,0]

    def matMul(m,v):
        return [m[0][0]*v[0]+m[0][1]*v[1],m[1][0]*v[0]+m[1][1]*v[1]]

    def add(v1,v2):
        return [v1[0]+v2[0],v1[1]+v2[1]]

    def scrTranform(v):
        s = 80
        return (round(v[0]*s+width/2),round(v[1]*-1*s+height))
    
    x = 0
    t = 0.9999
    
    while True:
        ext_app()
        
        n = random.uniform(0,1)
        if n < p1:
            v = add(matMul(f1,v),f1t)
        elif n < p1+p2:
            v = add(matMul(f2,v),f2t)
        elif n < p1+p2+p3:
            v = add(matMul(f3,v),f3t)
        else:
            v = add(matMul(f4,v),f4t)
        
        c = scrTranform(v)
        screen.set_at(c,(240-round(240*t**x),round(240*t**x),0))
        x += 1

        pygame.display.update()
        clock.tick(1000000)

        if x == 90000:
            screen.fill((0,0,0))
            x = 0
            b = random.uniform(0,0.1)
            f2 = [[a,b],
                [-b,a]]



def ext_app():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def update_screen():
    pygame.display.update()
    clock.tick(10)
    screen.fill((0,0,0))


def main():
    counter = 0
    flipper = 1
    while True:
        ext_app()
        buildTree(screen,math.pi/12,70,16,(400,800),f0=0.8,c=6)
        #buildTree(screen,math.radians(counter),50,counter//2,(400,400),c=6)
        #sTriangle(screen,400,400,400,5,illum=True)
        update_screen()
        counter += flipper
        if counter > 30 or counter < 1:
            flipper*=-1


width = 1200
height = 800
pygame.init()
pygame.display.set_caption('Fractals')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
#fern()
#main()
collatzGrapher(2000, screen)
