#! /usr/bin/python

'''
Viterbi algorithm to find the best tag sequence not matching
a given tag sequence. 
Uses an underlying FST (not explicit in this code)
Created on Nov 4th, 2013

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
    # true denotes that we are matching the best sequence so far

    pi_true = [] # needs to be maintained for k positions, where k is 
    # length of the sequence that matches the best sequence from the beginning

    pi_false = [] # needs to be maintained for n positions

    #print 'initializing...'
    pi_true.append(0.0)
    pi_false.append(0.0)

    # print 'main viterbi algorithm ...'
    for k in xrange(1, n):
        max_score = float("-inf")
        best_label = labelset[0] # dummy best label
        for u in labelset:
            if dd_u[k][u] > max_score:
                max_score = dd_u[k][u]
                best_label = u
        #if len(pi_true) == len(pi_false):
        if best_sequence[k] != best_label:
            print "not expected"
        # we are matching the best sequence
#                pi_true[k] = pi_true[k-1] + max_score
#                bp[k] = best_label
#            else:
#                
#        pi[k] = pi
#            bp[k][u] = argmax
#            if best_sequence[k] == u and flag[k-1][argmax] == True:
#                flag[k][u] = True
#        for w in labelset:
#            print "{0:.2f}".format(pi[k][w]) + " ",
#        print
    # print "decoding..."
#    best_label_seq = []
#    
#    max_score = float("-inf")
#    #best_last_label = list(labelset)[0] #"" # dummy best label - is it buggy?
#    for w in labelset:
#        
#        if flag[n-1][w] == False:
#            score = pi[n-1][w] + dd_u[n-1][w]
#        else:
#            score = float("-inf")
#        if score > max_score:
#            max_score = score
#            best_last_label = w
#    best_label_seq.append(best_last_label)
#
#    # tag extraction
#    for k in range(n-2, -1, -1):
#        last_label = best_label_seq[-1]
#        best_label_seq.append(bp[k+1][last_label])
#    
#    best_label_seq = list(reversed(best_label_seq))
#    
     return best_sequnece

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

