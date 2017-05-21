from constants import *
from util import vector, collision
import verlet, resources

class Gunner(verlet.VerletSprite):
    
    name = "gunner"
    health = 15
    bounding = collision.Circle(radius=8)
    invmass = 1.0 / 50
    
    def __init__(self, x, y, batch=None, context=None):
        verlet.VerletSprite.__init__(self,resources.gunner, x, y, batch=batch)
        self.rotation = 0
        self.color = (255,255,255)
        self.context = context
        self.scale = 0.6
        self.cooldown = 0
        self.forces.y = GRAVITY
        self.health = self.__class__.health
        self.dying = False
        self.alive = True
        
        
    def fire(self, xcomp, ycomp, angle):
        self.cooldown = 4
        self.context.add_bullet(self.x, self.y, xcomp, ycomp, angle)
        resources.fire_1.play()
    
    def on_hit(self):
        if not self.dying: 
            self.flash()
            self.health -= 5

    def on_collide(self, obj):
        if not self.dying: 
            self.flash()
            self.health -= 5
                
    def die(self):
        self.context.rope.constraints.pop()
        self.alive = False
        self.batch = None
        resources.hit_5.play()
        self.context.gunner_down()

    
    def update(self, dt2, keys):
                        
        if self.health <= 0 and not self.dying:  
            self.context.rope.constraints.pop(ROPE_SEGMENTS/2)
            self.dying = True
            resources.gunner_die.play()
                            
        if self.dying:
            if self.y <= 16: self.die()
            self.rotation += 2
        else:
                                
            if self.cooldown > 0:
                self.cooldown -= 1
            else:
                if keys[FIRE_RIGHT]:                
                    if keys[FIRE_UP]: 
                        self.fire(*DIR_UR)
                    elif keys[FIRE_DOWN]:
                        self.fire(*DIR_DR)
                    else: 
                        self.fire(*DIR_R)
                elif keys[FIRE_LEFT]:                
                    if keys[FIRE_UP]: 
                        self.fire(*DIR_UL)
                    elif keys[FIRE_DOWN]: 
                        self.fire(*DIR_DL)
                    else: 
                        self.fire(*DIR_L)
                elif keys[FIRE_UP]:
                    self.fire(*DIR_U)
                elif keys[FIRE_DOWN]:
                    self.fire(*DIR_D)
                
        verlet.VerletSprite.update(self, dt2, 0.99)