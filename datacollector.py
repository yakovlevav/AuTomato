from numpy import genfromtxt
from datetime import datetime, timedelta
from tqdm import tqdm
import settings as st
import os, tools
from glob import glob
import converters as conv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from scipy import polyfit
from matplotlib.ticker import FormatStrFormatter


def FindName(path, filetype):
	file = os.listdir(path)[0]
	return(file.split('.')[0])

def get(path, cols, skip_header = False, skip_footer = False, colnames = None, filetype = '*.txt'):
		'''
		Gel all data files with *.txt type from the folder.
		Append all files in one array and create dictionary
		with time key from all gived colomns in the file.
		Return {Key: [],[],...}
		Add keys names to the dictionary
		'''
		datafile = tools.getfilelist(path, filetype)
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
			        invalid_raise = False,
			        skip_header = skip_header,
			        skip_footer = skip_footer
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
		return(Data)

def MatchData(First, Second):
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
			if abs(CTime-Time) > timedelta(st.timeerror):
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

def AddRefOxygen():
	'''
	Get oxygen data in form of dictionaty {Time:[Oxygen level, Temperature]}
	and set it in dictionary
	'''
	data = MatchData(st.Data, 
		get(
			path = st.pathOx,
			cols = st.oxygencols,
			colnames = st.oxygencolnames
			))
	st.Data = data
	return(data)

def current(SetTime, averangetime = 5, pathCurrent = st.convertfolder, filetype = st.palmsenseExtention):
	'''
	Get data files from the folder. Strip time from the file
	Get data point from Time variable, create dictionary with
	time key and current at time measurment.
	Return dictionary {Time: [Current]}
	'''
	datafile = tools.getfilelist(pathCurrent, filetype = '*.csv')
	FinalDict = {}
	st.plotnames.append('Current@%ss'%(SetTime))
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
		        invalid_raise = False,
		        # encoding = 'UTF-8',
		        ).tolist()
		# Calculate minimum value
		GoalTimeLast = min(data[0], key=lambda x:abs(x-SetTime)) #Current at time
		indexlast = data[0].index(GoalTimeLast) #FindIndex
		indexprev = indexlast - averangetime
		Current = np.mean(data[1][indexprev:indexlast])
		FinalDict[time] = [Current]
	FinalDict['Time'] = ['Current@%ss'%GoalTimeLast]
	st.Data = FinalDict
	st.FinalDataName = FindName(pathCurrent, filetype).split('-')[0]
	return(FinalDict)

def writedata(resultfolder = st.resultfolder, FinalDataName = st.FinalDataName, ext = st.FinRAWExtention):
	'''
	Open file with the name ####.csv in resultfolder
	and write names from the dictionary with key 'Time' 
	in the first row and data from the dictionary like
	Key,Data,Data,Data...
	No return
	'''
	#Write dictionary with time key to the final CSV file
	filename = os.path.join(resultfolder, FinalDataName+ext)
	with open(filename, 'w') as file:
		output = 'Time,'+','.join(str(e) for e in st.Data.pop('Time'))+'\n'
		for key in st.Data:
			listtotext = ','.join(str(e) for e in st.Data[key])
			keytotext = key.strftime("%Y-%m-%d %H:%M:%S")+','
			output+=(keytotext+listtotext+'\n')
		file.write(output)
	print('Data for %s in %s form was saved in %s'%(FinalDataName,st.FinRAWExtention,st.resultfolder))


def get_ox_ps():
	'''
	Get oxygen data in form of dictionaty {Time:[Oxygen level, Temperature]}
	and set it in dictionary
	'''
	# folders = glob(st.pathcv + os.sep + '*' + os.sep)
	folders = tools.getfilelist(st.pathcv, os.sep, comment = 'Getting folder list for Oxygen curves')
	for x in folders:
		conv.ConvertPalmSenseCSV(pathcv = x)
		data = current(st.currentsetpoint, averangetime = st.averangetime,  pathCurrent = os.path.join(x,'converted'))
		st.Data = MatchData(data, 
			get(
				path = st.pathOx,
				cols = st.oxygencols,
				colnames = st.oxygencolnames
				))
		writedata(resultfolder = st.resultfolder, 
			FinalDataName = st.FinalDataName, 
			ext = st.FinRAWExtention)
	st.Data = data

	return(data)


def OxygenBoardData(filepath):
	FinalDict = {}
	data = genfromtxt(filepath, #Careful, not unpack of different dtypes!
		        delimiter=',',
		        unpack=True,
		        skip_footer = 10,
		        invalid_raise = False
		        ).tolist()
	#Create dictionaty for time and 
	for number, time in enumerate(data[0]):
		finaltime = datetime.fromtimestamp(time)
		FinalDict[finaltime] = [data[2][number]]
	FinalDict['Time'] = [st.OxResponseName]
	return(FinalDict)

def getoxygenboard():
	'''
	Get oxygen current lvl from borads
	data in form of {Time: [Current]}
	'''
	# a = glob(self.pathCurrentBoard+'/*.txt')[0]
	# print(a)
	#Strange and need to be fixed
	# b = re.sub(r'(-\d+.txt)', '', a)
	# self.FinalDataName = re.sub(self.pathCurrentBoard, '', b)

	files = tools.getfilelist(st.PathBoardCleaned, st.BoardFileExtention)
	for x in files:
		name = tools.FindFilename(x)
		st.Data = OxygenBoardData(x)
		st.Data = MatchData(st.Data, 
			get(
					path = st.pathOx, 
					cols = st.oxygencols, 
					colnames = st.oxygencolnames
					))
		writedata(st.resultfolder, name, st.FinRAWExtention)


#Pandas experimants

def ImportRaw(pathname):
	DataFrame = pd.read_csv(pathname)
	DF = DataFrame.dropna()
	return DataFrame

def	newgetrefox(pathname):
	'''
	Read CSV file from oxygen reference sensors and return pandas dataframe
	'''
	DF = pd.read_csv(pathname,
		names = ['Time', 'Oxygen', 'Partial pressure', 'Temperature', 'Pressure'],
		# parse_dates = [1], #Use it for dated in format of ISO 8601
		)
	DF['Time'] = pd.to_datetime(DF['Time'], format='%Y-%m-%d %H:%M:%S')
	return(DF)

def newgetcurrent(pathname, addtime = '2h'):
	'''
	Import file from Oxygen Board and create pandas data frame.
	Drop NaN and error bad lines
	'''
	DF = pd.read_csv(pathname,
		sep=',T:| C|O:| nA',
		engine='python',skipfooter = 12,
		usecols = [0,1,3],
		error_bad_lines = False,
		warn_bad_lines=False,
		names = {'Time': 0, 'Temperature':1, 'Current_nA':3},
		dtype = {'Time': str, 'Temperature':float, 'Current_nA':float},
		skip_blank_lines = True,
		).dropna()
	#Remove zero temperatures
	DF = DF.loc[DF['Temperature'] != 00.0]
	#For some reason have time difference in 2h, quick fix
	DF['Time'] = pd.to_datetime(DF['Time'], unit='s')+ pd.Timedelta(addtime)
	return(DF)

def newcomparetime(DF1, DF2, tolerance = '1s', MatchBy = 'Time'):
	'''
	Function for merging two pandas data frame with
	correcponding time. Inputs two data frames of pandas
	and toleranse as as string.
	'''
	DF1, DF2 = DF1.sort_values(by = 'Time'), DF2.sort_values(by = 'Time')
	MR = pd.merge_asof(DF1, DF2,
		on = MatchBy,			
		direction = 'nearest',
		suffixes = ('_Board', '_GR'),
		tolerance=pd.Timedelta(tolerance)
		).dropna()
	return(MR)

def ifnamefitthedate(pathname):
	'''
	Find date from filename
	In future is better to write date
	in better format.
	'''
	name = tools.FindFilename(pathname)
	date = name.split('_')
	print(date[1:])

def newgetoxygenboards():
	files = tools.getfilelist(st.pathCurrentBoard, st.BoardFileExtention)
	oxfiles = tools.getfilelist(st.pathOx, st.OxExt)
	ifnamefitthedate(oxfiles[0])
	

	# for x in files:
	# 	name = tools.FindFilename(x)
	# 	DF1 = newgetcurrent(x)

	# 	writedata(st.resultfolder, name, st.FinRAWExtention)

def	plt_current_ox(PdBoardOx, PdRefOx, comment = '', x = 'Current_nA', y = 'Oxygen'):
	df = newcomparetime(PdBoardOx, PdRefOx)
	df.plot(x, y, kind = 'scatter')
	xmin, xmax = df[x].min(), df[x].max()
	coeff = polyfit(df[x], df[y],1)
	f = np.poly1d(coeff)
	plt.title('%s\nFit: a = %.2E, b = %.2E\n'%(comment,*coeff))
	xnew = np.arange(xmin, xmax)
	plt.plot(xnew,f(xnew), 'r')
	return(coeff)

def plotTstab(relpath, tname = 'Temperature', cname = 'Current_nA'):
	name = tools.FindFilename(relpath)
	df = newgetcurrent(relpath)
	#Fit
	coeff = polyfit(df[tname], df[cname],1)
	f = np.poly1d(coeff)
	xnew = np.arange(df[tname].min(), df[tname].max())
	#
	df.plot(tname,cname,kind = 'scatter')
	plt.plot(xnew,f(xnew), 'r')
	plt.title('%s \nFit: a = %.2f, b = %.2f'%(name,*coeff))
	return(coeff[0])

def AddCorrectedCurrent(PdBoardOx, comp = 75.3):
	PdBoardOx['Current_nA(20C)'] = PdBoardOx['Current_nA']-(PdBoardOx['Temperature']-20)*comp
	return(PdBoardOx)

def reverscalc(value, t, comp, a, b):
	print('Current before - %.2f'%value)
	print('Current after - %.2f'%(value-(t-20)*comp))
	return((value-(t-20)*comp)*a+b)

def	plt_time_ox(df, comp, a, b):
	df['Ox_From_Calibration'] = (df['Current_nA']-(df['Temperature']-20)*comp)*a+b
	print(df)
	plt.gcf().autofmt_xdate()
	# df.plot('Ox_From_Calibration')
	fig, axes = plt.subplots(sharex=True)
	axes.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
	# axes.ticklabel_format(axis='y',style='sci',scilimits=(0,2))

	plt.ylim(18,22)
	plt.grid()
	df.plot('Time', 'Ox_From_Calibration', kind = 'line', ax=axes)
	mean, std = df['Ox_From_Calibration'].mean(), df['Ox_From_Calibration'].std()
	plt.title('Sensor accuracy - $%.2f \pm %.2f$'%(mean, std))
	plt.axhline(mean, color = 'r')
	plt.axhline(mean+std, color = 'r')
	plt.axhline(mean-std, color = 'r')
	plt.yticks(list(plt.yticks()[0])+[mean,mean+std, mean-std])
	df.plot('Time', 'Current_nA', kind = 'line', ax=axes, secondary_y=True)
	# axes.legend(loc='center left', bbox_to_anchor=(1.0, 1.0))


# def STPoxygen(DF):
# 	DF[]

############
# PdBoardOx = newgetcurrent('Data/OxygenBoard/18111602_raw_Ox.txt')
# PdRefOx = newgetrefox('Data/Oxygen/Oxygen_2018_10_16.txt')

# PdBoardOx = AddCorrectedCurrent(PdBoardOx, current = 75.3)

# plt_current_ox(PdBoardOx, PdRefOx, comment = 'No correction')
# plt_current_ox(PdBoardOx, PdRefOx, x = 'Current_nA(25C)', comment = 'Temp correction')

##########

comp = plotTstab('Data/OxygenBoard/TempStab/81019144.txt')

PdBoardOx = newgetcurrent('Data/OxygenBoard/81018144_raw.txt')
PdRefOx = newgetrefox('Data/Oxygen/Oxygen_2018_10_19.txt')

PdBoardOx = AddCorrectedCurrent(PdBoardOx, comp)
plt_current_ox(PdBoardOx, PdRefOx, comment = 'No correction')
c = plt_current_ox(PdBoardOx, PdRefOx, x = 'Current_nA(20C)', comment = 'Temp correction')

# print(reverscalc(4615, 24.6, comp, *c))

#Calibration check
calibrationtest = newgetcurrent('Data/OxygenBoard/TempStab/81019144.txt')
plt_time_ox(calibrationtest, comp, *c)
plt.show()
# newgetoxygenboards()
