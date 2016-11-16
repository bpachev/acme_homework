import numpy as np
import matplotlib.pyplot as plt

def dwt(arr,ndetails):
    """
    Arr must have length equal to a power of two for the code to work.
    """
    details = []
    A = np.copy(arr)
    sq2 = np.sqrt(2)
    for i in xrange(ndetails):
        #This ought to be equivalent to the low-pass filter plus downsampling
        details.append(A[0::2] * 1./sq2 - A[1::2] * 1./sq2)
        A = A[0::2] * 1./sq2 + A[1::2] * 1./sq2
    return [A] + details[::-1]

def iwt(coeffs):
    ndetails = len(coeffs) - 1
    A = coeffs[0]
    res = np.copy(A)
    sq2 = np.sqrt(2)
    for D in coeffs[1:]:
        new = np.zeros(2*len(res))
        new[0::2] = res * (1./sq2) + D*(1./sq2)
        new[1::2] = res*(1./sq2) - D*(1./sq2)
        res = new
    return res

if __name__ == "__main__":
    n = 2**10
    domain = np.linspace(0,4*np.pi, n)
    noise = np.random.random(n)*.1
    nsin = np.sin(domain) + noise
    details = 4
    coeffs = dwt(nsin, 4)
    print np.allclose(iwt(coeffs), nsin)
    plt.subplot(details+2, 1, 1)
    plt.plot(coeffs[0])
    plt.title("A")
    for detail in xrange(1, details+1):
        plt.subplot(details+2,1,detail+1)
        plt.plot(coeffs[detail])
        plt.title("D{}".format(detail))

    plt.subplot(details+2, 1, details+2)
    plt.plot(nsin)
    plt.title("X")
    plt.show()
    
    
