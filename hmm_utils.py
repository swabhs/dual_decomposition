# usr/bin/python
'''
Read data for HMM
Data is in a single file
Format:
For transition parameters: tr:prev_tag~>current_tag prob
For emission parameters:   em:tag~>word prob
'''

from __future__ import division
from collections import defaultdict
import math

'''
Returns transition and emission parameters in a single dictionary
and a list of tags in the data
The parameters are log prob parameters
'''
def get_param_tagset(hmm_file_name, tag_file_name):
    hmm = defaultdict()

    hmm_file = open(hmm_file_name, "r")
    while 1:
        line = hmm_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            param, prob = line.split(' ')
            hmm[param] = math.log(float(prob))
#            if param.startswith('em'):
#                tag, word = param[3:].split('~>')
#                tagset.add(tag)
#            else:
#                prev, current = param[3:].split('~>')
#                tagset.add(current)
#                tagset.add(prev)
#
    return hmm, list(get_tagset(tag_file_name))

def get_tagset(tag_file_name):
    tagset = set([])
    tag_file = open(tag_file_name, "r")
    while 1:
        line = tag_file.readline()
        if not line:
            break
        else:
            line = line.strip()
            tagset.add(line)

    return tagset
