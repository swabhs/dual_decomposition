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
    
    k_best = []
    for item in full:
        k_best.append(item[1:])

    return k_best

def compare(kbest_all, gold_all, k):
    corp_acc = 0.0
    dontcount = 0
    for gold in gold_all:
        i = gold_all.index(gold)
        if i == len(kbest_all): # because we don't have all sentences, yet
            print "am i breaking out?"
            break
        if len(kbest_all[i]) != 4: # because some sentences don't converge
            dontcount += 1
            continue
        print i
        kbest = kbest_all[i][:k]
        max_acc = 0.0
        for best in kbest:
            a = evaluate.accuracy(gold[0], best)
            if a > max_acc:
                max_acc = a
        corp_acc += max_acc
    return corp_acc/(i+1-dontcount)

if __name__ == "__main__":
    k_best = read_k_best(sys.argv[1])
    gold = read_k_best(sys.argv[2])
    print len(gold)
    for k in range(4):
        print compare(k_best, gold, k+1)
