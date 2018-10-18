from glob import glob
import sys, os
import settings as st

def getfilelist(path, filetype, comment = 'No comment'):
	'''
	Get list of files in path and check if files exist
	'''
	fullpath = os.path.join(path,'*'+filetype)
	filefils = sorted(glob(fullpath))
	print(comment)
	if not filefils: 
		print( 'No data in path: %s'%fullpath )
		sys.exit('Programm crashed!')
	else: 
		print('Collect data file for path %s and type %s'%(path, filetype))
		print('Number of files: {}'.format(len(filefils)))
		return filefils

def FindFilename(path):
	return os.path.splitext(os.path.basename(path))[0]