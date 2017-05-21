from constants import *
from util import vector, collision
import pyglet.gl

class Camera:
    
    bounding=collision.Rect(WIDTH, HEIGHT, WIDTH/2, HEIGHT/2)
    
    def __init__(self, x=0, y=0, vx=60.0, vy=0, automatic=True, track=None):
        
        self.vposition = vector.Vector(x,y)
        self.automatic = automatic
        self.track = track
        self.velocity = vector.Vector(vx, vy)
        
    def update(self,dt):
        #verlet.VerletObject.update(dt*dt)
        if self.automatic:
            self.vposition += self.velocity * dt
            if self.track != None and self.track.vposition.x - self.vposition.x > WIDTH/2:
                self.vposition = self.track.vposition - (WIDTH/2, HEIGHT/2)
        elif self.track != None:
            self.vposition = self.track.vposition - (WIDTH/2, HEIGHT/2)
    
    def enter(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-self.vposition.x, -self.vposition.y, 0)
    
    def exit(self):
        pyglet.gl.glPopMatrix()