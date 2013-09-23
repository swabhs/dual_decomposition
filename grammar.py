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
        units = []
        if line.startswith('('):
            line = line.strip()
            num_sentences += 1
            #if line.startswith('( (S') == False:
                #print line 4124824129
            sentences.append(sentence)
            sentence = []
        elements = ""
        for character in line:
            elements += character
            if character == ')':
               
            
    print num_sentences, len(sentences)
    print sentences[1000]

if __name__ == '__main__':
    treebank_file = sys.argv[1]
    read(treebank_file)
