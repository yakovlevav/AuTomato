import os, logging, sys, re
from glob import glob #List of files

def ConvertPalmSenseCSV(pathcv = 'Data/Curves/', decodefrom = 'utf-16', encodeto = 'utf-8'):
	#If where is no folder - create it!
	ResultFolder = pathcv+'converted/'

	#Check if folder for converted files exists	#Create list of all CSV files
	filestoconvert = glob(pathcv+'/*.csv')
	# If no files to convert break program
	if not filestoconvert:
		print('No CSV files from PalmSense to convert!')
		sys.exit()
	else:
		if not os.path.exists(ResultFolder): os.makedirs(ResultFolder)
		print('Number of files to convert - {}'.format(len(filestoconvert)))
	#Calculate number of digits for zero aading
	length = len(str(len(filestoconvert)))
	#Convert files and place them in new folder
	for i in filestoconvert:
		#Open file with encoding
		with open(i, 'r', encoding = decodefrom) as f: contents = f.read()
		logging.info('Write File %s!' % i)
		newfilename = addzero(
			filename = re.sub(pathcv, ResultFolder, i), 
			length = length
			)
		with open(newfilename, 'w', encoding = encodeto) as f: f.write(contents)
		print('Write File %s  - done!' % newfilename)	
	print('Files conversion to %s - done!' % encodeto)	

def addzero(filename, length):
	#Add zero to the stupid naming in PalmSense
	print(filename)
	numberoffile = re.findall(r'(\d+)', filename)[-1] #Find only last digit in the text
	zeros = '0'*(length-len(str(numberoffile)))
	newfilename = re.sub(r'(-\d+.csv)', '-'+zeros+numberoffile+'.csv', filename)
	return newfilename