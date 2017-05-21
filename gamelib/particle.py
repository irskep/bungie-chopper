import pyglet, resources, math, random, util.vector

class ParticleSystem():
    """A class used to simulate particle effects."""
    
    def __init__(self, prototype, rate=8.0):
        
        # prototype is a class object that is instantiated whenever a particle is emitted
        self.prototype = prototype
        
        self.period = rate/60
        self.timer = self.period
        self.particles = []
        self.particle_pool = []
        self.particle_batch = pyglet.graphics.Batch()
        
        # the objects list is a list of sprite objects that the particle effect is attached to 
        # if the object dies, the emitter it corresponds to dies as well
        self.objects = []
        self.emitters = []
        
    def add_emitter(self, object):      
      	self.objects.append(object)

    def update(self, dt):
        
        emit = False
        
        if self.period > 0:
            self.timer -= dt
            if self.timer < 0:
                self.timer += self.period
                emit = True
        
        for o in self.objects:
            if not o.alive:                
                self.objects.remove(o)
                continue
            elif emit:
                self.emit(o.x,o.y,1)
                
        for p in self.particles:
            if p.alive:
                p.update(dt)
            elif not p.pooled:                
                self.particle_pool.append(p)
                p.pooled = True
                                
    
    def emit(self, x, y, number=1, size=1.0):
        
        for n in range(number):
        
            if len(self.particle_pool) > 0:
                p = self.particle_pool.pop()
                p.__init__(x=x, y=y, size=size, batch=self.particle_batch)                
            else:
                p = self.prototype(x=x, y=y, size=size, batch=self.particle_batch)
                self.particles.append(p)
                  
    def draw(self):
        self.particle_batch.draw()
                
    def die(self):
        pass
      
        
class Particle(pyglet.sprite.Sprite):
    """Basic particle to subclass for particle systems"""
    
    img = None
    
    def __init__(self, x, y, rotation=0.0, velocity=0.0, acceleration=0.0, opacity=255, batch=None, size=1.0):
        pyglet.sprite.Sprite.__init__(self, img=self.__class__.img, x=x, y=y, batch=batch)
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration
        self.opacity = opacity
        self.life = 0
        self.size = size
        self.alive = True
        self.visible = True
        self.pooled = False
        
    def update(self, dt):
        pass