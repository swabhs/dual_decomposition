from __future__ import division
import sys

def calc(file_name):
    avg_acc = 0
    num = 0
    f = open(file_name, 'r')
    while 1:
       line = f.readline()
       if not line:
           break
       line = line.strip()
       ele = line.split(' ')
       if len(ele) > 4:
           if ele[-5] == ':tagger2,':
               num += 1
               avg_acc += float(ele[-1])
    print avg_acc/num


if __name__ == '__main__':
    calc(sys.argv[1])
