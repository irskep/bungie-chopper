from constants import *
from util import vector, collision
import verlet, resources

class Helicopter(verlet.VerletSprite):
    
    name = "helicopter"
    health = 250
    bounding = collision.Rect(width=64,height=32)
    
    def __init__(self, x, y, batch=None, context=None):        
        verlet.VerletSprite.__init__(self,resources.heli, x, y, batch=batch)
        self.rotation = 0
        self.color = (255,255,255)
        self.context = context
        self.scale = 1.0
        self.health = self.__class__.health
        self.dying = False
        self.alive = True        
        
    def on_hit(self):
        # Enemy bullet strength
        if not self.dying: 
            self.flash()
            self.health -= 5
        
            
    def on_collide(self, obj):
        if not self.dying: 
            self.flash()
            self.health -= 5
        
                        
    def die(self):
        self.context.stage.exploder.explode(self.x, self.y, 1.5)
        self.context.stage.exploder.explode(self.x-32, self.y-32, 1.5)
        self.context.stage.exploder.explode(self.x-32, self.y+32, 1.5)
        self.context.stage.exploder.explode(self.x+32, self.y-32, 1.5)
        self.context.stage.exploder.explode(self.x+32, self.y+32, 1.5)
        self.alive = False
        self.batch = None
        
        resources.explo_big_1.play()
        
        self.context.gunner.die()
        self.context.heli_down()
    
    def update(self, dt2, keys):
        
        if self.health <= 0 and not self.dying: 
            self.context.stage.exploder.explode(self.x, self.y)
            self.context.stage.smoker.add_emitter(self)
            self.context.stage.smoker.add_emitter(self)
            self.dying = True
                
        if self.dying:
            self.forces.y = GRAVITY
            self.forces.x = 360
            self.rotation += 1.5
            if self.y <= 16: self.die()
        else:
            self.forces.x = 180
            self.forces.y = 0 # GRAVITY * 0.25
            # Check keys for input. Adjust helicopter acceleration accordingly
            if keys[HELI_UP]: self.forces.y += HELI_POWER
            elif keys[HELI_DOWN]: self.forces.y -= HELI_POWER
            if keys[HELI_LEFT]: self.forces.x -= HELI_POWER
            elif keys[HELI_RIGHT]: self.forces.x += HELI_POWER
        
            v = self.last_vposition - self.vposition
            self.rotation = v.y
                
        verlet.VerletSprite.update(self, dt2, HELI_DAMPENING)