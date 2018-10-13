import converters as conv
import datacollector as dc
import settings as st
import PlotData as pt

def Oxboard():
	conv.ConvertOxygenBoard()
	dc.getoxygenboard()
	# pt.plotter(ShowTime = False)

def PalmSense():
	dc.get_ox_ps()
	pt.plotter()

if __name__ == '__main__':
	Oxboard()
	# PalmSense()