from constants import *
from util import vector
import base_enemy, random, math
import resources


class TurretBase(base_enemy.BaseEnemy):
    
    bounding = None
            
    def __init__(self, x, y, batch=None, context=None):
        base_enemy.BaseEnemy.__init__(self, img=resources.scaffold, x=x, y=0, batch=batch, context=context)
        self.x = x
        
        
class Turret(base_enemy.BaseEnemy):
    
    health = 60
    points = 500
    cooldown = 12
    jitter = 10
    invmass = 0.0
    
    def __init__(self, x, y, batch=None, context=None):
        
        base_enemy.BaseEnemy.__init__(self, img=resources.turret, 
                    x=x, y=y + 71, 
                    batch=batch, context=context)
        self.context.spawn(TurretBase, x, y)
        
                                    
    def ai(self):
        
        if self.x < self.context.camera.vposition.x: self.die()
        
        if self.cooldown == 0:
            jitter = random.randrange(-self.__class__.jitter,self.__class__.jitter)
            angle = 90-math.degrees(math.atan2(self.context.helicopter.y - self.y, self.context.helicopter.x - self.x)) + jitter
            self.fire(angle)
            self.cooldown = self.__class__.cooldown
        else:
            self.cooldown -= 1
    
    def on_die(self):    
        resources.explo_medium_1.play()
        super(Turret,self).on_die()