# /usr/bin/python
from collections import defaultdict
import data_reader, sys, hmm_utils

'''
Given train data file in word tag format, replaces first occurence of each word with _RARE_
'''
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

'''
Given test sentences, replace out of vocabulary words with _RARE_
'''
def replace_test(sentences, hmm, tagset):
    replaced_sentences = []
    for sentence in sentences:
        sent_with_rare = []
        position = 0
        for word in sentence:
            sent_with_rare.append(word)
            seen = False
            for tag in tagset:
                key = 'em:' + tag + '~>' + word
                if key in hmm:
                    seen = True
                    break
            if seen == False:
                sent_with_rare[position] = "_RARE_"
            position += 1
        replaced_sentences.append(sent_with_rare)
    return replaced_sentences

'''
Replaces all emissions with frequency <= 5 with the word
-RARE-
'''
def smooth_emission(emission_counts):
    e_counts = defaultdict()
    for key, val in emission_counts.iteritems():
        if val <= 5:
            tag, word = key.split('~>')
            new_key = tag + '~>-RARE-'
            if new_key in e_counts:
                e_counts[new_key] += val
            else:
                e_counts[new_key] = val
        else:
            e_counts[key] = val

    return e_counts

if __name__=='__main__':
    #replace(sys.argv[1])
    test_sent_tags = sys.argv[1]
    hmm, tagset = hmm_utils.get_param_tagset(sys.argv[2], sys.argv[3])
    ts, test_tags = data_reader.read_tagging_data(test_sent_tags)
    test_sentences = replace_test(ts, hmm, tagset)

    for ts in test_sentences:
        for word in ts:
            print word
        print 

