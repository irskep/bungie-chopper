from constants import *
import pyglet, resources, particle, random, math, colorsys, spark

class Exploder():
    """A Class used to splode stuff up."""
    
    def __init__(self):
        self.sparker = particle.ParticleSystem(prototype=FireParticle, rate=0.0)
        self.firer = particle.ParticleSystem(prototype=spark.SparkParticle, rate=0.0)
        
    def explode(self, x, y, size=1.0):    
        self.sparker.emit(x, y, 9, size)
        self.firer.emit(x, y, 4, size)

    def update(self, dt):
        self.sparker.update(dt)
        self.firer.update(dt)
        
    def draw(self):
        self.sparker.draw()
        self.firer.draw()
        
class FireParticle(particle.Particle):
    
    img = resources.flare3
    
    def __init__(self, **kwargs):
        particle.Particle.__init__(self, **kwargs)
                
        modifier = random.random() 
        modsqrt = math.sqrt(modifier)
        
        self.scale =    0.5
        self.life =     20
        self.velocity = 200 * modsqrt        
        color = colorsys.hsv_to_rgb(
            0.15 - 0.12 * modsqrt,      # hue
            0.25 + 0.75 * modsqrt,      # sat
            1.0                         # val
        )         
        self.color = (255*color[0], 255*color[1], 255*color[2])
        self.opacity = 255        
        self.rotation = random.randrange(360)
        self.xcomp = math.sin(math.radians(self.rotation)) * self.velocity * TIME_STEP
        self.ycomp = math.cos(math.radians(self.rotation)) * self.velocity * TIME_STEP        

    def update(self, dt):

        if self.life > 0:            
            self.life -= 1
                        
            if self.life <= 10:
                # Fade out
                self.scale = 0.5 + (20 - self.life) * .015
                self.opacity = int(self.life * .1 * 255)
                
            self.x += self.xcomp
            self.y += self.ycomp

        else:
            self.visible = False
            self.alive = False