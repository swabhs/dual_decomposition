# ! /usr/bin/python

'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''
from collections import defaultdict
import sys,re

def make_parse_list(sentence):
    parse_list = []
    element = ""
    for character in sentence:
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

    parse_list.insert(1, '**') # the start symbol for a pcfg
    return parse_list
