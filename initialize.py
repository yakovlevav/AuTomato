import	os
from glob import glob

class initialize:
	"""docstring for Itinialise"""

	Folders = {
		'Data': ['PalmSense', 'Humidity', 'Oxygen', 'OxygenBoard'], #Data Folders!
		'Result': ['Response', 'RawData', 'TimeOxygen']
		}

	# def __init__(self, arg):
	# 	super(Itinialise, self).__init__()
	# 	self.arg = arg

	def maker(self, i):
	    '''Makes a folder (and its parents) if not present'''
	    try:  
	        os.makedirs(i)
	    except FileExistsError as e:
	    	print(e, '\n Folder' + i +' already exists! \n')
	    except Exception as e:
	    	print(e, 'Sorry. Something went wrong!')
	    else:
	    	print('Folder '+i+' are created...')


	def cleaner(self,i):
		if not glob(i+'/*'):
			print('No files in derictory: ' + i)
		else:
			for x in glob(i+'/*'):
				try:
					os.remove(x)
				except FileNotFoundError as e:
					print(e, "\n Sorry, i can't clean files! Probably folder already empty!\n")
				except PermissionError as e:
					print(e, "\n Sorry, i can't clean files! Probably file in use, or opened!\n")
				except Exception as e: 
					print(e)
				else:
					print('File:' + x + ' was removed!')

	def create_folders(self):
		#Create Subfolders in Data
		for Lvl1, Lvl2  in self.Folders.items(): 
			self.maker(Lvl1)
			for x in Lvl2:
				self.maker(Lvl1+'/'+x)

	def clean_all_folders(self):
		for Lvl1, Lvl2  in self.Folders.items(): 
			for x in Lvl2:
				self.cleaner(Lvl1+'/'+x)
		print('Cleaning done!')


	def clean_data_folders(self):
		name = 'Data'
		for Folder in self.Folders[name]:
			# print(Folder) 
			self.cleaner(name+'/'+Folder)
		print('Cleaning data folders done!')

	def clean_specific(self, GoalFolder):
		# print(os.listdir('./'))
		for root, dirs, files in os.walk('./'):
			for names in dirs:
				if names == GoalFolder:
					# self.cleaner(name+'/'+Folder)
					self.cleaner(root+'/'+names)
				else:
					pass




