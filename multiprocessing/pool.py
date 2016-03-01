from multiprocessing import Pool

def fib(n):
 if n<2: return n
 return fib(n-1) + fib(n-2)

#allows to import without running code (DOH)
#necessary for multi-porcessing
if __name__ == '__main__':
 pool = Pool()
 x = [33]*20
 print x
 print pool.map(fib,x)
 
