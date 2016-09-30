# kdtrees.py
"""Volume 2A: Data Structures 3 (K-d Trees).
<Name>
<Class>
<Date>
"""

import numpy as np
import numpy.linalg as la

# Problem 1
def metric(x, y):
    """Return the euclidean distance between the 1-D arrays 'x' and 'y'.

    Raises:
        ValueError: if 'x' and 'y' have different lengths.

    Example:
        >>> metric([1,2],[2,2])
        1.0
        >>> metric([1,2,1],[2,2])
        ValueError: Incompatible dimensions.
    """
    return la.norm(x-y)


# Problem 2
def exhaustive_search(data_set, target):
    """Solve the nearest neighbor search problem exhaustively.
    Check the distances between 'target' and each point in 'data_set'.
    Use the Euclidean metric to calculate distances.

    Inputs:
        data_set ((m,k) ndarray): An array of m k-dimensional points.
        target ((k,) ndarray): A k-dimensional point to compare to 'dataset'.

    Returns:
        ((k,) ndarray) the member of 'data_set' that is nearest to 'target'.
        (float) The distance from the nearest neighbor to 'target'.
    """
    dists = la.norm(data_set-target, axis=1)
    k = np.argmin(dists)
    return data_set[k], dists[k]

points = np.arange(10).reshape((5,2))
print exhaustive_search(points, np.array([0,1]))

# Problem 3: Write a KDTNode class.
class BSTNode(object):
    """A Node class for Binary Search Trees. Contains some data, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the data attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value
        
class KTDNode(BSTNode):
    def __init_(self, data, axis):
        BSTNode.__init__(self, data)
        self.axis = axis

# Problem 4: Finish implementing this class by overriding
#            the __init__(), insert(), and remove() methods.
class KDT():
    """A k-dimensional binary search tree object.
    Used to solve the nearest neighbor problem efficiently.

    Attributes:
        root (KDTNode): the root node of the tree. Like all other
            nodes in the tree, the root houses data as a NumPy array.
        k (int): the dimension of the tree (the 'k' of the k-d tree).
    """
    def __init__(self):
        self.root = None
        self.k = None

    def find(self, data):
        """Return the node containing 'data'. If there is no such node
        in the tree, or if the tree is empty, raise a ValueError.
        """

        # Define a recursive function to traverse the tree.
        def _step(current):
            """Recursively step through the tree until the node containing
            'data' is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree")
            elif np.allclose(data, current.value):
                return current                      # Base case 2: data found!
            elif data[current.axis] < current.value[current.axis]:
                return _step(current.left)          # Recursively search left.
            else:
                return _step(current.right)         # Recursively search right.

        # Start the recursion on the root of the tree.
        return _step(self.root)

    def insert(self, data):
        """Insert a new node containing 'data' at the appropriate location.
        Return the new node. This method should be similar to BST.insert().
        """
        if self.k is None: self.k = len(data)

        def _step(current, prev):
            if current is None:
                return prev
            elif data[current.axis] < current.value[current.axis]:
                return _step(current.left, current)
            else:
                return _step(current.right, current)
        
        parent = _step(self.root, None)
        new_axis = (parent.axis+1) % self.k
        new_node = KDTNode(data, new_axis)
        
        if data[parent.axis] < parent.value[parent.axis]:
            parent.left = new_node
        else:
            parent.right = new_node


# Problem 5
def nearest_neighbor(data_set, target):
    """Use your KDT class to solve the nearest neighbor problem.

    Inputs:
        data_set ((m,k) ndarray): An array of m k-dimensional points.
        target ((k,) ndarray): A k-dimensional point to compare to 'dataset'.

    Returns:
        The point in the tree that is nearest to 'target' ((k,) ndarray).
        The distance from the nearest neighbor to 'target' (float).
    """

    def KDTsearch(current, neighbor, distance):
        """The actual nearest neighbor search algorithm.

        Inputs:
            current (KDTNode): the node to examine.
            neighbor (KDTNode): the current nearest neighbor.
            distance (float): the current minimum distance.

        Returns:
            neighbor (KDTNode): The new nearest neighbor in the tree.
            distance (float): the new minimum distance.
        """
        if current is None:
            return neighbor, distance
        
        axis = current.axis
        if target[axis] < current.value[axis]:
            left_cur, left_dist = KDTsearch(current.left, neighbor, distance)

            #update current if we found something better            
            if left_dist < distance:
                current = left_cur
                distance = left_dist

            #Check to see if the hypersphere about cur of radius distance has any points in the right branch
            #This is equivalent to seeing if |target[axis]-current.value[axis]| > distance            
            if current.value[axis] - target[axis] >= distance:                
                #need to search the right branch of the tree as well 
                right_cur, right_dist = KDTSearch(current.right, neighbor, distance)
                if right_dist < distance:
                    distance  = right_dist
                    current = right_cur
        
        else:
            right_cur, right_dist = KDTSearch(current.right, neighbor, distance)
            
            if right_dist < distance:
                distance  = right_dist
                current = right_cur
            
            if target[axis] - current.value[axis] >= distance:
                #we also have to search the left branch
                left_cur, left_dist = KDTSearch(current.left, neighbor, distance)
                #update current if we found something better            
                if left_dist < distance:
                    current = left_cur
                    distance = left_dist
                
        return current, distance        
        

    dist = metric(self.root.value, target)
    


# Problem 6
def postal_problem():
    """Use the neighbors module in sklearn to classify the Postal data set
    provided in 'PostalData.npz'. Classify the testpoints with 'n_neighbors'
    as 1, 4, or 10, and with 'weights' as 'uniform' or 'distance'. For each
    trial print a report indicating how the classifier performs in terms of
    percentage of correct classifications. Which combination gives the most
    correct classifications?

    Your function should print a report similar to the following:
    n_neighbors = 1, weights = 'distance':  0.903
    n_neighbors = 1, weights =  'uniform':  0.903       (...and so on.)
    """
    raise NotImplementedError("Problem 6 Incomplete")
