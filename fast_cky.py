# usr/bin/python

'''
Given a pcfg, and an input sentence, finds the highest probability 
tree for that sentence under the pcfg.
'''
import hw3_utils, sys, re, math
from collections import defaultdict
from time import time

min_prob = -50.0 # smoothing

def init(sentence, preterminals, pcfg_u, u):
    n = len(sentence)
    pi = defaultdict()
    bp = defaultdict()
    for i in xrange(0,n):
        pi[i] = defaultdict()
        bp[i] = defaultdict()
        for j in xrange(0,n):
            pi[i][j] = defaultdict()
            bp[i][j] = defaultdict()
            if i != j:
                continue
            if sentence[i] in pcfg_u:
                for X, p in pcfg_u[sentence[i]].iteritems():
                    if u == None:
                        pi[i][i][X] = p
                    else:
                        pi[i][i][X] = p + u[i][X]
                    bp[i][i][X] = X + '~~' + sentence[i]
            else:
                for X in preterminals:
                    if u == None:
                        pi[i][i][X] = min_prob #smoothing
                    else:
                        pi[i][i][X] = min_prob + u[i][X]
                    bp[i][i][X] = X + '~~' + sentence[i]
    return pi, bp
         
def run(sentence, leaves, start, prob, pcfg_u, u):
    n = len(sentence)
    pi, bp = init(sentence, leaves, pcfg_u, u)
    for l in xrange(1, n+1):
        for i in xrange(0, n-l):
            j = i + l
            for s in xrange(i, j): 
                for Y,val1 in pi[i][s].iteritems():
                    for Z, val2 in pi[s+1][j].iteritems():
                        key = Y + '~' + Z
                        if key in prob:
                            for X,val0 in prob[key].iteritems():
                                if X not in pi[i][j]:
                                    pi[i][j][X] = float("-inf")
                                score = val0 + val1 + val2
                                if score > pi[i][j][X]:
                                    pi[i][j][X] = score
                                    bp[i][j][X] = Y + ' ' + Z + ' ' + str(s)

    parse = decode(bp, 0, n-1, start)
    return parse

def decode(bp, i, j, X):
    if i == j:
        nonterm, word = bp[i][j][X].split('~~')
        return '( ' + nonterm + ' ' + word + ' )'
    Y, Z, split_pos = bp[i][j][X].split(' ')
    s = int(split_pos)
    return '( ' + X + ' ' + decode(bp, i, s, Y) + ' ' + decode(bp, s+1, j, Z) + ' )'
       
if __name__ == "__main__":
    #print "reading pcfg..."
    pcfg_u, inv, leaves, start = hw3_utils.get_pcfg(sys.argv[1])

    #print "reading data..."
    sentences = hw3_utils.get_sentences(sys.argv[2])

    #print "parsing using cky..."
    parsefile = open("candidate_parses_test.out", "w")
    total_diff = 0
    for sentence in sentences:
        if True:#len(sentence) <= 10:
            start_time = time()
            print sentences.index(sentence), ": size=", len(sentence)
            parse = run(sentence, leaves, start, inv, pcfg_u, None) 
            parsefile.write(parse + '\n')
            end_time = time()
            diff = end_time - start_time
            print diff,"\n"
            total_diff += diff
    parsefile.close()
    print "total time", total_diff
