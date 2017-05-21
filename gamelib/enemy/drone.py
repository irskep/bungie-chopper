from constants import *
from util import vector, collision
import base_enemy, random, math, pyglet.image
import resources

class Drone(base_enemy.BaseEnemy):
    
    name = "drone"
    health = 30
    points = 100
    cooldown = 6
    speed = 50
    bounding = collision.Circle(radius=16)
        
    def __init__(self, **kwargs):
        
        base_enemy.BaseEnemy.__init__(self, img=resources.drone, **kwargs)
        self.cooldown = 0
        self.rotation = 270
        self.last_vposition.x += 3
                                            
    def ai(self):
        
        if self.x < self.context.camera.vposition.x: self.die()
        
        if self.dying: 
            self.rotation -= 3
            self.forces.y = GRAVITY
            if self.y < 0: self.die()
                        
        modifier = math.cos(math.radians(self.x))
        self.rotation += modifier
            
        if self.cooldown == 0:
            if self.x < self.context.camera.vposition.x + WIDTH: 
                self.fire(self.rotation)
                
            self.forces = vector.Vector(-60, math.cos(math.radians(self.x)) * self.__class__.speed * 2)
            self.cooldown = self.__class__.cooldown
        else:
            self.cooldown -= 1

            
    def on_die(self):
        self.context.exploder.explode(self.x, self.y)
        self.context.award(self.__class__.points, self.x, self.y)
        resources.explo_medium_1.play()
        self.dying = True
    
    
class SuperDrone(Drone):
    
    name = "superdrone"
    points = 200
    health = 40
    
    def __init__(self, **kwargs):
        Drone.__init__(self, **kwargs)
        self.color = (255,180,180)
        
    def fire(self, angle):
        Drone.fire(self, self.rotation)
        Drone.fire(self, self.rotation + 30)
        Drone.fire(self, self.rotation - 30)