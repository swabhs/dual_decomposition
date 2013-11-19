# /usr/bin/python
from collections import defaultdict
import data_reader, sys

def replace(wt_filename):
    seenonce = []
    wt = open(wt_filename, "r")
    sentences = []
    tag_sequences = []
    sentence = []
    tags = []
    while 1:
        line = wt.readline()
        if not line:
            break
        line = line.strip()
        if line == '':
            sentences.append(sentence)
            tag_sequences.append(tags)
            sentence = []
            tags = []
            continue
        word, tag = line.split("\t")
        tags.append(tag)
        if word not in seenonce:
            seenonce.append(word)
            sentence.append("_RARE_")
        else:
            sentence.append(word)
    wt.close()
    data_reader.write_tagging_data(sentences, tag_sequences, 'rare_train.sentences_tags', 'rare_train.word_tag')

if __name__=='__main__':
    replace(sys.argv[1])
