# /usr/bin/python

import sys, operator
from hmm_utils import get_param_tagset
from smoothing import replace_test
'''
Given the tagset, emmission and transition probabilites, finds the log prob
of a tagseq for a sentence.
Note: sentence must have _RARE_ word replacement
'''
num = 0

def find_log_prob(hmm, tagset, sentence, tagseq):
    trans = "tr:*~>" + tagseq[0]
    if trans in hmm:
        score = hmm[trans]
    else:
        return ""
    for i in range(len(sentence)):
        emi = "em:" + tagseq[i] + "~>" + sentence[i]
        if emi in hmm:
            score += hmm[emi]
        else:
            return "" #float("-inf")
        
        if i == 0:
            continue 
        trans = "tr:" + tagseq[i-1] + "~>" + tagseq[i]
        if trans in hmm:
            score += hmm[trans]
        else:
            return "" #float("-inf")
    
    trans = "tr:" + tagseq[-1] + "~>STOP"
    if trans in hmm:
	score += hmm[trans]
    else:
	return "" #float("-inf")
    
    return score

'''
Recursive procedure to find all tag sequence permutations for
a string of length n
'''
def find_all_tagseqs(n, tagmap, prefix, tagseqs):
    global num
    if n == 0:
        return tagseqs
    if n == 1:
        string = ""
        for tag in tagmap[n]:
            tagseqs.append(prefix + " " + tag)
            #string += prefix + " " + tag + "\n"
            num += 1
            sys.stderr.write(str(num)+ "\r")
        return tagseqs
    
    for tag in tagmap[n]:
        tagseqs = find_all_tagseqs(n-1, tagmap, prefix+" "+tag, tagseqs)
    return tagseqs

def filter_tagset(sent_with_rare, tagset, hmm):
    tagmap = {}
    pos = len(sent_with_rare)
    size = 1
    for word in sent_with_rare:
        taglist = []
        for tag in tagset:
            emi = "em:" + tag + "~>" + word
            if emi in hmm:
                taglist.append(tag)
        tagmap[pos] = taglist
        size *= len(taglist)
        pos -=1 
    sys.stderr.write("total: " + str(pow(len(tagset), len(sent_with_rare))) + "\n" + str(size)+ "\n")
    return tagmap

def main():
    hmm_file = sys.argv[1]
    tag_file = sys.argv[2]
    hmm, tagset = get_param_tagset(hmm_file, tag_file)

    sentence = "The new three-year contracts , which replace ones that expired Aug. 5 , cover 41,000 Bell Atlantic employees .".split()
    #sentence = "By lunchtime , the selling was at near-panic fever .".split(' ')
    sentence = replace_test([sentence], hmm, tagset)[0]
    tagmap = filter_tagset(sentence, tagset, hmm)
    #tagseq = "IN NN , DT NN VBD IN JJ NN .".split(' ')
    tagseqs = find_all_tagseqs(len(sentence), tagmap, "", [])

#    resultmap = {}
#    f = open("tagseqs10.out", 'r')
#    i = 0
#    while 1:
#       line = f.readline()
#       if not line:
#           break
#       i += 1
#       sys.stderr.write(str(i)+"\r")
#       tagseq = line.strip().split(' ')
#       score = find_log_prob(hmm, tagset, sentence, tagseq)
#       if score != '':
#           key = ' '.join(tagseq)
#           resultmap[key] = score
#    f.close()
#
    resultmap = {}
    for tagline in tagseqs:
        tagseq = tagline.strip().split(' ')
        score = find_log_prob(hmm, tagset, sentence, tagseq)
        if score != '':
            key = ' '.join(tagseq)
            resultmap[key] = score
    sorted_x = sorted(resultmap.iteritems(), key=operator.itemgetter(1))
    for k, v in sorted_x:
        print k,v
  

if __name__ == "__main__":
    main()
