# ! /usr/bin/python

'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''
from rules import make_parse_list
from collections import defaultdict
import sys,re

global pos_counts, terminals, non_terminals, rule_counts

def read_sentences(file_name):
    treebank = open(file_name, 'r')
    num_sentences = 0
    sentences = []
    sentence = "dummy" #0th sentence
    while 1:
        line = treebank.readline()
        if not line:
            break
        if line.startswith('('): # new sentence
            line = line.strip()
            num_sentences += 1
            if sentence != "dummy":
                sentences.append(sentence) # previous sentence
            sentence = line
        else:
            sentence += line.strip()
    return sentences

def extract_pcfg(sentences):
    for sentence in sentences:
        s_stack = []
        elements = []
        for character in sentence:
             s_stack.append(character)
             if character == ')':
                 element = ''
                 popped = s_stack.pop()
                 while popped != '(':
                     element += popped
                     popped = s_stack.pop()
                 element += popped
                 elements.append(element[::-1])
        if (len(sentence) < 100):
            print sentence
            print elements, '\n'
        get_pos_tags(elements)

            
def extract_rules(elements):
    parent_stack = []
    child_map = defaultdict() # maps parent to a list of children
    for i in xrange(len(elements)):
        if elements[i] == '(':
            continue
        if elements[i] == ')':
            parent_stack.pop()
            continue
        if elements[i-1] == '(':
            if len(parent_stack) == 0:  # root node
                root = elements[i]
                parent_stack.append(root + '~' + str(i))
                child_map[root + '~' + str(i)] = []
            else:
                child_map[parent_stack[-1]].append(elements[i])
                if elements[i+1] != ')': # non terminal node
                    parent_stack.append(elements[i] + '~' + str(i))
                    child_map[elements[i] + '~' + str(i)] = []
        else:
            child_map[parent_stack[-1]].append(elements[i])
   
    for parent,children in child_map.iteritems():
        rule = parent[:parent.index('~')] + '~~'
        for child in children:
            rule += child + '~'
        rule = rule[:-1]
        if rule in rule_counts:
           rule_counts[rule] += 1
        else:
           rule_counts[rule] = 1
    return child_map       
    

def get_pos_tags(elements):
    for element in elements:
        x = re.match(r'\((\S*)(.*)\)', element) # matching all non-terminals
        if x:
           non_terminals.add(x.group(1))
        x = re.match(r'\((\S*) (\S+)\)', element) # matching all (pos_tag terminal) elements
        if x:
            terminals.add(x.group(2))
            key = x.group(2)+'~'+x.group(1)
            if key in pos_counts:
                new_count = pos_counts[key] + 1
                pos_counts[key] = new_count
            else:
                pos_counts[key] = 1

if __name__ == '__main__':
    pos_counts = defaultdict()
    terminals = set([])
    non_terminals = set([])
    rule_counts = defaultdict()

    treebank_file = sys.argv[1]
    sentences = read_sentences(treebank_file)
    for sentence in sentences:
        if len(sentence) < 100:
            print
            print sentence
            parse_list = make_parse_list(sentence)
            print parse_list
            rules = extract_rules(parse_list)
            print rules
            print rule_counts
            break
    #extract_pcfg(sentences[1:100])
