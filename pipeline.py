# ! /usr/bin/python


'''
Pipeline to run sequence labeling, pcfg parsing and dual decomposition.
Created on Sep 21, 2013

@author: swabha
'''

import sys,re, time
import utils

def execute(treebank, dev):
#    print "reading treebank..."
#    parses = utils.read_parses_no_indent(treebank)
#    pares_lists = []
#    for parse in parses:
#        parse_lists.append(utils.make_parse_list(parse))
#      
#    print "learning pcfg..."  
#    nonterms, terms, start, prob = grammar.learn(parse_lists)
#    
#    print "learning hmm..."
#    emission, transition = sequnece_labeler.learn(parse_lists)
#
    print "reading dev data..."
    dev_sentences = utils.get_sentences(dev)
    print dev_sentences[100] 
#    for sentence in dev_sentences:
#        parse = cky.run(sentence, nonterms, terms, start, prob)
#        sequnece = viterbi.run(sentence, emission, transition)
#
if __name__ == "__main__":
    treebank = sys.argv[1]
    dev = sys.argv[2]
    execute(treebank, dev)
