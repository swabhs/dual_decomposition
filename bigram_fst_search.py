# /usr/bin/python

'''
Diverse FST search (based on bigram Hamming distance)
'''
import unigram_fst_search

def init(tagset, dd_u, best):
    pi1 = {}
    for tag in tagset:
        pi1[tag] = unigram_fst_search.get_local_score(tag, best, 0) + dd_u[0][tag]
    return pi1        

# given a seq and dual scores, gives the best sequence not equal to given sequence
def run(best, dd_u, tagset):
    pi = []
    pi.append(init(tagset, dd_u, best))
    bp = {}

    n = len(best)
#    for tag in tagset:
#        print tag,"\t",
#    print
    for i in range(1, n):
        pi_i = {}
        bp_i = {}
        for tag in tagset:
            max_sc = float("-inf")
            best_tag = ''
            for prev_tag in tagset:
                score = pi[i-1][prev_tag] + get_local_score(tag, prev_tag, best, i) + dd_u[i][tag]
                if score > max_sc:
                    max_sc = score
                    best_tag = prev_tag
            pi_i[tag] = max_sc #+ dd_u[i][tag]
            bp_i[tag] = best_tag
        pi.append(pi_i)
        bp[i] = bp_i
#        for w in tagset:
#            print "{0:.2f}".format(pi[i][w]) + "\t",
#        print

    # decoding
    tagseq = []
    max_sc = float("-inf")
    last_tag = ''
    for tag in tagset:
        if pi[n-1][tag] > max_sc:
            max_sc = pi[n-1][tag]
            last_tag = tag
    tagseq.append(last_tag)
    i = n-1
    while i > 0:
        tagseq.append(bp[i][tagseq[-1]])
        i -= 1
    
    tags = list(reversed(tagseq))
    #print ' '.join(tags)
    return tags, max_sc

# TODO: penalizes bigram, how about some penalty for unigram matching too??
def get_local_score(tag, prev_tag, best, pos):
    if tag == best[pos] and prev_tag == best[pos-1]:
        return -1.0
    else:
        return 1.0

