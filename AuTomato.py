import AutoChrono
import initialize
import Plotter
import converters as conv

# import logging

# logging.basicConfig(level = logging.WARNING)

# def initclean():
	# init = initialize.initialize()
	# init.create_folders()
	# init.clean_all_folders()
	# init.clean_data_folders()
	# init.clean_specific('Oxygen')

# def PalmSenseProcedute():
	
	# Convert data from PalmSense
	# ConvertPalmSenseCSV()

def OxygenBoardProcedure():
	conv.ConvertOxygenBoard()
	dc = AutoChrono.DataCollector()
	dc.getoxygenboard()
	dc.writedata()
	pt = Plotter.Plotter()
	pt.plotnames = ['Oxygen lvl', 'Current(nA)', 'Time']
	pt.ShowTime = False
	pt.plotdata()

if __name__ == '__main__':
	OxygenBoardProcedure()

	
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


