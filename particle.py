import pygame, math, random
drag = 0.999
elasticity = 0.75
gravity = (math.pi,0.002)
(width,height) = (624,468)
"""Init"""
colorchange = 0 #change color dependent on how many bounce? 0=off 1=on
def addVectors((angle1, length1), (angle2, length2)):
  x = math.sin(angle1)*length1 +math.sin(angle2)*length2
  y = math.cos(angle1)*length1 +math.cos(angle2)*length2
  angle = 0.5*math.pi -math.atan2(y,x)
  length = math.hypot(x,y)
  return(angle, length)

def findPar(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1,p2):
  dx = p1.x - p2.x
  dy = p1.y -p2.y
  dist = math.hypot(dx,dy)
  if dist <p1.size + p2.size:
    p1.hitamount += 1
    if colorchange == 1:
      
      p1.color = (0,(50+p1.hitamount),0)
    tangent = math.atan2(dy, dx) #atan2
    angle = 0.5 * math.pi + tangent
    angle1 = 2 * tangent - p1.angle
    angle2 = 2 * tangent - p2.angle
    speed1 = p2.speed * elasticity
    speed2 = p1.speed * elasticity
    (p1.angle, p1.speed) = (angle1, speed1)
    (p2.angle, p2.speed) = (angle2, speed2)
    p1.x += math.sin(angle)
    p1.y -= math.cos(angle)
    p2.x -= math.sin(angle)
    p2.y += math.cos(angle)
  
  
    
#Particle
class par():
  def __init__(self, (x,y),size,spot,hitamount):
    self.x = x
    self.y = y
    self.size = size
    self.color = (0,0,255)
    self.thick = 50
    self.speed = 0.01
    self.angle = 0
    self.spot = spot
    self.hitamount = hitamount
    self.mass = 100
  def display(self):
    #pygame.draw.circle(screen,self.color,(self.x,self.y),self.size,self.thick)
    pass
  def move(self):
    (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
    self.x += math.sin(self.angle) * self.speed
    self.y -= math.cos(self.angle) * self.speed
    self.speed *=drag
    
  def accelerate(self, vector):
    """change angle and speed"""
    (self.angle, self.speed) = addVectors((self.angle, self.speed), vector)
  #bounce function....
  def bounce(self):

    print("i got hit ",self.hitamount)
    if self.x > width - self.size:
      self.x = 2 *(width -self.size) -self.x
      self.angle = -self.angle
      self.speed *= elasticity
    elif self.x < self.size:
      self.x = 2* self.size -self.x
      self.angle = -self.angle
      self.speed *= elasticity
    if self.y > height - self.size:
      self.y = 2 *(height -self.size) -self.y
      self.angle = math.pi -self.angle
      self.speed *= elasticity
    elif self.y < self.size:
      self.y = 2* self.size -self.y
      self.angle = math.pi - self.angle
      self.speed *= elasticity

mypar = []

class envi:
  def __init__(self,(width,height)):
    self.width = width
    self.height = height
    self.particles = []
    self.springs = []
    self.color = (255,255,255)
    self.elasticity = 0.75
    self.particle_functions1 = []
    self.particle_functions2 = []
    self.function_dict = {
    'move': (1, lambda p: p.move()),
    'drag': (1, lambda p: p.experienceDrag()),
    'bounce': (1, lambda p: self.bounce(p)),
    'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
    'collide': (2, lambda p1, p2: collide(p1, p2)),
    #'combine': (2, lambda p1, p2: combine(p1, p2)),
    'attract': (2, lambda p1, p2: p1.attract(p2))
    }

  def addParticle(self, n=1, **kargs):
    for i in range (n):
      size = kargs.get('size', random.randint(10,20))
      mass = kargs.get('mass', random.randint(100,10000))
      x = kargs.get('x',random.uniform(size, self.width-size))
      y = kargs.get('y',random.uniform(size,self.height-size))
      p = par((x,y),size,0,4)
      p.speed = kargs.get('speed',random.random())
      p.angle = kargs.get('angle', random.uniform(0, math.pi*2))
      self.particles.append(p)
  def bounce(self,particle):
  
      #print("i got hit ",particle.hitamount)
      if particle.x > width - particle.size:
        particle.x = 2 *(width -particle.size) -particle.x
        particle.angle = -particle.angle
        particle.speed *= elasticity
      elif particle.x < particle.size:
        particle.x = 2* particle.size -particle.x
        particle.angle = -particle.angle
        particle.speed *= elasticity
      if particle.y > height - particle.size:
        particle.y = 2 *(height -particle.size) -particle.y
        particle.angle = math.pi -particle.angle
        particle.speed *= elasticity
      elif particle.y < particle.size:
        particle.y = 2* particle.size -particle.y
        particle.angle = math.pi - particle.angle
        particle.speed *= elasticity    
      
  def update(self):
    for i, particle in enumerate(self.particles):
        particle.move()
        self.bounce(particle)
        for particle2 in self.particles[i+1:]:
            collide(particle, particle2)
    for spring in self.springs:
      spring.update()
  def addFunctions(self, function_list):
    for func in function_list:
        (n, f) = self.function_dict.get(func, (-1, None))
        if n == 1:
          self.particle_functions1.append(f)
        elif n == 2:
          self.particle_functions2.append(f)
        else:
          print "No such function: %s" % f
  def addSpring(self,p1,p2,length=50,strength=0.5):
    """add spring p1-p2"""
    self.springs.append(Spring(self.particles[p1],self.particles[p2],length,strength))
  def findPar(self,particles, x, y):

    for p in self.particles:
      if math.hypot(p.x-x, p.y-y) <= p.size:
        return p
    return None
class Spring:
  def __init__(self,p1,p2,length=50,strength=0.5):
    self.p1 = p1
    self.p2 = p2
    self.lent = length
    self.stren = strength
  def update(self):
    dx = self.p1.x - self.p2.x
    dy = self.p1.y - self.p2.y
    dist = math.hypot(dx, dy)
    theta = math.atan2(dy, dx)
    force = (self.lent - dist) * self.stren
        
    self.p1.accelerate((theta + 0.5 * math.pi, force/100)) #self.p1.mass
    self.p2.accelerate((theta - 0.5 * math.pi, force/100))
    