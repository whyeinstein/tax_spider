from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
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

pagination_urls_file = 'pagination_urls.json'

def open_url(new_url):
    command = [
        'start',
        'msedge',
        new_url,
        '--remote-debugging-port=9223',
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


# 模拟鼠标缓慢移动到目标位置
def simulate_mouse_move(driver, element, speed=10):
    location = element.location
    size = element.size
    end_x = location['x'] + size['width'] / 2
    end_y = location['y'] + size['height'] / 2

    # 随机初始位置
    start_x, start_y = random.randint(0, 100), random.randint(0, 100)
    steps = random.randint(5, 10)  # 随机设置步数

    actions = ActionChains(driver)
    for i in range(steps):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        actions.move_by_offset(x - start_x, y - start_y).perform()
        start_x, start_y = x, y
        time.sleep(random.uniform(0.01, 0.05))  # 随机延迟

# 模拟滚动到元素位置
def scroll_smoothly_to_element(driver, element):
    scroll_distance = 800  # 每次滚动的距离
    while True:
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        target_position = element.location['y']

        if current_scroll_position >= target_position - scroll_distance:
            break
        
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0.2, 0.6))  # 随机停顿

    # 最后精准滚动到目标位置
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(random.uniform(0.5, 2))  # 随机停顿

# 从文件中读取已经收集到的 URL
def load_pagination_urls():
    if os.path.exists(pagination_urls_file):
        with open(pagination_urls_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 将收集到的 URL 保存到文件
def save_pagination_urls(pagination_urls):
    with open(pagination_urls_file, 'w', encoding='utf-8') as f:
        json.dump(pagination_urls, f, ensure_ascii=False, indent=4)


# 设置WebDriver路径
webdriver_path = 'D:\\drivers_individual\\edgedriver_win64\\msedgedriver.exe'  # 替换为你的EdgeDriver路径
edge_service = EdgeService(webdriver_path)

# 设置Edge选项
options = Options()
options.add_argument('--remote-debugging-port=9223')
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
pagination_urls = load_pagination_urls() 
read_page=False
# pagination_urls = []
# read_page=True


# 打开文件以写入模式，所有输出都会保存到文件中


with open("output_log.txt", "w", encoding="utf-8") as f:
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
        save_pagination_urls(pagination_urls)


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
            scroll_smoothly_to_element(driver, download_button)
            # 模拟滚动到按钮位置
            driver.execute_script("arguments[0].scrollIntoView();", download_button)
            time.sleep(random.uniform(0.5, 2))  # 随机停顿
            # 模拟鼠标移动到按钮位置
            actions = ActionChains(driver)
            actions.move_to_element(download_button).perform()
            time.sleep(random.uniform(0.5, 2))  # 随机停顿
            # 模拟点击按钮
            download_button.click()

            # # 获取下载按钮
            # download_button = driver.find_element(By.CSS_SELECTOR, '.xxgk-download-box a')

            # # 模拟滚动到按钮位置
            # scroll_smoothly_to_element(driver, download_button)

            # # 模拟鼠标移动到按钮位置
            # simulate_mouse_move(driver, download_button)

            # # 模拟悬停一段时间
            # time.sleep(random.uniform(1, 3))

            # # 模拟点击按钮
            # download_button.click()
    
        except Exception as e:
            f.write(f"No download button found on page {law_url}: {e}\n")
            print(f"No download button found on page {law_url}: {e}\n")


        # 等待文件下载完成
        if wait_for_download(download_directory, file_name):
            f.write(f"{file_name} 下载完成\n")
            print(f"{file_name} 下载完成\n")
        else:
            f.write(f"{file_name} 下载超时\n")
            print(f"{file_name} 下载超时\n")


# 关闭浏览器
driver.quit()