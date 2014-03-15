# /usr/bin/python

from __future__ import division
import sys, math
import fst_search, viterbi

def init_dd_param(dd_u, n, tagset):
    for i in range(n):
        dd_u[i] = {}#defaultdict()
        for t in tagset:
            dd_u[i][t] = 0

# can be made faster, use dictionary shallow copying
def compute_indicators(seq, tagset):
    ind = {}
    for i in range(len(seq)):
        z = {}
        for t in tagset:
            if seq[i] == t:
                z[t] = 1
            else:
                z[t] = 0
        ind[i] = z
    return ind

'''
Executes the dual decomposition algorithm to get the k-best
list of sequences
'''
def run(sentence, tagset, hmm, k_best_list):
    max_iter = len(k_best_list)*200
    
    n = len(sentence)
    k = len(k_best_list)

    u = {} # dual decomposition parameter
    init_dd_param(u, n, tagset) 

    iteration = 1
    while iteration <= max_iter:
        #print iteration
        step_size = 1.0 / math.sqrt(iteration)
        #print "step size", step_size 
        
        seq1, score1, score2 = viterbi.run(sentence, tagset, hmm, u)
        y = compute_indicators(seq1, tagset)
        #print 0, ' '.join(seq1)

        seq2, fst_score = fst_search.run(k_best_list, u, tagset)
        z = compute_indicators(seq2, tagset)
        #print j+1, ' '.join(seq)
       
        # check for agreement
        if seq1 != seq2:
            update(y, z, u, step_size)
        else:
            return seq1, iteration

        iteration += 1
    return seq1, -1 

'''
Dual decomposition update
'''
def update(indi1, indi2, u, step_size):
    for i in range(len(indi1)):
        for t in u[i].iterkeys():
            u[i][t] -= (indi2[i][t] - indi1[i][t])*step_size


                
