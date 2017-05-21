from constants import *
from util import vector, collision
import verlet, resources

class Bullet(verlet.VerletSprite):
    
    bounding = collision.Circle(radius=2.5)
    
    def __init__(self, x, y, batch=None):
        verlet.VerletSprite.__init__(self,resources.bullet, x, y, batch=batch)
        self.visible = False
        self.alive = False
        self.pooled = True
                
    def die(self):
        self.alive=False
        self.visible=False
        
    def fire(self, x, y, x_comp, y_comp, angle, speed):
        self.rotation = angle        
        self.vposition.x = x + x_comp * 32
        self.vposition.y = y + y_comp * 32
        self.last_vposition.x = self.vposition.x + -x_comp * speed * TIME_STEP
        self.last_vposition.y = self.vposition.y + -y_comp * speed * TIME_STEP
        self.visible = True
        self.alive = True
        self.pooled = False