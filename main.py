from math import pi
import random
import os 
import sys
import math
assert sys.version_info >= (2, 5)
try:

  import pygame
except ImportError:
  print("Pygame not installed. Please install before running program.")
  exit()
import particle

(width, height) = (624,468)
screen = pygame.display.set_mode((width,height))
pygame.font.init()
myfont = pygame.font.SysFont('Sans Serif', 30)

pygame.display.set_caption('Springs')
paused = False
running = True
uni = particle.envi((width, height))
uni.color = (255,255,255)
uni.addFunctions(['move', 'bounce', 'collide', 'drag', 'accelerate'])
mypar = []
for p in range(9):
  particle = uni.addParticle(mass=100, size=16, speed=2, elasticity=1, color=(20,40,200))
  mypar.append(particle)
uni.addSpring(0,1, length=100, strength=0.5)
uni.addSpring(1,2, length=100, strength=0.1)
uni.addSpring(2,0, length=80, strength=0.05)
#
uni.addSpring(5,6,length=100,strength=0.4)
uni.addSpring(6,7,length=100,strength=0.4)
uni.addSpring(7,8,length=100,strength=0.4)
uni.addSpring(8,5,length=100,strength=0.4)
uni.addSpring(7,5,length=100,strength=0.4)
uni.addSpring(8,6,length=100,strength=0.4)
#uni.addSpring(9,5,length=100,strength=0.4)
selected_particle = None 
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
        elif event.type == pygame.MOUSEBUTTONDOWN:
          (mouseX, mouseY) = pygame.mouse.get_pos()
          selected_particle = uni.findPar(mypar,mouseX,mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
          selected_particle = None
    if selected_particle:
          
          (mouseX, mouseY) = pygame.mouse.get_pos()
          dx = mouseX - selected_particle.x
          dy = mouseY - selected_particle.y
          selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
          selected_particle.speed = math.hypot(dx, dy) * 0.1
    if not paused:
      uni.update()
    screen.fill(uni.color)
    for p in uni.particles:
      pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size, 0)
    for s in uni.springs:
      pygame.draw.aaline(screen,(0,0,0), (int(s.p1.x), int(s.p1.y)), (int(s.p2.x), int(s.p2.y)))
    clock.tick()
    text = "FPS: " + str(clock.get_fps())
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 20))
    pygame.display.flip()

