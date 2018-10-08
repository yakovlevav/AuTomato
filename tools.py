from glob import glob
import sys
import settings as st

def getfilelist(path, filetype, comment = 'No comment'):
	'''
	Get list of files in path and check if files exist
	'''
	filefils = sorted(glob(path + filetype))
	if not filefils: 
		print(comment)
		print('No data in path: %s'%path)
		sys.exit('Programm crashed!')
	else: 
		print('Collect data file for path %s'%(path+filetype))
		print('Number of files: {}'.format(len(filefils)))
		return filefils