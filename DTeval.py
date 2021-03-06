#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Check whether we are overwriting the input file. And if yes, do it 
# properly, i.e. first read it and only then overwrite it.

from __future__ import division

from sys import path as syspath
from os.path import dirname, abspath, basename

import argparse
from sympy import *

class Damage(object):
    def __init__(self, params, uncerts):
	self._params = params
	self._uncerts = uncerts
	self._parameters = dict(params.items() + uncerts.items())
	for key in self._parameters.keys() + 'U dU w'.split():
	    setattr(self, '_%s' % key, symbols(key))

    def powerf(self):
	""" 
	Given the calibration parameters a and b, calculates the power [W]
	from the voltage [V] measured by the photodiode.
	"""
	return self._a + self._b * self._U
    
    def beamsizef(self):
	return self._w / 2.
    
    def areaf(self):
	return pi * self.beamsizef()**2 / cos(self._theta / 360 * 2 * pi)
    
    def fluencef(self):
	return 2 * self.powerf() / (self.areaf() * self._f_rep * 10**4)

    def dfluencef(self):
	paramties = zip(sorted(self._params.keys() + ['U']),
		sorted(self._uncerts.keys() + ['dU']))
	derivs = [(self.fluencef().diff(S(param)) * S(uncert))**2
		for (param, uncert) in paramties]
	return sqrt(reduce(lambda x, y: x + y, derivs))

    def fluencefdU(self, i):
	return self.fluencef().diff(self._params.keys()[i])

    def power(self, U):
	return self.powerf().subs({
	    'a': self._params['a'],
	    'b': self._params['b'],
	    'U': U
	})

    def area(self):
	return self.areaf().subs(self._params)

    def fluence(self, U):
	if not hasattr(self, '_J'):
	    self._J = self.fluencef().subs(self._params)
	return self._J.subs({'U': U}).evalf()
    
    def dfluence(self, U, dU):
	if not hasattr(self, '_dJ'):
	    self._dJ = self.dfluencef().subs(self._parameters)
	return self._dJ.subs({'U': U, 'dU': dU}).evalf()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
	    description='Evaluates damage threshold data.',
	    epilog="""The input file must contain the following columns,
	    separated by whitespace:
	    <PD voltage> <SD voltage> <PD std.dev.> <SD std.dev.>""",
	    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('r'),
			help='input file')
    parser.add_argument('-o', dest='outfile', type=argparse.FileType('w'),
	    		default='-',
	    		help='write the resulting data to OUTFILE')
    parser.add_argument('-c', dest='config', type=str,
	    		default='parameters.py',
	    		help='read the setup parameters from CONFIG')
    parser.add_argument('-f', nargs='?', dest='figure', type=str,
	    		default=argparse.SUPPRESS, const='-',
	    		help='plot the data and write it in FIGURE. If\
			      FIGURE is ommited, show the plot in a window.')
    args = parser.parse_args()

    syspath.insert(0, dirname(abspath(args.config)))
    config = __import__(basename(args.config).split('.')[0],
	                fromlist=['params', 'uncerts'])

    lines = args.infile.read().splitlines()
    args.infile.close()

    # Convert the lines to a list of rows, each a list of float numbers
    rows = [map(float, line) for line in map(str.split, lines)]

    # At the moment doing nothing with the elapsed time
    powers, scatters, power_errs, scatter_errs, elapsed = zip(*rows)
    
    dt = Damage(config.params, config.uncerts)
    
    (fluences, errs) = (map(dt.fluence, powers), 
	    map(dt.dfluence, powers, power_errs))

    if hasattr(args, 'figure'):
	import matplotlib.pyplot as plot
	from numpy import arange
	
	# Setting the step for the xticks
	# plot.xticks(arange(0, 3.0, step=0.1))

	# Plot scatter signal vs fluence using red dash-dot with errorbars
	plot.errorbar(fluences, scatters, 
		     xerr=errs, yerr=scatter_errs, fmt='ro--')

	# Write the figure to args.figure if not empty
	# otherwise show it in a window
	if args.figure == '-':
	    plot.show()
	else:
	    plot.savefig(args.figure)

    for fluence, scatter, err, scatter_err in \
	    zip(fluences, scatters, errs, scatter_errs):
	args.outfile.write("%10.6f" * 4 % (fluence, scatter, err, scatter_err) + '\n')
    args.outfile.close()

