#! /usr/bin/python

'''
Main Viterbi algorithm
Created on Sep 12, 2013

@author: swabha
'''

import math, sys
import data_reader, evaluate, hmm_utils
from smoothing import replace_test
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
#        emi = 'em:' + tag + '~>_RARE_'
#        if emi in hmm:
#            escore = hmm[emi]
#        else:
        escore = float("-inf")
    return tscore + escore

def run(sentence, labelset, weights, dd_u):
    n = len(sentence)
    pi = []
    bp = []
    arg_default = labelset[0]

    # bit of a hack
    if '*' not in labelset:
        labelset.append('*')
#    if 'STOP' in labelset:
#        labelset.remove('STOP')

    #print 'initializing...'
    for i in xrange(0, n+1):
        pi.append(defaultdict())
        bp.append(defaultdict())
        for label in labelset:
            pi[i][label] = float("-inf")
            bp[i][label] = arg_default
    pi[0]['*'] = 0.0
    
    # print 'main viterbi algorithm ...'
    for k in xrange(1, n+1):
        for u in labelset:
            max_score = float("-inf")
            argmax = arg_default
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
#        print k
#        for w in labelset:
#            print "{0:.2f}".format(pi[k][w]) + "\t",
#        print

    tags = []
    
    max_score = float("-inf")
    best_last_label = arg_default 
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
    print "viterbi output:", ' '.join(tags)
    print "viterbi score = ", "{0:.2f}".format(max_score)
     
    return tags

if __name__ == "__main__":
    sentences, truetags = data_reader.read_tagging_data(sys.argv[1])
    hmm, tagset = hmm_utils.get_param_tagset(sys.argv[2], sys.argv[3])
    sentences = replace_test(sentences, hmm, tagset)
    print sentences

    i = 0     
    tot_acc = 0.0
    for sentence in sentences:
#        for tag in tagset:
#            print tag,"\t",
#        print
        tags = run(sentence, tagset, hmm, None) 
        #tot_acc += evaluate.accuracy(truetags, tags)
        print sentence
        print tags, evaluate.accuracy(truetags[i], tags)
        print truetags[i], " :gold"
        i+=1
        print "---------------------------"
    print tot_acc/i
