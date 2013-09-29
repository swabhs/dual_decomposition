# ! /usr/bin/python 
 
''' 
Extracts emission and transition probabilities for an HMM POS tagger
for a treebank.
Created on Sep 21, 2013 
 
@author: swabha 
''' 
from collections import defaultdict

def update_counts(elements, emission_counts, transition_counts):
    tags = ['*']
    
    for i in xrange(len(elements)):
        if elements[i] == '(' or elements[i] == ')':
            continue
        if elements[i-1] == '(' and elements[i+2] == ')':
            # updating transition counts
            tag = elements[i]
            transition_key = tags[-1] + '~>' + tag
            if transition_key in transition_counts:
                transition_counts[transition_key] += 1
            else:
                transition_counts[transition_key] = 1
            
            # updating emission counts
            terminal = elements[i+1]
            emission_key = tag + '~>' + terminal
            if emission_key in emission_counts:
                emission_counts[emission_key] += 1
            else:
                emission_counts[emission_key] = 1
                
            tags.append(tag)

#===============================================================================
# def extract_pcfg(sentence):
#    s_stack = []
#    elements = []
#    for character in sentence:
#         s_stack.append(character)
#         if character == ')':
#             element = ''
#             popped = s_stack.pop()
#             while popped != '(':
#                 element += popped
#                 popped = s_stack.pop()
#             element += popped
#             elements.append(element[::-1])
#    get_pos_tags(elements)
#===============================================================================

#===============================================================================
# def get_pos_tags(elements):
#    for element in elements:
#        x = re.match(r'\((\S*)(.*)\)', element) # matching all non-terminals
#        if x:
#           non_terminals.add(x.group(1))
#        x = re.match(r'\((\S*) (\S+)\)', element) # matching all (pos_tag terminal) elements
#        if x:
#            terminals.add(x.group(2))
#            key = x.group(2)+'~'+x.group(1)
#            if key in pos_counts:
#                pos_counts[key] += 1
#            else:
#                pos_counts[key] = 1
#===============================================================================

