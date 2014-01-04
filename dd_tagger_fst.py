# ! /usr/bin/python

'''
Dual decomposition for a tagger combined with an FST to avoid a
given sequence.
Created on Oct 15, 2013

@author: swabha
'''

from collections import defaultdict
import utils, cky, viterbi, fst_search, math


def init_dd_param(u, n, tagset):
    for i in xrange(0, n):
        u[i] = defaultdict()
        for t in tagset:
            u[i][t] = 0
    
'''
Executes the dual decomposition algorithm
'''
def run(sentence, tagset, hmm_prob):
    max_iterations = 1000
    #step_size = 100

    n = len(sentence)

    u = defaultdict() # dual decomposition parameter
    init_dd_param(u, n, tagset)
 
    k = 1 # number of iterations
    while k <= max_iterations:
       step_size = 5.4 / math.sqrt(k)
       print "\niteration:", k
       print "-------------------------------"
       #print "step size = ", "{0:.2f}".format(step_size)
       tags1 = viterbi.run(sentence, tagset, hmm_prob, u)
       #print "vit output:", ' '.join(tags1)
       if k == 1:
          best_tags = tags1
       tags2 = fst_search.run(tagset, best_tags, u)
       
       if agree(tags1, tags2): 
           return best_tags, k, tags1, tags2  # converges in the kth iteration
       y = compute_indicators(tags1, tagset)
       z = compute_indicators(tags2, tagset)
       update(y, z, u, step_size)

       k += 1
    return best_tags, -1, tags1, tags2 # does not converge

# can be made faster, use dictionary shallow copying
def compute_indicators(tags, labelset):
    ind = defaultdict()
    for i in xrange(0, len(tags)):
        z = defaultdict()
        for t in labelset:
            if tags[i] == t:
                z[t] = 1
            else:
                z[t] = 0
        ind[i] = z
    return ind

'''
Dual decomposition update
'''
def update(indi1, indi2, u, step_size):
    for i in xrange(0, len(indi1)):
        for t in u[i].iterkeys():
            u[i][t] -= -(indi2[i][t] - indi1[i][t])*step_size
'''
Check if two tag sequences agree
'''
def agree(tags1, tags2):
    for i in xrange(0, len(tags1)):
        if tags1[i] != tags2[i]:
            return False
        else:
            continue
    return True 

if __name__ == "__main__":
    labelset = ["a", "b", "c"]
    tags = ["a", "a", "c"]
    tags2 = ["c", "c", "c"]
    ind = compute_indicators(tags, labelset)
    ind2 = compute_indicators(tags2, labelset)
    u = defaultdict()
    init_dd_param(u, 3, labelset)
    for i in xrange(0, len(tags)):
        for t in labelset:
            print ind[i][t],
        print
    print 
    for i in xrange(0, len(tags)):
        for t in labelset:
            print ind2[i][t],
        print
    print 
    update(ind, ind2, u, 10)
