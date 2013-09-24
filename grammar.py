# ! /usr/bin/python

'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''
from collections import defaultdict
import sys,re

global pos_counts, terminals, non_terminals, rule_counts

def read_sentences(file_name):
    treebank = open(file_name, 'r')
    num_sentences = 0
    sentences = []
    sentence = []
    while 1:
        line = treebank.readline()
        if not line:
            break
        if line.startswith('('): # new sentence
            line = line.strip()
            num_sentences += 1
            sentences.append(sentence) # previous sentence
            #if (len(sentence) < 100):
                #print sentence
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
        get_pos_tags(elements)

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
            if key in rule_counts:
                new_count = rule_counts[key] + 1
                rule_counts[key] = new_count
            else:
                rule_counts[key] = 1


if __name__ == '__main__':
    pos_counts = defaultdict()
    terminals = set([])
    non_terminals = set([])
    rule_counts = defaultdict()

    treebank_file = sys.argv[1]
    sentences = read_sentences(treebank_file)
    extract_pcfg(sentences)
