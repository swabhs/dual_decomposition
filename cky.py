# usr/bin/python

'''
Given a pcfg, and an input sentence, finds the highest probability 
tree for that sentence under the pcfg.
'''
import utils, sys, re
from collections import defaultdict

def init(sentence, nonterms, prob):
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
                        pi[i][j][X] = prob[X][rule]
                        bp[i][j][X] = rule
                    else:
                        pi[i][j][X] = 0.0 
                else:
                    pi[i][j][X] = 0.0
                print pi[i][j][X]
    return pi, bp
         
def run(sentence, prob, nonterms, start):
    n = len(sentence)
    pi, bp = init(sentence, nonterms, prob)
    return
    for l in xrange(0,n-1):
        for i in xrange(0, n-l):
            j = i + l
            print i,j, len(nonterms)
            for X in nonterms:
                max_score = float("-inf")
                best_rule = ""
                for s in xrange(i, j): # check for bugs
                    print X in prob
                    for rule, p in prob[X].iteritems():
                        # re match for Y, Z
                        exp = re.match(r'([^~]*)~~([^~]*)~([^~]*)', rule)
                        
                        if exp:
                            #if X != exp.groups()[0]:
                                #print 'strange, rule nesting wrong'
                                #continue
                            Y,Z = exp.groups()[1:]

                        else:
                            continue
                        score = p * pi[i][s][Y] * pi[s+1][j][Z]
                        print score, p, pi[i][s][Y], pi[s+1][j][Z] 
                        if score > max_score:
                            max_score = score
                            best_rule = rule
                pi[i][j][X] = max_score
                bp[i][j][X] = best_rule
    return pi, bp

def decode(pi, bp):
    tree = defaultdict()
    return tree

def get_pcfg():
    prob = defaultdict()
    nonterms = []
    start = '**' # pass this across files?
    
    prob_file = open('pcfg.txt', 'r')
    while 1:
        line = prob_file.readline()
        if not line:
            break
        line = line.strip()
        rule, p = line.split(' ')
        exp = re.match(r'([^~]*)~~([^~]*)~([^~]*)', rule)
        if exp:
            X,Y,Z = exp.groups()
        else:
            exp2 = re.match(r'([^~]*)~~([^~]*)', rule)
            X,Y = exp2.groups()
        if X not in prob:
           prob[X] = defaultdict()
        prob[X][rule] = float(p)

    nt_file = open('nonterminals.txt', 'r')
    while 1:
        line = nt_file.readline()
        if not line:
           break
        line = line.strip()
        nonterms.append(line)

    return prob, nonterms, start
           
if __name__ == "__main__":
    dev_file = sys.argv[1]
    prob, nonterms, start = get_pcfg()
    
    sentences = utils.get_sentences(dev_file)
    for sentence in sentences:
        if len(sentence) <= 10:
            print sentence
            pi, bp = run(sentence, prob, nonterms, start) 
            print pi[0][len(sentence)-1]['**']
            break
        

