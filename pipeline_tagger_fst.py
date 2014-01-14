# ! /usr/bin/python

'''
Pipeline to run diverse sequence labeling using dual decomposition.
Created on Oct 15, 2013

@author: swabha
'''

import sys,re, time
import data_reader, hmm_utils, evaluate, viterbi, dd_tagger_fst
from smoothing import replace_test

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
 
    fst_acc = 0
    best_acc = 0
    wrong = 0
    for sentence in test_sentences:
       
        if True:
            i += 1
            truetags = test_tags[test_sentences.index(sentence)]
            
            sys.stderr.write('\n' + str(i)+ '\n')
            print ' '.join(ts[i-1])
            
            best_tags, num_iterations, tags1, tags2 = dd_tagger_fst.run(sentence, tagset, hmm)
            if tags2 == best_tags:
                print "YOU ARE WRONG!"
                wrong += 1
                break
            if num_iterations != -1:
                facc = evaluate.accuracy(truetags, tags2)
                #sys.stderr.write("fst tagger accuracy = " + str(facc) + "\n")
                fst_acc += facc

                bacc = evaluate.accuracy(truetags, best_tags)
                #sys.stderr.write("best tags accuracy = " + str(bacc) + "\n")
                best_acc += bacc

                sys.stderr.write("converges in " + str(num_iterations) + " iterations \n")
                converges += 1
                avg_iterations += num_iterations
            else:
                sys.stderr.write("does not converge :(\n")
            print ' '.join(best_tags)
            print ' '.join(tags2)
            #print "gold  : ", ' '.join(truetags)
            print
            
            #if i == 10:
                #break
    sys.stderr.write("\nsystem performance\n--------------------\n")
    sys.stderr.write("\ngoes wrong: " + str(wrong/converges) +"\n")
    sys.stderr.write("\naverage accuracy of best: " + str(best_acc/converges) +"\n")
    sys.stderr.write("average accuracy of 2nd best: " + str(fst_acc/converges) +"\n")
    
    sys.stderr.write("\nsystem efficiency\n---------------------\n")
    sys.stderr.write("\n" + str(avg_iterations/converges) + " iterations on average\n")
    sys.stderr.write(str(converges*100/i) +  " % convergence\n")
    sys.stderr.write("time_taken = "+ str(time.time() - start_time) + "\n")

if __name__ == "__main__":
    test_sent_tags = sys.argv[1]
    hmm_file = sys.argv[2]
    tag_file = sys.argv[3]
    execute(test_sent_tags, hmm_file, tag_file)
