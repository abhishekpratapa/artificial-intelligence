#from yahoo_finance import Currency
#import finsymbols
from yahoo_finance import Share
import re
import json
import sys
import time 
import os
from pprint import pprint
from google import search
from newspaper import Article
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize



class Selected:
	def __init__(self, name, typeOf):
		self.name = name
		self.typeof = typeOf

class Stocks:
	def __init__(self, tick, nam, exc, catName, catNr):
		self.ticker = tick
		self.name = nam
		self.exchange = exc 
		self.catName = catName
		self.catNr = catNr


####### Begin Parsing #######
def populate_stocks():
	global currentStocks;
	currentStocks = []

	file = open('stock_data/Stock.json', 'r')

	text = file.read()
	lines = text.split("}, {")


	for line in lines:
		line = re.sub('[{\[\]}]', '', line)
		element = json.loads("{"+line+"}");
		currentStocks.append(Stocks(element["Ticker"], element["Name"], element["Exchange"], element["categoryName"], element["categoryNr"]))
####### End Parsing #######

####### Begin Data Management #######

def global_parser(numProcessed):
	global currentStocks

	outputUniques = set()
	outputList = []
	
	for stock in currentStocks:
		if numProcessed == 0:
			outputUniques.add(stock.ticker)
			outputList.append(stock.ticker)
		elif numProcessed == 1:
			outputUniques.add(stock.exchange)
			outputList.append(stock.exchange)
		elif numProcessed == 2:
			outputUniques.add(stock.catName)
			outputList.append(stock.catName)
		elif numProcessed == 3:
			outputUniques.add(stock.catNr)
			outputList.append(stock.catNr)

	return outputUniques, outputList


def check_exists(string, numProcessed):
	Uniques, List = global_parser(numProcessed)
	for unique in Uniques:
		if unique == string:
			return True
	return False

def exchanges_display(numProcessed):

	#count uniques and set numbers

	outputUniques, outputList = global_parser(numProcessed)

	textOutput = []

	for unique in outputUniques:
		countOf = outputList.count(unique)
		textOutput.append(str(unique)+": "+str(countOf))

	for tickers in sorted(textOutput):
		print(tickers)
	print("\n\n")

def get_historical_data():
	global selected_Ticker
	UrlArray = []
	sid = SentimentIntensityAnalyzer()
	for url in search(selected_Ticker.name+" on cnn.com", tld='es', lang='es', stop=20):
		UrlArray.append(url)
	for urls in UrlArray:
		if "com/20" in urls:
			tokenize.sent_tokenize

			article = Article(urls)
			article.download()
			article.parse()
			article.nlp()

			lines_list = tokenize.sent_tokenize(article.text)

			for sentence in lines_list:
				ss = sid.polarity_scores(sentence)
				for k in sorted(ss):
					print('{0}: {1}, '.format(k, ss[k]), end='')
				print()

			print(article.summary)
			print(article.keywords)
			print(article.publish_date)
			time.sleep(10)
####### End Data Management #######

####### Begin Menus #######
def print_menu(menuid, errorid):
	global selected_Ticker

	namesTicker = ["Stocks", "Exchanges", "Catagory", "Number Selection"]

	if selected_Ticker is not None:
		print("Selected:\t"+selected_Ticker.name)
		print("Type:\t\t"+namesTicker[selected_Ticker.typeof])
		if selected_Ticker.typeof == 0:
			stock = Share(selected_Ticker.name)
			stock.refresh()
			print(stock.get_info())
			print(stock.get_price())
			print(stock.get_change())
			print(stock.get_volume())
		print("\n\n")

	if menuid == 0:
		print("------Menu------")
		print("    (e) exit")
		print("    (l) list")
		print("    (s) stats")
		error(errorid)
	elif menuid == 1:
		print("------Stats Menu------")
		print("    (a) all")
		print("    (u) uniques")
		print("    (b) back")
		if selected_Ticker is not None:
			print("    (r) run data collector")
			print("    (c) clear")
		error(errorid)
	elif menuid == 2:
		print("------All Data Menu------")
		print("    (e) exchanges")
		print("    (c) catagories")
		print("    (n) catagory Number")
		print("    (b) back")
		error(errorid)
	elif menuid == 3:
		print("------Unique Menu------")
		print("    (s) stock")
		print("    (e) exchange")
		print("    (c) catagories")
		print("    (n) catagory Number")
		print("    (b) back")
		error(errorid)
	elif menuid == 4:
		print("------Stock Tickers Selection------")
		exchanges_display(0)
		error(errorid)
	elif menuid == 5:
		print("------Exchanges Selection------")
		exchanges_display(1)
		error(errorid)
	elif menuid == 6:
		print("------Catagory Selection------")
		exchanges_display(2)
		error(errorid)
	elif menuid == 7:
		print("------Number Catagory Selection------")
		exchanges_display(3)
		error(errorid)

def error(id):
	if(id == 0):
		print("\n\nPlease type a selection listed, thank you\n\n")

def all_stats():
	error = -1

	while True:
		os.system('clear')
		print_menu(2, error)
		error = -1
		#prompt
		mydata = input('Prompt :')

		if mydata == "e":
			exchanges_display(1)
			next = input('Type anything to continue :')
		elif mydata == "c":
			exchanges_display(2)
			next = input('Type anything to continue :')
		elif mydata == "n":
			exchanges_display(3)
			next = input('Type anything to continue :')
		elif mydata == "b":
			break;
		else:
			error = 0
	os.system('clear')
		

def unique_stats():
	global selected_Ticker
	error = -1

	selected_Ticker = None

	while True:
		os.system('clear')
		print_menu(3, error)
		error = -1

		#prompt
		mydata = input('Prompt :')

		if mydata == "s":
			while True:
				os.system('clear')
				print_menu(4, error)
				error = -1
				
				selection = input('Selected Stock :')

				if check_exists(selection, 0):
					selected_Ticker = Selected(selection, 0)
					break
				else:
					error = 0
		elif mydata == "e":
			while True:
				os.system('clear')
				print_menu(5, error)
				error = -1
				
				selection = input('Selected Exchange :')

				if check_exists(selection, 1):
					selected_Ticker = Selected(selection, 1)
					break
				else:
					error = 0
		elif mydata == "c":
			while True:
				os.system('clear')
				print_menu(6, error)
				error = -1
				
				selection = input('Selected Catagory:')

				if check_exists(selection, 2):
					selected_Ticker = Selected(selection, 2)
					break
				else:
					error = 0
		elif mydata == "n":
			while True:
				os.system('clear')
				print_menu(7, error)
				error = -1
				
				selection = input('Selected Catagory Number:')

				if check_exists(selection, 3):
					selected_Ticker = Selected(selection, 3)
					break
				else:
					error = 0
		elif mydata == "b":
			break;
		else:
			error = 0

		if selected_Ticker is not None:
			break



def display_stats():
	global selected_Ticker;
	error = -1

	while True:
		os.system('clear')
		print_menu(1, error)
		error = -1
		#prompt
		mydata = input('Prompt :')

		if mydata == "a":
			all_stats()
		elif mydata == "u":
			unique_stats()
		elif mydata == "c":
			selected_Ticker = None
		elif mydata == "r":
			get_historical_data()
		elif mydata == "b":
			break;
		else:
			error = 0

	os.system('clear')

####### End Menus #######

def main(argv):
	global selected_Ticker;
	global currentStocks;
	populate_stocks();
	error = -1

	selected_Ticker = None


	while True:	
		os.system('clear')
		print_menu(0, error)
		error = -1
		#prompt
		mydata = input('Prompt :')

		if mydata == "e":
			break;
		elif mydata == "l":
			break;
		elif mydata == "s":
			display_stats()
		else:
			error = 0

	os.system('clear')
	exit()

if __name__ == "__main__":
    main(sys.argv)