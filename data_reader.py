# ! /usr/bin/python

'''
Utilities for reading and preprocessing treebank.
Assumes treebank has no traces.
Created on Sep 21, 2013

@author: swabha
'''
from collections import defaultdict
import sys,re, utils

'''
Given a file containing sentences and tag_sequences in consecutive lines,
returns two lists of lists.
First list contains the sentences, with each sentence as a list of words.
Second list contains the tag_sequences, with each tag_sequence as a list of tags.
'''
def read_tagging_data(stfilename):
    sentences = []
    tag_sequences = []
    st = open(stfilename, 'r')
    while 1:
        line = st.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
	    continue

	words = line.split()
	sentences.append(words)

	line = st.readline().strip()
	tags = line.split()
	tag_sequences.append(tags)

    st.close()
    return sentences, tag_sequences
	
'''
Writes sentences and pos tags from a treebank into a file with
sentences and their respective tag sequences in consecutive lines,
and to another file with a word and its tag on a single line.
A one-time utility.
'''
def write_tagging_data(sentences, tag_sequences, stfilename, wtfilename):
    stfile = open(stfilename, 'w')
    wtfile = open(wtfilename, 'w')
    j = 0
    for sentence in sentences:
        truetag = tag_sequences[j]
        sent = ''
        tags = ''
        for i in range(len(sentence)):
            wtfile.write(sentence[i] + '\t' + truetag[i] + '\n')
            sent += sentence[i] + ' '
            tags += truetag[i] + ' '
        wtfile.write('\n')

        stfile.write(sent + '\n')
        stfile.write(tags + '\n\n')
        j += 1

    stfile.close()
    wtfile.close()

'''
Given a treebank, extracts the sentences and their pos tag sequences
'''
def extract_tagging_data(treebank, st_filename, wt_filename):
    sentences = []
    tagseqs = []

    parses = read_parses_no_indent(treebank)
    for parse in parses:
        parse_list = utils.make_parse_list(parse)
        sentence, truetag = utils.get_terminals_tags(parse_list)
        sentences.append(sentence)
        tagseqs.append(truetag)

    write_tagging_data(sentences, tagseqs, st_filename, wt_filename)
    return sentences, tagseqs

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
        parse = utils.make_parse_list(line)
        sentence, tags = utils.get_terminals_tags(parse)
        sentences.append(sentence)
    return sentences

'''
Given a word_tag file, makes a sentences file
'''

def get_sentences_new(wtfilename):
    wtfile = open(wtfilename, 'r')
    sentences = []
    tagseqs = []
    sentence = []
    tagseq = []
    while 1:
       line = wtfile.readline()
       if not line:
           break
       line = line.strip()
       if line == '':
           sentences.append(sentence)
           tagseqs.append(tagseq)
           sentence = []
           tagseq = [] 
           continue
       word, tag = line.split(' ')
       sentence.append(word)
       tagseq.append(tag)
       
    wtfile.close()
    return sentences, tagseqs

if __name__ == "__main__":
    sentences, tagseqs = get_sentences_new(sys.argv[1])
    stfilename = "new_dev.sentences_tags"
    wtfilename = "new_dev.word_tag"
    write_tagging_data(sentences, tagseqs, stfilename, wtfilename)
    #dataset = sys.argv[1]
    #datasetname = sys.argv[2]
    # to convert treebank into tagging data
    # treebank is at /mal2/corpora/penn_tb_3.0_preprocessed/train.1.notraces
    #extract_tagging_data(dataset, datasetname+".sentences_tags", datasetname+".word_tag")
