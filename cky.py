# usr/bin/python

'''
Given a pcfg, and an input sentence, finds the highest probability 
tree for that sentence under the pcfg.
'''
import pcfg_utils, sys, re, math
from collections import defaultdict

def init(sentence, nonterms, prob, u, min_prob):
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
         
def run(sentence, prob, nonterms, start, u, min_prob):
    n = len(sentence)
    pi, bp = init(sentence, nonterms, prob, u, min_prob)
    for l in xrange(1, n+1):
        for i in xrange(0, n-l):
            j = i + l
            for X in nonterms:
                max_score = float("-inf")
                best_rule = "" #dummy rule, buggy? 
                for s in xrange(i, j): 
                    for rule, p in prob[X].iteritems():
                        # re match for Y, Z
                        exp = re.match(r'([^~]*)~~([^~]*)~([^~]*)', rule)
                        
                        if exp:
                            Y,Z = exp.groups()[1:]
                        else: # unary rule for terminal
                            continue
                        score = p + pi[i][s][Y] + pi[s+1][j][Z]
                        if score > max_score:
                            max_score = score
                            best_rule = Y + ' ' + Z + ' ' + str(s)
                pi[i][j][X] = max_score
                bp[i][j][X] = best_rule
    return pi, bp

def decode(bp, i, j, X):
    if i == j:
        nonterm, word = bp[i][j][X].split('~~')
        return '( ' + nonterm + ' ' + word + ' )'
    Y, Z, split_pos = bp[i][j][X].split(' ')
    s = int(split_pos)
    return '( ' + X + ' ' + decode(bp, i, s, Y) + ' ' + decode(bp, s+1, j, Z) + ' )'
       
if __name__ == "__main__":
    #print "reading pcfg..."
    prob, nonterms, start = pcfg_utils.get_pcfg(sys.argv[1])
    min_prob = -50.0 #pcfg_utils.smooth(prob)
    
    #print "reading data..."
    sentences = pcfg_utils.get_sentences(sys.argv[2])

    #print "parsing using cky..."
    parsefile = open("parse.out", "w")
    for sentence in sentences:
        if True: #len(sentence) <= 10:
            print sentences.index(sentence), ": ", sentence
            pi, bp = run(sentence, prob, nonterms, start, None, min_prob) 
            parse = decode(bp, 0, len(sentence) - 1, start)
            parsefile.write(parse + '\n')
            print parse, "\n"
            
    parsefile.close()
