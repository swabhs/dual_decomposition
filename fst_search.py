#! /usr/bin/python

'''
Viterbi algorithm to find the best tag sequence not matching
a given tag sequence. 
Uses an underlying FST (not explicit in this code)
Created on Nov 4th, 2013

@author: swabha
'''

import math, sys, utils, evaluate, operator
from collections import defaultdict

'''
Depending on the dd_u parameters, finds the best sequence
which is not equal to the best_sequence
'''
def run(labelset, best_sequence, dd_u):
    n = len(best_sequence)
    # true denotes that we are matching the best sequence so far

    pi_true = []
    # needs to be maintained for k positions, where k is 
    # length of the sequence that matches the best sequence from the beginning

    pi_false = []
    bp_false = []
    # needs to be maintained for n positions

    #print 'initializing...'
    pi_true.append(0.0)
    pi_false.append(0.0)

#    for pos, tags in dd_u.iteritems():
#        for tag, value in tags.iteritems():
#            print value,
#        print
#    print

    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        actual_best_label = best_sequence[k-1]

        sorted_dd_u = sorted(dd_u[k-1].iteritems(), key = operator.itemgetter(1)) 
        best_label = sorted_dd_u[-1][0]
        best_score = dd_u[k-1][best_label]

        if actual_best_label != best_label:
#            print actual_best_label, "actual", best_label, "best"
            #print sorted_dd_u
            next_best_label = best_label
            next_best_score = best_score
        else:
            # compare the actual_best with the 2nd best label, and store the backpointers accordingly
            next_best_label = sorted_dd_u[-2][0]
            next_best_score = dd_u[k-1][next_best_label]
 #           print k-1, next_best_label
	if (pi_false[-1] + best_score > pi_true[-1] + next_best_score and k != 1):
            bp_false.append(best_label) 
	    pi_false.append(pi_false[-1] + best_score)
  #          print "pi_false is better", pi_false[-1], pi_true[-1] + next_best_score
	else:
	    bp_false = best_sequence[:k-1]
	    bp_false.append(next_best_label)
	    pi_false.append(pi_true[-1] + next_best_score)
   #         print "pi_true" , pi_false[-1], pi_false[-1] + best_score
        
        pi_true.append(pi_true[-1] + dd_u[k-1][actual_best_label])
    return bp_false

