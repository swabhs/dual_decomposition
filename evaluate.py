# usr/bin/python

'''
Evaluation of sequence labeling
'''

from __future__ import division
from collections import defaultdict
import sys

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
    acc2 = accuracy(gold, seq2)
    for i in range(len(seq1)):
        
        if seq1[i] != seq2[i]:
            print seq1, '\n', seq2
            return 0.0, acc1, acc2
    
    return 1.0, acc1, acc2

def read_results(filename):
    f = open(filename, "r")
    
    flist = []
    #fmap = defaultdict()
    while 1:
        line = f.readline()
        if not line:
            break
        if line == '':
	    continue
        sentence = line.strip()
        tagline = f.readline().strip()
        tags = tagline.split(' ')
        #fmap[sentence] = tags
        flist.append(tags)
    return flist

'''
Input = file with sentence, best seq, 2nd best seq, newline
output = 2 files, each with sentence, one seq, newline
'''
def convert_12(filename):
    f = open(filename, "r")

    sentences = []
    best1 = []
    best2 = []
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
            continue
        sentences.append(line)
        best1.append(f.readline().strip())
        best2.append(f.readline().strip())
    f.close()

    out1 = open('lh_ptb_dev_best1.out', 'w')
    out2 = open('lh_ptb_dev_best2.out', 'w')
    for i in range(len(sentences)):
        out1.write(sentences[i] + '\n' + best1[i] + '\n\n')
        out2.write(sentences[i] + '\n' + best2[i] + '\n\n')
    out1.close()
    out2.close()
    
def fix_output(filename, devfilename, newfilename):
    f = open(devfilename, 'r')
    sentences = []
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
            continue
        sentences.append(line)
        line = f.readline()
    f.close()
    
    f = open(filename, 'r')
    tagseqs = []
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
            continue
        line = f.readline().strip()
        tagseqs.append(line)
    f.close()

    f = open(newfilename, 'w')
    for i in range(len(sentences)):
        f.write(sentences[i] + '\n' + tagseqs[i] + '\n\n')
    f.close()

def main():
    convert_12(sys.argv[1])

def main2():
    goldmap = read_results(sys.argv[1])
    lianghuangmap = read_results(sys.argv[2])
    mymap = read_results(sys.argv[3])
    
    acc = 0.0
    avg_lhacc = 0.0
    avg_myacc = 0.0
    for i in range(len(goldmap)):
        g = goldmap[i]
        lh = lianghuangmap[i]
        my = mymap[i]
        match_acc, lhacc, myacc = compare(g, lh, my)
        acc += match_acc
        avg_lhacc += lhacc
        avg_myacc += myacc
        break
    print "match accuracy =", acc/len(goldmap)
    print "lh accuracy = ", avg_lhacc/len(goldmap)
    print "my accuracy = ", avg_myacc/len(goldmap)

if __name__ == '__main__':
    main2()
