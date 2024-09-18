import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import time

# 设置WebDriver路径
webdriver_path = 'D:\\drivers_individual\\edgedriver_win64\\msedgedriver.exe'  # 替换为你的EdgeDriver路径
edge_service = EdgeService(webdriver_path)

# 设置Edge选项
options = Options()
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--user-data-dir=D:\\selenium\\EdgeProfile')  # 替换为你的用户数据目录路径

# 启动Edge浏览器
spec_url = "https://fgk.chinatax.gov.cn/zcfgk/c100009/c5212256/content.html"
command = [
    'start',
    'msedge',
    spec_url,
    '--remote-debugging-port=9222',
    '--user-data-dir=D:\\selenium\\EdgeProfile'  # 替换为你的用户数据目录路径
]
subprocess.run(command, shell=True)

# 初始化WebDriver
driver = webdriver.Edge(service=edge_service, options=options)

# 等待页面加载
time.sleep(5)  # 根据网络情况调整等待时间

# 提取法律信息
content = driver.find_element(By.TAG_NAME, 'body').text

# 打印提取的信息
print(content)

# 关闭浏览器
driver.quit()