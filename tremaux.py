import random
import sys
import time


"""
0 means unexplored
1 means wall
2 means start
3 means end
4 means on current path
"""

terms = [(0,-1),(-1,0),(0,1),(1,0)]

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

def get_coords_for_enum(pos,pair,backtracing = False):
    if backtracing:
        return (pos[0]+pair[0] * -1,pos[1]+pair[1] * -1)
    return (pos[0]+pair[0],pos[1]+pair[1])

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


def display_maze(maze,show_path = True):
    for row in maze:
        for col in row:
            if col == 0 or ((not show_path) and col == 4):
                print_normal(' ')
            elif col == 1:
                print_black(' ')
            elif col == 2:
                print_green(' ')
            elif col == 3:
                print_blue(' ')
            else:
                print_red(' ')
        print()


def code_safe(code):
    return code == 0 or code == 3

def square(n):
    return n * n

def tile_safe(maze,pos):
    return (0 <= pos[1] < len(maze[0]) and 0 <= pos[0] < len(maze)) and code_safe(maze[pos[0]][pos[1]])

def pythag_dist(pos1,pos2):
    return square(pos2[0]-pos1[0]) + square(pos2[1]-pos1[1])


def pick_best_vertex(maze,end,pos):
    shortest_distance = -1
    coord_term = False
    coord_pair = (0,0)
    for term in terms:
        pair = get_coords_for_enum(pos,term)
        if tile_safe(maze,pair):
            temp_dist = pythag_dist(end,pair)
            if shortest_distance == -1:
                shortest_distance = temp_dist
                coord_term = term
                coord_pair = pair
            elif temp_dist < shortest_distance:
                shortest_distance = temp_dist
                coord_term = term
                coord_pair = pair
    if shortest_distance == -1:
        return (False,False)
    return (coord_term,coord_pair)
        
    


def explore(maze,start,end):
    t = time.time()
    shortest_path = -1
    current_path = SLinkedList()
    current_path.headval = Node((start[0],start[1]))
    pos = (start[0],start[1])
    last_directions = SLinkedList()
    backtracing = False
    while pos != end:
        term,pair = pick_best_vertex(maze,end,pos)
        if not pair:
            if pos == start:
                return False
            backtracing = True
            maze[pos[0]][pos[1]] = 1
            pos = get_coords_for_enum(pos,stack_pop(last_directions),True)
            stack_pop(current_path)
        else:
            pos = pair
            stack_add(current_path,pos)
            stack_add(last_directions,term)
            if maze[pos[0]][pos[1]] == 3:
                f = time.time()
                print((f-t) * 1000)
                return current_path
            maze[pos[0]][pos[1]] = 4
            backtracing = False
    return current_path




def print_red(txt):
    print("\033[48;2;255;0;0m" + txt +"\033[0m",end='')

def print_blue(txt):
    print("\033[48;2;0;208;233m" + txt +"\033[0m",end='')

def print_green(txt):
    print("\033[48;2;9;152;13m" + txt +"\033[0m",end='')

def print_black(txt):
    print("\033[48;2;0;0;0m" + txt +"\033[0m",end='')

def print_normal(txt):
    print("\033[48;2;255;255;255m" + txt +"\033[0m",end='')

def display_path(maze,stack):
    stack_pop(stack)
    while stack.size > 0:
        node = stack_pop(stack)
        maze[node[0]][node[1]] = 8
    display_maze(maze)
                
        
def solve(width,height,freq,hide_unsolvable = False):
    maze,start,end = generate_maze(width,height,freq)
    if not hide_unsolvable:
        display_maze(maze)
        print("____________________________")
        print()
        
    stack = explore(maze,start,end)
    if not stack:
        if not hide_unsolvable:
            print("Unsolvable maze.")
        return False
    
    if hide_unsolvable:
        display_maze(maze,False)
        print("____________________________")
        print()
    display_path(maze,stack)
    return True
    
def test(args):
    w = int(args[1])
    h = int(args[2])
    f = float(args[3])/100.0
    if len(args) == 5:
        if args[4] == "s":
            solved = solve(w,h,f,True)
            while not solved:
                solved = solve(w,h,f,True)
        else:
            for i in range(0,int(args[4])):
                solve(w,h,f)
    else:
        solve(w,h,f)

##possibly could flag each tile with open directions, if returning one is only open direction, auto close (avoid 4 tile safes per backtrace)

    
if __name__ == "__main__":
   test(sys.argv)


