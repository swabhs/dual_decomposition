# usr/bin/python

'''
Evaluation of sequence labeling
'''

from __future__ import division

def accuracy(gold, test):
    if len(gold) != len(test):
        return
    correct = 0
    for pos in xrange(0, len(gold)):
        if gold[pos] == test[pos]:
            correct += 1
        
    return correct/len(gold)
