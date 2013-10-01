# ! /usr/bin/python

'''
Dual decomposition for a joint parser and tagger model.
Created on Sep 21, 2013

@author: swabha
'''

from collections import defaultdict
import utils, cky, viterbi

'''
Executes the dual decomposition algorithm
Note here that the nonterminals are more in number than the tags
'''
def run(sentence, pcfg_prob, nonterms, start, tagset, hmm_prob):
    max_iterations = 150
    step_size = 10

    n = len(sentence)

    u = defaultdict() # dual decomposition parameter
    for i in xrange(0, n):
        u[i] = defaultdict()
        for t in tagset:
            u[i][t] = 0
    
    k = 0 # number of iterations
    while k < max_iterations:
       print k
       pi, bp = cky.run(sentence, pcfg_prob, nonterms, start, u)
       parse = cky.find_best_parse(pi, bp, n)

       tags = viterbi.run(sentence, tagset, hmm_prob, u)
       
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
            #print u[i][tags[i]]
            u[i][parse_tags[i]] -= step_size
            #print u[i][parse_tags[i]]

def agree(parse, tags):
    parse_list = utils.make_parse_list(parse)
    terms, parse_tags = utils.get_terminals_tags(parse_list)
    
    print tags
    print parse_tags
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
