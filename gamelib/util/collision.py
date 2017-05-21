import vector, math

CIRCLE = 1
RECT = 2

def point_to_AABB(a_x, a_y, b_x, b_y, b_width, b_height):
    if a_x < b_x: return False
    if a_x > b_x + b_width: return False
    if a_y < b_y: return False
    if a_y > b_y + b_height: return False
    return True
    
def circle_to_AABB(a_x, a_y, a_radius, b_x, b_y, b_width, b_height):
    #todo: this needs to handle collisions with vertecies better
    if a_x + a_radius < b_x: return False
    if a_x - a_radius > b_x + b_width: return False
    if a_y + a_radius < b_y: return False
    if a_y - a_radius > b_y + b_height: return False
    
    return True    
    
def AABB_to_AABB(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    if a_x > b_x + b_width: return False
    if b_x > a_x + a_width: return False
    if a_y > b_y + b_height: return False
    if b_y > a_y + a_height: return False
    return True
            
def circle_to_circle(a_x, a_y, a_radius, b_x, b_y, b_radius):
    return math.hypot(a_x - b_x, a_y - b_y) < a_radius + b_radius
    
def collide(origin_a, origin_b, a, b):
    
    # uncoment this for multiple bounding shapes
    # if type(a) == "list":
    #     for aa in a: return collide(origin_a, origin_b, aa, b)
    # elif type(b) == "list":
    #     for bb in b: return collide(origin_a, origin_b, a, bb)
    # el
    if not a or not b: return False
    if a.__class__.type == CIRCLE and b.__class__.type == CIRCLE:        

        if not AABB_to_AABB(
            origin_a.x + a.vposition.x - a.radius, 
            origin_a.y + a.vposition.y - a.radius, 
            a.radius * 2, a.radius * 2,
            origin_b.x + b.vposition.x - b.radius, 
            origin_b.y + b.vposition.y - b.radius, 
            b.radius * 2, b.radius * 2
        ): return False
        
        return circle_to_circle(
            origin_a.x + a.vposition.x, origin_a.y + a.vposition.y, a.radius,
            origin_b.x + b.vposition.x, origin_b.y + b.vposition.y, b.radius)
            
    elif a.__class__.type == CIRCLE and b.__class__.type == RECT:
        return circle_to_AABB(
            origin_a.x + a.vposition.x, 
            origin_a.y + a.vposition.y, 
            a.radius, 
            origin_b.x + b.vposition.x, 
            origin_b.y + b.vposition.y,
            b.width, b.height)
            
    elif a.__class__.type == RECT and b.__class__.type == CIRCLE:
        return circle_to_AABB(
            origin_b.x + b.vposition.x, 
            origin_b.y + b.vposition.y,
            b.radius, 
            origin_a.x + a.vposition.x, 
            origin_a.y + a.vposition.y,
            a.width, a.height)
            
    elif a.__class__.type == RECT and b.__class__.type == RECT:
        return AABB_to_AABB(
            origin_a.x + a.vposition.x, 
            origin_a.y + a.vposition.y,
            a.width, a.height, 
            origin_b.x + b.vposition.x, 
            origin_b.y + b.vposition.y,
            b.width, b.height)
    else:
        return False


class Circle:
    
    type = CIRCLE
    
    def __init__(self,  radius, x=0, y=0):
        self.vposition = vector.Vector(x,y)
        self.radius = radius
        
class Rect:
    
    type = RECT
    
    def __init__(self, width, height, x=0, y=0,):
        self.vposition = vector.Vector(x-width/2, y-height/2)
        self.width = width
        self.height = height





# Recursive Dimensional Clustering: A Fast Algorithm for Collision Detection 
# Steve Rabin, Nintendo of America

#   1.  Start with the x-axis. 

#   2.  Construct a linked list of object boundaries in this dimension. 

#   3.  Sort that list by boundary position, from lowest to highest. 

#   4.  Find groups using the open/close "bracket matching" algorithm in Listing 
#       2.7.2. 

        # int count = 0 
        # Clear( currentGroup ) 
        # for( element in list ): 
        #   if( element is an "open bracket" ) { 
        #       count++ 
        #       Add entity to currentGroup
        #   else { #element is a "closed bracket" 
        #       count- -  
        #       if( count == 0 ) { #entire group found 
        #           Store( currentGroup ) 
        #           Clear( currentGroup ) 
        # assert( count == 0 )  
        

#   5.  For each group found in that dimension, repeat steps 2-5 in the other 
#       dimension(s) until the group no longer gets subdivided and all dimensions 
#       have been analyzed for that unique group. 




# def RDC (Pairs& pairs, Group& group, Axis axisl, Axis axis2, Axis axisS):
#
#     # "pairs" holds all final pairs that are in collision 
#     # "group" is the current group of objects to analyze 
#     # "axisl" is the axis to analyze within this function 
#     # "axis2", "a3" will be analyzed in recursive calls 
#     if( Size( group ) < 10 || axisl == INVALID_AXIS ): #end recursion and test for collisions 
#           BruteForceComparisonf pairs, subGroup )       
#     else:
#           # for this group, find the boundaries and sort them 
#           OpenCloseBoundaryList boundaries 
#           FindOpenCloseBoundaries( axisl, group, boundaries ) 
#           SortOpenCloseBoundaries( boundaries ) # O(nlogn) 
#           Group subGroup 
#           unsigned int count = 0 
#           Axis newAxisI = axis2 
#           Axis newAxis2 = axisS: 
#           Axis newAxis3 = INVALID_AXIS 
#           bool groupSubdivided = false 
#           # subdivide the group if possible and call recursively 
#           for( every curBoundary in boundaries list ): 
#               if( curBoundary is "open bracket" ): #this entity lies within a cluster group 
#                   count++ 
#                   AddToGroup( subGroup, curBoundary->entity ) 
#               else:
#                   count-- 
#                   if( count == 0 ): 
#                       # found the end of a cluster group - take subgroup 
#                       # and call recursively on remaining axis' 
#                       if( curBoundary != GetLastBoundary( boundaries )):
#                           # this group is being subdivided - remember 
#                           groupSubdivided = true
#                   
#                       if( groupSubdivided ): #reconsider all other axis' 
#                           if ( axisl == X_AXIS ):
#                               newAxisI = Y_AXIS 
#                               newAxis2 = Z_AXIS 
#                           elif ( axisl == Y_AXIS ):
#                               newAxisI = X_AXIS 
#                               newAxis2 = Z_AXIS 
#                           elif ( axisl == Z_AXIS ):
#                               newAxisI = X_AXIS 
#                               newAxis2 = Y_AXIS 
#
#                   # recursive call 
#                   RecursiveClustering( pairs, subGroup, newAxisI, newAxis2, INVALID_AXIS ) 
#                   Clear( subGroup ) #clear the subGroup for the next group 
