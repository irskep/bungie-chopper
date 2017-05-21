from constants import *
import helicopter, gunner, rope, bullet, resources
from util import vector, collision
import sys, math
import pyglet.graphics, pyglet.gl

class Game():
    
    """This is the class that holds our high-level game state. We will keep track of the player, enemies, bullets
    explosions terain, and anything else we might need. The update() method is called periodically, and thats where the physics are
    updated, and the collisions are performed. This class holds a dictionary object called "keys" which is used
    to figure out what keys are being pressed at any given update cycle. This is passed down from the parent
    window, using pyglet.window.key.KeyStateHandler(). This seems like an easier method than trying to respond to key
    up and down events, especially given that our physics runs at a fixed step.
    """
    gunners = ["JIMMY", "JOHNNY", "WILLY", "TOMMY", "BILLY"]
    
    def __init__(self, keys, context=None):
        """Initialize the game, set player objects."""
        self.context = context
        self.keys = keys        # keys dictionary so we know what keys are being pressed
        self.tick = 0           # The number of updates since the start of the game
        self.score = 0
        self.lives = 3
        
        self.score_label = pyglet.text.Label(
            text='000000', 
            font_name="Press Start K", 
            font_size=10, 
            x=10, y=HEIGHT-4,
            anchor_x='left', anchor_y='top')
        
        self.message_timer = 0
        self.message_priority = 0.0
        self.message_label = pyglet.text.Label(
            text='', 
            font_name="Press Start K", 
            font_size=10, 
            x=WIDTH//2, y=HEIGHT//2,
            anchor_x='center', anchor_y='center')
                    
        self.sprite_batch = pyglet.graphics.Batch()
        self.sprite_bullet_batch = pyglet.graphics.Batch()
        
        self.stage = None       # The stage object tracks the environment, enemies and powerups        
        
        self.gunners = self.__class__.gunners[:]
        self.helicopter = None
        self.gunner = None
        self.rope = None
        
    def load_stage(self, stage, demo=False): #, checkpoint=None):
        """Load a stage procedurally, or from a file. This method will import the named module, and load the class
        within. The class must be named Stage<Name> where <Name> is the capitalized version of the module name."""

        self.demo = demo
                    
        classname = "Stage%s" % stage.title()        
        module = __import__(stage)
        class_obj = getattr(module, classname)
        
        if not demo:
                                
            self.helicopter = helicopter.Helicopter(400, 400, batch=self.sprite_batch, context=self)
            self.gunner = gunner.Gunner(400, 400, batch=self.sprite_batch, context=self)
            self.rope = rope.Rope(length=ROPE_SEGMENTS, anchor_start=self.helicopter, anchor_end=self.gunner)
            self.message("GET READY SOLDIER")
            
        
        self.stage = class_obj(context=self)
        
        # Zero out all of the bullets
        self.bullets = []
        self.bullet_pool = []
        
        # Fill the bullet pool with dead bullet objects
        for i in range(BULLET_POOL):
            b = bullet.Bullet(x=0, y=0, batch=self.sprite_bullet_batch)
            self.bullet_pool.append(b)
            self.bullets.append(b)
        
        if self.stage.music == None:
            self.music_player = None
        else:
            self.music_player = pyglet.media.Player()
            self.music_player.queue(self.stage.music)
            self.music_player.eos_action = 'loop'
            self.music_player.play()
        
    def title(self):
        self.music_player.pause()
        self.load_stage("00", True)        
        self.helicopter = None
        self.gunner = None
        self.rope = None
        
        self.context.do_menu()
        
        
    def message(self, message, timer=3.0, priority=1.0):
        """Write a message on the screen"""
        # example: GET READY, or DANGER: BOSS APPROACHING!
        if self.message_timer <= 0 or priority >= self.message_priority:
            self.message_label.text = message
            self.message_timer = timer
        
    def restart_stage(self):
        
        if self.stage.checkpoint:
            
            self.stage.load_checkpoint()
            self.gunners = self.__class__.gunners[:]
            x, y = self.stage.camera.vposition.x + 400, 400
            self.helicopter.__init__(x, y, batch=self.sprite_batch, context=self)
            self.gunner.__init__(x, y, batch=self.sprite_batch, context=self)
            self.rope.__init__(length=ROPE_SEGMENTS, anchor_start=self.helicopter, anchor_end=self.gunner, x=x, y=y)
             
            self.message("GET READY SOLDIER")
            self.music_player.seek(0)
            self.music_player.play()
        else:
            # no checkpoint, reload level
            self.__init__(self.keys)
            self.load_stage("01")
        
                
    def heli_down(self):
        self.stage.failure()
        if self.music_player != None: self.music_player.pause()
        
        self.lives -= 1
        
        if self.lives > 0:
            self.message("FAIL - %d LIVES REMAINING" % self.lives, 5.0)
            self.stage.delay(self.restart_stage, 5.0)            
        else:
            self.message("GAME OVER", 10.0)
            self.stage.delay(self.title, 10.0)
                
    def gunner_down(self):        
    
        if not self.helicopter.dying:            
            self.message("NOO! THEY KILLED %s!" % self.gunners.pop(), 2.0)
            if len(self.gunners) > 0:
                self.stage.delay(self.new_gunner, 3.0)
            else:
                self.stage.delay(lambda: self.message("EVERYONE IS DEAD", 2.0), 2.0)
                self.stage.delay(self.title, 10.0)
            
    def new_gunner(self):
        if not self.helicopter.alive: return
        if len(self.gunners) > 1:
            self.message("YOU'RE UP %s" % self.gunners[-1], 2.0)
        else:
            self.message("%s, YOU'RE OUR LAST HOPE" % self.gunners[-1], 2.0)
            
        self.gunner = gunner.Gunner(self.helicopter.vposition.x,self.helicopter.vposition.y, batch=self.sprite_batch, context=self)
        self.rope = rope.Rope(length=ROPE_SEGMENTS, anchor_start=self.helicopter, anchor_end=self.gunner, x=self.helicopter.vposition.x,y=self.helicopter.vposition.y)
        resources.gunner_jump.play()
        
    
    def fire(self, x,y,angle,enemy=False):
        x_comp = math.sin(math.radians(angle))
        y_comp = math.cos(math.radians(angle))
        self.add_bullet(x,y,x_comp,y_comp,angle,enemy)
        
    def add_bullet(self, x, y, x_comp, y_comp, angle, enemy=False):                
        """Someone fired a bullet. Grab the bullet from the bullet pool and append it to the bullets list."""
        
        if len(self.bullet_pool) > 0:
            b = self.bullet_pool.pop()
        else:
            b = bullet.Bullet(x=0, y=0, batch=self.sprite_batch)
            self.bullets.append(b)
                    
        if enemy: 
            b.enemy = True
            speed = ENEMY_BULLET_SPEED
            b.image = resources.enemy_bullet
        else:
            b.enemy = False
            speed = PLAYER_BULLET_SPEED
            b.image = resources.bullet
                    
        b.fire(x, y, x_comp, y_comp, angle, speed)
            
                    
    def remove_bullet(self, b):
        """A bullet has died. Let's put it back in the pool for reuse."""    
        b.pooled = True
        self.bullet_pool.append(b)
        
                
    def update(self, dt):
        """Perform one step of verlet integration."""        
                
        self.tick += 1
        
        # if self.tick % 10 == 0:
        #     self.message("e: %d" % len(self.stage.enemies), 0.16)
        
        if self.message_timer > 0:
            self.message_timer -= dt
        
        # Update the enemies, powerups and camera in the Stage object
        self.stage.update(TIME_STEP)        
        
        # No helicopter, so no point in continuing
        if self.helicopter == None: return
        
        # Verlet Step
        if self.helicopter.alive: 
            self.helicopter.update(TIME_STEP_SQ, self.keys)            
        if self.gunner.alive: 
            self.gunner.update(TIME_STEP_SQ, self.keys)
        self.rope.update(TIME_STEP_SQ)
                        
        # Update all bullets
        for b in self.bullets:
            if b.alive:   
                b.update(TIME_STEP_SQ)
            elif not b.pooled:
                # This bullet is dead so get it out of here
                self.remove_bullet(b)
                       
        # Satisfy Constraints
        if self.gunner.alive:
            self.gunner.vposition.y = max(8, self.gunner.vposition.y)
            self.rope.satisfy_constraints()
        if self.helicopter.alive:
            self.helicopter.vposition.x = min(self.stage.camera.vposition.x+WIDTH-32,  max(self.stage.camera.vposition.x+32, self.helicopter.vposition.x))
            self.helicopter.vposition.y = min(self.stage.height - 16, max(16, self.helicopter.vposition.y))
            self.rope.satisfy_constraints()
            
            
        # Collisions
                
        for e in self.stage.enemies:
            
            if e.alive and not e.dying:
                
                # Enemies collide with the helicopter
                if self.collide(self.helicopter, e):
                    self.helicopter.on_collide(e)
                    e.on_collide(self.helicopter)
                
                # Enemies collide with the player
                if self.collide(self.gunner, e):
                    delta = self.gunner.vposition - e.vposition                    
                    normal = vector.normalize(delta)
                    
                    suminvmass = (self.gunner.__class__.invmass + e.__class__.invmass)
                    
                    pentration = 8 + 16 / vector.length(delta)
                    self.gunner.vposition += normal * pentration * self.gunner.__class__.invmass / suminvmass
                    e.vposition           -= normal * pentration * e.__class__.invmass / suminvmass 
                    
                    self.gunner.on_collide(e)
                    e.on_collide(self.gunner)
                    
                            
        # Perform collision tests for all bullets               
        for b in self.bullets:
            if not b.alive: continue
            # All bullets die at the edge of the screen
            if not self.collide(self.stage.camera, b):
                b.die()
                                                
            if b.enemy:
                # Enemy bullets collide with the helictoper                
                if self.collide(self.helicopter, b):
                    self.helicopter.on_hit()
                    b.die()
                    
                # Enemy bullets collide with the gunner
                if self.collide(self.gunner, b):
                   self.gunner.on_hit()
                   b.die()
            else:

                # Player bullets collide with enemies
                for e in self.stage.enemies:                    
                    if e.alive and self.collide(e, b):
                        e.on_hit()
                        b.die()
                        

    def collide(self,a,b):
        return collision.collide(a.vposition, b.vposition, a.__class__.bounding, b.__class__.bounding)
         

    def draw(self):
        """Draw the current game scene."""

        self.stage.camera.enter()        
        self.stage.draw()                   # Draw backgrounds and enemies
        
        if not self.demo:
            self.sprite_batch.draw()            # Draw player objects
            self.sprite_bullet_batch.draw()     # Draw bullets
        
            if self.helicopter.alive:
                for r in self.rope.constraints:
                    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                        ('v2f', (r.a.vposition.x,r.a.vposition.y,r.b.vposition.x,r.b.vposition.y)),
                        ('c4B', (50,50,50,255,75,75,75,255))
                    )
            
            for e in self.stage.effects:
                e.draw()
        
        self.stage.camera.exit()
        
        if not self.demo:            
            if self.helicopter.health > 0:
                health_image_heli = resources.healthbar.get_region(0, 0,
                        resources.healthbar.width*self.helicopter.health/100.0, resources.healthbar.height)
                health_image_heli.blit(120, HEIGHT-resources.healthbar.height-5)
            self.score_label.text = "%07d" % self.score    
        
            if self.message_timer > 0:
                self.message_label.draw()
            
            self.score_label.draw()