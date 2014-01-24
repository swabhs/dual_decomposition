# ! /usr/bin/python

'''
Pipeline to run diverse sequence labeling using dual decomposition.
Created on Jan 14, 2014

@author: swabha
'''

from __future__ import division
import sys, re, time
import data_reader, hmm_utils, evaluate, viterbi, dd_tagger_fst, dd_k_best
from smoothing import replace_test

def execute(dataset, hmm_file, tag_file):
    hmm, tagset = hmm_utils.get_param_tagset(hmm_file, tag_file)
    ts, test_tags = data_reader.read_tagging_data(dataset)
    test_sentences = replace_test(ts, hmm, tagset)

    i = 0
    conv = 0
    sec_conv = 0
    for sentence in test_sentences:
       
        if True: #len(sentence) < 15:
            i += 1
            truetags = test_tags[test_sentences.index(sentence)]
            
            sys.stderr.write('\n' + str(i)+ '\n')
            sys.stderr.write(' '.join(sentence) + "\n")
            print ' '.join(sentence)
            
            k_best = []
            best_tags, num_iter, tags1, tags2 = dd_tagger_fst.run(sentence, tagset, hmm)
            if tags2 == best_tags:
                sys.stderr.write("YOU ARE WRONG!\n")
                break
            if num_iter != -1:
                sec_conv += 1
                sys.stderr.write("2nd best converges in " + str(num_iter) + " iterations\n")
                k_best.append(best_tags)
                k_best.append(tags1)
                
                third_best, num_iter2 = dd_k_best.run(sentence, tagset, hmm, k_best)
                if num_iter2 != -1:
                    sys.stderr.write("3rd best converges in " + str(num_iter2) + " iterations\n")
                    conv += 1
                    k_best.append(third_best)
                    fourth_best, num_iter3 = dd_k_best.run(sentence, tagset, hmm, k_best)
                    sys.stderr.write("4th best converges in " + str(num_iter3) + "\n")
                    print ' '.join(fourth_best)
                else:
                    sys.stderr.write( "3rd best does not converge :(\n")
            else:
                sys.stderr.write("2nd best does not converge :(\n")
                continue
            print ' '.join(best_tags)
            print ' '.join(tags2)
            print ' '.join(third_best)
            print
    
    sys.stderr.write("% convergence of 2nd best =" + str(sec_conv*100/i) + "\n")
    sys.stderr.write("% convergence of 3rd best =" + str(conv*100/sec_conv) + "\n")

if __name__ == "__main__":
    test_sent_tags = sys.argv[1]
    hmm_file = sys.argv[2]
    tag_file = sys.argv[3]
    execute(test_sent_tags, hmm_file, tag_file)
