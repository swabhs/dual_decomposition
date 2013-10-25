#! /usr/bin/python

'''
Viterbi algorithm to find the best tag sequence not matching
a given tag sequence. 
Uses an underlying FST (not explicit in this code)
Created on Oct 15, 2013

@author: swabha
'''

import math, sys, utils, evaluate
from collections import defaultdict

'''
Depending on the dd_u parameters, finds the best sequence
which is not equal to the best_sequence
'''
def run(labelset, best_sequence, dd_u):
    n = len(best_sequence)
    pi = []
    bp = []
    flag = []

    #print 'initializing...'
    for i in xrange(0, n):
        pi.append(defaultdict())
        bp.append(defaultdict())
        flag.append(defaultdict())
        for label in labelset:
            pi[i][label] = 0.0
            bp[i][label] = list(labelset)[0] #"" # is it buggy?
            flag[i][label] = False
    flag[0][best_sequence[0]] = True
    
    # print 'main viterbi algorithm ...'
    for k in xrange(1, n):
        for u in labelset:
            max_score = float("-inf")
            argmax = list(labelset)[0] #"" # is it buggy?
            for w in labelset:
                score = pi[k-1][w] + dd_u[k-1][w] # dd factor
                if score > max_score:
                    max_score = score
                    argmax = w
            pi[k][u] = max_score
            bp[k][u] = argmax
            if best_sequence[k] == u and flag[k-1][argmax] == True:
                flag[k][u] = True
#        for w in labelset:
#            print "{0:.2f}".format(pi[k][w]) + " ",
#        print
    # print "decoding..."
    best_label_seq = []
    
    max_score = float("-inf")
    #best_last_label = list(labelset)[0] #"" # dummy best label - is it buggy?
    for w in labelset:
        
        if flag[n-1][w] == False:
            score = pi[n-1][w] + dd_u[n-1][w]
        else:
            score = float("-inf")
        if score > max_score:
            max_score = score
            best_last_label = w
    best_label_seq.append(best_last_label)

    # tag extraction
    for k in range(n-2, -1, -1):
        last_label = best_label_seq[-1]
        best_label_seq.append(bp[k+1][last_label])
    
    best_label_seq = list(reversed(best_label_seq))
    
    return best_label_seq

if __name__ == "__main__":
    tagfile = open("tagset.txt", 'r')
    tags = []
    while 1:
        line  = tagfile.readline()
        if not line:
            break
        tags.append(line.strip())
    
    dummy_best_sequence = ["NNS", "NNS", "NNS"]
    print run(tags, dummy_best_sequence)

