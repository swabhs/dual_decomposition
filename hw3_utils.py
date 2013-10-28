# usr/bin/python
'''
For HW3
'''

from __future__ import division
from collections import defaultdict

'''
Read pcfg 
'''
def get_pcfg(pcfg_file):
    pcfg_u = defaultdict() # unary rule probabilites
    pcfg_b = defaultdict() # binary rule probabilites
    pcfg = defaultdict()
    # keep these separate for efficiency, less number of rules to 
    # iterate over in cky

    nonterms = set([])
    start = 'S'
    
    prob_file = open(pcfg_file, 'r')
    while 1:
        line = prob_file.readline()
        if not line:
            break

        line = line.strip()
        X, yz, p = line.split('\t')
        nonterms.add(X)
         
        if X not in pcfg:
            pcfg[X] = defaultdict()
            pcfg_u[X] = defaultdict()

        if ' ' in yz:
            Y, Z = yz.split(' ')
            rule = X + '~~' + Y + '~' + Z
            if X not in pcfg_b:
                pcfg_b[X] = defaultdict()
            pcfg_b[X][rule] = float(p)
            nonterms.add(Y)
            nonterms.add(Z)
        else:
            rule = X + '~~' + yz
            pcfg_u[X][rule] = float(p)
        
        pcfg[X][rule] = float(p)
    return pcfg, pcfg_b, list(nonterms), start

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

'''
Read transition and emission parameters
'''
def get_hmm_tagset(tfile, efile):
    hmm = defaultdict()
    tagset = set([])

    trans_file = open(tfile, "r")
    while 1:
        line = trans_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            prev_tag, current_tag, prob = line.split('\t')
            param = "tr:" + prev_tag + '~>' + current_tag
            hmm[param] = float(prob)
            tagset.add(current_tag)
            tagset.add(prev_tag)

    print "transition size", len(hmm)

    em_file = open(efile,"r")
    while 1:
        line = em_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            tag, word, prob = line.split('\t')
            param = "em:" + tag + "~>" + word
            hmm[param] = float(prob)

    return hmm, list(tagset)

def print_size(pcfg):
    size = 0
    for nonterm, rules in pcfg.iteritems():
        size += len(rules)
    print size
