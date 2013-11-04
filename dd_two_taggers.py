# ! /usr/bin/python

'''
Dual decomposition for two tagger models.

Created on Sep 21, 2013

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

    u1 = defaultdict() # dual decomposition parameter
    u2 = defaultdict()
    for i in xrange(0, n):
        u1[i] = defaultdict()
        u2[i] = defaultdict()
        for t in tagset:
            u1[i][t] = 0
            u2[i][t] = 0
    
    k = 0 # number of iterations
    while k < max_iterations:

       tags1 = viterbi.run(sentence, tagset, hmm_prob, u1)
       tags2 = viterbi.run(sentence, tagset, hmm_prob, u2)
       
       if k == 0:
           print "initial tags:"
           print tags1, ":tagger1"
           print tags2, ":tagger2"
              
       if disagree(tags1, tags2): 
           return k, tags1, tags2  # converges in the kth iteration
       
       update(tags1, tags2, u1, u2, step_size)

       k += 1
    return -1, tags1, tags2 # does not converge

def update(tags1, tags2, u1, u2, step_size):
    
    for i in xrange(0, len(tags1)):
        if tags1[i] == tags2[i]:
            u1[i][tags1[i]] += step_size
            u2[i][tags2[i]] -= step_size

def disagree(tags1, tags2):
    for i in xrange(0, len(tags1)):
        if tags1[i] != tags2[i]:
            return True
        else:
            continue
    return False 

if __name__ == "__main__":
    parse = "(S (NP (NNP Ms.) (NNP Haag)) (VP (VBZ plays) (NP (NNP Elianti))) (. .))"
    tags = ["NNP", "NNP", "VBZ", "NNP", "."]
    print agree(parse, tags)    
