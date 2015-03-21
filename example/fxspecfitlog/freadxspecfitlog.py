#!/usr/bin/env python

import os 
import sys 
import yaml
import commands

DEBUG = False 

class XspecFitLog():
	def __init__(self, fitLog):
		self.fitLog = fitLog
		if not os.path.exists(self.fitLog):
			if DEBUG: print "file does not exits: %s" % self.fitLog
			quit()

	def getParameter(self, parameterNumber, norm=1.0):
		cmd = 'grep "#%4d" %s' % (int(parameterNumber),self.fitLog)
		output = commands.getoutput(cmd)
		if output.split()[7] == 'frozen':
			parameter = "%s(fix)" % output.split()[6]			
		elif output.split()[7] == '=':
			parameter = "=param%s(fix)" % output.split()[8]			
		else:
			try:
				parameter =	float(output.split("+/-")[0].split()[-1]) / norm 
			except:
				if DEBUG: sys.stderr.write('error: getting parameter %d.\n' % parameterNumber)
				parameter = None
		return parameter

	def getParameterErrorPlus(self, parameterNumber, norm=1.0):
		cmd = 'grep "#%6d" %s ' % (int(parameterNumber), self.fitLog)
		output = commands.getoutput(cmd)
		try:
			error = float(output.split()[4].split(',')[1].replace(')','')) / norm
		except:
			if DEBUG: sys.stderr.write('error: getting parameter error %d.\n' % parameterNumber)			
			error = None
		return error 

	def getParameterErrorMinus(self, parameterNumber, norm=1.0):
		cmd = 'grep "#%6d" %s ' % (int(parameterNumber), self.fitLog)		
		output = commands.getoutput(cmd)
		try:
			error = float(output.split()[4].split(',')[0].replace('(','')) / norm
		except:
			if DEBUG: sys.stderr.write('error: getting parameter error %d.\n' % parameterNumber)			
			error = None
		return error 

	def showParameter(self, parameterNumber, caption, datatype):
		if datatype == "I (10^-5 ph/s/cm2)":
			norm = 1e-5 
		elif datatype == "E (eV)":
			norm = 1e-3
		elif datatype == "Wid (eV)":
			norm = 1e-3			
		else:
			norm = 1.0
		value     = log.getParameter(parameterNumber,norm=norm)
		err_minus = log.getParameterErrorMinus(parameterNumber,norm=norm)
		err_plus  = log.getParameterErrorPlus(parameterNumber,norm=norm) 
		print "%s [% 3d] : " % (caption, parameterNumber), value, err_minus, err_plus

if len(sys.argv) != 3:
	sys.stderr.write('> %s param.yaml fit.log\n' % sys.argv[0]) 
	quit()
param_yaml    = sys.argv[1]	
fit_log       = sys.argv[2]	
sys.stdout.write('parameter yaml (param_yaml): %s\n' % param_yaml)
sys.stdout.write('fit log: %s\n' % fit_log)

log = XspecFitLog(fit_log)
param = yaml.load(open(param_yaml))
for compNumber in param:
	title = param[compNumber]["title"]
	for value in param[compNumber]:
		if value ==  'title':
			continue
		parameterNumber = param[compNumber][value]
		#print parameterNumber
		caption = '%-20s %-20s' % (title, value)
		log.showParameter(parameterNumber,caption,value)



