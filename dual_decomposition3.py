# ! /usr/bin/python

'''
Dual decomposition for a tagger combined with an FST to avoid a
given sequence.
Created on Oct 15, 2013

@author: swabha
'''

from collections import defaultdict
import utils, cky, viterbi

'''
Executes the dual decomposition algorithm
Note here that the nonterminals are more in number than the tags
'''
def run(sentence, tagset, hmm_prob):
    max_iterations = 200
    step_size = 15

    n = len(sentence)

    u = defaultdict() # dual decomposition parameter
    for i in xrange(0, n):
        u[i] = defaultdict()
        for t in tagset:
            u[i][t] = 0
    
    k = 0 # number of iterations
    while k < max_iterations:

       tags1 = viterbi.run(sentence, tagset, hmm_prob, u)
       if k == 0:
          best_tags = tags1
       tags2 = fst_viterbi.run(tagset, best_tags, u)
       
       if k == 0:
           print "initial tags:"
           print tags1, ":tagger1"
           print tags2, ":tagger2"
              
       if agree(tags1, tags2): 
           return k, tags1, tags2  # converges in the kth iteration
       y = compute_indicators(tags1, tagset)
       z = compute_indicators(tags2, tagset)
       update(y, z, u, step_size)

       k += 1
    return -1, tags1, tags2 # does not converge

def compute_indicators(tags, labelset):
    y = defaultdict()
    for i in xrange(0, len(tags)):
        z = defaultdict()
        for t in labelset:
            if tags[i] == t:
                z[t] = 1
            else:
                z[t] = 0
        y[i+1] = z
    return y

'''
Dual decomposition update
'''
def update(indi1, indi2, u, step_size):
    for i in xrange(1, len(indi1)+1):
        for t, val in u[i].iterkeys():
            u[i][t] -= (indi1[i][t] - indi2[i][t])*step_size

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
