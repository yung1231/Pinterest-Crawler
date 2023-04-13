from argparse import ArgumentParser, ArgumentTypeError
import configparser
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

def valid_input(value):
	if value.lower() not in ['pin', 'name_created', 'name_saved']:
		raise ArgumentTypeError(f"Invalid input '{value}', must be 'pin' or 'name'")
	return value

def readArgs():
	print(f'\n\033[32;1m[+] Read Args\033[0m')
	parser = ArgumentParser()
	parser.add_argument("-t", "--type", dest="ttype", type=valid_input, required=True, help="Search by 'pin' or 'name_created' or 'name_saved'(name is a string starting after @)")
	parser.add_argument("-s", "--search", dest="search", type=str, required=True, help="Keyword you want to query")
	# parser.add_argument("-t", "--times", dest="times", type=int, required=True, help="Number of page scrolls")

	args = parser.parse_args()

	return args


def readConfig():
	print(f'\n\033[32;1m[+] Read Config\033[0m')
	config = configparser.ConfigParser()
	config.read('./config.cfg')

	return config

def getDriver():
	print(f'\n\033[32;1m[+] Get Driver\033[0m')
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