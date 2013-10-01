# ! /usr/bin/python
 
''' 
Utilities for reading and preprocessing treebank.
Assumes treebank has no traces.
Created on Sep 21, 2013 
 
@author: swabha 
''' 
from collections import defaultdict 
import sys,re 

'''
Given a treebank with parse trees incrementally indented per level,
returns a single line per parse, removing all indentation.
'''
def read_parses(file_name):
    treebank = open(file_name, 'r')
    num_parses = 0
    parses = []
    parse = "dummy" #0th parse
    while 1:
        line = treebank.readline()
        if not line:
            break
        if line.startswith('('): # new parse
            line = line.strip()
            num_parses += 1
            if parse != "dummy":
                parses.append(parse) # previous parse
            parse = line
        else:
            parse += line.strip()
    return parses

'''
Given a treebank with one parse tree per line, returns a list of parses
'''
def read_parses_no_indent(file_name):
    treebank = open(file_name, 'r')
    num_parses = 0
    parses = []
    while 1:
        line = treebank.readline()
        if not line:
            break
        line = line.strip()
        parses.append(line)
        num_parses += 1
    return parses

'''
Given a parse as a single line, returns the different elements of the parse,
namely, terminals, non-terminals and parantheses, as a list.
Inserts the root of a parse (**) into the list.
'''
def make_parse_list(parse): 
    parse_list = [] 
    element = "" 
    for character in parse: 
        if character == '(' or character ==')': 
            if len(element) != 0: 
                parse_list.append(element) 
                element = "" 
            parse_list.append(character) 
        elif character.isspace(): 
            if element != "": 
                parse_list.append(element) 
                element = "" 
            continue 
        else: 
            element += character 
 
    parse_list.insert(0, '**') # the start symbol for a pcfg 
    return parse_list

'''
Given the dev file, extracts sentences from it, as lists of tokens
'''
def get_sentences(dev_file):
    dev = open(dev_file, 'r')
    sentences = []
    while 1:
        line = dev.readline()
        if not line:
            break
        line = line.strip()
        parse = make_parse_list(line)
        sentence, tags = get_terminals_tags(parse)
        sentences.append(sentence)
    return sentences

'''
Given a parse list, extracts the sentence and postags from it
'''
def get_terminals_tags(parse):
    tags = []
    terminals = []
    for i in xrange(0, len(parse)):
        if parse[i] == ")" or parse[i] == "(":
            continue
        if parse[i-1] == "(" and parse[i+2] == ')':
            tags.append(parse[i])
            terminals.append(parse[i+1])

    return terminals, tags
