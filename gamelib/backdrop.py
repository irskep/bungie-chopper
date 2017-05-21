from constants import *
import pyglet, random

class Backdrop:

    def __init__(self, camera):
        
        self.camera = camera            
        self.objects = []
    
    def load(self, image, x=0.0, y=0.0, depth=0.0):
        self.objects.append(BackgroundImage(image, x, y, depth))
        self.objects.sort(cmp=lambda obj1, obj2: int(obj1.depth) - int(obj2.depth))
        
    def update(self, dt):
        for obj in self.objects:
            obj.update(-self.camera.velocity.x * dt, -self.camera.velocity.y * dt)
    
    def draw(self):
        for obj in self.objects:
            obj.draw(self.camera.vposition.x, self.camera.vposition.y)
            
    def reset(self):
        for obj in self.objects:
            obj.x = 0 # self.camera.vposition.x - obj.image.width / 2
                
class BackgroundImage:
    
    def __init__(self, image, x=0.0, y=0.0, depth = 0.0):
        self.x, self.y = x, y
        self.image = image
        self.depth = depth
        
            
    def update(self, x, y):
        
        self.x += x * self.depth
        self.y += y * self.depth
                
        if self.x <= -self.image.width:
            self.x += self.image.width
        elif self.x > 0:
            self.x -= self.image.width
            
    
    def draw(self, x, y):                
        tile_x = 0
        while tile_x < WIDTH + self.image.width * 2:
            self.image.blit(x + tile_x + self.x, y + self.y)
            tile_x += self.image.width

# class BackgroundRect:
#     depth = 0.0
#     def __init__(self, x, y, w, h, depth = 0.0):
#         self.x, self.y, self.w, self.h, self.depth = x, y, w, h, depth
#         self.fill = None
#     
#     def update(self, x, y):
#         self.x += x * self.depth
#         self.y += y * self.depth
#     
#     def draw(self, camera_x):
#         
#         if self.fill:
#             fill = self.fill
#         else:
#             c = int(25 + 100*(self.depth/4))
#             fill = (c, c, c+100, 255) * 4
#         pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
#            ('v2f', (self.x,self.y,self.x,self.y+self.h,self.x+self.w,self.y+self.h,self.x+self.w,self.y)),
#            ('c4B', fill)
#         )