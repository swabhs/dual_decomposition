# ! /usr/bin/python

'''
Dual decomposition for a joint parser and tagger model.
Created on Sep 21, 2013

@author: swabha
'''

from collections import defaultdict
import utils

'''
Executes the dual decomposition algorithm
Note here that the nonterminals are more in number than the tags
'''
def run(sentence, pcfg_prob, nonterms, start, tagset, hmm_prob):
    max_iterations = 50
    step_size = 1

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
    parse_list = utils.make_parse_list(parse)
    terminals, parse_tags = utils.get_terminals_tags(parse_list)
    
    for i in xrange(0, len(tags)):
        if tags[i] == parse_tags[i]:
            u[i][tags[i]] = 0
        else:
            u[i][tags[i]] += step_size
            u[i][parse_tags[i]] -= step_size
           

def agree(parse, tags):
    parse_list = utils.make_parse_list(parse)
    terms, parse_tags = utils.get_terminals_tags(parse_list)
    
    for i in xrange(0, len(tags)):
        if tags[i] == parse_tags[i]:
            continue
        else:
            return False
    return True 

if __name__ == "__main__":
    parse = "(S (NP (NNP Ms.) (NNP Haag)) (VP (VBZ plays) (NP (NNP Elianti))) (. .))"
    tags = ["NNP", "NNP", "VBZ", "NNP", "."]
    print agree(parse, tags)    
