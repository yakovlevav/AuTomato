import matplotlib.pyplot as plt #For plotting
from scipy import interpolate #Interpolation and fit
from scipy.optimize import curve_fit #Curve fit
from glob import glob
import re
from numpy import genfromtxt, linspace
from datetime import datetime, timedelta

class Plotter():
	"""docstring for Plotter"""
	pathCurrent = 'Data/Curves/Converted/'
	pathOx = 'Data/Oxygen/'
	resultfolder = 'Result/RawData/'
	resultfolderplot = 'Result/Response/'
	plotnames = ['Oxygen lvl', 'Current@2.0s', 'Time']
	name  = ''
	ShowTime = True

	def __init__(self):
		#Find name of DataFile in resultfolder
		a = glob(self.resultfolder+'/*.csv')[0][:-4]
		b = re.sub(r'(-\d+.txt)', '', a)
		self.name = re.sub(self.resultfolder,'', b)

		# return(name)

	def findkeys(self, dictionary, name = 'Current'):
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

	def importfile(self, file):
		'''
		Import file created function
		and collect data as [] in dictionary by name
		Function return only data with names 'NamesToImport'
		as list [[],[]...]
		'''
		data = genfromtxt(self.resultfolder+self.name+'.csv',
			        delimiter=',',
			        unpack=True,
			        dtype=str,
			        )

		resultdict = {}

		# Convert arrays to the lists
		for x, data in enumerate(data): resultdict[data[0]] = data[1:].tolist()
		# Convert all strings to the floats and datetime
		for name in resultdict:
			if name == 'Time':
				resultdict[name] = [datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in resultdict[name]]
			else:
				resultdict[name] = [float(i) for i in resultdict[name]]
		export = []
		for name in self.plotnames: export.append(resultdict[name])
		return(export)

	def exportname(self):
		name = glob(self.resultfolder+'/*.csv')

		return(name[0][:-4])

	def plotdata(self):
		def func(x,a,b):
		    return a*x+b

		#Curve fitting
		def fit(x, y): #Gauss Fit Function
		    xnew = linspace(min(x),max(x),1000)
		    f = interpolate.interp1d(x, y)
		    popt, pcov = curve_fit(func, xnew, f(xnew))
		    ynew = func(xnew, *popt)
		    return (xnew, ynew, popt)

		x, y, t = self.importfile(self.resultfolder)

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
			if self.ShowTime == True:
				ax1.annotate(datetime.strftime(t[i], '%H:%M'), (xox,y[i]), 
					xytext=(1,1), textcoords='offset points',
	                family='sans-serif', fontsize=7, alpha = 0.8, color=colors[i])



		#Adjust plot parameters
		ax1.set_ylabel(u'Current, µA')
		ax1.set_xlabel(r'Oxygen, %')
		ax1.set_xlim(0,100)
		plt.title(self.name, y=1)
		ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
		ax1.minorticks_on()
		plt.grid()

		#Fit parameters on plot
		#Plot data
		# xn1, yn1, popt = fit(x, y)
		# b, = plt.plot(xn1,yn1,'r') #Line
		# plt.text(0.65, 0.95, 'y = {:.2E}x{:.2E}'.format(*popt),
		# 	horizontalalignment='center',
		# 	verticalalignment='center',
		# 	transform = ax1.transAxes,
		# 	fontsize = 8,
		# 	backgroundcolor = 'white')

		#Export
		###############################
		# plt.show()
		plt.savefig(self.resultfolderplot+self.name+'.png', dpi= 1000, bbox_inches='tight')
