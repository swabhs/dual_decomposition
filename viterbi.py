#! /usr/bin/python

'''
Main Viterbi algorithm
Created on Sep 12, 2013

@author: swabha
'''

import math, sys, utils
from collections import defaultdict

def get_hmm_tagset():
    hmm = defaultdict()
    
    hmm_file = open("hmm.txt", "r")
    while 1:
        line = hmm_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            param, prob = line.split(' ')
            hmm[param] = math.log(float(prob)) 
    
    tagset = set([])
    tag_file = open("tagset.txt", "r")
    while 1:
        line = tag_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            tagset.add(line) 

    return hmm, tagset

def get_local_score(word, prev_tag, tag, hmm):
    trans = 'tr:' + prev_tag + '~>' + tag
    if trans in hmm:
        tscore = hmm[trans]
    else:
        tscore = float("-inf")
    
    if word == "": # stopping local score
        return tscore

    emi = 'em:' + tag + '~>' + word
    if emi in hmm:
        escore = hmm[emi]
    else:
        escore = float("-inf")
    return tscore + escore

def run(sentence, labelset, weights, dd_u):
    
    n = len(sentence)
    pi = []
    bp = []

    #print 'initializing...'
    for i in xrange(0, n+1):
        pi.append(defaultdict())
        bp.append(defaultdict())
        for label in labelset:
            pi[i][label] = float("-inf")
            bp[i][label] = ""
    pi[0]['*'] = 0.0
    
    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        for u in labelset:
            max_score = float("-inf")
            argmax = ""
            for w in labelset:
                local_score = get_local_score(sentence[k-1], w, u, weights)
                score = pi[k-1][w] + local_score + dd_u[k-1][w] # dd factor
                if score > max_score:
                    max_score = score
                    argmax = w
            pi[k][u] = max_score
            bp[k][u] = argmax
#        for w in labelset:
#            print "{0:.2f}".format(pi[k][w]) + " ",
#        print
#    # print "decoding..."
    tags = []
    
    max_score = float("-inf")
    for w in labelset:
        local_score = get_local_score("", w, "STOP", weights)
        
        score = pi[n][w] + local_score
        if score > max_score:
            max_score = score
            best_last_label = w
    tags.append(best_last_label)

    # tag extraction
    for k in range(n-1, 0, -1):
        last_tag = tags[len(tags)-1]
        tags.append(bp[k+1][last_tag])
    
    tags = list(reversed(tags))
    
    return tags

if __name__ == "__main__":
    hmm, tagset = get_hmm_tagset()
    dev_file = sys.argv[1]
    parses = utils.read_parses_no_indent(dev_file)
    
    i = 0     
    for parse in parses:
        if len(parse) <= 100:
            parse_list = utils.make_parse_list(parse)
            terminals, truetags = utils.get_terminals_tags(parse_list)
            print terminals
            print truetags
            tags = run(terminals, tagset, hmm) 
            print tags
            i+=1
            print "---------------------------"
        if i==10:
            break
 
