from pyglet.gl import *
import pyglet.graphics

def box(x,y,width,height,fill,stroke = None):

    if len(fill) == 4: fill *= 4
    elif len(fill) == 8: fill *= 2

    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,            
       ('v2f', (x,y,x,y+height,x+width,y+height,x+width,y)),
       ('c4B', fill)
    )

    if not stroke: return

    if len(stroke) == 4: stroke *= 4
    elif len(stroke) == 8: stroke *= 2

    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,            
       ('v2f', (x,y,x,y+height,x+width,y+height,x+width,y)),
       ('c4B', stroke)
    )

def circle(x,y,radius, fill,stroke = None):    
    glPushMatrix()
    glColor4f(*fill)
    glTranslatef(x, y, 0)
    quadric = gluNewQuadric()    
    gluDisk(quadric, 0, radius, 60,  1)
    glPopMatrix()