# ! /usr/bin/python

'''
Pipeline to run sequence labeling, pcfg parsing and dual decomposition.
Created on Sep 21, 2013

@author: swabha
'''

import sys,re, time
import utils, cky, viterbi, dual_decomposition


'''
Reads the learnt parameters of pcfg and hmm from respective files
'''
def quick_execute(dev):
    print "loading learnt parameters..."
    pcfg_prob, nonterms, start = cky.get_pcfg()
    hmm, tagset = viterbi.get_hmm_tagset()

    print "reading dev data..."
    dev_sentences = utils.get_sentences(dev)

    for sentence in dev_sentences[100:200]:
        if len(sentence) <= 10:
            print '\n', sentence, '\n'
            #print dev_sentences.index(sentence)
            print "running dual decomposition..."
            dual_decomposition.run(sentence, pcfg_prob, nonterms, start, tagset, hmm)


'''
Learns the hmm, the pcfg from treebank and then executes the dual
decomposition code.
'''
def execute(treebank, dev):
    print "reading treebank..."
    parses = utils.read_parses_no_indent(treebank)
    parse_lists = []
    for parse in parses:
        parse_lists.append(utils.make_parse_list(parse))
      
    print "learning pcfg..."  
    nonterms, terms, start, prob = grammar.learn(parse_lists)
    
    print "learning hmm..."
    emission, transition = sequnece_labeler.learn(parse_lists)

    print "reading dev data..."
    dev_sentences = utils.get_sentences(dev)
    print dev_sentences[100] 
    for sentence in dev_sentences:
        parse = cky.run(sentence, nonterms, start, prob)
        sequnece = viterbi.run(sentence, emission, transition)


if __name__ == "__main__":
    treebank = sys.argv[1]
    dev = sys.argv[2]
    quick_execute(dev)
