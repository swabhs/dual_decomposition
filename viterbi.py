#! /usr/bin/python

'''
Main Viterbi algorithm
Created on Sep 12, 2013

@author: swabha
'''

from collections import defaultdict


def execute(sentence, labelset, weights):
    
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
            for w in labelset:
                local_score = 0.0 # compute???
                score = pi[k-1][w] + local_score
                if score > max_score:
                    max_score = score
                    argmax = w
            pi[k][u] = max_score
            bp[k][u] = argmax
    
    # print "decoding..."
    tags = []
    
    max_score = float("-inf")
    for w in labelset:
        local_score = 0.0 # compute?
        
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
