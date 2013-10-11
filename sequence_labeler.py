# ! /usr/bin/python 
 
''' 
Extracts emission and transition probabilities for an HMM POS tagger
for a treebank.
Created on Sep 21, 2013 
 
@author: swabha 
''' 
from __future__ import division
import sys, utils, operator
from collections import defaultdict

def update_counts(parse_list, emission_counts, transition_counts, tag_counts):
    terminals, tags = utils.get_terminals_tags(parse_list)

    # updating emission counts
    for i in xrange(0,len(terminals)):
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

def set_hmm_params(emission, transition, tag_counts):
    for em, count in emission.iteritems():
        tag, word = em.split('~>')
        emission[em] = count/tag_counts[tag]
    
    for tr, count in transition.iteritems():
        prev_tag, tag = tr.split('~>')
        transition[tr] = count/tag_counts[prev_tag]

def write_hmm_params(emission, transition, tag_counts):
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
Replaces all emissions with frequency <= 5 with the word
-RARE-
'''
def smooth_emission(emission_counts, tags):
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
    for tag in tags:
        key = tag + '~>-RARE-'
        if key not in e_counts:
            e_counts[key] = 1
    return e_counts

def learn(parses):
    emission_counts = defaultdict()
    transition_counts = defaultdict()
    tag_counts = defaultdict()

    for parse in parses:
        parse_list = utils.make_parse_list(parse)
        update_counts(parse_list, emission_counts, transition_counts, tag_counts)
    
#    emission_counts = smooth_emission(emission_counts, tag_counts.keys()) # I don't like this! Why won't u work otherwise, Python?
    set_hmm_params(emission_counts, transition_counts, tag_counts)
    write_hmm_params(emission_counts, transition_counts, tag_counts)
    return emission_counts, transition_counts

if __name__ == "__main__":
    treebank = sys.argv[1]
    parses = utils.read_parses_no_indent(treebank)
    emission, transition = learn(parses)


