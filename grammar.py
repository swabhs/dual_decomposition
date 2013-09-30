# ! /usr/bin/python

'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''
from __future__ import division
from collections import defaultdict
import sys,re
import utils, sequence_labeler

global pos_counts, terminals, non_terminals, rule_counts, parent_counts
global pcfg_prob

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

    return child_map

def ununarize(root,tree, unaries):
    if root not in tree:
        return
    for child in tree[root]:
        if child in tree and len(tree[child]) == 1:
            grandchild = tree[child][0]
            if grandchild in tree:
               unaries.append(root + '\t' + child + '\t' + grandchild)
        ununarize(child, tree, unaries)

def cnf(tree):
    unaries = []
    ununarize('**', tree, unaries)
    for unary in unaries[::-1]:
        root, child, grandchild = unary.split('\t')
        tree[root].append(grandchild)
        tree[root].remove(child)
        tree.pop(child)
    #print tree
    #print
    bin_tree = {}
    for parent, children in tree.iteritems():
        if len(children) > 2:
            c_list = children
            old_parent = parent
            while (len(c_list) > 2):
                bin_tree[old_parent] = [c_list[0]]
                prefix, suffix = c_list[1].split('~')
                new_parent = prefix + '\'~' + suffix
                bin_tree[old_parent].append(new_parent)
                bin_tree[new_parent] = [c_list[1]]
                c_list = c_list[1:]
                old_parent = new_parent 
            bin_tree[old_parent] = c_list               
        else:
            bin_tree[parent] = children
    #print bin_tree
    return bin_tree    

def update_counts(bin_tree):
    for parent,children in bin_tree.iteritems():
        if parent == '**':
            parent_name = parent
        else:
            parent_name = parent[:parent.index('~')]
        if parent_name in parent_counts:
            parent_counts[parent_name] += 1
        else:
            parent_counts[parent_name] = 1
        
        rule = parent_name + '~~'
        for child in children:
            child_name = child[:child.index('~')]
            rule += child_name + '~'
        rule = rule[:-1] # to remove the last ~
        
        if rule in rule_counts:
            rule_counts[rule] += 1
        else:
            rule_counts[rule] = 1

def set_pcfg_probabilities(rule_counts, parent_counts):
    #outfile = open('pcfg.txt', 'w')
    for key, val in rule_counts.iteritems():
        parent, children = key.split('~~')
        pcfg_prob[key] = val/parent_counts[parent]
        #outfile.write(key + ' ' + str(pcfg_prob[key]) + '\n')
    #outfile.close()

if __name__ == '__main__':
    emission_counts = defaultdict()
    transition_counts = defaultdict()
    
    terminals = set([])
    non_terminals = set([])
    rule_counts = defaultdict()
    parent_counts = defaultdict()
    pcfg_prob = defaultdict()

    treebank_file = sys.argv[1]
    parses = utils.read_parses_no_indent(treebank_file)
    for parse in parses:
        if parses.index(parse)% 1000 == 0:
           print parses.index(parse), '...'
        #print parse, '\n'
        parse_list = utils.make_parse_list(parse)
        #print parse_list
        tree = extract_cfg(parse_list)
        cnf_tree = cnf(tree)
        update_counts(cnf_tree)
        set_pcfg_probabilities(rule_counts, parent_counts)
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
        
