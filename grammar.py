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


def extract_cfg(elements, terminals, non_terminals, start):

    parent_stack = [start]
    child_map = defaultdict() # maps parent to a list of children
    child_map[start] = []
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

    return child_map, terminals, non_terminals

def ununarize(root,tree, unaries):
    if root not in tree:
        return
    for child in tree[root]:
        if child in tree and len(tree[child]) == 1:
            grandchild = tree[child][0]
            if grandchild in tree:
               unaries.append(root + '\t' + child + '\t' + grandchild)
        ununarize(child, tree, unaries)

def cnf(tree, start, nonterms):
    # remove unary rules
    unaries = []
    ununarize(start, tree, unaries)
    for unary in unaries[::-1]:
        root, child, grandchild = unary.split('\t')
        tree[root].append(grandchild)
        tree[root].remove(child)
        tree.pop(child)

    # remove 3rd and higher fertility rules
    bin_tree = {}
    for parent, children in tree.iteritems():
        if len(children) > 2:
            c_list = children
            old_parent = parent
            while (len(c_list) > 2):
                bin_tree[old_parent] = [c_list[0]]
                prefix, suffix = c_list[1].split('~')
                new_parent = prefix + '\'~' + suffix
                nonterms.add(prefix + '\'') # I'm not happy with this
                bin_tree[old_parent].append(new_parent)
                bin_tree[new_parent] = [c_list[1]]
                c_list = c_list[1:]
                old_parent = new_parent 
            bin_tree[old_parent] = c_list               
        else:
            bin_tree[parent] = children
    return bin_tree    

def update_counts(bin_tree, start, rule_counts, parent_counts):
    for parent,children in bin_tree.iteritems():
        if parent == start: # hack, better solution?
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
    return rule_counts, parent_counts

def write_pcfg_probabilities(rule_counts, parent_counts):
    pcfg_prob = defaultdict()
    outfile = open('pcfg.txt', 'w')
    for key, val in rule_counts.iteritems():
        parent, children = key.split('~~')
        pcfg_prob[key] = val/parent_counts[parent]
        outfile.write(key + ' ' + str(pcfg_prob[key]) + '\n')
    outfile.close()
    return pcfg_prob

def write_terms_nonterms(terms, non_terms, start):
    outfile = open('terminals.txt', 'w')
    for term in terms:
        outfile.write(term + '\n')
    outfile.close()
    outfile2 = open('nonterminals.txt', 'w')
    outfile2.write(start + '\n')
    for nonterm in non_terms:
        outfile2.write(nonterm + '\n')
    outfile2.close()

def learn(parse_lists):
    rule_counts = defaultdict()
    parent_counts = defaultdict()

    terms = set([])
    nonterms = set([])
    start = '**'

    for parse_list in parse_lists:
        if parse_lists.index(parse_list)% 1000 == 0:
           print parse_lists.index(parse_list), '...'

        tree, terms, nonterms = extract_cfg(parse_list, terms, nonterms, start)
        cnf_tree = cnf(tree, start, nonterms)
        rule_counts, parent_counts = update_counts(cnf_tree, start, rule_counts, parent_counts) # python globals???
    
    prob = write_pcfg_probabilities(rule_counts, parent_counts)
    write_terms_nonterms(terms, nonterms, start)
    #sequence_labeler.update_counts(parse_list, emission_counts, transition_counts)
        
    return nonterms, terms, start, prob

if __name__ == "__main__":
    treebank = sys.argv[1]
    
    print "reading treebank..."
    parses = utils.read_parses_no_indent(treebank)
    parse_lists = []
    for parse in parses:
        parse_lists.append(utils.make_parse_list(parse))

    print "learning pcfg..."
    nonterms, terms, start, prob = learn(parse_lists)

