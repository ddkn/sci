#!/usr/bin/env python3
#-
# Copyright (c) 2015, David Kalliecharan <david.kalliecharan@dal.ca>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# @file     asc2xy.py
#
# @author   David Kalliecharan <david.kalliecharan@dal.ca>
#
# @brief    This file parses the ASCII output of the Diffractometer 500 XRD + 
#           MDIScan software interface, and saves either a .xy or .txt file
#

from argparse import ArgumentParser

from re import findall
from numpy import array, savetxt

import os.path as path

def convert(ifile):
    asc = open(ifile, 'r')
    asc = asc.read()
    expr_line = '\ +[0-9]+\.[0-9]+\t\ +[0-9]+';
    data = findall(expr_line, asc)
    expr_values = '[0-9]+\.[0-9]+|[0-9]+';
    x = []
    y = []
    z = []
    for i in range(len(data)):
        a, b = findall(expr_values, data[i])
        x.append(float(a))
        y.append(int(b))
        z.append(1)
    xy = array([x, y, z]).transpose()
    
    return xy

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('FILE', type=str, 
                         help='Ascii file to be parsed to xy',)
    args = parser.parse_args()
    filename = args.FILE
    
    dirname = path.dirname(filename)
    basename = path.basename(filename)

    xy = convert(filename)
    
    ofile = path.join(dirname, basename[:-3] + "xy")
    print('Writing ', ofile)
    savetxt(ofile, xy, fmt='%.5e',
                      delimiter=' ', newline='\r\n')

    print("Finished.")
