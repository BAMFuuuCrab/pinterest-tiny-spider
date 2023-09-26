from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import os
import requests
from concurrent.futures import ThreadPoolExecutor, wait
from tqdm import tqdm
  
param = ''
max = 0

print('tips: sipder running')

# 读取txt 第一行目标id 第二行获取数量

with open("./target.txt", "r") as file:
    lines = file.readlines()
    param += lines[0].strip()
    max = int(lines[1].strip())
    
first = True

count = 0
href = f'https://www.pinterest.com/pin/{param}/'
options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(href)
# imgCount = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="pin-count"]')

imgList = []
scroll = 0
triger = True

def getImg():
    global imgList, scroll, count, triger, first
    scroll = scroll + 450
    print(scroll)
   
    if first:
      sleep(5)
      first = False
    else:
      sleep(0.5)
    
    driver.execute_script("window.scrollBy(0, 450);")
    imgs = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="pin"] img')
    incount = 0
    for i in tqdm(imgs):
        try:
            url = ''
            url = i.get_attribute('src')
            if url != '' and (url not in imgList and len(imgList) <= max):
                incount += 1
                imgList.append(url)
                count += 1
            if len(imgList) >= max:
                  break
        except:
          break
    # if (incount == 0):
    #       triger = False

def download(src):
    url = src.replace('236x','originals')
    name = url.split('/')[::-1][0].split('.jpg')[0].split('--')[0]
    jpg = requests.get(url)
    path = f'./download/{param}'
    if not os.path.isdir(path):
      os.mkdir(path)
    f = open(f'{path}/{name}.jpg', 'wb')
    f.write(jpg.content)
    f.close()
    
# executor = ThreadPoolExecutor()

# point = 0


# 这部分注释的内容为每搜集100条下载地址就下载一次，当前已弃用
# while triger:
# 	# print(imgList)
# 	lastCount = 0
# 	print(len(imgList))
# 	getImg()
    
# 	if (len(imgList) >= 100):
# 		ratio = len(imgList) // 100
# 		f_list = []
# 		print('ratio: ')
# 		print(ratio)          
# 		if (100 * ratio > point):
# 				downloadArr = imgList[point:100 * ratio]
# 				print('下载数组: ')
# 				print(downloadArr)
# 				for url in downloadArr:
# 					future = executor.submit(download, url)
# 					f_list.append(future)
# 				wait(f_list)
# 				point = 100 * ratio
# 				f_list.clear()
# 	if driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.scrollHeight;"):
# 		break
# 	try:
# 		if len(imgList) >= max:
# 			break
# 	except:
# 			break
    
executor = ThreadPoolExecutor()

point = 0
lastCount = 0

while triger:
	# print(imgList)
	
	print(len(imgList))
	getImg()
	if lastCount != len(imgList):
		f_list = []   
		downloadArr = imgList[lastCount:]
		for url in downloadArr:
			future = executor.submit(download, url)
			f_list.append(future)
		wait(f_list)
		lastCount = len(imgList)
		f_list.clear()
  # 判断当前页面是否滚动到底部
	if driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.scrollHeight;"):
		break
	try:
		if len(imgList) >= max:
			break
	except:
			break