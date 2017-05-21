'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pyglet
pyglet.options['deebug_gl'] = False
from constants import *
from settings import *
import game, menu, util.fixedsteploop, sys, data, resources, util.draw
from pyglet.window import key
from pyglet import gl

class GameWindow(pyglet.window.Window):
    
    """This window subclasses the Pyglet window class. It holds the main game instance, and dutifuly 
    passes events from the mouse and keyboard to the current state object. The general idea is that events
    can be passed down to any module, being the game object, the title screen, or the menus. This class
    is also respoisble for calling updates periodically. Right now that function is delegated to the
    FixedStepLoop class (located in util.fixedsteploop). This class will call the physics updates at
    a constant framerate, but will run the drawing routines as fast as possible. (actually, this is
    handled implicitly through the pyglet.Window.event.on_draw method)"""
    
    def __init__(self, width=800, height=600):
        if settings['fullscreen']:
            pyglet.window.Window.__init__(self, fullscreen=True)
        else:
            pyglet.window.Window.__init__(self, width=width, height=height)
        self.set_caption ("Elite Bungie Chopper Squadron")
        self.fps_display = pyglet.clock.ClockDisplay()
        self.keys = pyglet.window.key.KeyStateHandler() # What keys/commands are currently being pressed?
        self.push_handlers(self.keys)            
        
        self.timer = util.fixedsteploop.FixedStepLoop(self.update, TIME_STEP, MAX_CYCLES_PER_FRAME)
                
        self.game = game.Game(self.keys, self)
        self.game.load_stage("00", True)
        
        self.menu = menu.Menu(self)
        
        self.state = self.menu
        self.push_handlers(self.menu)
        self.timer.play()
                
        gl.glClearColor(128,128,255,255)
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glShadeModel(gl.GL_SMOOTH)# Enables Smooth Shading
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)#Type Of Blending To Perform
        gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT,gl.GL_NICEST);#Really Nice Perspective Calculations
        gl.glHint(gl.GL_POINT_SMOOTH_HINT,gl.GL_NICEST);#Really Nice Point Smoothing
        gl.glDisable(gl.GL_DEPTH_TEST)
                        
        self.clear()
        
        resources.chopper_blades.play()
    
    def do_play(self):
        if self.state == self.menu: self.pop_handlers()
        if self.game.demo:
            self.game.load_stage("01")
            
        self.state = self.game
        self.timer.play()

    def do_menu(self):
        if self.state != self.menu and not self.game.demo: self.timer.pause()
        self.state = self.menu
        self.push_handlers(self.menu)
                
    def update(self, dt):
        self.game.update(dt) 
                
    def on_draw(self):
        self.clear()
        gl.glPushMatrix()
        zoom = float(self.height) / float(HEIGHT)
        gl.glScalef(zoom, zoom, 1)
        offset_x = (self.width/zoom-WIDTH)/2
        if offset_x > 0:    #letterboxing pt. 1
            gl.glTranslatef(offset_x,0,0)
        
        self.game.draw()
        #self.fps_display.draw()
        
        if self.state == self.menu:
            self.menu.draw()
        
        if offset_x > 0:    #letterboxing pt. 2
            gl.glTranslatef(-offset_x,0,0)
            gl.glColor4f(0,0,0,1)
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex3f(0,0,0)
            gl.glVertex3f(offset_x,0,0)
            gl.glVertex3f(offset_x,HEIGHT,0)
            gl.glVertex3f(0,HEIGHT,0)
            gl.glVertex3f(offset_x+WIDTH,0,0)
            gl.glVertex3f(offset_x*2+WIDTH,0,0)
            gl.glVertex3f(offset_x*2+WIDTH,HEIGHT,0)
            gl.glVertex3f(offset_x+WIDTH,HEIGHT,0)
            gl.glEnd()
            gl.glColor4f(1,1,1,1)
        gl.glPopMatrix()

    
    # INPUT EVENT HANDLERS
        
    # def on_mouse_motion(self, x, y, dx, dy):
    #     pass
    #     
    # def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    #     pass
    #     
    # def on_mouse_press(self, x, y, button, modifiers):
    #     print x, y, button, modifiers
    # 
    # def on_mouse_release(self, x, y, button, modifiers):
    #     pass
    #         
    # def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    #     pass
    #         
    def on_key_press(self, symbol, modifiers):
        if symbol == key.F and modifiers & key.MOD_COMMAND or modifiers & key.MOD_ALT:
            self.set_fullscreen(not self.fullscreen)
            settings['fullscreen'] = not settings['fullscreen']
        elif symbol == key.ESCAPE:
            self.do_menu()        
        elif self.state == self.menu:
            pass #self.menu.on_key_press(symbol, modifiers)
    #                   
    # def on_key_release(self, symbol, modifiers):
    #     pass

def main():
    sys.path.append("gamelib")
    sys.path.append("gamelib/stages")
    sys.path.append("libs")
    g = GameWindow(width=800, height=600)
    pyglet.app.run()
    save_settings()

    