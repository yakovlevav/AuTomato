from numpy import genfromtxt
from datetime import datetime, timedelta
from tqdm import tqdm
import settings as st
import os, tools
from glob import glob
import converters as conv
import numpy as np


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
		GoalTimeSecond = GoalTimeLast - averangetime #Current at time
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
	folders = glob(st.pathcv + os.sep + '*' + os.sep)
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

def ImportRaw(pathname):
	'''
	Import file created function
	and collect data as [] in dictionary by name
	Function return only data with names 'NamesToImport'
	as list [[],[]...]
	'''
	dictionary = {}
	data = genfromtxt(pathname, #Careful, do not unpack of different dtypes!
	    delimiter=',',
	    dtype = None,
	    deletechars= '',
	    names = True,
	    invalid_raise = False,
	    converters={0: lambda x: datetime.strptime(x.decode("utf-8"), "%Y-%m-%d %H:%M:%S")},
	    )

	names = data.dtype.names
	#Create dictionary keys
	for x in names:
		dictionary[x] = []
	#Add data to dictionary keys
	for lines in data:
		for numbers, cells in enumerate(lines.tolist()):
			dictionary[names[numbers]].append(cells)
	return(dictionary)
