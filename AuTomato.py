import AutoChrono
import initialize

if __name__ == '__main__':

	init = initialize.WoldCreation()
	init.create_folders()
	init.clean_folders()

	# AutoChrono.CSVConverter()
	# dc = AutoChrono.DataCollector()
	# dc.GetOxygenFromBoard()
	# dc.getcurrent(2)
	# dc.getoxygen()
	# dc.gethumidity()
	# dc.writedata()

	# pt = AutoChrono.Plotter()
	# pt.plotdata()