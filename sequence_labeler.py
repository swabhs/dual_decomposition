# ! /usr/bin/python 
 
''' 
Extracts emission and transition probabilities for an HMM POS tagger
for a treebank.
Created on Sep 21, 2013 
 
@author: swabha 
''' 
from __future__ import division
import sys, utils
from collections import defaultdict

def update_counts(parse_list, emission_counts, transition_counts):
    tags = ['*']
    
    for i in xrange(len(parse_list)):
        if parse_list[i] == '(' or parse_list[i] == ')':
            continue
        if parse_list[i-1] == '(' and parse_list[i+2] == ')':
            # updating transition counts
            tag = parse_list[i]
            transition_key = tags[-1] + '~>' + tag
            if transition_key in transition_counts:
                transition_counts[transition_key] += 1
            else:
                transition_counts[transition_key] = 1
            
            # updating emission counts
            terminal = parse_list[i+1]
            emission_key = tag + '~>' + terminal
            if emission_key in emission_counts:
                emission_counts[emission_key] += 1
            else:
                emission_counts[emission_key] = 1
                
            tags.append(tag)
    final_key = tag + '~>STOP'
    if final_key in transition_counts:
       transition_counts[final_key] += 1
    else:
       transition_counts[final_key] = 1

def write_hmm_params(emission, transition):
    tag_counts = defaultdict()
    for tr, count in transition.iteritems():
        tag, new_tag = tr.split('~>')
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1
        if new_tag == 'STOP': # more hacks!!!!
            if 'STOP' in tag_counts:
                tag_counts['STOP'] += 1
            else:
                tag_counts['STOP'] = 1
    
    # super hacky, change!!!!
    em_tag_counts = defaultdict()
    for em, count in emission.iteritems():
        tag, word = em.split('~>')
        if tag in em_tag_counts:
           em_tag_counts[tag] += 1
        else:
           em_tag_counts[tag] = 1

    #update both tag counts
    for em_tag, count in em_tag_counts.iteritems():
        if em_tag not in tag_counts:
           tag_counts[em_tag] = count
        else:
           tag_counts[em_tag] = max(count, tag_counts[tag])

    outfile = open('hmm.txt', 'w')
    for em, count in emission.iteritems():
        tag, word = em.split('~>')
        emission[em] = count/tag_counts[tag]
        outfile.write(em + ' ' + str(emission[em]) + '\n')

    for tr, count in transition.iteritems():
        prev_tag, tag = tr.split('~>')
        transition[tr] = count/tag_counts[prev_tag]
        outfile.write(tr + ' ' + str(transition[tr]) + '\n')
    
    outfile.close()    
    return emission, transition

def learn(parse_lists):
    emission_counts = defaultdict()
    transition_counts = defaultdict()

    for parse_list in parse_lists:
        update_counts(parse_list, emission_counts, transition_counts)
        
    return write_hmm_params(emission_counts, transition_counts)

if __name__ == "__main__":
    treebank = sys.argv[1]
    parses = utils.read_parses_no_indent(treebank)
    parse_lists = []
    for parse in parses:
        parse_lists.append(utils.make_parse_list(parse))

    learn(parse_lists)
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

