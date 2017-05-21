from util import vector
import camera, backdrop, smoke, explosion, spark, score, enemy.turret
from constants import *
import pyglet.graphics, pyglet.gl
import random, time, copy

class Stage:
    
    def __init__(self, width, height, context=None):
                    
        self.timer = 0                      # time in seconds since the stage began, used for triggers
        self.width = width                  # width of the stage
        self.height = height                # height of the stage
        self.music = None

        self.checkpoint = None
        
        self.powerups = []                  # list of powerups.
        self.triggers = []                  # list of stage triggers. See stages/01.py for an explanation
        self.enemies = []                   # list of enemies. Try to avoid spawning enemies until they are needed
        self.enemy_count = 0
        self.enemy_pool_limit = ENEMY_POOL
        
        self.multiplier = 1
        self.last_chain_time = 0.0

        self.camera = camera.Camera()       # the camera object 
        self.backdrop = backdrop.Backdrop(self.camera)
        self.enemy_sprite_batch = pyglet.graphics.Batch()
        
        # effects    
        self.smoker = smoke.Smoker()
        self.exploder = explosion.Exploder()
        self.pointer = score.Pointer()
            
        self.effects = []
        self.effects.append(self.smoker)
        self.effects.append(self.exploder)
        self.effects.append(self.pointer)
        
        self.set_context(context)
                
    def set_context(self, context):
        """Set a reference to the main objects"""
        self.context = context
        self.helicopter = context.helicopter
        self.gunner = context.gunner
        self.camera.track = self.helicopter

    def set_checkpoint(self):
        self.checkpoint = Checkpoint(self.camera, self.triggers, self.timer)
    
    def clear_checkpoint(self):
        self.checkpoint = None
        
    def load_checkpoint(self):
        
        self.camera.vposition = self.checkpoint.camera.vposition
        self.camera.velocity = self.checkpoint.camera.velocity
        self.camera.automatic = self.checkpoint.camera.automatic
        self.camera.track = self.checkpoint.camera.track
        self.triggers = self.checkpoint.triggers
        self.timer = self.checkpoint.timer        
        self.backdrop.reset()
        del self.powerups[:]
        del self.enemies[:]
        self.enemy_count = 0

    def message(self, *args):
        """Write a message on the screen"""        
        self.context.message(*args)

    def victory(self):
        """The stage has been completed"""
        self.context.message("CONGRATULATIONS. YOU WIN!", 10.0)
        self.delay(self.context.title, 10.0)

    def failure(self):
        """The stage has been failed"""
        self.triggers = []


    def delay(self, callback, time):
        time = self.timer + time
        self.triggers.append(Trigger(lambda: self.timer >= time, callback, False))

    
    def award(self, points, x=None, y=None):        
        # Combo bonus for killing a group of enemies in a chain
        if self.timer - self.last_chain_time < 0.8:
            self.multiplier += 1
            points *= self.multiplier
        else:            
            self.multiplier = 1
        
        self.last_chain_time = self.timer
        if x != None: self.pointer.emit(x, y, points)
        self.context.score += points
        
    def spawn_list(self, objects):
        """Spawn a list of objects"""
        for o in objects:
            self.spawn_ahead(*o)
            
    def spawn_ahead(self, enemy_class, x, y):
        return self.spawn(enemy_class, x=x+self.camera.vposition.x, y=y+self.camera.vposition.y)
                        
    def spawn(self, enemy_class, x, y):
        """Spawn an enemy at position"""
        #print "spawning %s at %d, %d" % (enemy_class, x, y)
        
        e = enemy_class(x=x,y=y, batch=self.enemy_sprite_batch, context=self)
        self.enemies.append(e)
        self.enemy_count += 1
        
        if self.enemy_count >= self.enemy_pool_limit:
            self.empty_enemy_pool()
            
        return e
        
        
    def empty_enemy_pool(self):
        """Create a new enemies list with only alive enemies"""        
        self.enemies = filter(lambda e: e.alive, self.enemies)
            
        # If more than hald of the enemies in the list are still alive, it's time for a bigger pool
        if len(self.enemies) > self.enemy_pool_limit // 2:
            self.enemy_pool_limit += ENEMY_POOL
                
                                    
    def draw(self):
        self.backdrop.draw()
        self.enemy_sprite_batch.draw()
        
    def update(self, dt):        
        self.timer += dt
        self.camera.update(dt)
        self.backdrop.update(dt)
        
        for e in self.enemies:
            if e.alive: e.update(dt*dt)

        for e in self.effects:
            e.update(dt)
        
        if self.context.tick % 10 == 0:            
            # Perfom enemy AI 6 times per second
            for e in self.enemies:        
                if e.alive: e.ai()
            
            # Test all of the stage triggers, and execute callbacks if they evaluate to true.
            for t in self.triggers:
                if t.condition():
                    t.callback()
                    if not t.repeat and t in self.triggers:
                        self.triggers.remove(t)
                          
              
class Checkpoint:
    
    def __init__(self, cam, triggers, timer):
        self.camera = camera.Camera(
            x=cam.vposition.x, y=cam.vposition.y, 
            vx=cam.velocity.x, vy=cam.velocity.y, 
            automatic=cam.automatic, track=cam.track)
        self.triggers = triggers[:]
        self.timer = timer
        
        
class Trigger:
        
    def __init__(self, condition, callback, repeat=False):
        # this is a function that can be tested in the scope of the stage object
        self.condition = condition
        self.callback = callback
        self.repeat = repeat