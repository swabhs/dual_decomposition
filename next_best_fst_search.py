# /usr/bin/python

import sys, ast

'''
FST search algorithm to return a sequence strictly not equal to the one-best
Used to get k-best list
'''
# for float comparison
allowed_error = 0.000001

# given a seq and dual scores, gives the best sequence not equal to given sequence
def run(best, dd_u):
    tagset = dd_u[0].keys()
    
    # dynamic programming var building up the best seq
    pi_true = []
    pi_true.append(dd_u[0][best[0]])

    # dynamic programming var building up the second best seq
    pi_false = []
    bp_false = []

    first, second = get_top_two(dd_u[0])
    if first == best[0]:
        pi_false.append(dd_u[0][second])
        bp_false.append(second)
    else:
        pi_false.append(dd_u[0][first])
        bp_false.append(first)

    pos = 1
    for tag in best[1:]:
        first, second = get_top_two(dd_u[pos])
        first_score = dd_u[pos][first]
        sec_score = dd_u[pos][second]

        if first == tag:
            alt = second
            a = pi_false[-1] + first_score
            b = pi_true[-1] + sec_score
        else: # first != tag # it confuses me when this would happen
            alt = first
            a = pi_false[-1] + first_score
            b = pi_true[-1] + first_score

	c = compare(a, b)
	if c == 1:
	    pi_false.append(a)
	    bp_false.append(first)
	else:
	    pi_false.append(b)
	    bp_false = best[:pos]
	    bp_false.append(alt)
        
        pi_true.append(pi_true[-1]+dd_u[pos][best[pos]])
        
        pos += 1

    return bp_false, pi_false[-1]
    
    
# given a map return the two keys with the highest values
def get_top_two(imap):
    if compare(imap.values()[0], imap.values()[1]) > -1:
        first = imap.keys()[0]
        second = imap.keys()[1]
    else:
        first = imap.keys()[1]
        second = imap.keys()[0]
    
    rest = imap.keys()[2:]
    for key in rest:
        c = compare(imap[key], imap[first])
        if c == 1:
            second = first
            first = key
        elif c == 0:
            second = key
        else:
            if compare(imap[key], imap[second]) == 1:
                second = key
    return first, second
    
# comparing two floats
def compare(a, b):
    if a > b + allowed_error:
        return 1
    elif b > a + allowed_error:
        return -1
    else:
        return 0

if __name__ == "__main__":
    line = "{0: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 1.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 1: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 1.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 2: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 1.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 3: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 1.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 4: {'VB': 1.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 5: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 1.0, 'VBZ': -1.0, 'NNS': 0.0}, 6: {'VB': 0.0, 'NN': 1.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}, 7: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': 0.0, '.': 0.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 1.0}, 8: {'VB': 0.0, 'NN': 0.0, '*': 0.0, 'STOP': -1.0, '.': 2.0, 'TO': 0.0, 'VBP': 0.0, 'PRP': 0.0, 'RB': 0.0, 'IN': 0.0, 'VBZ': -1.0, 'NNS': 0.0}}"
    m = ast.literal_eval(line)
    print '\t'.join(m[0].keys()) 
    for key, valmap in m.iteritems():
        for tag, val in valmap.iteritems():
            print val, "\t",
        print

    print get_top_two(m[0])
    best = "PRP VBP RB TO VB IN NN NNS .".split(" ")
    
    sec_best = run(best, m) 
    print " ".join(best)
    print " ".join(sec_best)
