# /usr/bin/python

'''
Diverse FST search (based on unigram Hamming distance)
'''
import sys, ast

# given a seq and dual scores, gives the best sequence not equal to given sequence
def run(best, dd_u, tagset):
    pi = []
    pi.append(0.0)
    bp = []

    n = len(best)
    for i in range(n):
        max_sc = float("-inf")
        best_tag = ''
        for tag in tagset:
            score = get_local_score(tag, best, i) + dd_u[i][tag]
            if score > max_sc:
                max_sc = score
                best_tag = tag
        pi.append(pi[-1] + score)
        bp.append(best_tag)
    return bp, pi[-1]

def get_local_score(tag, best, pos):
    if tag == best[pos]:
        return -1.0
    else:
        return 1.0
        
if __name__ == "__main__":
    line = "{0: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 1.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 1: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 1.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 2: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 1.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 3: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 1.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 4: {'VB': 1.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 5: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 1.0, 'VBZ': -1.0, 'NNS': 0.0}, 6: {'VB': 0.0, 'NN': 1.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 7: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 1.0}, 8: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': -1.0, '.': 2.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}}"
    m = ast.literal_eval(line)
    print '\t'.join(m[0].keys()) 
    for key, valmap in m.iteritems():
        for tag, val in valmap.iteritems():
            print val, "\t",
        print

    best = "PRP VBP RB TO VB IN NN NNS .".split(" ")
    
    sec_best = run(best, m) 
    print " ".join(best)
    print " ".join(sec_best)
