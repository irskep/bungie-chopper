from constants import *
from util import vector, collision
import resources
import math
import pyglet


class VerletObject():
    """This class is the base class for any object that needs to be simulated as a verlet particle."""
    
    bounding = None
    
    def __init__(self, x, y):
        self.vposition = vector.Vector(x,y)
        self.last_vposition = vector.Vector(x,y)
        self.forces = vector.Vector(0,0)
        
        
    def update(self, dt2, dampening=1.0):
        p = self.vposition   
        self.vposition = self.vposition * (1.0 + dampening) - self.last_vposition * dampening + self.forces * dt2
        self.last_vposition = p


class VerletSprite(VerletObject, pyglet.sprite.Sprite):

    """This class is the base class for any sprite that needs to be simulated as a verlet particle."""
    
    def __init__(self, img, x, y, batch=None):
        VerletObject.__init__(self, x, y)
        pyglet.sprite.Sprite.__init__(self,img=img, x=x, y=y, batch=batch)
        self.hit_animation_cycles = 0
        
    def update(self, dt2, dampening=1.0):
        VerletObject.update(self, dt2, dampening)
        self.x = self.vposition.x
        self.y = self.vposition.y
        
        if self.hit_animation_cycles > 0:
            self.hit_animation_cycles -= 1
            self.color = (255,150,150)
            if self.hit_animation_cycles == 0:
                self.color = (255,255,255)
        
    def flash(self):
        self.hit_animation_cycles = 3



class Constraint:
    
    def __init__(self, a, b, restlength):
        self.a = a
        self.b = b
        self.restlength = restlength
    
    def angle():
        """Get the angle in degrees of the line made by the two points"""
        delta = a - b
        return math.degrees(math.atan2(delta.y, delta.x))
        
    def __repr__(self):
        return "%s <--%d--> %s" % (self.a, self.restlength, self.b)