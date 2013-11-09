# ! /usr/bin/python

'''
Pipeline to run diverse sequence labeling using dual decomposition.
Created on Oct 15, 2013

@author: swabha
'''

import sys,re, time
import utils, hmm_utils, evaluate, viterbi, dd_tagger_fst

'''
'''
def execute(dataset, hmm_file, tag_file):
    print "loading learnt parameters..."
    hmm, tagset = hmm_utils.get_param_tagset(hmm_file, tag_file)

    print "reading dev data..."
    test_sentences, test_tags = utils.get_tagging_data(dataset, '', '')

    i = 0
    converges = 0
    avg_iterations = 0
    start_time = time.time()
    for tree in treebank[10:]:
       
        if True: #len(tree) < 100:
            i+=1
            parse_list = utils.make_parse_list(tree)
            sentence, truetags = utils.get_terminals_tags(parse_list)
            print '\n', i, '\n', sentence, '\n'
            
            print "running dual decomposition..."
            best_tags, num_iterations, tags1, tags2 = dd_tagger_fst.run(sentence, tagset, hmm)
            if num_iterations != -1:
                print
                print tags1, ":tagger1, accuracy = ", evaluate.accuracy(truetags, tags1)
                print tags2, ":tagger2, accuracy = ", evaluate.accuracy(truetags, tags2)
                print best_tags, "best tags accuracy = ", evaluate.accuracy(truetags, best_tags)
                print "converges in ", num_iterations ," iterations \n"
                converges += 1
                avg_iterations += num_iterations
            else:
                print "does not converge :(\n"
            print "\n", truetags, " :true tags"
            print "-----------------------------------------------"
        
        if i==100:
            break     
    print avg_iterations/converges, "iterations on average"
    print converges*100/i, "% convergence"
    print "time_taken = ", time.time() - start_time

if __name__ == "__main__":
    test = sys.argv[1]
    hmm_file = sys.argv[2]
    tag_file = sys.argv[3]
    execute(test, hmm_file, tag_file)
