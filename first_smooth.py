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

def replace_test(sentences, hmm, tagset):
    new_sen = []
    for sentence in sentences:
        new_s = []
        position = 0
        for word in sentence:
            new_s.append(word)
            seen = False
            for tag in tagset:
                key = 'em:' + tag + '~>' + word
                if key in hmm:
                    seen = True
                    break
            if seen == False:
                new_s[position] = "_RARE_"
            position += 1
        new_sen.append(new_s)
    return new_sen

if __name__=='__main__':
    replace(sys.argv[1])
    #hmm={'em:A~>apple': 0.0, 'em:A~>elephant':0, 'em:B~>boy':0}
    #sentences = [['apple'], ['apple', 'boy'], ['cat', 'dog'], ['cat', 'boy']]
    #tagset=['A','B']
    #print replace_test(sentences, hmm, tagset)
    #sentences
