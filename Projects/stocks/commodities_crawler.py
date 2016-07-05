import finsymbols

sp500 = finsymbols.get_sp500_symbols()

for entry in sp500:
	symbol = entry["symbol"]
	os.system("get_stocks_data.py "+symbol+" nonverbose")
	print("done with: " + symbol)