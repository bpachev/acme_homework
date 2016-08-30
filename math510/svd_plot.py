import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def plot_arrow(vec):
    plt.arrow(0,0,vec[0], vec[1])

def ellipse_by_axes(center, x,y):
    width, height = la.norm(x), la.norm(y)
    theta = np.arctan2(x[1], x[0])
    theta *= 180/np.pi
    return Ellipse(center, 2*width, 2*height, angle = theta, fill=False)

def plot_uv(A):
    """Plot the right singular vectors, and the stretched left singular vectors."""
    assert (A.shape == (2,2)), "Matrix must be 2x2"
    u, s, v = la.svd(A)
    u1, u2 = A.dot(v[0]), A.dot(v[1])
    
    #the rows of v should be the right singular vectors
    fig, ax = plt.subplots()
    plot_arrow(v[0])
    plot_arrow(v[1])
    ax.add_artist(plt.Circle((0,0), 1, fill=False))
    ax.set_ylim([-1.3,1.3])
    ax.set_xlim([-1.3,1.3])
    ax.set_aspect('equal')
    ax.grid(True, which="both")
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.show()
    
    #now plot the ellipse
    print v
    fig, ax = plt.subplots()
    plot_arrow(u1)
    plot_arrow(u2)
    ax.add_artist(ellipse_by_axes((0,0), u1, u2))
    ax.set_ylim([-4,4])
    ax.set_xlim([-4,4])
    ax.set_aspect('equal')
    ax.grid(True, which="both")
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.show()
    
 #   fig, ax = plt.subplots()

A = np.array([[1,2],[0,2]])    
plot_uv(A)
