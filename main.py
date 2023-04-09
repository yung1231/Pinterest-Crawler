from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import requests
from selenium.webdriver.common.by import By
import json
import time
import os

def getDriver():
  cr_options = ChromeOptions()
  cr_options.add_argument("--start-maximized")
  cr_options.add_argument("--incognito")

  driver = Chrome('./chromedriver.exe', options=cr_options)
  return driver


def downloadFile(save_pth, org_imgs):
	print(f'\033[32;1m[+] Start Download\033[0m')
	total_size = len(org_imgs)
	print('#img_urls: ', total_size)
	for idx, org_img in enumerate(org_imgs, start=1):
		filename = org_img.split('/')[-1]
		try:
			r = requests.get(org_img, stream=True,timeout=30)
			with open(save_pth+f'\{filename}', 'wb') as f:
				for chunk in r.iter_content():
					f.write(chunk)
			print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Download Successful\033[0m', end='')
		except Exception as e:
			print(e)
			print(f'\033[31;1mDownload failed\033[0m')


def getImgUrls(queries, driver):
	print('Window size: ', driver.get_window_size())   

	org_imgs = set()
	for query in queries:
		base_url = f'https://www.pinterest.com/search/pins/?q={query}&rs=typed'
		driver.get(base_url)
		time.sleep(3)

		for i in range(3):
			img_urls = driver.find_elements(By.XPATH, '//div[@data-test-id="pin-visual-wrapper"]/div[1]/div[1]/img')
			total_size = len(img_urls)
			print('#img_urls: ', total_size)
			for idx, img_url in enumerate(img_urls):
				print(f'\r\033[36;1mProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
				try:
					org_img = img_url.get_attribute('src').replace('236x', 'originals')	# 將縮圖換為原圖
					org_imgs.add(org_img)
				except Exception as e:
					print('e: ', e)
			print()
			driver.execute_script(f'window.scrollTo({i * 2000},{(i + 1) * 2000})')
			time.sleep(5)
	
	return org_imgs


if __name__=='__main__':
	print(f'\033[32;1m[+] Read Usage Data\033[0m')

	driver = getDriver()

	queries = [
		'蠢貓咪',
	]
	org_imgs = getImgUrls(queries, driver)
	print(len(org_imgs))

	save_pth = '.\download_1'
	os.makedirs(save_pth, exist_ok=True)
	downloadFile(save_pth, org_imgs)