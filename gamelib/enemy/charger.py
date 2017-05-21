from constants import *
from util import vector, collision
import base_enemy, random, math
import resources

class Charger(base_enemy.BaseEnemy):
    
    name = "charger"
    health = 20
    points = 100
    speed = 50
    bounding = collision.Circle(radius=12)
        
    def __init__(self, **kwargs):
        base_enemy.BaseEnemy.__init__(self, img=resources.charger, **kwargs)
        self.cooldown = 20
        self.rotation = 270
        self.last_vposition.x += 2
                                            
    def ai(self):
        
        if self.dying: 
            self.rotation -= 3
            self.forces.y = GRAVITY
            if self.y < 0: self.die()
        
        if self.x < self.context.camera.vposition.x: 
            # off camera
            self.die()
                
        #modifier = math.cos(math.radians(self.x))
        #self.rotation += modifier

        if self.cooldown <= 0:
            #if abs(self.x - self.context.helicopter.x) < WIDTH*0.9: self.fire(self.rotation)
            self.forces.x = -2000
            if self.image != resources.charger_burn: self.image = resources.charger_burn
            #self.cooldown = self.__class__.cooldown
        else:    
            if self.image != resources.charger: self.image = resources.charger
            self.cooldown -= 1            
            if self.x > self.context.camera.vposition.x + WIDTH: 
                self.forces.x = -200 * random.random()
            else:
                self.forces.x = 100 * random.random()
                
        self.forces.y = (self.context.helicopter.y - self.y)  * random.random() * 1.5
        
    def on_collide(self,obj):
        obj.health -= 20
        self.health -= 20
        
    def on_die(self):    
        resources.explo_medium_1.play()
        super(Charger,self).on_die()