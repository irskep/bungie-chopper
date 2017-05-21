from constants import *
from util import vector
import verlet, math

class Rope:
    
    """This class implements a rope of varaible length, which is anchored to two objects. Each of the objects (anchor_start and
    anchor_end) must have a "position" property, which is a vector. """
    
    def __init__(self, length, anchor_start, anchor_end,x=400,y=400):
        """Build a rope out of a list of nodes"""        
        self.length = length
        self.anchor_start = anchor_start
        self.anchor_end = anchor_end        
        self.constraints = []
        self.nodes = []
                
        # Build the rope
        for n in range(self.length):   
            node = verlet.VerletObject(x, y)
            node.forces.y = GRAVITY # Gravity
            self.nodes.append(node)
            
            if n > 0: 
                # Create constraints between rope nodes
                self.constraints.append(verlet.Constraint(self.nodes[n-1], self.nodes[n], ROPE_SEGMENT_LENTH))
            
        self.start = self.nodes[0]
        self.end = self.nodes[self.length-1]        
        
        # Attach the end anchor to the end of the rope
        self.constraints.append(verlet.Constraint(self.end, anchor_end, 1))
                    
                    
    def update(self, dt2):
        """Update each rope node."""     
        for n in self.nodes:            
            n.update(dt2, ROPE_DAMPENING)
        
        
    def satisfy_constraints(self):
        """Satisfy the rope constaints so it behaves like a rope. This method does not yet take particle mass
        into account."""
        
        # for n in self.nodes:
        #     # collide with the floor
        #     n.vposition.y = max(0, n.vposition.y)
        
        
        for i in range(ROPE_RELAXATION):
            for c in self.constraints:                
                delta = c.a.vposition - c.b.vposition                
                rl2 = c.restlength * c.restlength  # precalculate restlength ** 2
                delta *= rl2 / (vector.dot(delta,delta) + rl2) - 0.5                
                c.a.vposition += delta
                c.b.vposition -= delta
                
            self.start.vposition.x = self.anchor_start.vposition.x
            self.start.vposition.y = self.anchor_start.vposition.y - 16