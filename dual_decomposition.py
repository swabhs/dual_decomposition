# ! /usr/bin/python

'''
Dual decomposition for a joint parser and tagger model.
Created on Sep 21, 2013

@author: swabha
'''

from collections import defaultdict
import utils, cky, viterbi, hw3_utils, sys

'''
Executes the dual decomposition algorithm
Note here that the nonterminals are more in number than the tags
'''

def agree(parse_tags, tags):
    for i in xrange(0, len(tags)):
        if tags[i] == parse_tags[i]:
            continue
        else:
            return False
    return True 

def compute_indicators(tags, labelset):
    y = defaultdict()
    for i in xrange(0, len(tags)):
        z = defaultdict()
        for t in labelset:
            if tags[i] == t:
                z[t] = 1
            else:
                z[t] = 0
        y[i] = z
    return y

'''
Dual decomposition update
'''
def update(indi1, indi2, u, step_size):
    for i in xrange(0, len(indi1)):
        for t in u[i].iterkeys():
            u[i][t] -= (indi2[i][t] - indi1[i][t])*step_size
            #print u[i][t],
        #print

def init_dd_param(u, n, tagset):
    for i in xrange(0, n):
        u[i] = defaultdict()
        for t in tagset:
            u[i][t] = 0

def run(sentence, tagset, non_terms, start, hmm_prob, pcfg, pcfg_b):
    max_iterations = 20
    step_size = 4.5

    n = len(sentence)

    u = defaultdict() # dual decomposition parameter
    init_dd_param(u, n, tagset)

    k = 0 # number of iterations
    while k < max_iterations:
          
        tags = viterbi.run(sentence, tagset, hmm_prob, u)

        parse = cky.run(sentence, nonterms, start, pcfg, pcfg_b, u)
        parse_list = utils.make_parse_list(parse)
        terms, parse_tags = utils.get_terminals_tags(parse_list)

        print k
        print tags, "tagger"
        print parse_tags, "parser"

        if agree(parse_tags, tags):
            return k, tags, parse  # converges in the kth iteration
        y = compute_indicators(tags, tagset)
        z = compute_indicators(parse_tags, tagset)
        step_size += 0.5
        update(y, z, u, step_size)

        k += 1
    return -1, tags, parse # does not converge

if __name__ == "__main__":
    #print "reading pcfg..."
    prob, pcfg_b, nonterms, start = hw3_utils.get_pcfg(sys.argv[1])

    # print "reading hmm..."
    trans_file = sys.argv[2]
    em_file = sys.argv[3]

    hmm, tagset = hw3_utils.get_hmm_tagset(trans_file, em_file)

    #print "reading data..."
    sentences = hw3_utils.get_sentences(sys.argv[4])

    #print "parsing using cky..."
    parsefile = open("candidate_parses_dev2.out", "w")
    posfile = open("candidate_postags_dev2.out", "w")
    

    for sentence in sentences:
        if True: #len(sentence) <= 10:
            print sentences.index(sentence), ": ", sentence, "\n"
            k, tags, parse = run(sentence, tagset, nonterms, start, hmm, prob, pcfg_b)
            if k == -1:
                print "does not converge"
                parsefile.write('\n')
                posfile.write('\n')
            else:
                parsefile.write(parse + '\n')
                for tag in tags:
                    posfile.write(tag + ' ')
                posfile.write('\n')
            print "------------------------------------------------------------------------------------------------------------"
    parsefile.close()
    posfile.close()

