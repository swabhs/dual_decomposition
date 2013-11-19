# usr/bin/python

'''
Evaluation of sequence labeling
'''

from __future__ import division

def accuracy(gold, test):
    if test == []:
        return 0
    if len(gold) != len(test):
        return
    correct = 0
    for pos in range(len(gold)):
        if gold[pos] == test[pos]:
            correct += 1
        
    return correct/len(gold)

def compare(seq1, seq2, gold):
    acc1 = accuracy(gold, seq1)
    if seq1 == seq2:
        our_result = 1.0
        acc2 = acc1
    else:
	our_result = 0.0
	acc2 = accuracy(gold, seq2)
    return our_result, acc1, acc2

def read_results(filename):
    f = open(filename, "r")
    
    fmap = defaultdict()
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
	    continue
        sentence = line   
        tagline = f.readline().strip()
        tags = tagline.split(' ')
        fmap[sentence] = tags
    return fmap

if __name__ == "__main__":
    goldmap = read_results(sys.argv[1])
    lianghuangmap = read_results(sys.argv[2])
    mymap = read.results(sys.argv[3])
    
    acc = 0.0
    for sentence in goldmap.iterkeys():
        match_acc, lhacc, myacc = compare(goldmap[sent], lianghuangmap[sent], mymap[sent])
        acc += myacc
    
    print "match accuracy =", acc/len(goldmap)
