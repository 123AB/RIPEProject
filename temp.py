# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:36:39 2019

@author: Brian
"""

#Write list of tuples to file
def write_result(result):
    with open('somefile.txt', 'w+') as f:
        for row in result:
            blah = True
            for item in row:
                if blah:
                    blah = False
                    continue
                f.write(str(item))
                f.write("\t")
            f.write("\n")

#Write dict of lists of numbers to file
def write_all_cc(result_dict):
    with open('somefile2.txt', 'w+') as f:
        for key in result_dict.keys():
            f.write(str(key))
            f.write("\t")
            for cc in result_dict[key]:
                f.write(str(cc))
                f.write("\t")
            f.write("\n")