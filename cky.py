# usr/bin/python

'''
Given a pcfg, and an input sentence, finds the highest probability 
tree for that sentence under the pcfg.
'''
import hw3_utils, sys, re, math
from collections import defaultdict
from time import time

min_prob = -50.0 # smoothing

def init(sentence, nonterms, prob, u):
    n = len(sentence)
    pi = defaultdict()
    bp = defaultdict()
    for i in xrange(0,n):
        pi[i] = defaultdict()
        bp[i] = defaultdict()
        for j in xrange(0,n):
            pi[i][j] = defaultdict()
            bp[i][j] = defaultdict()
            for X in nonterms:
                if i == j:
                    rule = X + '~~' + sentence[i]
                    if rule in prob[X]:
                        if u == None: # simple cky without dd
                            pi[i][j][X] = prob[X][rule]
                        else: # cky with dd
                            pi[i][j][X] = prob[X][rule] + u[i][X] #dd factor
                    else: #smoothing
                        pi[i][j][X] = min_prob
                    bp[i][j][X] = rule 
                else:
                    pi[i][j][X] = float("-inf")
    
    return pi, bp
         
def run(sentence, nonterms, start, prob, pcfg_b, u):
    n = len(sentence)
    pi, bp = init(sentence, nonterms, prob, u)
    for l in xrange(1, n+1):
        for i in xrange(0, n-l):
            j = i + l
            for X in nonterms:
                max_score = float("-inf")
                best_rule = "" #dummy rule, buggy?

                if X in pcfg_b:
                    for s in xrange(i, j): 
                        for rule, p in pcfg_b[X].iteritems():
                            # re match for Y, Z
    #                        exp = re.match(r'([^~]*)~~([^~]*)~([^~]*)', rule)
    #                        
    #                        if exp:
    #                            Y,Z = exp.groups()[1:]
    #                        else: # unary rule for terminal
    #                            continue
    #
    #                        if pmap == prob:
    #                            print "think! ",
                            x,yz = rule.split('~~')
                            if '~' not in yz:
                                continue
                            Y,Z = yz.split('~')
                            score = p + pi[i][s][Y] + pi[s+1][j][Z]
                            if score > max_score:
                                max_score = score
                                best_rule = Y + ' ' + Z + ' ' + str(s)
                pi[i][j][X] = max_score
                bp[i][j][X] = best_rule
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
    prob, pcfg_b, nonterms, start = hw3_utils.get_pcfg(sys.argv[1])
    hw3_utils.print_size(prob)
    hw3_utils.print_size(pcfg_b)

    #print "reading data..."
    sentences = hw3_utils.get_sentences(sys.argv[2])

    #print "parsing using cky..."
    parsefile = open("candidate_parses_test.out", "w")
    total_diff = 0
    for sentence in sentences:
        if True:#len(sentence) <= 10:
            start_time = time()
            print sentences.index(sentence), ": size=", len(sentence)
            parse = run(sentence, nonterms, start, prob, pcfg_b, None) 
            parsefile.write(parse + '\n')
            end_time = time()
            diff = end_time - start_time
            print diff,"\n"
            total_diff += diff
    parsefile.close()
    print "total time", total_diff
