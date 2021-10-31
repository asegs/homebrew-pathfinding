import random

class Node:
    def __init__(self,path_parent,arrival,remaining,row,col):
        self.path_parent = path_parent
        self.arrival = arrival
        self.remaining = remaining
        self.row = row
        self.col = col
        self.left = None
        self.right = None
        self.graph_parent = None

    def estimate(self):
        return self.arrival + self.remaining

    def matches(self,node):
        return self.row == node.row and self.col == node.col

class PriorityQueue:
    def __init__(self):
        self.head = None


terms = [(0,-1),(-1,0),(0,1),(1,0)]

def insert_node_helper(parent,node):
    if parent.matches(node):
        if node.estimate() < parent.estimate():
            parent.path_parent = node.path_parent
            parent.arrival = node.arrival
    if node.estimate() >= parent.estimate():
        if not parent.right:
            node.graph_parent = parent
            parent.right = node
            return
        insert_node_helper(parent.right,node)
    else:
        if not parent.left:
            node.graph_parent = parent
            parent.left = node
            return
        insert_node_helper(parent.left,node)

def insert(queue,node):
    if not queue.head:
        queue.head = node
    else:
        insert_node_helper(queue.head,node)

def take_closest_helper(parent):
    if not parent.left:
        if parent.right:
            parent_root = parent.graph_parent
            parent_root.left = parent.right
            parent.right.graph_parent = parent_root
        else:
            parent.graph_parent.left = None
            
        return parent
    else:
        return take_closest_helper(parent.left)
def pop(queue):
    if not queue.head:
        return None
    if not queue.head.left:
        to_return = queue.head
        if queue.head.right:
            queue.head = queue.head.right
        else:
            queue.head = None
        return to_return
    return take_closest_helper(queue.head)


def print_depth(msg,depth):
    for i in range(0,depth):
        print("\t",end="")
    print(msg)
    
def print_tree(queue,depth):
    print_depth(queue.estimate(),depth)
    if queue.left:
        print_tree(queue.left,depth+1)
    if queue.right:
        print_tree(queue.right,depth+1)

##maze tracks type,visited
def generate_maze(width,height,freq):
    maze = []
    for row in range(0,height):
        row = [(0,False)] * width
        for col in range(0,width):
            if random.random() < freq:
                row[col] = (1,True)
        maze.append(row)
    start = (random.randint(0,height-1),random.randint(0,width-1))
    maze[start[0]][start[1]] = (2,True)
    end = (random.randint(0,height-1),random.randint(0,width-1))
    maze[end[0]][end[1]] = (3,False)
    return (maze,start,end)

def square(n):
    return n*n

def pythag_distance(pos1,pos2):
    return square(pos2[0]-pos1[0]) + square(pos2[1]-pos1[1])

def tile_good(maze,pos):
    return (0 <= pos[1] < len(maze[0]) and 0 <= pos[0] < len(maze)) and not maze[pos[0]][pos[1]][1]

def get_coords_for_pair(pos,pair):
    return (pos[0]+pair[0],pos[1]+pair[1])

def get_adjacent_valid_tiles(maze,pos):
    adjacent_tiles = []
    for pair in terms:
        new_coord = get_coords_for_pair(pos,pair)
        if tile_good(maze,new_coord):
            adjacent_tiles.append(new_coord)
    return adjacent_tiles

def unwrap_path(end):
    path = [0] * (end.arrival + 1)
    while end:
        path[end.arrival] = (end.row,end.col)
        end = end.path_parent
    return path

def astar(maze,start,end):
    queue = PriorityQueue()
    s = Node(None,0,pythag_distance(start,end),start[0],start[1])
    queue.head = s
    while queue.head:
        position = pop(queue)
        coords = (position.row,position.col)
        if coords == end:
            return unwrap_path(position)
        maze_data = maze[position.row][position.col]
        maze[position.row][position.col] = (maze_data[0],True)
        adjacent = get_adjacent_valid_tiles(maze,coords)
        for tile in adjacent:
            node = Node(position,position.arrival+1,pythag_distance(tile,end),tile[0],tile[1])
            insert(queue,node)
    return None

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

def display(maze,path):
    for i,row in enumerate(maze):
        for b,col in enumerate(maze):
            item = maze[i][b]
            if item[0] == 2:
                print_green(' ')
            elif item[0] == 3:
                print_blue(' ')
            elif (i,b) in path:
                print_red(' ')
            elif item[0] == 0:
                print_normal(' ')
            elif item[0] == 1:
                print_black(' ')
        print('\n')



maze,start,end = generate_maze(10,10,0.2)
path = astar(maze,start,end)
display(maze,path)
    
    
