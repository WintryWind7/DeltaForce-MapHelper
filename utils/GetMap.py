from selenium import webdriver
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import By
import requests
import os
from urllib.parse import urlparse

driver = webdriver.Edge()
driver.get('https://df.qq.com/cp/a20240729directory/index.html')
time.sleep(3)

download_list = os.listdir('../resource/origin/')

def getmap():
    global download_list
    # 遍历 img 标签并下载图片
    try:
        elements = driver.find_elements(By.XPATH, "//div[@class='leaflet-layer ']/div")
        for div in elements:
            images = div.find_elements(By.TAG_NAME, "img")
            if len(images) > 10:
                break
            else:
                continue
    except:
        print("error")
        time.sleep(1)
        return 0
    try:
        for index, img in enumerate(images):
            # 获取 img 标签的 src 属性
            src = img.get_attribute("src")

            if src:  # 确保 src 属性存在
                file_name = os.path.basename(urlparse(src).path)
                if file_name not in download_list:
                    download_list.append(file_name)
                else:
                    continue
                try:

                    # 下载图片
                    response = requests.get(src, stream=True)
                    response.raise_for_status()  # 检查 HTTP 请求是否成功

                    # 保存图片到本地
                    image_path = os.path.join("../resource/origin", file_name)  # 保存为 jpg 格式
                    with open(image_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)

                    print(f"成功下载图片：{image_path}")
                except Exception as e:
                    print(f"下载失败：{src}，错误信息：{e}")
    except:
        time.sleep(1)
        return 0
time.sleep(35)
for i in range(500):
    getmap()
    print("Done for one")
    time.sleep(1)


