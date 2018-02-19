import csv

data = []
data.append(['A1','B1','C1','A1','B1','C1','X1','Y1','Z1'])
data.append(['A2','B2','C2','A2','B2','C2','X2','Y2','Z2'])
data.append(['A3','B3','C3','A3','B3','C3','X3','Y3','Z3'])

def writeCSV():	 
	# with open('persons.csv', 'w', newline='') as csvfile:
	#     filewriter = csv.writer(csvfile, delimiter=',',
	#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
	#     filewriter.writerow(['Name', 'Profession'])
	#     filewriter.writerow(['Derek', 'Software Developer'])
	#     filewriter.writerow(['Steve', 'Software Developer'])
	#     filewriter.writerow(['Paul', 'Manager'])
	with open('COM_Measurements.csv', 'w', newline='') as csvfile:
	    filewriter = csv.writer(csvfile, delimiter=',',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    filewriter.writerow(['Orientation 1', '', '', 'Orientation 2', '', '', 'COM Coordinates'])
	    filewriter.writerow(['LoadCellA', 'LoadCellB', 'LoadCellC', 'LoadCellA', 'LoadCellB', 'LoadCellC', 'X', 'Y', 'Z'])
	    for i in data:
		    filewriter.writerow(i)


def readCSV():
	array = []
	with open('COM_Measurements.csv', 'r') as f:
	    reader = csv.reader(f)
	 
	    # read file row by row
	    for row in reader:
	    	array.append(row)


	    print (array)


writeCSV()
readCSV()


