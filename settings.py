#Settings for application

pathcv = 'Data/Curves/'
#Folder for conversion of PalmSense files
convertfolder = pathcv + 'converted/'

pathCurrentBoard = 'Data/OxygenBoard/'
BoardFileExtention = '*.txt'

ErrorCodes = [
	(" nA", ""), (" C|O:",","), 
	(",T: ",","), 
	("\nPower was interrupted!\nTime and Date have been reset.\nCurrent state: Stopped\n\n","")
	]

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

#Settings for PalmSense converte
decodefrom = 'utf-16'
encodeto = 'utf-8'