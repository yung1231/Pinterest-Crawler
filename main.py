import os
import time
from p_crawler import PCrawler
from tools.tools import readArgs, readConfig, getDriver


if __name__=='__main__':
	args = readArgs()
	search = args.search
	ttype = args.ttype
	print('-'*20)
	print('Type: ', ttype)
	print('Search: ', search)
	print('-'*20)

	config = readConfig()
	save_pth = config['conf']['save_pth']+f'\\{ttype}'
	print('save_pth: ', save_pth)
	
	driver = getDriver()

	pc = PCrawler(ttype, save_pth, search, driver)
	pc.startSearch()