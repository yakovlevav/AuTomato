import AutoChrono
import initialize
import Plotter
import converters as conv
import datacollector as dc2
import settings as st
import tools as tools
import PlotData as pt

# import logging

# logging.basicConfig(level = logging.WARNING)

# def initclean():
	# init = initialize.initialize()
	# init.create_folders()
	# init.clean_all_folders()
	# init.clean_data_folders()
	# init.clean_specific('Oxygen')

# def PalmSenseProcedute():
	
# 	Convert data from PalmSense
# 	ConvertPalmSenseCSV()

# def OxygenBoardProcedure():
# 	conv.ConvertOxygenBoard()
# 	dc = AutoChrono.DataCollector()
# 	dc.getoxygenboard()
# 	dc.writedata()

# 	#Plotiing
# 	pt = Plotter.Plotter()
# 	pt.plotnames = ['Oxygen lvl', 'Current(nA)', 'Time']
# 	pt.ShowTime = False
# 	pt.plotdata()

def NewPalmSense():
	conv.ConvertPalmSenseCSV()
	dc2.current(0.5)
	dc2.AddRefOxygen()
	dc2.writedata()
	pt.plotOxygen()

def NewOxboard():
	conv.ConvertOxygenBoard()
	dc2.getoxygenboard()
	pt.plotter()

def function():
	# conv.multiconverter()
	# dc2.current(0.5, pathCurrent = st.convertfolder)
	dc2.get_ox_ps()
	pt.plotter()


if __name__ == '__main__':
	# OxygenBoardProcedure()
	# OxygenPalmSense()
	# experiment()

	# NewPalmSense()
	# NewOxboard()

	function()

	# PalmSenseProcedute()
	# dc = AutoChrono.DataCollector()


	# initclean()
	# cv = CSVConverter()


	# AutoChrono.CSVConverter()
	# dc = AutoChrono.DataCollector()
	# # dc.OxygenBoardData()
	# # dc.getoxygen()

	# dc.getoxygenboard()
	# # print(dc.Data)
	# # dc.GetOxygenFromBoard()

	# # dc.getcurrent(2)
	# # dc.getoxygen()
	# # dc.gethumidity()
	# dc.writedata()


