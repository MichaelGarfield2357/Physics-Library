import os
import pygame


def ext_app():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise TimeoutError("Video Viewer Closed")


def update_screen():
    pygame.display.update()
    clock.tick(FPS)
    screen.fill((0,0,0))


fileName = "GalaxyCollision2.txt"
circleRadius = 1
FPS = 30

with open(fileName,'r') as file:
    config = file.readline()
c = config.split()

match c[0]:

    case "!config":
        width,height = c[1:]
        width = int(width)
        height = int(height)
    
    case "!configC":
        width,height,circleRadius = c[1:]
        width = int(width)
        height = int(height)
        circleRadius = int(circleRadius)

    case _:
        print("Error loading config line")
        quit()

pygame.init()
pygame.display.set_caption('VideoPlayer')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
run = True

trace = True
traceColor = (0,255,0)
traceIndex = 1

with open(fileName,'r') as file:
    for line in file:
        ext_app()
        pygame.draw.line(screen,(126,126,126),(width/2,0),(width/2,height))
        pygame.draw.line(screen,(126,126,126),(0,height/2),(width,height/2))
        if line[0] != "!":
            particles = line.split("|")[:-1]
            for i,particle in enumerate(particles):
                x,y = particle.split(",")
                x = int(x)
                y = int(y)
                if trace and i == traceIndex:
                    pygame.draw.circle(screen,traceColor,(x,y),circleRadius+2)                    
                else:
                    pygame.draw.circle(screen,(255,255,255),(x,y),circleRadius)
        update_screen()
print("End of video")
