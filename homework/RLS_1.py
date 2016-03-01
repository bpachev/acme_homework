import numpy as np
import numpy.linalg as la

def RLS(A, R, B):
 """
 Inputs:
 A -- a list of p x n matrices
 R -- a list of p x p matrices representing the covariance of the error terms
 B -- a list of length p vectors
 
 The lengths of A, R and B must be the same, or an error will result
 
 Returns:
 x -- the best linear unbiased estimator the system defined by B_k = A_k x, 1 <= 
 with noise term epsilon_k of covariance R_k 
 This is a weighted least squares problem with weight W = diag( R_1^-1 ... R_k^-1 )
 """
 
 N = len(A)
 if not N == len(R) or not N == len(B):
  raise ValueError("The lengths of A, R, and B must be the same.")
 
 R_inv = la.inv(R[0])
 G = A[0].T.dot(R_inv).dot(A[0])
 K = la.inv(G)
 x = WLS(A[0], R_inv, B[0])
# print K, G.dot(K), K.dot(G), G,np.dot(K,G)
# print x 
 for i in xrange(1, N):
  K = K - K.dot( A[i].T.dot( la.inv(R[i] + A[0].dot(K).dot(A[0].T)).dot( A[i].dot(K) )))
  x = x - K.dot( np.dot( A[i].T.dot(la.inv(R[i])), A[i].dot(x) - B[i]) )
 # print x 
 return x

def WLS(A,W,b):
 """
 Weighted least squares.
 """
 temp = A.T.dot(W)
 return la.solve(temp.dot(A),temp.dot(b))

# do some tests

p = 3
n = 2
N = 5
A_l = [np.random.random((p,n)) for i in xrange(N)]
R_l = [np.eye(p) for i in xrange(N)] #ensure invertibility
B_l = [np.random.random(p) for i in xrange(N)]



print RLS(A_l, R_l, B_l)
print WLS(np.vstack(A_l), np.eye(p*N), np.hstack(B_l))


