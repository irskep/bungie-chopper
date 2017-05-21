from constants import *
import pyglet, resources, particle, random, math, colorsys

class Sparker(particle.ParticleSystem):
    """A Class used to simulate spark effects."""
    
    def __init__(self):
        particle.ParticleSystem.__init__(self, prototype=SparkParticle, rate=0.0)
        
    def spark(self, x,y):
        self.emit(x, y, 2)

        
class SparkParticle(particle.Particle):

    img = resources.flare5
    
    def __init__(self, **kwargs):
        particle.Particle.__init__(self, **kwargs)
        self.life = 35
        self.opacity = 255        
        self.rotation = random.randrange(360)
        
        modifier = random.random() * self.size
        
        self.velocity = 100 + 400 * modifier
        self.acceleration = -600
        
        self.scale = 0.03 + 0.1 * modifier
        
        self.aycomp = self.acceleration * TIME_STEP
        self.vxcomp = math.sin(math.radians(self.rotation)) * self.velocity
        self.vycomp = math.cos(math.radians(self.rotation)) * self.velocity
        

    def update(self, dt):

        if self.life > 0:            
            self.life -= 1

            if self.life < 10:
                # Fade out
                self.opacity = int(self.life * 0.1 * 255)
            
            self.vycomp += self.aycomp
            #self.vxcomp += self.axcomp
            self.x += self.vxcomp * dt
            self.y += self.vycomp * dt
          
        else:
            self.visible = False
            self.alive = False