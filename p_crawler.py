import os
import time
import requests
from selenium.webdriver.common.by import By
import concurrent.futures

class PCrawler:
  def __init__(self, ttype, save_pth, query, driver):
    print(f'\n\033[32;1m[+] Start Pinterest Crawler\033[0m')
    self.ttype = ttype
    self.save_pth = save_pth
    self.query = query
    self.driver = driver
    

  def getImgUrls(self, base_url):
    print(f'\033[32;1m[+] Get Img Urls\033[0m')
    org_imgs = set()
    
    self.driver.get(base_url)
    pre_total = 0
    cnt = 0
    times = 1
    while True:
      # print(f'\033[32;1m---> scroll: {times}\033[0m')
      time.sleep(5)
      img_urls = self.driver.find_elements(By.XPATH, '//div[@class="PinCard__imageWrapper"]/div')
      total_size = len(img_urls)
      if total_size == pre_total:
        cnt+=1
      else:
        pre_total = total_size
        cnt = 0
      if cnt==4:
        break

      if total_size!=0:
        for idx, img_url in enumerate(img_urls, start=1):
          print(f'\r\033[36;1m---> scroll: {times}\tProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
          try:
            img_type = img_url.get_attribute('data-test-id').split('-')[1]
            img_url = img_url.find_element(By.XPATH, './/img')
            org_img = img_url.get_attribute('src').replace('236x', 'originals')
            org_img = org_img if img_type == 'image' else org_img.replace('.jpg', '.gif')
            org_imgs.add(org_img)
          except Exception as e:
            pass
        # print()
        self.driver.execute_script(f'window.scrollTo({times * 2000},{(times + 1) * 2000})')	# window.scrollTo(start, end): js method, Used to scroll the web page to the specified position
        times+=1
      else:
        print(f'\033[31;1mNot Found\033[0m')
        break
    
    print('\n#org_imgs: ', len(org_imgs))
    print()
    return org_imgs


  def requestDownload(self, url, save_pth, filename):
    with requests.get(url, stream=True) as r:	# The request will be processed as a stream rather than downloading the entire file at once
      r.raise_for_status()	# If the HTTP request status code is not 200, an exception will be raised, otherwise the call will be ignored
      with open(os.path.join(save_pth, filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
          if chunk:
            f.write(chunk)


  def downloadImg(self, img, save_pth):
    filename = img.split('/')[-1]

    try:
      self.requestDownload(img, save_pth, filename)
    except requests.exceptions.HTTPError as e:
      try:
        self.requestDownload(img[:-4]+'.png', save_pth, filename)
      except requests.exceptions.HTTPError as e:
        try:
          self.requestDownload(img[:-4]+'.jpg', save_pth, filename)
        except requests.exceptions.HTTPError as e:
          print(f'\n\033[31;1mHTTP error occurred\033[0m')
    # except requests.exceptions.Timeout as e:
    # 	print(f'\n\033[31;1mTimeout error occurred: {e}\033[0m')
    # except requests.exceptions.RequestException as e:
    # 	print(f'\n\033[31;1mError occurred: {e}\033[0m')


  def downloadFile(self, save_pth, org_imgs):
    print(f'\n\033[32;1m[+] Start Download\033[0m')
    total_size = len(org_imgs)
    print('#img_urls: ', total_size)

    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = list()
      futures = [executor.submit(self.downloadImg, org_img, save_pth) for org_img in org_imgs]	# Submit the image download task to the threaded pool via the `executor.submit method`
      for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):	# Wait for all tasks to be completed
        try:
          future.result()	# When a picture is downloaded, the `future.result()` method will be called to get the result
          print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Download Successful\033[0m', end='')
        except Exception as e:
          print(f'\033[31;1mDownload failed: {e}\033[0m')
    print()
    print(f'\n\033[32;1m[+] Finish\033[0m')

  def boardCards(self, base_url):
    print(f'\n\033[32;1m[+] Get Board Cards\033[0m')
    self.driver.get(base_url)
    time.sleep(5)

    board_card_urls = set()
    for i in range(10):
      try:
        names = self.driver.find_elements(By.XPATH, '//div[@data-test-id="board-card"]/a')
        for name in names:
          href = name.get_attribute('href')
          board_card_urls.add(href)
        self.driver.execute_script(f'window.scrollTo({i * 2000},{(i + 1) * 2000})')
      except:
        break

    print('#board_cards: ', len(board_card_urls))
    return board_card_urls


  def startSearch(self):
    print(f'\n\033[32;1m[+] From Search\033[0m')
    org_imgs = list()
    if self.ttype.lower()=='pin':
      base_url = f'https://www.pinterest.com/search/pins/?q={self.query}&rs=typed'
      org_imgs.append(self.getImgUrls(base_url))
    elif self.ttype.lower()=='name_created':
      base_url = f'https://www.pinterest.com/{self.query}/_created/'
      org_imgs.append(self.getImgUrls(base_url))
    elif self.ttype.lower()=='name_saved':
      base_url = f'https://www.pinterest.com/{self.query}/_saved/'
      board_card_urls = self.boardCards(base_url)

      total_size = len(board_card_urls)
      for idx, board_card_url in enumerate(board_card_urls, start=1):
        print(f'\033[36;1mboard card: {idx}\033[0m')
        org_imgs.append(self.getImgUrls(board_card_url))
        time.sleep(30)
      print()

    org_imgs = [img for org_img in org_imgs for img in org_img]
    self.driver.quit()

    save_pth = os.path.join(self.save_pth, self.query.replace(' ', '_'))
    if len(org_imgs)!=0:
      os.makedirs(save_pth, exist_ok=True)
      self.downloadFile(save_pth, org_imgs)