import re, os, sys, logging
from glob import glob #List of files 
from datetime import datetime, timedelta
from numpy import genfromtxt, linspace
from tqdm import tqdm #For progress bar
import matplotlib.pyplot as plt #For plotting
from scipy import interpolate #Interpolation and fit
from scipy.optimize import curve_fit #Curve fit


logging.basicConfig(filename='converter.log', level=logging.INFO,
	format='%(asctime)s : %(message)s')

class CSVConverter():
	'''
	Developer: Aleksandr V. Yakovlev
	Convert encoding from CSV files created by PalmSense
	to new encoding and place them in new folder.
	In addition, add zero to file name numbering.
	'''
	pathCV = 'Data/Curves/'
	ResultFolder = pathCV +'Converted/'
	decodefrom = 'utf-16'
	encodeto = 'utf-8'

	def __init__(self): 
		if not glob(self.ResultFolder + '/*.csv'): self.convert()
		else: print('Files already converted!')

	def convert(self):
		#If where is no folder - create it!
		if not os.path.exists(self.ResultFolder): os.makedirs(self.ResultFolder)
		#Create list of all CSV files
		filestoconvert = glob(self.pathCV+'/*.csv')
		# If no files to convert break program
		if not filestoconvert:
			logging.error('No CSV files to convert!')
			sys.exit()
		else:
			logging.info('Number of files to convert - {}'.format(len(filestoconvert)))
		#Calculate number of digits for zero aading
		length = len(str(len(filestoconvert)))
		#Convert files and place them in new folder
		for i in filestoconvert:
			#Open file with encoding
			with open(i, 'r', encoding = self.decodefrom) as f: contents = f.read()
			logging.info('Write File %s!' % i)
			newfilename = self.addzero(
				filename = re.sub(self.pathCV, self.ResultFolder, i), 
				length = length
				)
			with open(newfilename, 'w', encoding = self.encodeto) as f: f.write(contents)
			logging.info('Write File %s  - done!' % newfilename)	
		logging.info('Files conversion to %s - done!' % self.encodeto)	

	def addzero(self, filename, length):
		#Add zero to the stupid naming in PalmSense
		numberoffile = re.findall(r'(\d+)', filename)[-1] #Find only last digit in the text
		zeros = '0'*(length-len(str(numberoffile)))
		newfilename = re.sub(r'(-\d+.csv)', '-'+zeros+numberoffile+'.csv', filename)
		return newfilename

class DataCollector():
	'''
	Developer: Aleksandr V. Yakovlev
	'''

	pathCurrent = 'Data/Curves/Converted/'
	pathOx = 'Data/Oxygen/'
	pathRH = 'Data/Humidity/'
	resultfolder = 'ResultPlots/'
	pathCurrentBoard = 'Data/OxygenBoard/'

	#Naming and col numbers for oxygen level
	oxygencols = (0,1,3)
	oxygencolnames = ['Oxygen lvl', 'Temperature']

	#Naming and col numbers for humidity level
	humiditycols = (0,1)
	humiditycolnames = ['Humidity']

	oxygenboardcolnames = ['CurrentOnBoard']
	oxygenboardcols = (0,1)

	# 
	timeerror = 5
	# SetTime = 0 #Time in curve !!! Need to be fixed somehow because of stupid
	
	#
	FinalDataName = 'Data'

	#
	Data = {}

	def __init__(self):
		a = glob(self.pathCurrent+'/*.csv')[0]
		#Strange and need to be fixed
		b = re.sub(r'(-\d+.csv)', '', a)
		self.FinalDataName = re.sub(self.pathCurrent, '', b)
		# CSVConverter()

	def getfilelist(self, path, filetype):
		'''
		Get list of files in path and check if files exist
		'''
		filefils = sorted(glob(path + filetype))
		if not filefils: 
			print('No data in path: %s'%path)
			sys.exit('Programm crashed!')
		else: 
			print('Collect data file for path %s'%(path+filetype))
			return filefils

	def get(self, path, cols, skip_header = False, colnames = None, filetype = '*.txt'):
		'''
		Gel all data files with *.txt type from the folder.
		Append all files in one array and create dictionary
		with time key from all gived colomns in the file.
		Return {Key: [],[],...}
		Add keys names to the dictionary
		'''
		datafile = self.getfilelist(path, filetype)
		Data, temp = {}, []
		# Create temp for imporing data respective to columns
		for i in cols: temp.append([])
		# Get date from all files in the folder and create one list
		for i in datafile:
			data = genfromtxt(i, #Careful, do not unpack of different dtypes!
			        delimiter=',',
			        unpack=True,
			        dtype=str,
			        usecols = cols,
			        skip_header = skip_header
			        ).tolist()
			for i, d in enumerate(temp):
				temp[i].extend(data[i])
		# Create Dictionary from data with the date-time key
		Data['Time'] = colnames 
		for i, d in enumerate(temp[0]):
				try: #Fix for the empty number in dictionary - Error in float()
					Data[datetime.strptime(d, "%Y-%m-%d %H:%M:%S")] =\
					[float(x[i]) for x in temp[1:]] #Append rest of the as list
				except Exception as e:
					continue
		return Data

	def MatchData(self, First, Second):
		'''
		Append dictionary First to the Second if where is corresponding
		time key with time delta 5 seconds
		If some data appended - return dictionary with extended data for all
		keys. If not - retunr initial first dictionary
		'''
		result = {}
		#Remove names elements from dictionaty and 
		result['Time'] = First.pop('Time') + Second.pop('Time')
		# print('''Appending of humidity data to the oxygen\n**It can take some time**''')

		#Find close time from the list of times
		timelist = list(First.keys())
		ClosestTime = lambda a, b: min(b, key=lambda d: abs(d - a))

		for Time in tqdm(Second):
			CTime = ClosestTime(Time, timelist)
			if abs(CTime-Time) > timedelta(self.timeerror):
				continue
			else:
				result[CTime] = First.get(CTime) + Second.get(Time)
		#Check is you have zero results
		if len(result) == 1:
			print('No corresponding time data!')
			return(First)
		else:
			print('Appending - done!')
			return(result)

	def getoxygen(self):
		'''
		Get oxygen data on form of dictionaty {Time:[Oxygen level, Temperature]}
		'''
		self.Data = self.MatchData(self.Data, 
			self.get(
				path = self.pathOx, 
				cols = self.oxygencols, 
				colnames = self.oxygencolnames
				))

	def gethumidity(self):
		'''
		Get humidity data in form of {Time: [Humidity]}
		'''
		self.Data = self.MatchData(self.Data, 
			self.get(path = self.pathRH, 
				cols = self.humiditycols,
				colnames = self.humiditycolnames
			))

	def current(self, SetTime):
		'''
		Get data files from the folder. Strip time from the file
		Get data point from Time variable, create dictionary with
		time key and current at time measurment.
		Return dictionary {Time: [Current]}
		'''
		datafile = self.getfilelist(self.pathCurrent, filetype = '*.csv')
		FinalDict = {}
		for filenames in datafile:
			with open(filenames, 'rb') as f: contents = f.read()
			# Get time from the file
			time = datetime.strptime(contents[15:34].decode('UTF-8'), "%Y-%m-%d %H:%M:%S")
			# print(filenames)
			data = genfromtxt(filenames, #Careful, not unpack of different dtypes!
			        delimiter=',',
			        unpack=True,
			        skip_header = 6,
			        skip_footer = 1,
			        encoding = 'UTF-8',
			        ).tolist()
			# Calculate minimum value
			GoalTime = min(data[0], key=lambda x:abs(x-SetTime)) #Current at time
			index = data[0].index(GoalTime) #FindIndex
			Current = data[1][index]
			FinalDict[time] = [Current]
		FinalDict['Time'] = ['Current@%ss'%GoalTime]
		return FinalDict

	def GetOxygenFromBoard(self):
        # get all the referencesensor datafiles
		datafile = self.getfilelist(self.pathCurrentBoard, filetype = '*.txt')
		Data, temp = {}, []
		# Create temp for imporing data respective to columns
		for i in self.oxygenboardcols: temp.append([])
		# Get date from all files in the folder and create one list
		for i in datafile:
			data = genfromtxt(i, #Careful, do not unpack of different dtypes!
			        delimiter=',',
			        unpack=True,
			        dtype=str,
			        usecols = (self.oxygenboardcols),
			        # skip_header = skip_header
			        ).tolist()
			for i, d in enumerate(temp):
				temp[i].extend(data[i])
		Data['Time'] = self.oxygenboardcolnames 
		for i, d in enumerate(temp[0]):
				try: #Fix for the empty number in dictionary - Error in float()
					Data[datetime.strptime(d, "%Y-%m-%d %H:%M:%S")] =\
					[float(x[i]) for x in temp[1:]] #Append rest of the as list
				except Exception as e:
					continue
					
		# return Data
		a = int(data[0][0])
		print(a.astype(np.int64)//10**9)
		# print(FinalDict)

		# for filenames in datafile:


        # # SensorData = pd.DataFrame()
        # for i in range(len(filelistReference)):
        #     dataRead = pd.read_csv(directory + filelistReference[i], sep=',', header = None, names=["date", "o2", "press1", "temp", "press2"])
        #     SensorData = SensorData.append(dataRead, ignore_index = True)
        # # change date from datetime to unix timestamp
        # index = pd.DatetimeIndex(SensorData.date)
        # index = index.astype(np.int64)//10**9
        # SensorData.date = index
        # return SensorData

	def getcurrent(self, *arg):
		if not arg:
			self.Data = self.current(0)
		else:
			for i in arg:
				if not self.Data:
					self.Data = self.current(arg[0])
					continue
				self.Data = self.MatchData(self.Data, 
				self.current(i))

	def writedata(self):
		'''
		Open file with the name Data.csv in resultfolder
		and write names from the dictionary with key 'Time' 
		in the first row and data from the dictionary like
		Key,Data,Data,Data...
		No return
		'''
		#Write dictionary with time key to the final CSV file
		with open(self.resultfolder+self.FinalDataName+'.csv', 'w') as file:
			output = 'Time,'+','.join(str(e) for e in self.Data.pop('Time'))+'\n'
			for key in self.Data:
				listtotext = ','.join(str(e) for e in self.Data[key])
				keytotext = key.strftime("%Y-%m-%d %H:%M:%S")+','
				output+=(keytotext+listtotext+'\n')
			file.write(output)
		print('Final dictionary file writed!')

	def OxygenCurrentMode(self):
		self.Data = self.MatchData(self.getoxygen(),self.getcurrent())

	def AddHumidity(self):
		self.Data = self.MatchData(self.Data,self.gethumidity())

class Plotter():
	"""docstring for Plotter"""
	pathCurrent = 'Data/Curves/Converted/'
	pathOx = 'Data/Oxygen/'
	resultfolder = 'ResultPlots/'
	plotnames = ['Oxygen lvl', 'Current@2.0s', 'Time']
	name  = ''
	ShowTime = True

	def __init__(self):
		#Find name of DataFile in resultfolder
		a = glob(self.resultfolder+'/*.csv')[0][:-4]
		self.name = re.sub(self.resultfolder,'', a)

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
		Import file created from the CollectData function
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
		fig1.set_size_inches(3.54,3.54)

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

		#Plot data
		xn1, yn1, popt = fit(x, y)
		b, = plt.plot(xn1,yn1,'r') #Line

		#Adjust plot parameters
		ax1.set_ylabel(u'Current, µA')
		ax1.set_xlabel(r'Oxygen, %')
		ax1.set_xlim(0,100)
		plt.title(self.name, y=1)
		ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
		ax1.minorticks_on()
		plt.grid()

		#Fit parameters on plot
		plt.text(0.65, 0.95, 'y = {:.2E}x{:.2E}'.format(*popt),
			horizontalalignment='center',
			verticalalignment='center',
			transform = ax1.transAxes,
			fontsize = 8,
			backgroundcolor = 'white')

		#Export
		###############################
		plt.savefig(self.resultfolder+self.name+'.png', dpi= 1000, bbox_inches='tight')
