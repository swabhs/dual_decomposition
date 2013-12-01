# ! /usr/bin/python 
 
''' 
Extracts emission and transition probabilities for an HMM POS tagger
for a treebank.
Created on Sep 21, 2013 
 
@author: swabha 
''' 
from __future__ import division
from collections import defaultdict
import sys, operator
import data_reader

def update_counts(terminals, tags, emission_counts, transition_counts, tag_counts):
    # updating emission counts
    for i in range(len(terminals)):
        emission_key = tags[i] + '~>' + terminals[i]
        if emission_key in emission_counts:
            emission_counts[emission_key] += 1
        else:
            emission_counts[emission_key] = 1
    
    tags.insert(0, '*')
    tags.append('STOP')
    
    # updating transition counts
    for i in xrange(1, len(tags)):
        transition_key = tags[i-1] + '~>' + tags[i]
        if transition_key in transition_counts:
            transition_counts[transition_key] += 1
        else:
            transition_counts[transition_key] = 1

    # updating tag counts
    for tag in tags:
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1

def test_for_prob_dist(param):
    tags = defaultdict()
    for par, prob in param.iteritems():
        tag, word = par.split('~>')
        if tag in tags:
            tags[tag] += prob
        else:
            tags[tag] = prob
    for tag, prob in tags.iteritems():
        if str(prob) != '1.0':
            print "problem with", tag

def set_hmm_params(emission, transition, tag_counts):
    for em, count in emission.iteritems():
        tag, word = em.split('~>')
        emission[em] = count/tag_counts[tag]
    
    for tr, count in transition.iteritems():
        prev_tag, tag = tr.split('~>')
        transition[tr] = count/tag_counts[prev_tag]
    
    test_for_prob_dist(em_counts)
    test_for_prob_dist(trans_counts)

def write_hmm_params(emission, transition, tag_counts):
    set_hmm_params(emission, transition, tag_counts)
    outfile = open('hmm.txt', 'w')
    for em, count in emission.iteritems():
        outfile.write('em:' + em + ' ' + str(emission[em]) + '\n')
    for tr, count in transition.iteritems():
        outfile.write('tr:' + tr + ' ' + str(transition[tr]) + '\n')
    outfile.close()    

    outfile2 = open('tagset.txt', 'w')
    for tag in tag_counts.iterkeys():
        outfile2.write(tag + '\n')
    outfile2.close()

'''
Writes the hmm probabilities in a format readable by my implementation of 
Liang Huang's algorithm
'''
def write_for_java(emission_counts, transition_counts):
    counts = open("pos.counts", "w")
    #emission_counts = smooth_emission(emission_counts)
    for em, count in emission_counts.iteritems():
        tag, terminal = em.split('~>')
        counts.write(str(count)+ " WORDTAG "+ tag+ " "+ terminal+ "\n")
    for trans, count in transition_counts.iteritems():
        prev_tag, current_tag = trans.split("~>")
        counts.write(str(count)+ " 2-GRAM "+ prev_tag+ " "+ current_tag+ "\n")
    counts.close() 

'''
Replaces all emissions with frequency <= 5 with the word
-RARE-
'''
def smooth_emission(emission_counts): 
    e_counts = defaultdict()
    for key, val in emission_counts.iteritems():
        if val <= 5:
            tag, word = key.split('~>') 
            new_key = tag + '~>-RARE-'
            if new_key in e_counts:
                e_counts[new_key] += val
            else:
                e_counts[new_key] = val
        else:
            e_counts[key] = val
    
    return e_counts


def learn(sentences, tagseqs):
    em_counts = defaultdict()
    trans_counts = defaultdict()
    tag_counts = defaultdict()

    for i in range(len(sentences)):
        sentence = sentences[i]
        tagseq = tagseqs[i]
        update_counts(sentence, tagseq, em_counts, trans_counts, tag_counts)
#   I'm not doing smoothing because smoothing gives very bad results
#   Every -RARE- word gets assigned to the FW tag, and then all following tags are FW. 
#   Because FW->-RARE- and FW->FW have high probabilities

#   em_counts = smooth_emission(emission_counts, tag_counts)
#   I don't like this! Why won't u work otherwise, Python?


#    write_hmm_params(em_counts, trans_counts, tag_counts)
    write_for_java(em_counts, trans_counts)
    return em_counts, trans_counts

if __name__ == "__main__":
    rare_sent_tags = sys.argv[1]
    sentences, tagseqs = data_reader.read_tagging_data(rare_sent_tags)
    emission, transition = learn(sentences, tagseqs)


