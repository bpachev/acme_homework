import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def plot_arrow(vec):
    plt.arrow(0,0,vec[0], vec[1], head_width=.5, head_length=.3)

def ellipse_by_axes(center, x,y):
    width, height = la.norm(x), la.norm(y)
    theta = np.arctan2(x[1], x[0])
    theta *= 180/np.pi
    return Ellipse(center, 2*width, 2*height, angle = theta, fill=False)

def plot_singular_vectors(A):
    """Plot the right singular vectors, and the stretched left singular vectors."""
    assert (A.shape == (2,2)), "Matrix must be 2x2"
    u, s, v = la.svd(A)
    u1, u2 = A.dot(v[0]), A.dot(v[1])
    
    #the rows of v should be the right singular vectors
    ax1 = plt.subplot(121)
    plot_arrow(v[0])
    plot_arrow(v[1])
    ax1.add_artist(plt.Circle((0,0), 1, fill=False))
    ax1.set_ylim([-1.3,1.3])
    ax1.set_xlim([-1.3,1.3])
    ax1.set_aspect('equal')
    ax1.grid(True, which="both")
    ax1.axhline(y=0, color='k')
    ax1.axvline(x=0, color='k')
    plt.title("Unit circle.")
    
    #now plot the ellipse
    ax2 = plt.subplot(122)
    plot_arrow(u1)
    plot_arrow(u2)
    ax2.add_artist(ellipse_by_axes((0,0), u1, u2))
    ax2.set_ylim([-4,4])
    ax2.set_xlim([-4,4])
    ax2.set_aspect('equal')
    ax2.grid(True, which="both")
    ax2.axhline(y=0, color='k')
    ax2.axvline(x=0, color='k')
    plt.title("Image of unit circle under A.")
    plt.suptitle(r'A = '+str(A))
    plt.show()

if __name__ == "__main__":
    #The matrix from (3.7)
    A = np.array([[1,2],[0,2]])
    #The 2x2 matrices from 4.3
    other_mats = [np.array([[3,0],[0,-2]]), np.array([[2, 0], [0,3]]), np.array([[1,1], [0,0]]), np.array([[1,1],[1,1]])]
    plot_singular_vectors(A)
    for m in other_mats:
        plot_singular_vectors(m)

  

