import csv
from bs4 import BeautifulSoup

def parse_html_to_csv(html_content, csv_filename):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title = soup.find('h3').text.strip()
    parsed_data = []
    
    # 提取注释
    annotation_section = soup.find('div', class_='zscont')
    if annotation_section:
        annotation_text = annotation_section.find('p').text.strip()
        parsed_data.append([title, "注释", annotation_text])
    
    # 提取条款
    article_sections = soup.find_all('p', style="text-indent: 2em;")
    for section in article_sections:
        text = section.text.strip()
        if text.startswith("第") and "条" in text:
            current_section = text.split(" ")[0]
            content = text.split(" ", 1)[1] if " " in text else text
            parsed_data.append([title, current_section, content])
        else:
            # 如果当前段落不是新的条款，则将其视为前一条款的继续
            if parsed_data and len(parsed_data[-1]) == 3:
                parsed_data[-1][2] += " " + text
    
    # 写入CSV文件
    with open(csv_filename, mode='w', newline='', encoding='gbk') as file:
        writer = csv.writer(file)
        for row in parsed_data:
            writer.writerow(row)

    print(f"数据已写入 {csv_filename}")

# 从文件中读取HTML内容
with open('tt.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML并写入CSV
csv_filename = 'law_output.csv'
parse_html_to_csv(html_content, csv_filename)

# import csv
# from bs4 import BeautifulSoup
# from docx import Document

# def parse_html_to_csv(html_content, csv_filename):
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     title = soup.find('h3').text.strip()
#     parsed_data = []
    
#     # 提取注释
#     annotation_section = soup.find('div', class_='zscont')
#     if annotation_section:
#         annotation_text = annotation_section.find('p').text.strip()
#         parsed_data.append([title, "注释", annotation_text])
    
#     # 提取条款
#     article_sections = soup.find_all('p', style="text-indent: 2em;")
#     for section in article_sections:
#         text = section.text.strip()
#         if text.startswith("第") and "条" in text:
#             current_section = text.split(" ")[0]
#             content = text.split(" ", 1)[1] if " " in text else text
#             parsed_data.append([title, current_section, content])
#         else:
#             # 如果当前段落不是新的条款，则将其视为前一条款的继续
#             if parsed_data and len(parsed_data[-1]) == 3:
#                 parsed_data[-1][2] += " " + text
    
#     # 写入CSV文件
#     with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         for row in parsed_data:
#             writer.writerow(row)

#     print(f"数据已写入 {csv_filename}")

# # 从Word文档中读取内容
# def read_docx_to_html(docx_filename):
#     doc = Document(docx_filename)
#     full_text = []
#     for para in doc.paragraphs:
#         full_text.append(para.text)
#     return '\n'.join(full_text)

# # 读取Word文档并转换为HTML
# docx_filename = 'tt.docx'  # 请确保您的文件扩展名为 .docx
# html_content = read_docx_to_html(docx_filename)

# # 解析HTML并写入CSV
# csv_filename = 'law_output.csv'
# parse_html_to_csv(html_content, csv_filename)