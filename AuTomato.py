import converters as conv
import datacollector as dc
import settings as st
import PlotData as pt
import initialize as init

def Oxboard():
	conv.ConvertOxygenBoard()
	dc.getoxygenboard()
	pt.plotter(ShowTime = False)

def PalmSense():
	dc.get_ox_ps()
	pt.plotter(ShowTime = True)

if __name__ == '__main__':
	#Create folder structure
	# init = init.initialize()
	# init.create_folders()
	# Oxygen boards measurment

	'''If you see NaN error, please check data!
	At the moment it's not implemented completely'''
	Oxboard()

	# Palm Sense collecting and plotting
	# PalmSense()