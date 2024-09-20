from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import random
import subprocess
import os
import json
import parse_html
import spider_tool

# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options



# 设置WebDriver路径
webdriver_path = 'D:\\drivers_individual\\edgedriver_win64\\msedgedriver.exe'  # 替换为你的EdgeDriver路径
edge_service = EdgeService(webdriver_path)

# 设置Edge选项
options = Options()
options.add_argument('--remote-debugging-port=9223')
options.add_argument('--user-data-dir=D:\\selenium\\EdgeProfile')  # 替换为你的用户数据目录路径

# 设置 Edge 浏览器的下载路径
download_directory = "D:\\Visual Studio Workspace\\爬虫\\Spider1\\doc\\法律"

# 启动Edge浏览器
base_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/listflfg_fg.html"
spec_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212256/content.html"
spider_tool.open_url_edge(base_url)

# 启动Edge浏览器
driver = webdriver.Edge(service=edge_service, options=options)



# # 设置WebDriver路径
# webdriver_path = '.\\chromedriver-win64\\chromedriver.exe'  # 替换为你的ChromeDriver路径
# chrome_service = ChromeService(webdriver_path)

# # 设置Chrome选项
# options = Options()
# options.add_argument('--remote-debugging-port=9224')
# options.add_argument('--user-data-dir=D:\\selenium\\ChromeProfile')  # 替换为你的用户数据目录路径

# # 设置 Chrome 浏览器的下载路径
# download_directory = "D:\\Visual Studio Workspace\\爬虫\\Spider1\\doc\\法律"

# # 启动Chrome浏览器
# base_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/listflfg_fg.html"
# spec_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212256/content.html"
# spider_tool.open_url(base_url)

# # 启动Chrome浏览器
# driver = webdriver.Chrome(service=chrome_service, options=options)


# 初始化分页处理
pagination_urls = spider_tool.load_pagination_urls() 
read_page=False
# pagination_urls = []
# read_page=True


# 打开文件以写入模式，所有输出都会保存到文件中


with open("output_log.txt", "w+", encoding="utf-8") as f:
    if read_page is True:
        while True:
            time.sleep(5)
            # 获取当前页面的所有条目链接
            links_elements = driver.find_elements(By.CSS_SELECTOR, '.list ul li p.bt a')
            links = [link.get_attribute('href') for link in links_elements]
            pagination_urls.extend(links)

            # 打印当前页的所有链接
            f.write(f"当前页的链接: {links}\n")
            print(f"当前页的链接: {links}")


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
                f.write(f"Error navigating to next page: {e}\n")
                print(f"Error navigating to next page: {e}\n")

                break

        f.write(f"最终收集到的URL数量: {len(pagination_urls)}\n")
        print(f"最终收集到的URL数量: {len(pagination_urls)}\n")
        spider_tool.save_pagination_urls(pagination_urls)


    count = 0
    # 定义重试次数
    max_retries = 3
    
    # 遍历每个链接
    for law_url in pagination_urls:
        count += 1
        f.write(f"{str(count)} cur url: {law_url}\n")
        print(f"{str(count)} cur url: {law_url}\n")

        retries = 0
        load_status = False
        while retries < max_retries:
            try:
                # driver.get(law_url)
                # driver.get("https://huaweicloud.csdn.net/")

                # 模拟用户在地址栏输入URL
                # driver.get("about:blank")  # 先打开一个空白页面
                # time.sleep(1)  # 给浏览器一些缓冲时间
                # driver.find_element(By.TAG_NAME, 'body').send_keys(law_url + Keys.ENTER)
                driver.execute_script("window.location.href = arguments[0];", law_url)
            
                # 等待页面加载
                time.sleep(10)  # 可以根据页面的响应速度调整这个时间
            
                # 等待下载按钮和页面元素出现
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.xxgk-download-box a')))
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detials.contentLeft h3')))
            
                # 成功加载页面，跳出重试循环
                load_status = True
                break
            except TimeoutException:
                retries += 1
                f.write(f"超时异常，第 {retries} 次重试: {law_url}\n")
                print(f"超时异常，第 {retries} 次重试: {law_url}\n")
            
                if retries == max_retries:
                    f.write(f"加载页面失败，跳过: {law_url}\n")
                    print(f"加载页面失败，跳过: {law_url}\n")
                    break  # 达到重试次数后跳过此 URL            
        

        if not load_status:
            continue

        # 直接解析html
        # cur_html = driver.page_source
        # parse_html.parse_html_to_csv(cur_html,"law_output.csv")
        # time.sleep(15)

        # 获取标题
        title_element = driver.find_element(By.CSS_SELECTOR, 'div.detials.contentLeft h3')
        title_text = title_element.text
        file_name = title_text + ".doc"

        # 提取法律信息
        content = driver.find_element(By.TAG_NAME, 'body').text
        f.write(f"标题: {title_text}\n")  # 内容只显示前100个字符作为示例
        print(f"标题: {title_text}\n")  # 内容只显示前100个字符作为示例


        # 模拟下载操作
        try:
            # 获取下载按钮
            download_button = driver.find_element(By.CSS_SELECTOR, '.xxgk-download-box a')
            # 模拟滚动到按钮位置
            spider_tool.scroll_smoothly_to_element(driver, download_button)
            # 模拟滚动到按钮位置
            driver.execute_script("arguments[0].scrollIntoView();", download_button)
            time.sleep(random.uniform(0.5, 2))  # 随机停顿
            # 模拟鼠标移动到按钮位置
            actions = ActionChains(driver)
            actions.move_to_element(download_button).perform()
            time.sleep(random.uniform(0.5, 2))  # 随机停顿
            # 模拟点击按钮
            download_button.click()
    
        except Exception as e:
            f.write(f"No download button found on page {law_url}: {e}\n")
            print(f"No download button found on page {law_url}: {e}\n")


        # 等待文件下载完成
        if spider_tool.wait_for_download(download_directory, file_name):
            f.write(f"{file_name} 下载完成\n")
            print(f"{file_name} 下载完成\n")
        else:
            f.write(f"{file_name} 下载超时\n")
            print(f"{file_name} 下载超时\n")


# 关闭浏览器
driver.quit()

