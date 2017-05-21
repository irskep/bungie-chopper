import pyglet

class FixedStepLoop(object):
    """ 
    A fixed time step loop for pyglet. 
    """ 
    def __init__(self, update_function, step, max_step): 
        self.update_function = update_function 
        self.step = step 
        self.max_step = max_step 
        self.simulation_time = 0.0 - self.step 
        self.real_time = 0.0 
        self.frame_time = 0.0 
        self.playing = False
            
    def play(self):
        if not self.playing:
            pyglet.clock.schedule(self._tick)
            self.playing = True
        
    def pause(self):
        pyglet.clock.unschedule(self._tick)
        self.playing = False
            
    def _tick(self, T): 
        self.real_time += T 
        self.frame_time += T 

        if T > self.max_step: 
            self.simulation_time = self.real_time - self.step 

        while self.simulation_time <= self.real_time: 
            self.update_function(self.step) 
            self.simulation_time += self.step 
            self.frame_time = 0.0 
            
            self.step_fraction =  self.frame_time / self.step