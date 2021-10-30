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


def insert_node_helper(parent,node):
    if parent.matches(node):
        if node.estimate < parent.estimate():
            parent.path_parent = node.path_parent
            parent.arrival = node.arrival
    if node.estimate() >= parent.estimate():
        if not parent.right:
            node.graph_parent = parent
            parent.right = node
            return
        insert_node(parent.right,node)
    else:
        if not parent.left:
            node.graph_parent = parent
            parent.left = node
            return
        insert_node(parent.left,node)

def insert(queue,node):
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

p = PriorityQueue()

n = Node(None,0,10,4,4)

c = Node(n,1,9,5,5)

b = Node(n,1,6,3,3)

p.head = n

insert(p,c)
insert(p,b)
print_tree(p.head,0)
print(pop(p))
print_tree(p.head,0)
