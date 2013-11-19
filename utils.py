# ! /usr/bin/python
 
''' 
Utilities for various functions to help read the treebank in its native form.
 
@author: swabha 
''' 
from collections import defaultdict 
import sys,re 

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

