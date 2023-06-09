import requests
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'cookie': '_zap=767d1454-0c7b-46ec-b8da-050d5a0aaa93; d_c0=AJBYkt_ELhaPTvUczNjxCN3WPO_TKQiTx-g=|1673875738; YD00517437729195%3AWM_TID=fHzdMBWVSQdFEBVVUEKBd4vJ5WGpVZim; __snaker__id=Oe8P9kngAdJ0kSku; YD00517437729195%3AWM_NI=4%2Bkpvm%2FesYRJSfCIzdORb6iQOD3VQcqIeqW57OBiS%2FxiHN1q3EcqovIeh7HHeSpy96wTRRbhQCoyWibuYetQ2HpM5HTE%2F2McOU%2BG1dT0frYs8DhcHYla%2FAl46%2FlykLSHTzY%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eea6d14e929caf8ef664ad928ea2d84f828a9eacc44593eaabb0b86f8f87a78ef92af0fea7c3b92af8f5a591f567edbbbdbad14291ba8daaf9708d8eaed7ec5b8d9cfdb7d469b397ab92d63ff5918e8ad225bcb788afb47bf19bad92ee7e8bbba8d8cb44a78dc09abc3eb58c9eb3e164939da19ad663a2ab9786f75bf298c0aeb844989be1d3d0698d8be5a8b47098f0aa93dc79fc9ca884cb53b0bfe1a2ef40f6f1a49aea4891989c9bdc37e2a3; q_c1=9ace7044e7864329a3417a733deaaa28|1676035079000|1676035079000; _xsrf=2b4c9541-00fd-4628-93b3-b603d4cb61b4; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1683878661,1684306574,1684419604,1684485167; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1684485222; z_c0=2|1:0|10:1684485226|4:z_c0|80:MS4xMXk5VENBQUFBQUFtQUFBQVlBSlZUUmFDVTJXTWYxTk5LX3k5OU5mbkNrSkpSdjFLRXJlckN3PT0=|3ef9a66f04b9321866d2885264234f0ce543b1b618e9ecf7c4713f5309f385b4; KLBRSID=3d7feb8a094c905a519e532f6843365f|1684485243|1684485169',
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

font_path = 'C:/Windows/Fonts/msyh.ttc'  # 设置微软雅黑字体
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
