# ! /usr/bin/python

'''
Extract grammar from treebank
Created on Sep 21, 2013

@author: swabha
'''

import sys,re

def read(file_name):
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
            if (len(sentence) < 100):
                print sentence
            sentence = line
        else:
            sentence += line.strip()
    print num_sentences, len(sentences)

if __name__ == '__main__':
    treebank_file = sys.argv[1]
    read(treebank_file)
