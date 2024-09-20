import csv
import re
from bs4 import BeautifulSoup

def parse_html_to_csv(html_content, csv_filename):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title = soup.find('h3').text.strip()
    entries = []
    
    # 提取注释
    annotation_section = soup.find('div', class_='zscont')
    if annotation_section:
        annotation_text = annotation_section.find('p').text.strip()
        entries.append([title, "注释", annotation_text])
    
    # 提取条款
    article_sections = soup.find_all('p')
    for section in article_sections:
        text = section.text.strip()
        if text.startswith("第") and "条" in text:
            # current_section = text.split(" ")[0]
            # content = text.split(" ", 1)[1] if " " in text else text
            # entries.append([title, current_section, content])
            # 使用正则表达式提取条款编号
            match = re.match(r"(第[^条]*条)", text)
            if match:
                current_section = match.group(1)
                content = text[len(current_section):].strip()
                entries.append([title, current_section, content])
        else:
            # 如果当前段落不是新的条款，则将其视为前一条款的继续
            if entries and len(entries[-1]) == 3:
                entries[-1][2] += " " + text
    
    # 写入CSV文件
    with open(csv_filename, mode='w', newline='', encoding='gbk') as file:
        writer = csv.writer(file)
        for row in entries:
            writer.writerow(row)

    print(f"数据已写入 {csv_filename}")


