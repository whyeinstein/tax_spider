from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import subprocess
import os

def open_url(new_url):
    command = [
        'start',
        'msedge',
        new_url,
        '--remote-debugging-port=9222',
        '--user-data-dir=D:\\selenium\\EdgeProfile'  # 替换为你的用户数据目录路径
    ]
    subprocess.run(command, shell=True)

def wait_for_download(download_directory, file_name, timeout=60):
    file_path = os.path.join(download_directory, file_name)
    end_time = time.time() + timeout
    while time.time() < end_time:
        # 检查文件是否存在并且下载完成（没有 .crdownload 后缀）
        if os.path.exists(file_path) and not file_path.endswith('.crdownload'):
            return True
        time.sleep(1)
    return False



# 设置WebDriver路径
webdriver_path = 'D:\\drivers_individual\\edgedriver_win64\\msedgedriver.exe'  # 替换为你的EdgeDriver路径
edge_service = EdgeService(webdriver_path)

# 设置Edge选项
options = Options()
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--user-data-dir=D:\\selenium\\EdgeProfile')  # 替换为你的用户数据目录路径

# 设置 Edge 浏览器的下载路径
download_directory = "D:\\Visual Studio Workspace\\爬虫\\Spider1\\doc\\法律"
# prefs = {
#     'download.default_directory': download_directory,
#     'profile.default_content_setting_values.automatic_downloads': 1  # 允许自动下载
# }
# options.add_experimental_option('prefs', prefs)


# 启动Edge浏览器
base_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/listflfg_fg.html"
spec_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212256/content.html"
# command = [
#     'start',
#     'msedge',
#     base_url,
#     '--remote-debugging-port=9222',
#     '--user-data-dir=D:\\selenium\\EdgeProfile'  # 替换为你的用户数据目录路径
# ]
# subprocess.run(command, shell=True)
open_url(base_url)

# 启动Edge浏览器
driver = webdriver.Edge(service=edge_service, options=options)

# 初始化分页处理
pagination_urls = []
while True:
    # next = input("next: ")

    # 获取当前页面的所有条目链接
    time.sleep(5)
    links_elements = driver.find_elements(By.CSS_SELECTOR, '.list ul li p.bt a')
    links = [link.get_attribute('href') for link in links_elements]
    pagination_urls.extend(links)


    # 打印当前页的所有链接
    # print(links)

    try:
        # 查找并点击“下一页”按钮
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.layui-laypage-next')))
        next_button = driver.find_element(By.CSS_SELECTOR, '.layui-laypage-next')
        if "layui-disabled" in next_button.get_attribute("class"):
            break  # 如果“下一页”按钮被禁用，说明已经到最后一页
        next_button.click()
        
        # 等待下一页加载完成
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list ul li p.bt a')))
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

print(f"最终收集到的URL数量: {len(pagination_urls)}")
zzz= input("end: ")

# 等待页面加载
# time.sleep(5)
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list ul li p.bt a')))

# 获取所有条目链接
# links_elements = driver.find_elements(By.CSS_SELECTOR, '.list ul li p.bt a')
# links = [link.get_attribute('href') for link in links_elements]

# print(links)

count = 0
# 遍历每个链接
for law_url  in pagination_urls:
    count = count + 1
    # 获取链接地址
    # law_url = link.get_attribute('href')
    print(str(count) + "cur url: " + law_url)
    driver.get(law_url)

    
    # 等待页面加载
    # x=input("waiting")
    time.sleep(10)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.xxgk-download-box a')))
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detials.contentLeft h3')))


    # 获取标题
    title_element = driver.find_element(By.CSS_SELECTOR, 'div.detials.contentLeft h3')
    title_text = title_element.text
    file_name = title_text + ".doc"


    # 提取法律信息
    content = driver.find_element(By.TAG_NAME, 'body').text

    # 打印提取的信息
    print("content")

    # 模拟下载操作（根据实际情况调整选择器）
    try:
        # 获取下载按钮
        download_button = driver.find_element(By.CSS_SELECTOR, '.xxgk-download-box a')
        # 模拟滚动到按钮位置
        driver.execute_script("arguments[0].scrollIntoView();", download_button)
        time.sleep(random.uniform(0.5, 1.5))  # 随机停顿
        # 模拟鼠标移动到按钮位置
        actions = ActionChains(driver)
        actions.move_to_element(download_button).perform()
        time.sleep(random.uniform(0.5, 1.5))  # 随机停顿
        # 模拟点击按钮
        download_button.click()
    except:
        print(f"No download button found on page {law_url}")

    # 等待下载完成（根据实际情况调整时间或使用其他方法检测下载完成）
    # z=input("waiting download")
    time.sleep(10)
    # 等待文件下载完成
    if wait_for_download(download_directory, file_name):
        print(file_name+"下载完成")
    else:
        print(file_name+"下载超时")


# 关闭浏览器
driver.quit()