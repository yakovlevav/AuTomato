import matplotlib.pyplot as plt #For plotting
from scipy import interpolate #Interpolation and fit
from scipy.optimize import curve_fit #Curve fit
import settings as st
import datacollector as dc
import numpy as np
from datetime import datetime, timedelta
import tools, os

def findkeys(dictionary, name = 'Current'):
	"""
	Function keys starting from "name" and replace
	one key for separate keys
	and 
	"""
	finkeys = []
	for key in dictionary:
		t = key.find(name)
		if t >= 0: finkeys.append(key)
	finkeys.sort()
	return(finkeys)

def PlotOxygen(pathname, ShowTime = True):
	# def func(t, c0, c1, c2, c3):
	# 	return c0 + c1*t - c2*np.exp(-c3*t)
	def func(x, a, b, c):
	    return a*x**2+b*x+c
		# return d+(a-d)/(1+(x/c)**b)

	#Curve fitting
	def fit(x, y):
		xnew = np.linspace(min(x),max(x),1000)
		f = interpolate.interp1d(x, y)
		popt, pcov = curve_fit(func, xnew, f(xnew))
		ynew = func(xnew, *popt)
		# r2 = 1. - sum((func(x, *popt) - y) ** 2) / sum((y - np.mean(y)) ** 2)
		return (xnew, ynew, popt)

	data = dc.ImportRaw(pathname)
	for x in data.keys(): 
		if 'Current' in x: CurrentName = x

	y, x, t = data['Oxygen_lvl'], data[CurrentName], data['Time']

	#Curve function
	fig1 = plt.figure()
	ax1 = plt.subplot(111)
	# # Figure size in inches

	#Adjusting
	plt.tick_params(
		axis='both', which='both', bottom='on', 
		top='off', right = 'off', labelright = 'off')
	#Plot data with colors on the time coloring
	colors=plt.cm.rainbow(np.linspace(0,1,len(y)))

	for i, xox in enumerate(x):
		ax1.plot(xox,y[i], '.', color = colors[i], markersize = 2)
		if ShowTime == True:
			ax1.annotate(datetime.strftime(t[i], '%H:%M'), (xox,y[i]), 
				xytext=(1,1), textcoords='offset points',
                family='sans-serif', fontsize=7, alpha = 0.8, color=colors[i])


	xn1, yn1, popt = fit(x, y)
	b, = plt.plot(xn1,yn1,'r') #Line
	name = tools.FindFilename(pathname)
	#Adjust plot parameters
	ax1.set_xlabel('Current \n(\muA for PS/nA for boards)')
	ax1.set_ylabel(r'Oxygen, %')
	ext = 'y = {:.2E}xˆ2{:+.2E}x{:+.2E}'.format(*popt)
	test = func(3500,*popt)
	plt.title(name+'\n'+ext, y=1)
	ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
	ax1.minorticks_on()
	plt.grid()

	#np.export
	###############################
	plt.savefig(st.ResponseFolder+os.sep+name+'.png', dpi= 300, 
		bbox_inches='tight')
	print('Plot for sensors %s - done'%name)

def plotter(ShowTime = False):
	names = tools.getfilelist(st.resultfolder, 
		st.FinRAWExtention, 
		comment = 'Get files for oxygen plotting...')
	for x in names:
		PlotOxygen(x, ShowTime)
