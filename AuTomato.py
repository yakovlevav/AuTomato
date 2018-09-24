import AutoChrono
import initialize

def initclean():
	init = initialize.initialize()
	# init.create_folders()
	# init.clean_all_folders()
	# init.clean_data_folders()
	# init.clean_specific('Oxygen')

if __name__ == '__main__':
	
	initclean()

	# AutoChrono.CSVConverter()
	# dc = AutoChrono.DataCollector()
	# dc.GetOxygenFromBoard()
	# dc.getcurrent(2)
	# dc.getoxygen()
	# dc.gethumidity()
	# dc.writedata()

	# pt = AutoChrono.Plotter()
	# pt.plotdata()