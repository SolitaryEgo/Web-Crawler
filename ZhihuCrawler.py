import requests
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from lxml import etree

headers = {
    'user-agent': '用自己的agent',
    'cookie': '用自己的cookie',
}
url = 'https://www.zhihu.com/hot'

def get_question_num(url, headers):
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)  # 构造一个XPath解析对象并对HTML文本进行自动修正。
    result = html.xpath("//section[@class='HotItem']")  # 选取所有section子元素，不管位置
    question_list = []  # 问题列表（问题ID，问题标题）

    for question in result[0:20]:  # 获取热榜前二十
        number = question.xpath("./div[@class='HotItem-index']//text()")[0].strip()  # 问题ID
        title = question.xpath(".//h2[@class='HotItem-title']/text()")[0].strip()  # 问题标题
        excerpt_elements = question.xpath(".//p[@class='HotItem-excerpt']/text()")  # 问题简介
        excerpt = excerpt_elements[0].strip() if excerpt_elements else ""  # 检查列表是否为空
        href = question.xpath("./div[@class='HotItem-content']/a/@href")[0].strip()  # 问题链接
        question_num = href.split('/')[-1]  # 取切割的最后一块，即问题ID
        question_list.append([question_num, title, excerpt])
        print(number, '\n', title, '\n', href, '\n', excerpt)

    with open('知乎热榜.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question ID', 'Title', 'Excerpt'])
        writer.writerows(question_list)

    return question_list


question_data = get_question_num(url, headers)

titles = [data[1] for data in question_data]  # 提取可视化的问题标题

font_path = 'C:/Windows/Fonts/msyh.ttc'  # 设置微软雅黑字体，看自己电脑字体位置
font_prop = FontProperties(fname=font_path)  # 设置字体属性

# 创建一个问题标题的条形图
plt.figure(figsize=(10, 6))
plt.bar(range(len(titles)), titles)
plt.xticks(range(len(titles)), titles, rotation=90, fontproperties=font_prop)
plt.xlabel('Question Titles', fontproperties=font_prop)
plt.ylabel('Count', fontproperties=font_prop)
plt.title('Top 20 Questions on Zhihu', fontproperties=font_prop)
plt.tight_layout()
plt.show()
