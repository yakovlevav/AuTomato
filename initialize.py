import	os

FunctionsFolder = 'Functions'

DataFolderName = 'Data'
DataFolders = ['PalmSense', 'Humidity', 'Oxygen']

ResultFolder = 'Result'
ResultFolders = ['Response', 'RawData', 'Oxygen']


def make_folders(i):
    '''Makes a folder (and its parents) if not present'''
    try:  
        os.makedirs(i)
        print('Folder '+i)
    except:
        pass

if __name__ == '__main__':
	make_folders(DataFolderName)
	#Create Subfolders in Data
	for i in DataFolders: 
		make_folders(DataFolderName+'/'+i)
	#Create result folder
	make_folders(ResultFolder)
	make_folders(FunctionsFolder)



