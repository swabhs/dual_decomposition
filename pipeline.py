# /usr/bin/python

'''
Pipeline to run k-best/k-diverse-best sequence labeling using dual
decomposition.
'''


from __future__ import division
import sys, re, time
import data_reader, hmm_utils, evaluate, viterbi, dd_tagger_fst, dd_k_best
from smoothing import replace_test

def execute(dataset, hmm_file, tag_file, k):
    hmm, tagset = hmm_utils.get_param_tagset(hmm_file, tag_file)
    ts, test_tags = data_reader.read_tagging_data(dataset)
    test_sentences = replace_test(ts, hmm, tagset)

    i = 0
    conv_rates = [] # to keep track of the convergence rates varying with k
    for j in range(k):
        conv_rates.append(0.0)

    for sentence in test_sentences:
        k_best = []
        if True: 
            i += 1
            truetags = test_tags[test_sentences.index(sentence)]

            sys.stderr.write('\n' + str(i)+ '\n')
            sys.stderr.write(' '.join(sentence) + "\n")
            print ' '.join(sentence)

            best_tags, num_iter, second_best, sb2 = dd_tagger_fst.run(sentence, tagset, hmm)
            conv_rates[0] += 1
            k_best.append(best_tags)
            if num_iter == -1:
                sys.stderr.write("2nd best does not converge :( \n")
                print ' '.join(best_tags)
                continue
            j = 2 # we have the best, and the second best now
            conv_rates[j-1] += 1
            sys.stderr.write(str(j) + " best converges in " + str(num_iter) + " iterations \n")
            k_best.append(second_best)
         
            while j < k:
                next_best, num_iter = dd_k_best.run(sentence, tagset, hmm, k_best)
                if num_iter != -1:
                    conv_rates[j] += 1
                    k_best.append(next_best)
                    sys.stderr.write(str(j+1) + " best converges in " + str(num_iter) + " iterations \n")
                else:
                    sys.stderr.write(str(j+1) + "th best does not converge\n")
                    break
                j += 1

        for best in k_best:
            print ' '.join(best)                
        print

    for j in range(k):
        sys.stderr.write("convergence rate of " + str(j) + " best = " + str(conv_rates[j]*100/conv_rates[0]) + "% \n")

if __name__ == "__main__":
    test_sent_tags = sys.argv[1]
    hmm_file = sys.argv[2]
    tag_file = sys.argv[3]
    k = 4
    execute(test_sent_tags, hmm_file, tag_file, k)            


