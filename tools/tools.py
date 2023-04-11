from argparse import ArgumentParser
import configparser
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

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
	opts.add_argument("start-maximized")
	opts.add_argument("disable-infobars")
	opts.add_experimental_option("excludeSwitches", ["enable-automation"])
	opts.add_experimental_option('useAutomationExtension', False)
	ser = Service("./chromedriver.exe")
	driver = Chrome(service=ser, options=opts)

	stealth(driver,
					user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
					languages= ["en-US", "en"],
					vendor=  "Google Inc.",
					platform=  "Win32",
					webgl_vendor=  "Intel Inc.",
					renderer=  "Intel Iris OpenGL Engine",
					fix_hairline= False,
					run_on_insecure_origins= False,
	)
	print('Window size: ', driver.get_window_size()) 
		
	return driver