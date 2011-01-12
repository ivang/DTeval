#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
from os.path import basename

from sympy.utilities.iterables import flatten

if __name__ == '__main__':

    if len(argv) < 2:
	print "Usage", basename(argv[0]), "<file1> [file2 [...]]"
	exit(1)

    files = []
    for filename in argv[1:]:
	with open(filename, 'r') as fd:
	    files.append(map(str.split, fd.readlines()))

    lines = map(flatten, zip(*files))

    float_lines = [map(float, line) for line in lines]
    for line in float_lines:
	print "%10.6f" * len(line) % tuple(line)

