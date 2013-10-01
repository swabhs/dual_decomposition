# ! /usr/bin/python

'''
Dual decomposition for a joint parser and tagger model.
Created on Sep 21, 2013

@author: swabha
'''

from collections import defaultdict

'''
Executes the dual decomposition algorithm
Note here that the nonterminals are more in number than the tags
'''
def run(sentence, pcfg_prob, nonterms, start, tagset, hmm_prob):
    max_iterations = 50
    step_size = 0.01

    n = len(sentence)

    u = defaultdict() # dual decomposition parameter
    for i in xrange(0, n):
        u[i] = defaultdict()
        for t in tagset:
            u[i][t] = 0.0
    
    k = 0 # number of iterations
    while k < max_iterations:
       pi, bp = cky.run(sentence, prob, nonterms, start)
       parse = find_best_parse(pi, bp, n)

       tags = viterbi.execute(sentence, nonterms, hmm_prob)
       
       if agree(parse, tags): 
           print "converges at ", k
           return parse, tags

       update(u, parse, tags, step_size)
       k += 1
    print "does not converge :("


def update(u, parse, tags, step_size):
    #TODO

def agree(parse, tags):
    #TODO
