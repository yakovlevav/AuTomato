import matplotlib.pyplot as plt #For plotting
from scipy import interpolate #Interpolation and fit
from scipy.optimize import curve_fit #Curve fit
import settings as st
import datacollector as dc
from numpy import genfromtxt, linspace
from datetime import datetime, timedelta
import tools

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
	def func(x,a,b):
	    return a*x+b

	#Curve fitting
	def fit(x, y): #Gauss Fit Function
	    xnew = linspace(min(x),max(x),1000)
	    f = interpolate.interp1d(x, y)
	    popt, pcov = curve_fit(func, xnew, f(xnew))
	    ynew = func(xnew, *popt)
	    return (xnew, ynew, popt)

	data = dc.ImportRaw(pathname)
	for x in data.keys(): 
		if 'Current' in x: CurrentName = x

	x,y, t = data['Oxygen_lvl'], data[CurrentName], data['Time']

	#Curve function
	fig1 = plt.figure()
	ax1 = plt.subplot(111)
	# # Figure size in inches
	# fig1.set_size_inches(3.54,3.54)

	#Adjusting
	plt.tick_params(
		axis='both', which='both', bottom='on', 
		top='off', right = 'off', labelright = 'off')
	#Plot data with colors on the time coloring
	colors=plt.cm.rainbow(linspace(0,1,len(y)))

	for i, xox in enumerate(x):
		ax1.plot(xox,y[i], '.', color = colors[i], markersize = 2)
		if ShowTime == True:
			ax1.annotate(datetime.strftime(t[i], '%H:%M'), (xox,y[i]), 
				xytext=(1,1), textcoords='offset points',
                family='sans-serif', fontsize=7, alpha = 0.8, color=colors[i])

	#Adjust plot parameters
	ax1.set_ylabel(u'Current, µA')
	ax1.set_xlabel(r'Oxygen, %')
	ax1.set_xlim(0,100)
	plt.title(st.FinalDataName, y=1)
	ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
	ax1.minorticks_on()
	plt.grid()

	xn1, yn1, popt = fit(x, y)
	b, = plt.plot(xn1,yn1,'r') #Line
	plt.text(0.65, 0.95, 'y = {:.2E}x{:.2E}'.format(*popt),
		horizontalalignment='center',
		verticalalignment='center',
		transform = ax1.transAxes,
		fontsize = 8,
		backgroundcolor = 'white')

	#Export
	###############################
	name = tools.FindFilename(pathname)
	plt.savefig(st.ResponseFolder+name+'.png', dpi= 1000, bbox_inches='tight')
	print('Plot for sensors %s - done'%name)

def plotter():
	names = tools.getfilelist(st.resultfolder, 
		st.FinRAWExtention, 
		comment = 'Get files for oxygen plotting...')
	for x in names:
		PlotOxygen(x)
	





