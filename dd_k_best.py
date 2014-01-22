# /usr/bin/python

from __future__ import division
import sys, math
import fst_search, viterbi

def init_dd_param(dd_u, n, tagset):
    for i in xrange(0, n):
        dd_u[i] = {}#defaultdict()
        for t in tagset:
            dd_u[i][t] = 0

# can be made faster, use dictionary shallow copying
def compute_indicators(seq, tagset):
    ind = {}
    for i in xrange(0, len(seq)):
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
    max_iter = 10
    
    n = len(sentence)
    k = len(k_best_list)

    u = [] # dd parameter list
    for j in range(k+1):
        u_j = {}
        init_dd_param(u_j, n, tagset)
        u.append(u_j)
    w = {}
    init_dd_param(w, n, tagset)
    ku = {}
    init_dd_param(ku, n, tagset)
 
    iteration = 1
    while iteration <= max_iter:
        print iteration
        step_size = 10.0 #/ math.sqrt(iteration)
        #print "step size", step_size 
        
        seqs = []
        indicators = []
        for i in u[0].iterkeys():
            for t in u[0][i].iterkeys():
                ku[i][t] = 1 * u[0][i][t]
        seq1, score1, score2 = viterbi.run(sentence, tagset, hmm, ku)
        seqs.append(seq1)
        indicators.append(compute_indicators(seq1, tagset))
        print 0, ' '.join(seq1)


        for j in range(k):
            seq, fst_score = fst_search.run(k_best_list[j], u[j+1])
            print j+1, ' '.join(seq)
            seqs.append(seq)
            indicators.append(compute_indicators(seq, tagset))
       
        # check for agreement
        agree = True
        for seq in seqs[1:]:
            if seq == seq1:
                print seqs.index(seq)
                return
            if seq != seq1:
                agree = False
                break
       
        if agree == False:
            update(indicators, u, w, step_size)
        else:
            return seq1, iteration

        iteration += 1
    return seq1, -1 

'''
Update
'''
def update(indicators, u, w, step_size):
    n = len(w)
    k = len(indicators)
    j = 0
    for u_j in u:
        print "dd param for", j
        for i in u_j.iterkeys():
            for t in u_j[i].iterkeys():
                print u_j[i][t], 
            print
        j += 1
    #sys.stderr.write(str(n*len(w[0])) + "\n")
    for i in range(n):
        for t in w[i]:
            sum_ind = 0.0
            for ind in indicators:
                sum_ind += ind[i][t]
            w[i][t] = sum_ind/k

    for i in range(n):
        for t in w[i]:
            j = 0
            for ind in indicators:
                u[j][i][t] = u[j][i][t] - step_size * (ind[i][t] - w[i][t])
                j += 1
    check_dd_param(u)
        
def check_dd_param(u):
    for i in u[0].iterkeys():
        for t in u[0][i].iterkeys():
            s = 0
            for u_j in u:
                s += u_j[i][t]
            if s > 0.00000001:
                print "DD IS WRONG"
                return


                
