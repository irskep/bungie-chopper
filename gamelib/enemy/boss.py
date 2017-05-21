from constants import *
from util import vector, collision
import verlet, random, math
import resources
import missile, base_enemy

class Boss(verlet.VerletObject):
    
    name = "luxobot"
    health = 2000
    points = 10000
    bounding = collision.Rect(230, 240, 0, 150)
    invmass = 0
            
    def __init__(self, x, y, batch, context):
        verlet.VerletObject.__init__(self, x, y)
        self.context = context
        self.neck = Neck(x=x, y=y, batch=batch, context=context)        
        self.track = self.context.spawn(Track, x=x, y=y-165)
        # Track(x=x, y=y-165, batch=batch, context=context)        
        self.head = Head(x=x, y=y+150, batch=batch, context=context)
        self.alive = True
        self.dying = False
        self.target_angle = 270
        
        self.head_attached = True
        self.neck_attached = True
        
    def update(self, dt2):
        verlet.VerletObject.update(self, dt2, 0.99)
        
        self.movement_x = self.vposition.x - self.last_vposition.x
        modifier = math.cos(self.track.rotation/19.098593171027) * 15
        
        self.head.update(dt2,0.99)
        if self.head_attached:
            self.head.vposition.x = self.vposition.x
            self.head.vposition.y = self.vposition.y + 150 + modifier
            self.head.rotation += min(0.2, max(-0.2, self.target_angle - self.head.rotation))
        else:            
            self.head.vposition.y = max(140, self.head.vposition.y)
        
        self.neck.update(dt2,0.99)
                
        if self.neck_attached:
            self.neck.vposition.x = self.vposition.x
            self.neck.vposition.y = self.vposition.y + modifier
        else:
            neck_floor = 25 + 200 * (90 - self.neck.rotation) / 90
            self.neck.x = self.neck.vposition.x + 175.0 * self.neck.rotation / 90 
            if self.neck.rotation < 90:
                self.neck.rotation += 1
            self.neck.vposition.y = max(neck_floor, self.neck.vposition.y)    
                
        #self.track.update(dt2)
        self.track.vposition.x = self.vposition.x
        self.track.vposition.y = self.vposition.y - 165 + modifier
        self.track.rotation += self.movement_x / 972 * 360        
                
        if self.health <= 0 and not self.dying:
            self.on_die()
                    
    
    def ai(self):
        
        if self.dying:
            
            self.dying_count += 1
                                    

            if self.dying_count < 20:
                self.context.exploder.explode(self.vposition.x + random.randrange(-120,120), self.vposition.y + random.randrange(-250,250), 2.0)
                resources.explo_big_2.play()
            elif self.dying_count < 60:
                self.context.exploder.explode(self.vposition.x + random.randrange(-120,120), self.vposition.y + random.randrange(-250,0), 2.0)
                resources.explo_big_2.play()
                
            if self.dying_count == 20:
                self.head_attached = False
                self.head.forces.x = 0
                self.head.forces.y = GRAVITY
                self.head.last_vposition.y -= 10
                self.head.last_vposition.y += 10
            
            if self.dying_count == 40:
                self.neck_attached = False
                self.neck.forces.x = 0
                self.neck.forces.y = GRAVITY    
                
            if self.dying_count > 60:
                if self.track.rotation < 340: self.forces.x = 10
                else: self.forces.x = 0
                self.alive = False                
            return
            
        if self.vposition.x > self.context.camera.vposition.x + WIDTH:
            self.forces.x = 0
        else:
            self.forces.x = random.randrange(128,135)
        
        self.target_angle = 180-vector.angle(self.context.helicopter.vposition - self.head.vposition)
        
        if random.random() > 0.70:
            self.fire_missile()
            
        if random.random() > 0.70:
            self.fire()
        
    def fire_missile(self):
        x = self.head.vposition.x + math.sin(math.radians(self.head.rotation-90)) * 140
        y = self.head.vposition.y + math.cos(math.radians(self.head.rotation-90)) * 140
        self.context.spawn(missile.Missile, x, y )
        
    def fire(self):
        x = self.head.vposition.x + math.sin(math.radians(self.head.rotation-90)) * 140
        y = self.head.vposition.y + math.cos(math.radians(self.head.rotation-90)) * 140
        self.context.context.fire(x, y,self.head.rotation-90,True )
        
    
    def on_hit(self):
        if not self.dying:
            self.head.flash()
            self.track.flash()
            self.health -= 10
        
    def on_collide(self, obj):    
        pass
            
    def on_die(self):        
        self.context.award(self.__class__.points, self.head.x, self.head.y)
        self.forces.x = 20
        self.dying = True
        self.track.dying = True
        self.dying_count = 0
        
    
    
    
    
class Head(verlet.VerletSprite):
        
    invmass = 0    
    
    def __init__(self, x, y, batch=None, context=None):
        verlet.VerletSprite.__init__(self, img=resources.boss_head, x=x, y=y, batch=batch)
        self.context = context
    
class Neck(verlet.VerletSprite):
    
    def __init__(self, x, y, batch=None, context=None):
        verlet.VerletSprite.__init__(self, img=resources.boss_arm, x=x, y=y, batch=batch)
        self.context = context
    
    
class Track(base_enemy.BaseEnemy):
    
    bounding = collision.Circle(radius=120)
    invmass = 0
    
    def __init__(self, x, y, batch=None, context=None):
        base_enemy.BaseEnemy.__init__(self, img=resources.boss_track, x=x, y=y, batch=batch)
        #verlet.VerletSprite.__init__(self, img=resources.boss_track, x=x, y=y, batch=batch)
        self.context = context
    
    def on_hit(self):                
        pass

    def on_collide(self, obj):
        pass

    def on_die(self):
        pass
        
    def ai(self):
        pass
        