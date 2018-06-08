import os
import csv
from datetime import datetime
from collections import defaultdict

'''
This program creates a csv file to hold expenses, writes new expenses to the csv file, 
and reads expenses from the csv file. The program is run from the main().

Note: the path directory, master_file, must be set before the program is run.
'''

def main():
	cwd = os.path.dirname(os.path.realpath(__file__)) #gets directory of the expenses.py. Put in function?
	master_file = cwd + '/expenses.csv' #must change this to the appropriate directory.
	file_exists = os.path.isfile(master_file)
	data = collect() #runs the collect function and stores a list in a variable.
	if not file_exists: #creates csv file if it does not already exist.
		create_file(master_file)
	add_data(master_file, data, file_exists)
	read_data(master_file)

def collect(): #This function returns a list of items along with the items' extra information.
	l = []
	currentmonth = datetime.now().strftime('%B')
	currentyear = datetime.now().year

	while True:
		item = raw_input('Enter the item: ').strip().lower()
		cost = raw_input('Enter the cost (exclude dollar sign) of ' + str(item) + ': ').strip()
		try:
			cost_test_number = float(cost)
		except ValueError:
			print('Expected a number; inputting null for ' + str(item) + '; moving on...')
			cost = None
		category = raw_input('Enter category (e.g. food, travel, or other) of ' + str(item) + ': ').strip().lower()
		record = (item, cost, category, currentmonth, currentyear)
		l.append(record)

		go = str(raw_input('Do you want to add another entry? ')).strip()
		if go.lower() in ['n', 'no','quit', 'q', 'exit']:
			break #exits and closes program.
	return l

def create_file(master_file): ##create function that creates the csv file and writes headers.
	with open(master_file, 'w') as fc:
		headers = ['item', 'cost', 'category', 'month', 'year']
		w = csv.writer(fc, delimiter=',')
		w.writerow(headers)

def add_data(master_file, data, file_exists): #This function adds data to the master_file.
	with open(master_file, 'a') as f:
		if file_exists: #need to add a linebreak if file exists because open-append csv does not add the linebreak upon first csv file open.
			f.write('\n')
		w = csv.writer(f, delimiter=',', lineterminator='\n') #This closes the csv file without a linebreak.

		for row in data: #write input to csv file.
			w.writerow(row)

def read_data(master_file): #This function reads the data from the master_file.
	with open(master_file, 'rU') as fr:
		r = csv.DictReader(fr)
		year_exp = defaultdict(float)
		month_exp = defaultdict(float)
		categories = defaultdict(float)
		tot_expense = 0

		for item in r:
			try:
				year_exp[item["year"]] += float(item["cost"])
				month_exp[item["month"] + ' ' + item["year"]] += float(item["cost"]) #Create a dictionary including a key for month and year.	
				categories[item["category"]] += float(item["cost"])							
			except:
				print('There are non-number values in the cost column in ' + '\n' + master_file)

		print('The total spending by year is:')
		print("\n".join("{}: ${:,.2f}".format(k, v) for k, v in year_exp.items()))
		print('')

		print('The total spending by month is:')
		print("\n".join("{}: ${:,.2f}".format(k, v) for k, v in month_exp.items()))
		print('')

		print('The total spending per category is:')
		print("\n".join("{}: ${:,.2f}".format(k, v) for k, v in categories.items()))
		print('')
		
if __name__ == "__main__":
	main() #Runs the program.
