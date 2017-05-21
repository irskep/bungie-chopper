from constants import *
from util import vector, collision
import verlet, random, math, resources

class BaseEnemy(verlet.VerletSprite):
    
    name = "enemy"
    health = 100
    points = 100
    bounding = collision.Circle(radius=16)
    invmass = 1.0/500
    
    def __init__(self, x, y, img=None, batch=None, context=None):
        verlet.VerletSprite.__init__(self, img, x, y, batch=batch)
        self.context = context
        self.health = self.__class__.health        
        self.alive=True
        self.dying=False    
        
    def fire(self, angle):
        """Fire a bullet"""
        self.context.context.fire(self.vposition.x, self.vposition.y, angle, True)

    def die(self):        
        self.alive = False
        self.visible = False            

    def update(self, dt2, dampening=0.99):
        verlet.VerletSprite.update(self, dt2, dampening)
        if self.health <= 0 and not self.dying:            
            self.on_die()            

    def ai(self):
        """AI routines. Override me."""
        if self.x < self.context.camera.vposition.x: self.die()
                
    def on_hit(self):                
        if not self.dying: 
            self.flash()                    
            self.health -= 10 # player bullet strength

    def on_collide(self, obj):
        if not self.dying and obj.__class__.name != "gunner": 
            self.flash()
            self.health -= 10
            #obj.health -= 10
            resources.hit_2.play()
        
    def on_die(self):
        self.dying = True
        self.context.exploder.explode(self.x, self.y)
        self.context.award(self.__class__.points, self.x, self.y)
        self.die()