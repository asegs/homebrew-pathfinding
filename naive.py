import random
import math
from enum import Enum

class Direction(Enum):
    LEFT = (0,-1)
    UP = (-1,0)
    RIGHT = (0,1)
    DOWN = (1,0)

"""
0 means unexplored
1 means wall
2 means start
3 means end
4 means on current path
"""

class Node:
    def __init__(self,dataval=None):
        self.dataval = dataval
        self.nextval = None
class SLinkedList:
    def __init__(self):
        self.headval = None
        self.size = 0
        

def stack_add(stack,data):
    new_node = Node(data)
    new_node.nextval = stack.headval
    stack.headval = new_node
    stack.size += 1
    

def stack_pop(stack):
    new_node = stack.headval
    stack.headval = new_node.nextval
    stack.size -= 1
    return new_node.dataval

def get_coords_for_enum(pos,enum_str,backtracing = False):
    mod = Direction[enum_str].value
    if backtracing:
        return (pos[0]+mod[0] * -1,pos[1]+mod[1] * -1)
    return (pos[0]+mod[0],pos[1]+mod[1])

def generate_maze(width,height,freq):
    maze = []
    for row in range(0,height):
        row = [0] * width
        for col in range(0,width):
            if random.random() < freq:
                row[col] = 1
        maze.append(row)
    start = (random.randint(0,height-1),random.randint(0,width-1))
    maze[start[0]][start[1]] = 2
    end = (random.randint(0,height-1),random.randint(0,width-1))
    maze[end[0]][end[1]] = 3
    return (maze,start,end)


def display_maze(maze):
    for row in maze:
        print(row)


def code_safe(code):
    return code == 0 or code == 3

def square(n):
    return n * n

def tile_safe(maze,pos):
    m_height = len(maze)
    m_width = len(maze[0])
    return (0 <= pos[1] < m_width and 0 <= pos[0] < m_height) and code_safe(maze[pos[0]][pos[1]])

def pythag_dist(pos1,pos2):
    return math.sqrt(abs(square(pos2[0]-pos1[0])) + abs(square(pos2[1]-pos1[1])))


def pick_best_vertex(maze,end,pos):
    terms = ["LEFT","UP","RIGHT","DOWN"]
    shortest_distance = -1
    has_set_shortest = False
    coord_term = False
    coord_pair = (0,0)
    for term in terms:
        pair = get_coords_for_enum(pos,term)
        if tile_safe(maze,pair):
            temp_dist = pythag_dist(pos,pair)
            if not has_set_shortest:
                shortest_distance = temp_dist
                coord_term = term
                coord_pair = pair
                has_set_shortest = True
            elif temp_dist < shortest_distance:
                shortest_distance = temp_dist
                coord_term = term
                coord_pair = pair
    if not has_set_shortest:
        return (False,False)
    return (coord_term,coord_pair)
        
    


def explore(maze,start,end):
    ##need directions stack
    shortest_path = -1
    found_paths = []
    current_path = SLinkedList()
    current_path.headval = Node((start[0],start[1]))
    pos = (start[0],start[1])
    last_dir = False
    backtracing = False
    while pos != end:
        term,pair = pick_best_vertex(maze,end,pos)
        if not pair:
            if pos == start:
                return found_paths
            backtracing = True
            print(pos)
            maze[pos[0]][pos[1]] = 1
            pos = get_coords_for_enum(pos,last_dir,True)
            stack_pop(current_path)
        else:
            pos = pair
            stack_add(current_path,pos)
            maze[pos[0]][pos[1]] = "*"
            last_dir = term
    found_paths.append(current_path)
    return found_paths
            
        
        
        


maze,start,end = generate_maze(10,10,0.10)
stack = explore(maze,start,end)[0]
display_maze(maze)



