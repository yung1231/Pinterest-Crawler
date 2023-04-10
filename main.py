import os
import configparser
from argparse import ArgumentParser
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
import requests
from selenium.webdriver.common.by import By
import concurrent.futures

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
  ser = Service(".\chromedriver.exe")
  
  driver = Chrome(service=ser, options=opts)
  print('Window size: ', driver.get_window_size()) 
   
  return driver


def getImgUrls(query, scroll, driver):
	org_imgs = set()
	base_url = f'https://www.pinterest.com/search/pins/?q={query}&rs=typed'
	driver.get(base_url)
	time.sleep(3)

	for i in range(scroll):
		print(f'\033[32;1m---> scroll: {i+1}\033[0m')
		img_urls = driver.find_elements(By.XPATH, '//div[@data-test-id="pin-visual-wrapper"]/div[1]/div[1]/img')
		total_size = len(img_urls)
		print('#img_urls: ', total_size)
		if total_size!=0:
			for idx, img_url in enumerate(img_urls, start=1):
				print(f'\r\033[36;1mProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
				try:
					org_img = img_url.get_attribute('src').replace('236x', 'originals')	# Replace the thumbnail with the original image
					org_imgs.add(org_img)
				except Exception as e:
					print('e: ', e)
			print()
			driver.execute_script(f'window.scrollTo({i * 2000},{(i + 1) * 2000})')	# window.scrollTo(start, end): js method, Used to scroll the web page to the specified position
			time.sleep(3)
		else:
			print(f'\033[31;1mNot Found\033[0m')
			break
	
	return org_imgs


def downloadImg(img, save_pth):
	filename = img.split('/')[-1]

	try:
		with requests.get(img, stream=True) as r:	# The request will be processed as a stream rather than downloading the entire file at once
			r.raise_for_status()	# If the HTTP request status code is not 200, an exception will be raised, otherwise the call will be ignored
			with open(os.path.join(save_pth, filename), 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192):
					if chunk:
						f.write(chunk)
	except requests.exceptions.HTTPError as e:
		print(f'\n\033[31;1mHTTP error occurred: {e}\033[0m')
	except requests.exceptions.Timeout as e:
		print(f'\n\033[31;1mTimeout error occurred: {e}\033[0m')
	except requests.exceptions.RequestException as e:
		print(f'\n\033[31;1mError occurred: {e}\033[0m')


def downloadFile(save_pth, org_imgs):
	print(f'\033[32;1m[+] Start Download\033[0m')
	total_size = len(org_imgs)
	print('#img_urls: ', total_size)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = list()
		for org_img in org_imgs:
			future = executor.submit(downloadImg, org_img, save_pth)	# Submit the image download task to the threaded pool via the `executor.submit method`
			futures.append(future)
		for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):	# Wait for all tasks to be completed
			try:
				future.result()	# When a picture is downloaded, the `future.result()` method will be called to get the result
				print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Download Successful\033[0m', end='')
			except Exception as e:
				print('e: ', e)
				print(f'\033[31;1mDownload failed\033[0m')
	print()


if __name__=='__main__':
	print(f'\n\033[32;1m[+] Read Args\033[0m')
	args = readArgs()
	query = args.query
	scroll = args.scroll

	print(f'\n\033[32;1m[+] Read Config\033[0m')
	config = readConfig()
	save_pth = config['conf']['save_pth']

	print(f'\n\033[32;1m[+] Get Driver\033[0m')
	driver = getDriver()
	time.sleep(5)

	print(f'\n\033[32;1m[+] Start Search\033[0m')
	print('-'*20)
	print('Searching: ', query)
	print('#Scroll: ', scroll)
	print('-'*20)
	org_imgs = getImgUrls(query, scroll, driver)

	print(f'\n\033[32;1m[+] Start Download\033[0m')
	save_pth = os.path.join(save_pth, query.replace(' ', '_'))
	if len(org_imgs)!=0:
		os.makedirs(save_pth, exist_ok=True)
		print('#imgs: ', len(org_imgs))
		downloadFile(save_pth, org_imgs)
	print(f'\n\033[32;1m[+] Finish\033[0m')