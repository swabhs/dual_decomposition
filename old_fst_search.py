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

allowed_error = 0.00001

'''
Depending on the dd_u parameters, finds the best sequence
which is not equal to the best_sequence
'''
def run(best_sequence, dd_u):
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

    #print "dual weights before FST search: row = position, column = tag"

    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        actual_best_label = best_sequence[k-1]
        actual_best_score = dd_u[k-1][actual_best_label]

        first, second = get_top_two(dd_u[k-1])
        best_label = first
        best_score = dd_u[k-1][best_label]
        
        if abs(actual_best_score - best_score) > allowed_error:
        #if best_label != actual_best_label:
            next_best_label = best_label
            next_best_score = best_score
            print actual_best_label, best_label, k-1, "sentence length =", n
        else:
            # compare the actual_best with the 2nd best label, and store the backpointers accordingly
            #next_best_label = sorted_dd_u[-2][0]
            next_best_label = second
            next_best_score = dd_u[k-1][next_best_label]
	if (pi_false[-1] + best_score > pi_true[-1] + next_best_score and k != 1):
            bp_false.append(best_label) 
	    pi_false.append(pi_false[-1] + best_score)
	else:
	    bp_false = best_sequence[:k-1]
	    bp_false.append(next_best_label)
	    pi_false.append(pi_true[-1] + next_best_score)
        
        pi_true.append(pi_true[-1] + dd_u[k-1][actual_best_label])
    print ' '.join(bp_false), " : fst"
    fst_score = (pi_false[-1])
    #get_fsa_score(bp_false, dd_u)
    
#    print '\t'.join(dd_u[0].keys())
#    for pos, tags in dd_u.iteritems():
#        for tag, value in tags.iteritems():
#            print "{0:.1f}".format(value) + "\t",
#        print
    return bp_false, fst_score

def get_fsa_score(seq, dd_u):
    score = 0.0
    for k in range(len(seq)):
        tag = seq[k]
        score += dd_u[k][tag]
    print "tot fsa score =", score

'''
Given a map finds the keys of the two highest values in the map
'''
def get_top_two(imap):
    if imap.values()[0] > imap.values()[1] + allowed_error:
        first = imap.keys()[0]
        second = imap.keys()[1]
    else:
        first = imap.keys()[1]
        second = imap.keys()[0]
        
    rest = imap.keys()[2:]

    for k in rest:
        v = imap[k]
        cond1 = v > imap[first] + allowed_error # current value more than best
        cond2 = abs(v - imap[first]) < allowed_error # current value same as best
        cond3 = v > imap[second] + allowed_error # current value more than 2ndbest

        if cond1 or cond2:
            second = first
            first = k
        elif cond3:
            second = k
        
    return first, second


if __name__ == "__main__":
    i = {'a':0.000, 'b':0.00, 'c':0.00, 'd':0.00, 'e':0.000}
    print get_top_two(i)
