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


def write_hmm_params(emission, transition, tag_counts):

    outfile = open('hmm.txt', 'w')
    for em, count in emission.iteritems():
        tag, word = em.split('~>')
        emission[em] = count/tag_counts[tag]
        outfile.write('em:' + em + ' ' + str(emission[em]) + '\n')

    for tr, count in transition.iteritems():
        prev_tag, tag = tr.split('~>')
        transition[tr] = count/tag_counts[prev_tag]
        outfile.write('tr:' + tr + ' ' + str(transition[tr]) + '\n')
    
    outfile.close()    

    outfile2 = open('tagset.txt', 'w')
    for tag in tag_counts.iterkeys():
        outfile2.write(tag + '\n')
    outfile2.close()
    return emission, transition

def learn(parses):
    emission_counts = defaultdict()
    transition_counts = defaultdict()
    tag_counts = defaultdict()

    for parse in parses:
        parse_list = utils.make_parse_list(parse)
        update_counts(parse_list, emission_counts, transition_counts, tag_counts)
        #TODO smoothing of emission counts, transition_counts, tag_counts
         
    return write_hmm_params(emission_counts, transition_counts, tag_counts)

if __name__ == "__main__":
    treebank = sys.argv[1]
    parses = utils.read_parses_no_indent(treebank)
    emission, transition = learn(parses)

#===============================================================================
# def extract_pcfg(sentence):
#    s_stack = []
#    parse_list = []
#    for character in sentence:
#         s_stack.append(character)
#         if character == ')':
#             element = ''
#             popped = s_stack.pop()
#             while popped != '(':
#                 element += popped
#                 popped = s_stack.pop()
#             element += popped
#             parse_list.append(element[::-1])
#    get_pos_tags(parse_list)
#===============================================================================

#===============================================================================
# def get_pos_tags(parse_list):
#    for element in parse_list:
#        x = re.match(r'\((\S*)(.*)\)', element) # matching all non-terminals
#        if x:
#           non_terminals.add(x.group(1))
#        x = re.match(r'\((\S*) (\S+)\)', element) # matching all (pos_tag terminal) parse_list
#        if x:
#            terminals.add(x.group(2))
#            key = x.group(2)+'~'+x.group(1)
#            if key in pos_counts:
#                pos_counts[key] += 1
#            else:
#                pos_counts[key] = 1
#===============================================================================

