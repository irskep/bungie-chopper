import pyglet, resources, particle, random, math

class Smoker(particle.ParticleSystem):
    """A Class used to simulate smoke effects."""
    
    def __init__(self):
        particle.ParticleSystem.__init__(self, prototype=SmokeParticle, rate=10.0)


class SmokeParticle(particle.Particle):
    
    img=resources.smoke
        
    def __init__(self, **kwargs):
        particle.Particle.__init__(self, **kwargs)
        self.life = 100
        self.opacity = 128
        self.scale = 0
        self.rotation = random.randrange(360)        
        
    def update(self, dt):

      if self.life > 0:            
          self.life -= 1
          self.opacity = int(self.life * 0.01 * 255)
          self.scale = (100-self.life) * 0.01
          self.y += 1
          self.x += math.cos(dt)
      else:
          self.visible = False
          self.alive = False