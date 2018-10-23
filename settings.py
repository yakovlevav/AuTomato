import os

Data = {}
#Settings for application
pathcv = os.path.join(os.getcwd(),'Data','Curves')
#Folder for conversion of PalmSense files
convertfolder = os.path.join(os.getcwd(),pathcv,'converted')

pathCurrentBoard = os.path.join(os.getcwd(), 'Data','OxygenBoard')
palmsenseExtention = '.csv'

#Filenames for boards
BoardFileExtention = '.txt'

FinRAWExtention = '.csv'

ErrorCodes = [
	(" nA", ""), (" C|O:",","), 
	(",T: ",","), 
	("\nPower was interrupted!\nTime and Date have been reset.\nCurrent state: Stopped\n\n",""),
	("\nLogger Memory Full!\nCurrent state: Stopped\nPlease Reset.\n\n","")
	]

plotnames = ['Oxygen lvl', 'Time']

#Name of response for boards
OxResponseName = 'Current(nA)'

# Path for RAW data 
resultfolder = os.path.join(os.getcwd(),'Result','RawData')
ResponseFolder =os.path.join(os.getcwd(),'Result','Response')
FinalDataName = 'RawData'

#Files path for cleaned data from boards
PathBoardCleaned = os.path.join(os.getcwd(),pathCurrentBoard,'converted')

#Naming and col numbers for oxygen level
oxygencols = (0,1,3)
oxygencolnames = ['Oxygen lvl', 'Temperature']

#Naming and col numbers for humidity level
humiditycols = (0,1)
humiditycolnames = ['Humidity']

oxygenboardcolnames = ['CurrentOnBoard']
oxygenboardcols = (0,1)
# 
timeerror = 2
currentsetpoint = 0.1

#POINTS!!!!
averangetime = 5

# Path for oxygen reference data
pathOx = os.path.join(os.getcwd(),'Data','Oxygen')
OxExt = '.txt'

#Settings for PalmSense converte
decodefrom = 'utf-16'
encodeto = 'utf-8'