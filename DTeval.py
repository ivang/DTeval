#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from sys import argv, exit
from os.path import basename

from sympy import *

from parameters import params, uncerts

class Damage(object):
    def __init__(self, params, uncerts):
	self._params = params
	self._uncerts = uncerts
	self._parameters = dict(params.items() + uncerts.items())
	variables = 'U dU w z zR'.split()

	for key in self._params.keys() + self._uncerts.keys() + variables:
	    eval(compile(
		'self._%s = symbols("%s", each_char=False)' % (key, key),
		'<string>', 'single'
	    ))

    def powerf(self):
	""" 
	Given the calibration parameters a and b, calculates the power [W]
	from the voltage [V] measured by the photodiode.
	"""
	return self._a * 10**(-3) + self._b * self._U
    
    def beamsizef(self):
	return self._w * sqrt(1 / (2 * log(2))) * \
		sqrt(1 + self._z**2 / self._zR**2)
    
    def axisf(self, plane):
	return self.beamsizef().subs({
	    'w': 'w_' + plane,
	    'z': 'z_' + plane,
	    'zR': 'zR_' + plane,
	})

    def areaf(self):
	return pi * self.axisf('x') * self.axisf('y') / \
		cos(self._theta / 360 * 2 * pi)
    
    def fluencef(self):
	return 2 * self.powerf() / (self.areaf() * self._f_rep * 10**4)

    def dfluencef(self):
	paramties = zip(sorted(self._params.keys() + ['U']), \
	    sorted(self._uncerts.keys() + ['dU']))
	derivs = [(self.fluencef().diff(S(param)) * S(uncert))**2 \
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
	if '_J' not in dir(self):
	    self._J = self.fluencef().subs(self._params)
	return self._J.subs({'U': U}).evalf()
    
    def dfluence(self, U, dU):
	if '_dJ' not in dir(self):
	    self._dJ = self.dfluencef().subs(self._parameters)
	return self._dJ.subs({'U': U, 'dU': dU}).evalf()


if __name__ == '__main__':

    if len(argv) < 3:
	print "Usage", basename(argv[0]), "<power_file> <error_file>"
	exit(1)	

    _, power_file, error_file = argv
    
    dt = Damage(params, uncerts)
    
    with open(power_file, 'r') as fd:
	powers = fd.readlines()

    with open(error_file, 'r') as fd:
	sigmas = fd.readlines()
    
    fluences, errors = map(dt.fluence, powers), map(dt.dfluence, powers, sigmas)

    for fluence, error in zip(fluences, errors): 
	print "%.6f %.6f" % (fluence, error)

