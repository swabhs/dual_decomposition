# ! /usr/bin/python


'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''
from collections import defaultdict
import sys,re
import utils, sequence_labeler

global pos_counts, terminals, non_terminals, rule_counts

def extract_cfg(elements):
    parent_stack = ['**']
    child_map = defaultdict() # maps parent to a list of children
    child_map['**'] = []
    for i in xrange(len(elements)):

        if elements[i] == '(':
            continue

        if elements[i] == ')':
            parent_stack.pop()
            continue

        if elements[i-1] == '(':# non-terminal node
            non_terminals.add(elements[i])
            child_map[parent_stack[-1]].append(elements[i] + '~'+ str(i))
            parent_stack.append(elements[i] + '~' + str(i))
            child_map[elements[i] + '~' + str(i)] = []
        
        if elements[i+1] == ')': # terminal node
            terminals.add(elements[i])
            child_map[parent_stack[-1]].append(elements[i]+ '~' + str(i))

#    for parent,children in child_map.iteritems():
#        rule = parent[:parent.index('~')] + '~~'
#        for child in children:
#            rule += child + '~'
#        rule = rule[:-1]
#        if rule in rule_counts:
#           rule_counts[rule] += 1
#        else:
#           rule_counts[rule] = 1
#
    return child_map

def ununarize(root,tree, unaries):
    if root not in tree:
        return
    for child in tree[root]:
        if child in tree and len(tree[child]) == 1:
            grandchild = tree[child][0]
            
            if grandchild in tree:
               unaries.append(root + '\t' + child + '\t' + grandchild)
               #print "removing", child, "~~>", grandchild
               #tree[root].append(grandchild)
               #tree[root].remove(child)
               
               #ununarize(grandchild, tree, unaries)
               #tree.pop(child) 
        ununarize(child, tree, unaries)

if __name__ == '__main__':
    emission_counts = defaultdict()
    transition_counts = defaultdict()
    
    terminals = set([])
    non_terminals = set([])
    rule_counts = defaultdict()

    treebank_file = sys.argv[1]
    parses = utils.read_parses_no_indent(treebank_file)
    for parse in parses:
        #print parse, '\n'
        parse_list = utils.make_parse_list(parse)
        #print parse_list
        tree = extract_cfg(parse_list)
        #print tree
        unaries = []
        ununarize('**', tree, unaries)
        for unary in unaries[::-1]:
            #print unary
            elements = unary.split('\t')
            root = elements[0]
            child = elements[1]
            grandchild = elements[2]
            tree[root].append(grandchild)
            tree[root].remove(child)
            tree.pop(child)
        #print tree, '\n'
        sequence_labeler.update_counts(parse_list, emission_counts, transition_counts)
#        if len(parse) < 100:
#            print
#            print terminals
#            print
#            print non_terminals, '\n'
#            print rule_counts
#            print
#            print emission_counts
#            print
#            print transition_counts
#            print
#            break
#
        
