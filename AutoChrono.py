import re, os, sys, logging
from glob import glob #List of files 
from datetime import datetime, timedelta
from numpy import genfromtxt, linspace
from tqdm import tqdm #For progress bar


logging.basicConfig(filename='converter.log', level=logging.INFO,
	format='%(asctime)s : %(message)s')

class DataCollector():
	'''
	Developer: Aleksandr V. Yakovlev
	'''
	pathCurrent = 'Data/Curves/Converted/'
	pathOx = 'Data/Oxygen/'
	pathRH = 'Data/Humidity/'
	resultfolder = 'Result/RawData/'
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

	def OxygenBoardData(self):
		datafile = self.getfilelist(self.pathCurrentBoard, '*.txt')
		print(datafile)

		#Remove shit from file
		with open(datafile[0], 'r', encoding="utf-8") as f: 
			contents = f.read()
			contents = contents.replace("Power was interrupted!\nTime and Date have been reset.\nCurrent state: Stopped\n\n", "")
			contents = contents.replace(",T: ", ",")
			contents = contents.replace(" nA", "")
			contents = contents.replace(" C|O:", ",")

		newfilename = datafile[0].replace('.txt', '_b.txt')
		with open(newfilename, 'w',  encoding="utf-8") as f: f.write(contents)
		####

		FinalDict = {}
		data = genfromtxt(newfilename, #Careful, not unpack of different dtypes!
			        delimiter=',',
			        unpack=True,
			        skip_footer = 12,
			        ).tolist()

		#Create dictionaty for time and 
		for number, time in enumerate(data[0]):
			finaltime = datetime.fromtimestamp(time)
			print(finaltime)
			FinalDict[finaltime] = [data[2][number]]
		FinalDict['Time'] = ['Current(nA)']
		# print(FinalDict)
		return(FinalDict)

	def getoxygenboard(self):
		'''
		Get oxygen current lvl from borads
		data in form of {Time: [Current]}
		'''
		a = glob(self.pathCurrentBoard+'/*.txt')[0]
		print(a)
		#Strange and need to be fixed
		b = re.sub(r'(-\d+.txt)', '', a)
		self.FinalDataName = re.sub(self.pathCurrentBoard, '', b)

		self.Data = self.OxygenBoardData()
		self.Data = self.MatchData(self.Data, 
			self.get(
					path = self.pathOx, 
					cols = self.oxygencols, 
					colnames = self.oxygencolnames
					))
		
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