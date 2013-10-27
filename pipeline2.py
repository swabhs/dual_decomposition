# ! /usr/bin/python

'''
Pipeline to run diverse sequence labeling using dual decomposition.
Created on Oct 15, 2013

@author: swabha
'''

import sys,re, time
import utils, evaluate, viterbi, dual_decomposition3


'''
Reads the learnt parameters of pcfg and hmm from respective files
'''
def quick_execute(dev):
    print "loading learnt parameters..."
    hmm, tagset = viterbi.get_hmm_tagset()

    print "reading dev data..."
    parses = utils.read_parses_no_indent(dev)

    i = 0
    converges = 0
    for parse in parses:
       
        if True: #len(parse) <100:
            i+=1
            parse_list = utils.make_parse_list(parse)
            sentence, truetags = utils.get_terminals_tags(parse_list)
            print '\n', i, '\n', sentence, '\n'
            
            print "running dual decomposition..."
            num_iterations, tags1, tags2 = dual_decomposition3.run(sentence, tagset, hmm)
            if num_iterations != -1:
                print
                print tags1, ":tagger1, accuracy = ", evaluate.accuracy(truetags, tags1)
                print tags2, ":tagger2, accuracy = ", evaluate.accuracy(truetags, tags2)
                print "converges in ", num_iterations ," iterations \n"
                converges += 1
            else:
                print "does not converge :(\n"
            print "\n", truetags, " :true tags"
            print "-----------------------------------------------"
        
        if i==10000:
            break     
    print converges*100/i, "% convergence"
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
