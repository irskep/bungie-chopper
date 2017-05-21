from constants import *
import pyglet
from pyglet.window import key

class Menu:
    
    def __init__(self, context):
        
        self.context = context
        kwargs = dict(
            font_name="Press Start K", font_size=16, 
            anchor_x='center', anchor_y='center'
        )
        
        self.title = pyglet.text.Label(text="ELITE BUNGIE CHOPPER SQUADRON", x=WIDTH//2, y=HEIGHT*0.84, **kwargs)
        self.title_border_1 = pyglet.text.Label(text="-----------------------------", 
            x=WIDTH//2, y=self.title.y+20, **kwargs)
        self.title_border_2 = pyglet.text.Label(text="-----------------------------", 
            x=WIDTH//2, y=self.title.y-20, **kwargs)
        
        self.move_msg = pyglet.text.Label(text="Arrow keys: MOVE HELICOPTER", x=WIDTH//2, y=HEIGHT*0.6, **kwargs)
        self.shoot_msg = pyglet.text.Label(text="A/S/D/W: SHOOT", x=WIDTH//2, y=HEIGHT*0.54, **kwargs)
        
        self.fullscreen_msg = pyglet.text.Label(text="Cmd-F, Alt-F: TOGGLE FULLSCREEN", x=WIDTH//2, y=HEIGHT*0.36, **kwargs)
        self.quit_msg = pyglet.text.Label(text="Esc, Cmd-Q, Alt-Q: QUIT", x=WIDTH//2, y=HEIGHT*0.3, **kwargs)
        
        self.start_msg = pyglet.text.Label(text="Space: START GAME", x=WIDTH//2, y=HEIGHT*0.1, **kwargs)
        self.start_border_1 = pyglet.text.Label(text="-----------------", x=WIDTH//2, y=self.start_msg.y+20, **kwargs)
        self.start_border_2 = pyglet.text.Label(text="-----------------", x=WIDTH//2, y=self.start_msg.y-20, **kwargs)
        
        self.outline_labels = [
            (self.title, (100,100,255,255)),
            (self.title_border_1, (100,100,255,255)),
            (self.title_border_2, (100,100,255,255)),
            (self.move_msg, (240,240,0,255)),
            (self.shoot_msg, (255,128,0,255)),
            (self.start_msg, (0,255,0,255)),
            (self.start_border_1, (0,255,0,255)),
            (self.start_border_2, (0,255,0,255)),
            (self.quit_msg, (255,0,0,255)),
            (self.fullscreen_msg, (128,128,128,255)),
        ]
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER or symbol == key.SPACE:
            self.context.do_play()
        if symbol == key.ESCAPE:
            pyglet.app.exit()
    
    def draw_label_with_outline(self, label, fill_color = (100,100,255,255), outline_color = (255,255,255,255)):
        label.color = outline_color
        label.y -= 2
        label.draw()
        label.y += 4
        label.draw()
        label.x += 2
        label.y -= 2
        label.draw()
        label.x -= 4
        label.draw()
        label.x += 2
        label.color = fill_color
        label.draw()

    def draw(self):
        for label, color in self.outline_labels:
            self.draw_label_with_outline(label, fill_color=color)