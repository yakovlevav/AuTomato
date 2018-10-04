import AutoChrono
import initialize
from converters import ConvertPalmSenseCSV
# import logging

# logging.basicConfig(level = logging.WARNING)

# def initclean():
	# init = initialize.initialize()
	# init.create_folders()
	# init.clean_all_folders()
	# init.clean_data_folders()
	# init.clean_specific('Oxygen')

if __name__ == '__main__':
	ConvertPalmSenseCSV()

	
	# initclean()
	# cv = CSVConverter()


	# # AutoChrono.CSVConverter()
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

	# pt = AutoChrono.Plotter()
	# pt.plotnames = ['Oxygen lvl', 'Current(nA)', 'Time']
	# pt.ShowTime = False
	# pt.plotdata()