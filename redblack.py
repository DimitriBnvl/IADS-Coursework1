
# File:     redblack.py
# Author:   John Longley
# Date:     October 2026

# Template file for Inf2-IADS (2026-27) Coursework 1, Part B:
# Implementation of dictionaries by red-black trees, space-saving version.

# Provided code:

from enum import Enum

# Colour and direction tags

Colour = Enum('Colour', ['Red','Black'])
Red, Black = Colour.Red, Colour.Black

def colourStr(c):
    return 'R' if c==Red else 'B'

Dir = Enum('Dir', ['Left','Right'])
Left, Right = Dir.Left, Dir.Right

def opposite(d):
    if d==Left: return Right
    else: return Left

def branchLabel(d):
    if d==Left: return 'l'
    else: return 'r'


class Node():
    """Class for nodes with keys, values, colours and links to children"""
    
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None
        
    def getChild(self,branch):
        if branch==Left:
            return self.left
        else:
            return self.right

    def setChild(self,branch,y):
        if branch==Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) +':'+ str(self.value) +':'+ colourStr(self.colour)

# Use None for all trivial leaf nodes, which are black

def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour


class RedBlackTree():

    def __init__ (self):
        self.root = None
        self.stack = []


# TODO: Task 1.

    def lookup_(self, x, key):
        """Search for key by comparing key values"""
        if x is None:      return None
        elif key == x.key: return x.value
        elif key < x.key:  return self.lookup_(x.getChild(Left), key)
        else:              return self.lookup_(x.getChild(Right), key)

    def lookup(self,key):
        """Search for key in whole tree, returning associated value or None"""
        return self.lookup_(self.root, key)


# TODO: Task 2.

    def plainInsert_(self, x, key, value):
        """Insert new key-value pair in tree at position given by ordering,"""
        self.stack.append(x)
        if key == x.key:
            x.value = value
            return
        direction = Left if key < x.key else Right
        self.stack.append(direction)
        child = x.getChild(direction)
        if child is None:
            new_node = Node(key,value)
            x.setChild(direction, new_node)
            self.stack.append(new_node)
        else:
            self.plainInsert_(child, key, value)


    def plainInsert(self,key,value):
        """Insert new key-value pair in tree at position given by ordering,
        New node should be red. No RB-tree fixup performed."""
        self.stack = []
        if self.root is None:
            self.root = Node(key,value)
            self.stack.append(self.root)
        else:
            self.plainInsert_(self.root, key, value)




# TODO: Task 3.

    def tryRedUncle(self):
        """Apply red uncle rule if possible at tree position given by current
        stack state. Return whether the rule was applicable."""
        if len(self.stack) < 5: return False

        current, parent  = self.stack[-1], self.stack[-3]
        grand            = self.stack[-5]
        uncle = grand.getChild(opposite(self.stack[-4]))

        if not all(colourOf(n) == Red for n in (current, parent, uncle)):
            return False

        parent.colour = Black
        uncle.colour  = Black
        grand.colour  = Red
        [self.stack.pop() for _ in range(4)]
        return True
        
    def repeatRedUncle(self):
        """Apply red uncle rule as often as possible starting from current
        tree position"""
        while self.tryRedUncle():
            pass


# Provided code to support Task 4:

    def toNextBlackLevel(self,node):
        """Inspect subtree down to the next level of blacks
        and return list of components (subtrees or nodes) in L-to-R order.
        In cases of interest there will be 7 components A,a,B,b,C,c,D)."""
        if colourOf(node.left)==Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right)==Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf

    def balancedTree(self,comps):
        """Build a new (balanced) subtree from a list of 7 components."""
        [A,a,B,b,C,c,D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b


# TODO: Task 4.

    def endgame(self):
        """Apply final RB-tree fixup after repeatRedUncle is applied."""
        current = self.stack[-1]
        if len(self.stack) == 1:
            current.colour = Black
            return

        parent = self.stack[-3]
        if current.colour is not Red or parent.colour is not Red:
            return
        if len(self.stack) == 3:
            parent.colour = Black
            return

        grand  = self.stack[-5]
        elems  = self.toNextBlackLevel(grand)
        newTop = self.balancedTree(elems)
        if len(self.stack) == 5:
            self.root = newTop
        else:
            greatGrand    = self.stack[-7]
            dirGreatGrand = self.stack[-6]
            greatGrand.setChild(dirGreatGrand, newTop)


    def insert(self,key,value):
        """Insert new key-value pair in tree and perform RB-tree fixup."""
        self.plainInsert(key,value)
        self.repeatRedUncle()
        self.endgame()

# Provided code:
    
    def __str__(self,x):
        """Convert tree contents to a readable string"""
        if x==None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        """Display stack contents in readable form"""
        return [x.__str__() if isinstance(x,Node) else branchLabel(x)
                for x in self.stack]

    # All keys by left-to-right traversal
    
    def keysLtoR_(self,x):
        if x==None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)

# End of class RedBlackTree


# Creating a tree by hand:

sampleTree = RedBlackTree()
sampleTree.root = Node(2,'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1,'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4,'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3,'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6,'six')
sampleTree.root.right.right.colour = Black


# For fun: sorting algorithm using trees
# Will remove duplicates (not good)

def treeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x,None)
    return T.keysLtoR()

# End of file
