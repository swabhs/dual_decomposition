#! /usr/bin/python

'''
Main Viterbi algorithm
Created on Sep 12, 2013

@author: swabha
'''

import math, sys, hw3_utils
from collections import defaultdict

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
        escore = -20.0 #smoothing value
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
            bp[i][label] = labelset[0] #"" # is it buggy?
    pi[0]['sentence_boundary'] = 0.0
    
    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        for u in labelset:
            max_score = float("-inf")
            argmax = labelset[0] #"" # is it buggy?
            for w in labelset:
                local_score = get_local_score(sentence[k-1], w, u, weights)
                if dd_u == None:
                    score = pi[k-1][w] + local_score
                else:
                    score = pi[k-1][w] + local_score + dd_u[k-1][w] # dd factor
                if score > max_score:
                    max_score = score
                    argmax = w
            pi[k][u] = max_score
            bp[k][u] = argmax
    #for w in labelset:
        #print "{0:.2f}".format(pi[0][w]) + " ",
    #print

#    # print "decoding..."
    tags = []
    
    max_score = float("-inf")
    best_last_label = labelset[0] #"" # dummy best label - is it buggy?
    for w in labelset:
        local_score = get_local_score("", w, "sentence_boundary", weights)
        
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
    trans_file = sys.argv[1]
    em_file = sys.argv[2]

    hmm, tagset = hw3_utils.get_hmm_tagset(trans_file, em_file)
#    for key in hmm.iterkeys():
#        if 'tr' in key:
#            print key, '\t',
#    #print hmm['tr:sentence_boundary~>FUT']

    sentences = hw3_utils.get_sentences(sys.argv[3])
    posfile = open("candidate_postags_test.out", "w")
    for sentence in sentences:
        print sentences.index(sentence), sentence
        postags = run(sentence, tagset, hmm, None) 
        for tag in postags:
            posfile.write(tag + ' ')
        posfile.write("\n")
        print postags
        print
    posfile.close()
