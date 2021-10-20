import random
import math

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

def tile_safe(maze,row,col):
    m_height = len(maze)
    m_width = len(maze[0])
    return (0 <= col < m_width and 0 <= row < m_height) and code_safe(maze[row][col])

def pythag_distance(r1,c1,r2,c2):
    return math.sqrt(abs(square(r2-r1)) + abs(square(c2-c1)))



def pick_best_vertex(maze,end,row,col):
    coord_pairs = []
    shortest_distance = 0
    has_set_shortest = False
    coord_idx = 0
    directions = [0,-1,-1,0,0,1,1,0]
    for i in range(0,len(directions),2):
        pair = (row + directions[i],col + directions[i+1])
        if tile_safe(maze,pair[0],pair[1]):
            coord_pairs.append(pair)
    for i,pair in enumerate(coord_pairs):
        temp_dist = pythag_distance(end[0],end[1],pair[0],pair[1])
        if not has_set_shortest:
            shortest_distance = temp_dist
            has_set_shortest = True
        else:
            if temp_dist < shortest_distance:
                shortest_distance = temp_dist
                coord_idx = i
    if not has_set_shortest:
        return False
    return coord_pairs[coord_idx]

def explore(maze,start,end):
    print(pick_best_vertex(maze,end,start[0],start[1]))


maze,start,end = generate_maze(10,10,0.25)
explore(maze,start,end)
display_maze(maze)



