# usr/bin/python
'''
For HW3
'''

from __future__ import division
from collections import defaultdict

'''
Find the lowest unary-rule prob associated with each nonterminal
'''
def smooth(prob):
    min_probs = defaultdict()
    avg = 0.0
    internal = 0
    for nonterm,rule_p in prob.iteritems():
        min_p = 100
        for rule,p in rule_p.iteritems():
              x,yz = rule.split('~~')
              if '~' in yz:
                  if p < min_p:
                      min_p = p 
        if min_p != 100:
            min_probs[nonterm] = min_p
            avg += min_p
            print min_p
        else:
             internal += 1

    avg /= len(min_probs)
    print "avg min", avg
    print "internal nodes", internal
    print "total nodes", len(prob)
    return avg

'''
Read pcfg 
'''
def get_pcfg(pcfg):
    prob = defaultdict()
    nonterms = set([])
    start = 'S' # pass this across files?

    prob_file = open(pcfg, 'r')
    while 1:
        line = prob_file.readline()
        if not line:
            break

        line = line.strip()
        X, yz, p = line.split('\t')
        nonterms.add(X)

        if ' ' in yz:
            Y, Z = yz.split(' ')
            rule = X + '~~' + Y + '~' + Z
            nonterms.add(Y)
            nonterms.add(Z)
        else:
            rule = X + '~~' + yz

        if X not in prob:
           prob[X] = defaultdict()
        prob[X][rule] = float(p)

    return prob, list(nonterms), start

def get_sentences(datafile):
    sentences = []
    data = open(datafile, 'r')
    while 1:
       line =  data.readline()
       if not line:
          break
       line = line.strip()
       sentences.append(line.split(' '))
    return sentences

