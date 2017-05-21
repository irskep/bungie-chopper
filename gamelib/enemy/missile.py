from constants import *
from util import vector, collision
import base_enemy, random, math
import resources

class Missile(base_enemy.BaseEnemy):
    
    name = "missile"
    health = 22
    points = 10
    speed = 1500
    bounding = collision.Circle(radius=8)
        
    def __init__(self, **kwargs):
        base_enemy.BaseEnemy.__init__(self, img=resources.missile, **kwargs)
        self.rotation = 270
        self.last_vposition.y -= 0
        self.rotation = self.target_angle = 90-vector.angle(self.context.helicopter.vposition - self.vposition)
    
    def update(self, dt2):
        base_enemy.BaseEnemy.update(self, dt2, 0.90)
                
        difference = self.target_angle - self.rotation
        if difference >= 180: difference -= 360
        elif difference < -180: difference += 360        
        self.rotation += min(1.5, max(-1.5, difference))
                
        self.forces.x = math.sin(math.radians(self.rotation)) * self.__class__.speed
        self.forces.y = math.cos(math.radians(self.rotation)) * self.__class__.speed
        
                                            
    def ai(self):
        
        if self.x < self.context.camera.vposition.x: 
            # off camera
            self.die()
            
        if self.y < 15:
            # hit ground
            self.on_die()    
        
        if self.health > 1:     
            self.target_angle = 90-vector.angle(self.context.helicopter.vposition - self.vposition)
            self.health -= 1
        else:
            self.target_angle = 180
                

    def on_hit(self):                
        self.context.award(self.__class__.points, self.x, self.y)
        self.on_die()

    def on_collide(self, obj):
        obj.health -= 10
        self.on_die()

    def on_die(self):
        resources.explo_medium_1.play()
        self.context.exploder.explode(self.x, self.y)        
        self.die()