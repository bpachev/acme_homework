import numpy as np
from math import log
from itertools import product
from numpy.random import normal,random
import numpy.linalg as la
import sklearn.utils.linear_assignment_ as las


def perturbed_uniform_init(shape, sum_axis=0, var = 3*1e-1):
 mat = np.ones(shape) + var * (random(shape) -.5)
 #force the matrix to be column or row stochastic depending on sum_axis
 # sum_axis = 0 corresponds to column stochastic matrices, 1 to row
 mat /= np.sum(mat, axis = sum_axis)
 return mat

class HMM():
 def __init__(self,hidden_alphabet, observed_alphabet, A=None,B=None, p=None):
  self.A = A
  self.B = B
  self.p = p
  self.hidden = hidden_alphabet
  self.observed = observed_alphabet
  self.nstates = len(hidden_alphabet)
  self.noutputs = len(observed_alphabet)
  self.state_list = [None] * self.nstates
  for state in self.hidden:
    self.state_list[self.hidden[state]] = state

 def is_not_init(self):
  return self.A is None or self.B is None or self.p is None

 def check_init(self):
  if self.is_not_init():
   raise ValueError("Model parameters have not been initialized.")

 def naive_prob(self,observed_sequence):
  self.check_init()
  prob = 0
  l = len(self.hidden)
  num_observations = len(observed_sequence)
  obs_inds = self.observation_inds(observed_sequence)
  for state_sequence in product(range(l), repeat = num_observations):
    increment = self.p[state_sequence[0]] * self.B[obs_inds[0], state_sequence[0]]
    for i in xrange(1,num_observations):
     last_state, curr_state = state_sequence[i-1], state_sequence[i]
     increment *= self.A[curr_state, last_state]
     increment *= self.B[obs_inds[i], curr_state]
    prob += increment
  return prob

 def observation_inds(self, observations):
  if type(observations[0]) == int or type(observations[0]) == np.int64:
   return observations
  return [self.observed[o] for o in observations]

 def smart_prob(self, observations):
   alpha = self.alpha_pass(observations)
   return np.sum(alpha[-1,:])


 def convert_to_states(self, state_inds):
   return [self.state_list[i] for i in state_inds]

 def viturbi_seq(self, observations):
   """
   Returns the best state sequence in the DP sense
   """
   num_observations = len(observations)
   obs_inds = self.observation_inds(observations)
   d = np.log(self.p * self.B[0,:])
   paths = np.zeros((num_observations, self.nstates), dtype=int)
   state_seq = np.array(num_observations)
   for t in xrange(1, num_observations):
     d_new = np.zeros(self.nstates)
     for i in xrange(self.nstates):
       temp = np.log(self.A[i,:])  +  d + log(self.B[obs_inds[t], i])
       best_previous_state = np.argmax(temp)
       d_new[i] = temp[best_previous_state]
       paths[t-1, i] = best_previous_state
     d = d_new

   best_final_state = np.argmax(d)
   res = np.zeros(num_observations, dtype=int)
   res[-1] = best_final_state
   last_best = best_final_state
   for i in xrange(num_observations - 2, -1, -1):
     last_best = paths[i, last_best]
     res[i] = last_best
   return self.convert_to_states(res)

 def alpha_pass(self, observations, normalize = False):
  obs_inds = self.observation_inds(observations)
  nobs = len(obs_inds)
  alpha = np.zeros((nobs, self.nstates))
  alpha[0,:] = self.B[obs_inds[0],:] * self.p
  if normalize:
    c_arr = np.zeros(nobs)
    c_arr[0] = np.sum(alpha[0,:])
    self.logprob = log(c_arr[0])
    alpha[0,:] /= c_arr[0]
  A,B = self.A, self.B
  for i in xrange(1, nobs):
    alpha[i,:] = B[obs_inds[i],:] * np.dot(A, alpha[i-1,:])
    if normalize:
      c_arr[i] = np.sum(alpha[i,:])
      self.logprob += log(c_arr[i])
      alpha[i,:] /= c_arr[i]
  if normalize:
    return alpha, c_arr
  else:
    return alpha

 def beta_pass(self, obs_inds, normalize = False, c_arr = None):
  nobs = len(obs_inds)
  beta = np.ones((nobs, self.nstates))
  if normalize:
    beta[-1,:] /= c_arr[-1]
#    c = np.sum(beta[-1,:])
 #   self.logprob += log(c)
  #  beta[-1,:] /= c

  for i in xrange(1, nobs):
    beta[nobs-i-1,:] = self.B[obs_inds[nobs-i],:] * np.dot(self.A.T, beta[nobs-i,:])
    if normalize:
      beta[nobs-i-1,:] /= c_arr[nobs-i-1]
#       c = np.sum(beta[nobs-i-1,:])
 #      self.logprob += log(c)
  #     beta[nobs-i-1,:] /= c

  return beta

 def best_seq(self, observations, normalize = False):
   """
   Return the state sequence that maximizes the number of correct states.
   """
   #make sure is numeric
   obs = self.observation_inds(observations)
   if normalize:
     alpha, c_arr = self.alpha_pass(obs, normalize=True)
     beta = self.beta_pass(obs, c_arr=c_arr, normalize=True)
   else:
     alpha, beta = self.alpha_pass(obs), self.beta_pass(obs)
   return self.convert_to_states(np.argmax(alpha*beta, axis = 1))

 def init_random(self):
   if self.A is None:
     self.A = perturbed_uniform_init((self.nstates, self.nstates))
   if self.B is None:
     self.B = perturbed_uniform_init((self.noutputs, self.nstates))
   if self.p is None:
     self.p = perturbed_uniform_init(self.nstates, sum_axis = 0)


 def train(self, observations, iters = 50, update_A = True, update_B = True, update_p = True):
   O = self.observation_inds(observations)
   T = len(O)
   oldprob = -np.inf
   if self.is_not_init():
    self.init_random()
 #  print self.A
   for it in xrange(iters):
     alpha, c_arr = self.alpha_pass(O,normalize=True)
     beta = self.beta_pass(O, normalize = True, c_arr=c_arr)
     digamma = np.zeros((self.nstates, self.nstates, T-1))
     gamma = np.zeros((T, self.nstates))
     BB = np.zeros((T-1, self.nstates))
     for i in xrange(0,T-1):
       BB[i,:] = self.B[O[i+1], :] * beta[i+1, :]
       digamma[:,:,i] = self.A.T * np.outer(alpha[i,:], BB[i,:])
       digamma[:,:,i] /= np.sum(digamma[:,:,i])
       gamma[i,:] = np.sum(digamma[:,:,i], axis = 1)

     gamma[-1, :] = alpha[-1, :]
     if update_p:  self.p = gamma[0,:]
     if update_A:
       for i in xrange(self.nstates):
         for j in xrange(self.nstates):
           numer = np.sum(digamma[j,i,:T-1])
           denom = np.sum(gamma[:T-1,j])
           self.A[i,j] = numer / denom

     if update_B:
       self.B = np.zeros(self.B.shape)
       for i in xrange(T):
         self.B[O[i], :] += gamma[i,:]

       for j in xrange(self.nstates):
         self.B[:,j] = self.B[:,j] / np.sum(gamma[:,j])
     print "Log Probability: ",self.logprob
     if self.logprob < oldprob:
       break
     else:
       oldprob = self.logprob

   print "Final Probability: ", self.logprob

def small_probs():
 model = HMM({"H":0, "C":1}, {"S":0, "M":1, "L": 2})
 model.A = np.array([[.7,.4],[.3,.6]])
 model.B = np.array([[.1,.7],[.4,.2],[.5, .1]])
 model.p = np.array([0., 1.])
 oseq = ["M", "S", "L"]
 print model.naive_prob(oseq) #1(a)
 print model.smart_prob(oseq) #1(b)
 print model.viturbi_seq(oseq) #2(a)
 print model.best_seq(oseq) #2(b)

 model.p = np.array([.6,.4])
 #Problem 3
 naive_sum = 0
 smart_sum = 0
 for o in product(range(3), repeat=4):
   naive_sum += model.naive_prob(o)
   smart_sum += model.smart_prob(o)
 print naive_sum, smart_sum

def make_list(alphabet):
 nsymbols = len(alphabet)
 alist = [None] * nsymbols
 for k in alphabet:
   alist[alphabet[k]] = k
 return alist

def print_model_states(model, observation_alphabet):
 states = [[] for i in xrange(model.nstates)]
 olist = make_list(observation_alphabet)
 for i in xrange(len(observation_alphabet)):
   states[np.argmax(model.B[i,:])].append(olist[i])
 for state in states:
  print state

def alphabet_helper(observations, observation_alphabet, nstates = 2, nobs = 50000, iters = 100, A=None, p =None):
 hidden_alphabet = {i:i for i in xrange(nstates)}
 model = HMM(hidden_alphabet, observation_alphabet)
 model.A = A
 model.p = p
 model.train(observations[:nobs], iters = iters)
 print model.p
 print model.A
 print model.B
 print_model_states(model, observation_alphabet)

def parse_char_file(filename):
 f = open(filename, "r")
 l = f.readline().strip()
 nobs = len(l)
 observations = np.zeros(nobs, dtype = int)
 observation_alphabet = {' ' : 26}
 for off in xrange(26):
   observation_alphabet[chr(ord('a')+off)] = off
 for i in xrange(nobs):
   observations[i] = observation_alphabet[l[i]]
 return observations, observation_alphabet

def alphabet_prob(filename = "brown.txt"):
 observations, observation_alphabet = parse_char_file(filename)
 alphabet_helper(observations, observation_alphabet, 2,50000, iters=100,A = np.array([[.47468,.51656], [.52532,.48344]]), p = np.array([.51316,.48684]))
# alphabet_helper(observations, observation_alphabet, 3,50000, iters=200)
 #alphabet_helper(observations, observation_alphabet, 4,50000, iters=200)

def decrypt(ciphertext, sub_dict):
 res = ""
 for c in ciphertext:
  res += sub_dict[c]
 print res

def crypto_prob(cipher_file = "ciphertext.txt", digraph_file = "full_digraph.npy"):
  observations, observation_alphabet = parse_char_file(cipher_file)
  osq = observations[:100]
  hidden_alphabet = {i:i for i in xrange(2)}
  #model = HMM(hidden_alphabet, observation_alphabet)
  #model.train(observations[:100])
  #print_model_states(model, observation_alphabet)
  A = np.load(digraph_file)
  nsymbs = len(observation_alphabet)
  hidden_alphabet = {i:i for i in xrange(nsymbs)}
  model = HMM(observation_alphabet, hidden_alphabet)
  model.A = A
  model.train(observations, update_A = False, iters=100)
  probs = np.real(la.eig(A)[1][:,0])
  probs /= np.sum(probs)
#  t = las.linear_assignment(-np.log(model.B*probs+1e-10))
  tb = np.argmax(model.B, axis = 1)
  tb = np.argsort(np.bincount(observations))
#  print probs
  #tp = np.argsort(probs)
  #observations,o = parse_char_file("brown.txt")
 # tp = np.argsort(np.bincount(observations))
  tp = np.array([26, 4, 19, 0, 14, 8, 13, 18, 17, 7, 11, 3, 2, 20, 12, 5, 6, 15, 22, 24, 1, 21, 10, 9, 23, 25, 16])
  tp = tp[::-1]
#  print tp, np.argsort(probs)
#  print model.B
  olist = make_list(observation_alphabet)
  substitution_dict = {i: olist[tb[i]] for i in xrange(nsymbs)}
  substitution_dict = {tb[i]: olist[tp[i]] for i in xrange(nsymbs)}
  print substitution_dict
  print "".join([olist[o] for o in osq])
  print decrypt(osq, substitution_dict)

alphabet_prob("ciphertext.txt")
#crypto_prob(cipher_file = "ciphertext.txt")

def create_digraph(filename, outfile = "full_digraph.npy"):
 observations, observation_alphabet = parse_char_file(filename)
 nsymbs = len(observation_alphabet)
 A = np.zeros((nsymbs,nsymbs))
 i = 0
 nobs = len(observations)
 while i < nobs-1:
  A[observations[i+1], observations[i]] += 1
  i += 1
 A /= np.sum(A, axis = 0)
 np.save(outfile, A)
#create_digraph("brown.txt")
