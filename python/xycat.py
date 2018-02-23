#!/usr/bin/env python3
#-
# Copyright (c) 2018, David Kalliecharan <dave@dal.ca>
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
# @file     xystitch.py
#
# @author   David Kalliecharan <dave@dal.ca>
#
# @brief    Takes two asc, or xy files generated from a Diffractometer XRD + 
#           MDIScan software interface, and concatenates them together
#           Outputs a *.xy file.
#

import asc2xy
from numpy import concatenate, empty, loadtxt, savetxt
import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from sys import exit


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    file_lst = []

    print('REMEMBER! Order matters!')
    while True:
        new_file = askopenfilename(title='Add a file to stitch?',
                                   filetypes=(("ASCII files","*.asc"),
                                              ("XY files","*.xy"),
                                              ("All files","*.*")))
        if new_file == '':
            break
        file_lst.append(new_file)
        print('>> adding', file_lst[-1])

    print('\nReview files')
    c = 'y'
    while str.lower(c) not in ['n', 'no']:
        for i, f in enumerate(file_lst):
            print('{})'.format(i), os.path.split(f)[1])
        if len(file_lst) == 0:
            print('No files in queue, exiting...')
            exit(0)

        c = input('Delete a file? [0-{}, or "no"]: '.format(len(file_lst)-1))
        if str.isnumeric(c):
            file_lst.pop(int(c))
            c = 'y'

    xy = empty((0, 3))
    for f in file_lst:
        if str.lower(os.path.splitext(f)[1]) == '.asc':
            data = asc2xy.convert(f)
        elif str.lower(os.path.splitext(f)[1]) == '.xy':
            data = loadtxt(f, unpack=True)
        xy = concatenate((xy, data))

    print('\nStitched output')
    print(xy)

    odir = askdirectory()
    ofile = input('Output file name? (no extension): ') + '.xy'
    ofilepath = os.path.join(odir, ofile)
    savetxt(ofilepath, xy, fmt='%.5e', delimiter=' ', newline='\r\n')
    print('saving', ofile)
