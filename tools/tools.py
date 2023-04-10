from argparse import ArgumentParser
import configparser
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

def readArgs():
	parser = ArgumentParser()
	parser.add_argument("-q", "--query", dest="query", type=str, required=True, help="Keyword you want to query")
	parser.add_argument("-s", "--scroll-times", dest="scroll", type=int, required=True, help="Number of page scrolls")

	args = parser.parse_args()

	return args


def readConfig():
	config = configparser.ConfigParser()
	config.read('./config.cfg')

	return config

def getDriver():
	opts = ChromeOptions()
	opts.add_argument("--start-maximized")
	opts.add_argument("--incognito")
	# opts.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
	ser = Service("./chromedriver.exe")

	driver = Chrome(service=ser, options=opts)
	print('Window size: ', driver.get_window_size()) 
		
	return driver