import resources, stage
from enemy import drone
from constants import *

class Stage00(stage.Stage):
    """This is the demo Stage"""
    
    def __init__(self, **kwargs):
        
        stage.Stage.__init__(self, 10000, 600, **kwargs)
       
        # move camera to the right automatically at 60 pixels per second
        self.camera.__init__(vx=75.0, automatic=True)
        self.backdrop.load(image=resources.sky, depth=0.0)
        self.backdrop.load(image=resources.stars, y=280, depth=0.25)
        self.backdrop.load(image=resources.mountains, depth=0.5)
        self.backdrop.load(image=resources.trees, depth=0.75)        
        self.backdrop.load(image=resources.ground, depth=1.0, y=-5)
