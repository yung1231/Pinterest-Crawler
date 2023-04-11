import os
import time
from tools.tools import readArgs, readConfig, getDriver
import requests
from selenium.webdriver.common.by import By
import concurrent.futures


def getImgUrls(query, scroll, driver):
	org_imgs = set()
	base_url = f'https://www.pinterest.com/search/pins/?q={query}&rs=typed'
	driver.get(base_url)

	for i in range(scroll):
		print(f'\033[32;1m---> scroll: {i+1}\033[0m')
		time.sleep(3)
		img_urls = driver.find_elements(By.XPATH, '//div[@class="PinCard__imageWrapper"]/div')
		total_size = len(img_urls)
		# print('#img_urls: ', total_size)
		if total_size!=0:
			for idx, img_url in enumerate(img_urls, start=1):
				print(f'\r\033[36;1mProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
				try:
					img_type = img_url.get_attribute('data-test-id').split('-')[1]
					img_url = img_url.find_element(By.XPATH, './/img')
					org_img = img_url.get_attribute('src').replace('236x', 'originals')
					org_img = org_img if img_type == 'image' else org_img.replace('.jpg', '.gif')
					org_imgs.add(org_img)
				except Exception as e:
					pass
			print()
			driver.execute_script(f'window.scrollTo({i * 2000},{(i + 1) * 2000})')	# window.scrollTo(start, end): js method, Used to scroll the web page to the specified position
		else:
			print(f'\033[31;1mNot Found\033[0m')
			break
	
	return org_imgs


def requestDownload(url, save_pth, filename):
	with requests.get(url, stream=True) as r:	# The request will be processed as a stream rather than downloading the entire file at once
		r.raise_for_status()	# If the HTTP request status code is not 200, an exception will be raised, otherwise the call will be ignored
		with open(os.path.join(save_pth, filename), 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192):
				if chunk:
					f.write(chunk)


def downloadImg(img, save_pth):
	filename = img.split('/')[-1]

	try:
		requestDownload(img, save_pth, filename)
	except requests.exceptions.HTTPError as e:
		try:
			requestDownload(img[:-4]+'.png', save_pth, filename)
		except requests.exceptions.HTTPError as e:
			try:
				requestDownload(img[:-4]+'.jpg', save_pth, filename)
			except requests.exceptions.HTTPError as e:
				print(f'\n\033[31;1mHTTP error occurred\033[0m')
	# except requests.exceptions.Timeout as e:
	# 	print(f'\n\033[31;1mTimeout error occurred: {e}\033[0m')
	# except requests.exceptions.RequestException as e:
	# 	print(f'\n\033[31;1mError occurred: {e}\033[0m')


def downloadFile(save_pth, org_imgs):
	total_size = len(org_imgs)
	print('#img_urls: ', total_size)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = list()
		futures = [executor.submit(downloadImg, org_img, save_pth) for org_img in org_imgs]	# Submit the image download task to the threaded pool via the `executor.submit method`
		for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):	# Wait for all tasks to be completed
			try:
				future.result()	# When a picture is downloaded, the `future.result()` method will be called to get the result
				print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Download Successful\033[0m', end='')
			except Exception as e:
				print(f'\033[31;1mDownload failed: {e}\033[0m')
	print()


if __name__=='__main__':
	print(f'\n\033[32;1m[+] Read Args\033[0m')
	args = readArgs()
	query = args.query
	scroll = args.scroll if args.scroll<10 else 10

	print(f'\n\033[32;1m[+] Read Config\033[0m')
	config = readConfig()
	save_pth = config['conf']['save_pth']
	print('save_pth: ', save_pth)

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
		downloadFile(save_pth, org_imgs)
	print(f'\n\033[32;1m[+] Finish\033[0m')