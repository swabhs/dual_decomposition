# usr/bin/python

'''
Given a pcfg, and an input sentence, finds the highest probability 
tree for that sentence under the pcfg.
'''
import utils, sys, re, math
from collections import defaultdict

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
                        if u == None:
                            pi[i][j][X] = prob[X][rule] #dd factor
                        else:
                            pi[i][j][X] = prob[X][rule] + u[i][X] #dd factor
                    else: #smoothing
                        pi[i][j][X] = -50.00 #float("-inf") 
                    bp[i][j][X] = rule #"" 
                else:
                    pi[i][j][X] = float("-inf")
    return pi, bp
         
def run(sentence, prob, nonterms, start, u):
    n = len(sentence)
    pi, bp = init(sentence, nonterms, prob, u)
    for l in xrange(1,n):
        for i in xrange(0, n-l):
            j = i + l
            for X in nonterms:
                max_score = float("-inf")
                best_rule = "NP~~NOUN~ADJ" #dummy rule, buggy? 
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
       
def find_best_parse(pi, bp, n):
    max = float("-inf")
    best = "NP~~NOUN~ADJ" # dummy rule, buggy?
    for nonterm, logprob in pi[0][n-1].iteritems():
        if logprob > max:
            max = logprob
            best = nonterm
    return decode(bp, 0, n-1, best)

def get_pcfg(pcfg):
    prob = defaultdict()
    nonterms = set([])
    start = '**' # pass this across files?
    
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

if __name__ == "__main__":
    print "reading pcfg..."
    prob, nonterms, start = get_pcfg(sys.argv[1])
    
    print "reading data..."
    sentences = get_sentences(sys.argv[2])

    print "parsing using cky..."
    parses = []
    for sentence in sentences:
        if True: #len(sentence) <= 10:
            print sentences.index(sentence), ": ", sentence
            pi, bp = run(sentence, prob, nonterms, start, None) 
            parse = find_best_parse(pi, bp, len(sentence))
            parses.append(parse)
            print parse, "\n"
            
    parsefile = open("parse.out", "w")
    for parse in parses:
        parsefile.write(parse + '\n')
    parsefile.close()
