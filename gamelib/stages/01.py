import resources, stage, random
from enemy import drone, turret, charger, boss
from constants import *

class Stage01(stage.Stage):
    
    def __init__(self, **kwargs):
        
        stage.Stage.__init__(self, 10000, 600, **kwargs)
        
        self.music = resources.Music1
        
        # A Primer on Stage Triggers:
        #
        # Triggers are a way to add simple event triggers into a stage.
        # A trigger is a object with 3 properties:
        # condition, callback, and repeat
        #
        # 1.    condition: a function or closure that returns a boolean.
        #       every frame, this condition will be tested. If it is true
        #       then the callback function is called.
        #
        # 2.    callback: a function or closure that is executed in the
        #       scope of the stage object if the trigger condition is True.
        #
        # 3.    repeat: a boolean value that determines whether the trigger
        #       will continue to be tested after it is executed. If it is
        #       false, that trigger will not be tested again.
        
        self.SPAWN_BUFFER=WIDTH+400 #should probably never be <WIDTH+100
        
        wave1 = [
            (drone.Drone,      self.SPAWN_BUFFER+0, 200),
            (drone.Drone,      self.SPAWN_BUFFER+0, 264),
            (drone.Drone,      self.SPAWN_BUFFER+0, 328),  
                       
            (drone.Drone,      self.SPAWN_BUFFER+400, 328),
            (drone.Drone,      self.SPAWN_BUFFER+400, 392),
            (drone.Drone,      self.SPAWN_BUFFER+400, 456),
            
            (drone.Drone,      self.SPAWN_BUFFER+800, 200),
            (drone.SuperDrone, self.SPAWN_BUFFER+800, 300),
            (drone.Drone,      self.SPAWN_BUFFER+800, 400),            
            
            (turret.Turret,    self.SPAWN_BUFFER, 0),
            (turret.Turret,    self.SPAWN_BUFFER+200, 0)
        ]
        
        wave2 = [
            (charger.Charger, self.SPAWN_BUFFER+0, 100),
            (charger.Charger, self.SPAWN_BUFFER+0, 164),        
            (charger.Charger, self.SPAWN_BUFFER+0, 228),
            (charger.Charger, self.SPAWN_BUFFER+0, 292),
            (charger.Charger, self.SPAWN_BUFFER+0, 364),       
            (charger.Charger, self.SPAWN_BUFFER+0, 428),
            (charger.Charger, self.SPAWN_BUFFER+0, 492),
            (charger.Charger, self.SPAWN_BUFFER+0, 556),
            
            (turret.Turret,    self.SPAWN_BUFFER+300, 0),
            (turret.Turret,    self.SPAWN_BUFFER-100, 0)
        ]
        
        wave3 = [
        
            (drone.SuperDrone,self.SPAWN_BUFFER+0, 450),
            (drone.Drone,     self.SPAWN_BUFFER+64, 450),
            (drone.Drone,     self.SPAWN_BUFFER+128, 450),
            (drone.Drone,     self.SPAWN_BUFFER+256, 450),
            (drone.Drone,     self.SPAWN_BUFFER+320, 450),    
            (drone.Drone,     self.SPAWN_BUFFER+384, 450),
             
            (drone.SuperDrone,self.SPAWN_BUFFER+864, 150),
            (drone.Drone,     self.SPAWN_BUFFER+928, 150),
            (drone.Drone,     self.SPAWN_BUFFER+992, 150),
            (drone.Drone,     self.SPAWN_BUFFER+1056, 150),
            (drone.Drone,     self.SPAWN_BUFFER+1120, 150),    
            (drone.Drone,     self.SPAWN_BUFFER+1184, 150)
        ]
        
        wave4 = [
                        
            (drone.SuperDrone,  self.SPAWN_BUFFER+0, 300),
            (drone.Drone,       self.SPAWN_BUFFER+64, 236),
            (drone.Drone,       self.SPAWN_BUFFER+64, 364),                
            (drone.Drone,       self.SPAWN_BUFFER+128, 428),       
            (drone.Drone,       self.SPAWN_BUFFER+128, 428)
        ]
        
        
        def camera_pos_check(x):
            def check(): return self.camera.vposition.x > x
            return check
        
        def spawnlist(wave):
            def sp_lst(): self.spawn_list(wave)
            return sp_lst
        
        def simple_wave_trigger(x, wave):
            return stage.Trigger(condition=camera_pos_check(x), callback=spawnlist(wave))
        
        self.triggers = [
            simple_wave_trigger(0, wave1),
            simple_wave_trigger(900, wave2),
            simple_wave_trigger(1200, wave2),
            simple_wave_trigger(1600, wave2),            
            simple_wave_trigger(2000, wave3),
            simple_wave_trigger(2800, wave4),   
            simple_wave_trigger(3300, wave2),
            simple_wave_trigger(3600, wave2),
            simple_wave_trigger(4200, wave1),
            simple_wave_trigger(4900,  wave3),
            simple_wave_trigger(4900+900, wave2+wave4),
            simple_wave_trigger(4900+1200, wave2),
            simple_wave_trigger(4900+1600,wave4),
            stage.Trigger(condition=camera_pos_check(7000), callback=self.set_checkpoint, repeat=False),
            stage.Trigger(condition=camera_pos_check(7200), callback=self.boss_battle, repeat=False)
            
        ]
        
        # move camera to the right automatically at 60 pixels per second
        self.camera.__init__(vx=75.0, automatic=True)
        self.backdrop.load(image=resources.sky, depth=0.0)
        self.backdrop.load(image=resources.stars, y=280, depth=0.25)
        self.backdrop.load(image=resources.mountains, depth=0.5)
        self.backdrop.load(image=resources.trees, depth=0.75)        
        self.backdrop.load(image=resources.ground, depth=1.0, y=-5)
        
        self.set_checkpoint()
    
                
    def boss_battle(self):
        
        chargers = [
            (charger.Charger, self.SPAWN_BUFFER+0, 100),
            (charger.Charger, self.SPAWN_BUFFER+0, 164),        
            (charger.Charger, self.SPAWN_BUFFER+0, 228),
            (charger.Charger, self.SPAWN_BUFFER+0, 292),
            (charger.Charger, self.SPAWN_BUFFER+0, 364),       

        ]
        
        self.message("BOSS APPROACHING")
        self.boss = self.spawn_ahead(boss.Boss, self.SPAWN_BUFFER, 300)
        self.camera.velocity.x = 200.0

        self.triggers += [
            stage.Trigger(condition=lambda: self.boss.alive and not self.boss.dying and random.random() > 0.97, callback=lambda: self.spawn_list(chargers), repeat=True),
            stage.Trigger(condition=lambda: self.boss.dying, callback=self.boss_battle_over, repeat=False),
            stage.Trigger(condition=lambda: not self.boss.alive, callback=self.victory, repeat=True)
        ]
        
    def boss_battle_over(self):
        self.camera.velocity.x = 100.0