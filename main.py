import os
import time
from p_crawler import PCrawler
from tools.tools import readArgs, readConfig, getDriver


if __name__=='__main__':
	args = readArgs()
	search = args.search
	times = args.times if args.times<10 else 10
	ttype = args.ttype
	print('-'*20)
	print('Type: ', ttype)
	print('Search: ', search)
	print('#Times: ', times)
	print('-'*20)

	config = readConfig()
	save_pth = config['conf']['save_pth']
	print('save_pth: ', save_pth)
	
	driver = getDriver()

	pc = PCrawler(ttype, save_pth, search, times, driver)
	pc.startSearch()