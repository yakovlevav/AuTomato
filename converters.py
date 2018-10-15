import os, logging, sys, re
from glob import glob #List of files
import settings as st

def ConvertPalmSenseCSV(pathcv = st.pathcv, 
	decodefrom = st.decodefrom, encodeto = st.encodeto, 
	convertfolder = st.convertfolder):

	#If where is no folder - create it!
	convertfolder = os.path.join(pathcv,'converted')

	#Check if folder for converted files exists	#Create list of all CSV files
	filestoconvert = glob(os.path.join(pathcv,'*.csv'))
	# If no files to convert break program
	if not filestoconvert:
		print('No CSV files from PalmSense to convert!')
		sys.exit()
	else:
		if not os.path.exists(convertfolder): os.makedirs(convertfolder)
		print('Number of files to convert - {}'.format(len(filestoconvert)))
	#Calculate number of digits for zero aading
	length = len(str(len(filestoconvert)))
	#Convert files and place them in new folder
	for i in filestoconvert:
		#Open file with encoding
		with open(i, 'r', encoding = decodefrom) as f: contents = f.read()
		logging.info('Write File %s!' % i)
		newfilename = addzero(
			filename = os.path.join(convertfolder, os.path.basename(i)),
			length = length
			)
		with open(newfilename, 'w', encoding = encodeto) as f: f.write(contents)
		print('Write File %s  - done!' % newfilename)	
	print('Files conversion to %s - done!' % encodeto)	

def addzero(filename, length):
	#Add zero to the stupid naming in PalmSense
	numberoffile = re.findall(r'(\d+)', filename)[-1] #Find only last digit in the text
	zeros = '0'*(length-len(str(numberoffile)))
	newfilename = re.sub(r'(-\d+.csv)', '-'+zeros+numberoffile+'.csv', filename)
	return newfilename

def ConvertOxygenBoard(path = st.pathCurrentBoard, ext = st.BoardFileExtention,
	cpath = st.PathBoardCleaned, a = st.ErrorCodes):
	#Get all files from folder
	filestoconvert = glob(path+os.sep+'*'+ext)
	if not os.path.exists(cpath): 
		os.makedirs(cpath)
	else: 
		print('Folder %s already exists'%cpath)
	for x in filestoconvert:
		#Remove shit from file
		with open(x, 'r', encoding="utf-8") as f: 
			contents = f.read()
			#Replace truples of errors
			for i in a: contents = contents.replace(*i)
		#Place files in subfolder with cleaned data
		filename = os.path.basename(x)
		finalpath = os.path.join(cpath,filename)
		# print(newname)
		with open(finalpath, 'w+',  encoding="utf-8") as f: f.write(contents)
		print('File %s was cleaned.' % filename)
	print('Files cleaned from errors and placed in folder %s - done!' % cpath)
