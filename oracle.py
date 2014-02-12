# /usr/bin/py

from __future__ import division
import sys
import evaluate


def read_k_best(filename):
    full = []
    one = []
    f = open(filename, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            full.append(one)
            one = []
            continue
        ele = line.split(" ")
        one.append(ele)
      
    f.close()
    
#    k_best = []
#    for item in full:
#        if len(item) == 1:
#            k_best.append([])
#        else:
#            k_best.append(item[1:])
    k_best = {}
    i = 0
    for item in full:
        sentence = ' '.join(item[0])
        k_best[i] = item[1:]
        #if len(k_best[i]) == 4:
             #print i, "," ,
        i += 1
    return k_best

def compare(kbestall, goldall, k):
    count = 0
    avgacc = 0.0 # corpus acc for k best
    for i, gold in goldall.iteritems():
        if len(kbestall[i]) >= k:
            kbest = kbestall[i][:k]
            count += 1
        else:
            kbest = kbestall[i]
        maxacc = 0.0
        for best in kbest:
            if len(gold[0]) != len(best):
                print i
            a = evaluate.accuracy(gold[0], best)
            if a > maxacc:
                maxacc = a
        avgacc += maxacc
    conv_rate = count/len(goldall)
    avgacc /= len(goldall)
    return conv_rate, avgacc

if __name__ == "__main__":
    k_best = read_k_best(sys.argv[1])
    gold = read_k_best(sys.argv[2])
    
    #print len(k_best), len(gold)
    
    for k in range(4):
        crate, acc = compare(k_best, gold, k+1)
        #print acc, ",",
        print "oracle acc of ", k+1, "best = ", acc, "\tconvergence rate = ", crate
