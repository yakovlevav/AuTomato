Data = {}
#Settings for application

pathcv = 'Data/Curves/'
#Folder for conversion of PalmSense files
convertfolder = pathcv + 'converted/'

pathCurrentBoard = 'Data/OxygenBoard/'
palmsenseExtention = '.csv'

#Filenames for boards
BoardFileExtention = '.txt'

FinRAWExtention = '.csv'

ErrorCodes = [
	(" nA", ""), (" C|O:",","), 
	(",T: ",","), 
	("\nPower was interrupted!\nTime and Date have been reset.\nCurrent state: Stopped\n\n","")
	]

plotnames = ['Oxygen lvl', 'Time']

#Name of response for boards
OxResponseName = 'Current(nA)'

# Path for RAW data 
resultfolder = 'Result/RawData/'
ResponseFolder ='Result/Response/'
FinalDataName = 'RawData'

#Files path for cleaned data from boards
PathBoardCleaned = pathCurrentBoard + 'converted/'

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

# Path for oxygen reference data
pathOx = 'Data/Oxygen/'

#Settings for PalmSense converte
decodefrom = 'utf-16'
encodeto = 'utf-8'