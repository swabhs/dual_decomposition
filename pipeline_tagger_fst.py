# ! /usr/bin/python

'''
Pipeline to run diverse sequence labeling using dual decomposition.
Created on Oct 15, 2013

@author: swabha
'''

import sys,re, time
import data_reader, hmm_utils, evaluate, viterbi, dd_tagger_fst
from smoothing import replace_test

def tagprint(sequence):
    for element in sequence:
        print element,
    print

def execute(dataset, hmm_file, tag_file):
    #sys.stderr.write("loading learnt parameters...\n")
    hmm, tagset = hmm_utils.get_param_tagset(hmm_file, tag_file)

    #sys.stderr.write("reading dev data...\n")
    ts, test_tags = data_reader.read_tagging_data(dataset)
    test_sentences = replace_test(ts, hmm, tagset)

    i = 0
    converges = 0
    avg_iterations = 0
    start_time = time.time()

    for sentence in test_sentences:
       
        if len(sentence) > 0 :#True: #len(tree) < 100:
            i += 1
            truetags = test_tags[test_sentences.index(sentence)]
            
            sys.stderr.write('\n' + str(i)+ '\n')
            tagprint(ts[i-1])
            best_tags, num_iterations, tags1, tags2 = dd_tagger_fst.run(sentence, tagset, hmm)
           
            tagprint(best_tags)
            tagprint(tags2)
            if num_iterations != -1:
                
                sys.stderr.write("fst tagger accuracy = " + str(evaluate.accuracy(truetags, tags2)) + "\n")
                sys.stderr.write("best tags accuracy = " + str(evaluate.accuracy(truetags, best_tags)) + "\n")
                sys.stderr.write("converges in " + str(num_iterations) + " iterations \n")
                converges += 1
                avg_iterations += num_iterations
            else:
                sys.stderr.write("does not converge :(\n")
            #tagprint(truetags)
            print
        #if i==100:
            #break     
    sys.stderr.write("\n" + str(avg_iterations/converges) + " iterations on average\n")
    sys.stderr.write(str(converges*100/i) +  " % convergence\n")
    sys.stderr.write("time_taken = "+ str(time.time() - start_time) + "\n")

if __name__ == "__main__":
    test_sent_tags = sys.argv[1]
    hmm_file = sys.argv[2]
    tag_file = sys.argv[3]
    execute(test_sent_tags, hmm_file, tag_file)
