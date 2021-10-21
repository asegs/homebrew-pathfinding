import random
import math
from enum import Enum
import sys
import heapq

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


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f
        

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

def generate_maze(width,height,freq,use_symbols = True):
    maze = []
    for row in range(0,height):
        row = [0] * width
        for col in range(0,width):
            if random.random() < freq:
                row[col] = 1
        maze.append(row)
    start = (random.randint(0,height-1),random.randint(0,width-1))
    
    end = (random.randint(0,height-1),random.randint(0,width-1))
    if use_symbols:
        maze[start[0]][start[1]] = 2
        maze[end[0]][end[1]] = 3
        
    return (maze,start,end)


def display_maze(maze,show_path = True,start = False,end = False):
    for row in maze:
        for col in row:
            if col == 0 or ((not show_path) and col == 4):
                print_normal(' ')
            elif col == 1:
                print_black(' ')
            elif col == 2 or (end and (row,col) == end ) :
                print_green(' ')
            elif col == 3 or (start and (row,col) == start):
                print_blue(' ')
            else:
                print_red(' ')
        print()


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
            temp_dist = pythag_dist(end,pair)
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
                return current_path
            maze[pos[0]][pos[1]] = 4
            backtracing = False
    return current_path


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def astar(maze,start,end,allow_diagonal_movement = False):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    return False
 



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

def display_astar_path(maze,arr,start,end):
    maze[start[0]][start[1]] = 2
    maze[end[0]][end[1]] = 3
    arr = arr[0:len(arr)-1]
    for coords in arr:
        maze[coords[0]][coords[1]] = 8
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


def solve_astar(width,height,freq,hide_unsolvable = False):
    maze,start,end = generate_maze(width,height,freq)
    if not hide_unsolvable:
        display_maze(maze,False,start,end)
        print("____________________________")
        print()
        
    stack = astar(maze,start,end)
    if not stack:
        if not hide_unsolvable:
            print("Unsolvable maze.")
        return False
    
    if hide_unsolvable:
        display_maze(maze,False,start,end)
        print("____________________________")
        print()
    display_astar_path(maze,stack,start,end)
    return True


def test(args):
    if len(args) == 1:
        return
    w = int(args[1])
    h = int(args[2])
    f = float(args[3])/100.0
    if len(args) == 5:
        if args[4] == "s":
            solved = solve_astar(w,h,f,True)
            while not solved:
                solved = solve_astar(w,h,f,True)
        else:
            for i in range(0,int(args[4])):
                solve_astar(w,h,f)
    else:
        solve_astar(w,h,f)



if __name__ == "__main__":
   test(sys.argv)


