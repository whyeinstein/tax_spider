from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import random
import subprocess
import time


pagination_urls_file = 'pagination_urls.json'

def open_url_chrome(new_url):
    command = [
        'start',
        'chrome',
        new_url,
        '--remote-debugging-port=9224',
        '--user-data-dir=D:\\selenium\\ChromeProfile'  # 替换为你的用户数据目录路径
    ]
    subprocess.run(command, shell=True)

def open_url_edge(new_url):
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
        if os.path.exists(file_path) and not file_path.endswith('.crdownload'):
            return True
        time.sleep(1)
    return False

def simulate_mouse_move(driver, element, speed=10):
    location = element.location
    size = element.size
    end_x = location['x'] + size['width'] / 2
    end_y = location['y'] + size['height'] / 2

    start_x, start_y = random.randint(0, 100), random.randint(0, 100)
    steps = random.randint(5, 10)

    actions = ActionChains(driver)
    for i in range(steps):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        actions.move_by_offset(x - start_x, y - start_y).perform()
        start_x, start_y = x, y
        time.sleep(random.uniform(0.01, 0.05))

def scroll_smoothly_to_element(driver, element):
    scroll_distance = 800
    while True:
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        target_position = element.location['y']

        if current_scroll_position >= target_position - scroll_distance:
            break
        
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0.2, 0.6))

    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(random.uniform(0.5, 2))

def load_pagination_urls():
    if os.path.exists(pagination_urls_file):
        with open(pagination_urls_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_pagination_urls(pagination_urls):
    with open(pagination_urls_file, 'w', encoding='utf-8') as f:
        json.dump(pagination_urls, f, ensure_ascii=False, indent=4)