import pyglet, resources, particle, random, math

class Pointer(particle.ParticleSystem):
    """A Class used to show points awarded for various kills."""
    
    def __init__(self):
        particle.ParticleSystem.__init__(self, prototype=ScoreParticle, rate=10.0)        
        
    def emit(self, x, y, points):
        
        if len(self.particle_pool) > 0:
            p = self.particle_pool.pop()
            p.__init__(x=x, y=y, text="%s" % points, batch=self.particle_batch)
        else:
            p = self.prototype(x=x, y=y, text="%s" % points, batch=self.particle_batch)
            self.particles.append(p)
        
        

class ScoreParticle(pyglet.text.Label):
        
    def __init__(self, **kwargs):
        pyglet.text.Label.__init__(self, font_name="Press Start K", **kwargs)
        self.anchor_x = "center"
        self.font_size = 8
        self.life = 50
        self.alive = True
        self.pooled = False
        
    def update(self, dt):

      if self.life > 0:            
          self.life -= 1
          
          if self.life < 10:
              self.color = (255,255,255,int(self.life * 0.1 * 255))
         
          self.y += 1         
      else:
          self.visible = False
          self.alive = False