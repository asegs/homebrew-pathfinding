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
            parent.right = node
            return
        insert_node(parent.right,node)
    elif node.estimate() < parent.estimate:
        if not parent.left:
            parent.left = node
            return
        insert_node(parent.left,node)

def insert(queue,node):
    insert_node_helper(queue.head,node)


p = PriorityQueue()

n = Node(None,0,10,4,4)

c = Node(n,1,9,5,5)

p.head = n

insert(p,c)

print(p.head.right)
