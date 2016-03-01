import numpy as np
import gmmhmm as GH
import MFCC
from scipy.io.wavfile import read as wread
import glob
import pickle

def sample_gmmhmm(gmmhmm, n_sim):
 """
 Simulate sampling from a GMMHMM.
 [A, weights, means, covars, pi]
 Returns
 -------
 states : ndarray of shape (n_sim,)
 The sequence of states
 obs : ndarray of shape (n_sim, K)
 The generated observations (column vectors of length K)
 """

 state_dist = gmmhmm[-1]
 A = gmmhmm[0]
 weights = gmmhmm[1]
 means, covars = gmmhmm[2], gmmhmm[3]
 K = means[0,0].size
 
 states = np.zeros(n_sim, dtype = int)
 obs = np.zeros((n_sim, K))
 for i in xrange(n_sim):
  s = np.random.multinomial(1,state_dist)[0]
  states[i] = s
  component = np.random.multinomial(1, weights[s, :])[0]
  mu, sig = means[s, component,:], covars[s, component, :, :]
  obs[i,:] =  np.random.multivariate_normal(mu, sig)
#  print "state ", states[i], obs[i]
  state_dist = A.dot(state_dist)
 return states, obs


def test_sample():
 A = np.array([[.65, .35], [.15, .85]])
 pi = np.array([.8, .2])
 weights = np.array([[.7, .2, .1], [.1, .5, .4]])
 means1 = np.array([[0., 17., -4.], [5., -12., -8.], [-16., 22., 2.]])
 means2 = np.array([[-5., 3., 23.], [-12., -2., 14.], [15., -32., 0.]])
 means = np.array([means1, means2])
 covars1 = np.array([5*np.eye(3), 7*np.eye(3), np.eye(3)])
 covars2 = np.array([10*np.eye(3), 3*np.eye(3), 4*np.eye(3)])
 covars = np.array([covars1, covars2])
 gmmhmm = [A, weights, means, covars, pi]
 sample_gmmhmm(gmmhmm, 10)


def initialize(n):
 T = np.random.random((n,n))
 pi = np.random.random(n)
 pi /= np.sum(pi)
 T /= np.sum(T, axis = 1).reshape((n,1))
 return pi, T

def load():
 names = ["Mathematics", "Biology", "PoliticalScience", "Statistics", "Psychology"]
 sampledict = {}
 for name in names:
  sampledict[name] = []
  for fname in glob.glob("Samples/"+name+" *"):
   w = wread(fname)
   sampledict[name].append(MFCC.extract(w[1])[:30])
 return names, sampledict 

def load_and_train():
 names, sampledict = load()
 best_models = {}
 for name in names:
  bestprob = -np.inf
  bestmodel = None
  #Random Restarts
  for i in xrange(10):
   startprob, transmat = initialize(5)
   model = GH.GMMHMM(n_components=5, n_mix=3, transmat=transmat, startprob=startprob,  cvtype='diag')
   # these values for covars_prior and var should work well for this problem
   model.covars_prior = 0.01
   model.fit(sampledict[name][:20], init_params='mc', var=0.1)
   print "Trained Again on "+name+", new prob: ", model.logprob
   if model.logprob > bestprob:
     bestprob = model.logprob
     bestmodel = model
     print "New Best Prob for "+name+" "+str(bestprob)
  best_models[name] = bestmodel

 #save
 f = open("gmmmodels","wb")
 pickle.dump(best_models, f)
 f.close()
 return best_models, names, sampledict

def test():
 models, names, sampledict  = load_and_train()
 accuracies = {}
 for name in names:
   tot = len(sampledict[name]) - 20
   cor = 0.
   for sample in sampledict[name][20:]:
     mscore = -np.inf
     bname = None
     for cand_name in names:
      score =  models[cand_name].score(sample)
      if score > mscore:
       mscore = score
       bname = cand_name
     if bname == name:
      cor += 1.
   accuracies[name] = 100*cor/tot
 return accuracies
adict = test()
print "Accuracy Breakdown: ", adict
print "Overall Accuracy: ", sum([adict[name] for name in adict])/len(adict.keys())
