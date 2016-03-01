import numpy as np
import matplotlib.pyplot as plt

#three coins problem
def gen_coin_data(theta, num_samples):
 data = np.empty(num_samples,dtype = int)
 for i in xrange(num_samples):
  if np.random.rand() < theta[0]:
   data[i] = np.random.binomial(3,theta[1])
  else:
   data[i] = np.random.binomial(3,theta[2])
 return data

secret_theta = [.6, .1, .7]
data = gen_coin_data(secret_theta,20000)

#do EM
def solve_tri_coin(theta, data, iterations = 500):
 n = data.size
 for i in xrange(iterations):
  l, p1, p2 = theta
  temp1 = l * p1**data * (1-p1) ** (3-data)
  temp2 = (1-l)* p2 ** data * (1-p2) ** (3-data)
  mu = temp1/(temp1 + temp2)
  musum = np.sum(mu)
  l = musum / n
  p1 = 1/musum * 1./3 * np.dot(data, mu)
  p2 = 1/(n-musum) * 1./3 * np.dot(data, 1-mu)
  theta_new = [l, p1, p2]
  if sum([abs(theta[j]-theta_new[j]) for j in xrange(len(theta))]) < 1e-10:
    return theta_new
  theta = theta_new
 return theta

#Probability density function for bernoulli distribution with 3 trials
P = lambda p, heads: (p)**heads*(1-p)**(3-heads) 

def tri_coin_likelihood(theta, data):
  l, p, q = theta[0], theta[1], theta[2]
  likelihood = 0
  for heads in xrange(len(data)):
   likelihood += data[heads] * np.log(l * P(p,heads) + (1-l) * P(q,heads))
  return likelihood
  
def faster_tri_coin(theta, data, max_iters = 500):
  heads = np.arange(4)
  n = np.sum(data)
  for _ in xrange(max_iters):
   l, p, q = theta[0], theta[1], theta[2]
   t1, t2 = l*P(p, heads), (1-l)*P(q, heads)
   mu = data * t1/(t1 + t2)
   musum = np.sum(mu)
   l = musum / n
   p = np.dot(heads, mu)/ (3*musum)
   q = np.dot(heads, data-mu) / (3 *(n-musum))
   theta = np.array([l, p, q])
  return theta
def smarter_tri_coin(data, nguesses = 50, max_iters = 100):
  #We count the number of occurences of each number of heads
  d = np.bincount(data)
  maxl = -np.inf
  best_theta = None
  for _ in xrange(nguesses):
    theta = np.random.random(3)
    theta = faster_tri_coin(theta, d, max_iters)
    likelihood = tri_coin_likelihood(theta, d)
    if likelihood > maxl:
     maxl = likelihood
     best_theta = theta
  return best_theta
 

print secret_theta
print smarter_tri_coin(data,nguesses=100, max_iters = 100)
print solve_tri_coin(np.random.random(3), data)

def plot_gaussian_mixture(l, m ,s):
 n = len(l)
 max_sigma = max(s)
 x = np.linspace(max(m)+3*max_sigma,min(m) - 3*max_sigma,300)
 y = np.zeros(x.size)
 for i in xrange(n):
  y += l[i] * np.exp(-((x-m[i])/(np.sqrt(2)*s[i]))**2 ) / (s[i] * (2*np.pi)**.5)
 plt.plot(x,y)
 

#guess = [.1,.8,.6]
#print solve_tri_coin(guess, data)
def gaussian_data(lambdas, mus, sigmas, npoints):
 data = np.zeros(npoints)
 if abs(sum(lambdas)-1.) > 1e-14:
  raise ValueError("Lambdas must sum to 1.")
 draws = np.random.multinomial(npoints, lambdas)
 curr_ind = 0
 for i in xrange(len(lambdas)):
  data[curr_ind:curr_ind+draws[i]] = np.random.normal(mus[i],sigmas[i], draws[i])
  curr_ind += draws[i]
  
 return data

#secret_lambda = [.3,.3,.4]
#secret_mu = [0.,1.,2.]
#secret_sigma = [1.,.5,.4]
#data = gaussian_data(secret_lambda, secret_mu, secret_sigma, 10000)

def solve_gaussian_mixture(lambdas, mus, sigmas, data, iterations = 300):
 n = len(lambdas)
 m = data.size
 w_arr = np.empty((n,m))
 for _ in xrange(iterations):
  #calculate w matrix 
  for j in xrange (n):
   w_arr[j,:] =  lambdas[j]*np.exp(-((mus[j]-data)/(np.sqrt(2)*sigmas[j]))**2) / (sigmas[j]*(2*np.pi)**.5)
  
  w_arr = w_arr / np.sum(w_arr, axis = 0)
  #print w_arr
  w_sums = np.sum(w_arr, axis=1)

  #perform update
  lambdas = 1./m * w_sums
  mus = w_arr.dot(data) / w_sums
  for j in xrange(n):
   sigmas[j] = np.sqrt(np.dot(w_arr[j,:], (data-mus[j])**2)/w_sums[j])  
  
 return lambdas, mus, sigmas

#lambda_init = [.2,.4,.4]
#mus = [.1,.3,.4]
#sigmas = [.9,.7,.8]

#l, m, s = solve_gaussian_mixture(lambda_init, mus, sigmas, data)

#plot_gaussian_mixture(secret_lambda, secret_mu, secret_sigma)
#plot_gaussian_mixture(l, m, s)
#plt.show()
 


