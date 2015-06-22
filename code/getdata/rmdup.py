#!/usr/local/bin/python
"""
remove duplicated line in report
"""

import re
import sys

def main():
    print sys.argv
    dupset=set()
    fr = open(sys.argv[1], 'r')
    fw = open(sys.argv[1] + '.nodup', 'w')
    i=0

    for line in fr:
        strs = re.split(r'\t', line)
        comstr = strs[0]+strs[1] + strs[3] + strs[6]
        if comstr in dupset:
            i = i+1
            print "dup line " + str(i)
            print comstr.decode('utf-8')
        else:
            dupset.add(comstr)
            fw.write(line)

if __name__ == "__main__":
    main()
