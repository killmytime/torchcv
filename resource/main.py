# import xml.dom.minidom as minidom
import os

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup


# 遍历html文件的dom树，h3为论文题目
# h5和p为章节标题及次级标题
# p为正文，但要处理link，image和table
# 换行处的处理：有些有'-'连接，有些没有；要区分是否是一个单词
# 公式

def title_found(text, titles):
    '''
    :param text: 一段文本
    :param titles: 从html中提取的标题列表
    :return: 文本是否是出现标题
    '''

    # 论文题目和引用要和其他的标题要分开，一般其他标题都有标号，避免误判
    if text in titles['h1']:
        return True, 'h1'
    if text in ['Abstract', 'References']:
        return True, 'h2'

    index = text.find(' ') + 1
    if index:
        for k in titles.keys():
            if not k == 'h1':
                if text[index:] in titles[k]:
                    return True, k
    return False, ''


def recursively_extract_text(element, titles, md_path):
    '''
    :param element: xml最外层的元素
    :param titles: 从html中提取的标题列表
    :param md_path: 输出md文件的路径
    :return:
    '''

    with open(md_path, 'w', encoding='utf-8') as of:
        title_form = {'h1': '## ', 'h2': '### ', 'h3': '#### '}
        figure_occurred = table_occurred = False

        for child in element.iter():
            if child.tag == '{adobe:ns:meta/}xmpmeta':  # xml文件中的meta data，与正文无关，排除
                child.clear()
            found, hclass = title_found(str(child.text).strip(), titles)
            if found:  # 是标题
                # print(child.tag, ' ', child.text, ' ', hclass)
                of.write('\n' + title_form[hclass] + child.text.strip() + '\n')
            else:
                if child.tag == 'Figure':
                    figure_occurred = True
                    figure_src = child.find('ImageData').attrib['src']
                    of.write('\n\n![alt text](' + figure_src + ')\n')
                    child.clear()
                elif child.tag == 'Link':
                    of.write(' ' + ' '.join(child.text.split()) + ' ')
                elif child.tag == 'Table':  # 这段对于表格目前识别不好
                    table_occurred = True
                    print('\n\n')
                    for i in range(len(child)):
                        row = child[i]
                        of.write('\n|')
                        for col in row:
                            of.write(' ' + col.text + ' |')
                        if i == 0:  # 表头
                            of.write('\n|')
                            for j in range(len(row)):
                                of.write(' - |')
                        if i == len(child) - 1:
                            of.write('\n')
                    child.clear()  # 删除子元素，防止后面遍历到
                elif child.text:
                    of.write(' '.join(child.text.split()))
                    if figure_occurred and child.text.startswith('Figure'):  # 图片下面的说明文字
                        of.write('\n\n')
                        figure_occurred = False
                    if table_occurred and child.text.startswith('Table'):  # 表格下面的说明文字
                        of.write('\n\n')
                        table_occurred = False
                if child.tail:
                    of.write(' '.join(child.tail.split()))


def extract_titles(html_path):
    '''
    :param html_path: html文件路径
    :return: 论文中的标题列表
    '''
    soup = BeautifulSoup(open(html_path, encoding='utf-8'), features='lxml')
    body = soup.body
    titles = {'h1': [], 'h2': [], 'h3': []}  # 经观察，论文中题目是h1，一级标题是h2，二级标题是h3，不会有更深的层级

    res = body.find_all('h1')
    if res:
        for r in res:
            titles['h1'].append(r.get_text())
    res = body.find_all('h2')
    if res:
        abstract_occurred = False
        for r in res:
            if r.get_text() == 'Abstract':
                abstract_occurred = True
            if abstract_occurred:
                text = r.get_text()
                if str.isdigit(text[0]):
                    index = text.find(' ') + 1
                    text = text[index:]
                titles['h2'].append(text)
    res = body.find_all('h3')
    if res:
        for r in res:
            titles['h3'].append(r.get_text())
    return titles


def extract_single(xml_path, html_path, md_path):
    print('File:  ', xml_path)
    tree = ET.parse(xml_path, parser=ET.XMLParser(encoding='utf-8'))
    root = tree.getroot()
    print(root[0].tag)
    titles = extract_titles(html_path)
    for k in titles.keys():
        print(k, ' ', titles[k])
    recursively_extract_text(root, titles, md_path)


if __name__ == "__main__":
    xml_dir = '../paper-xml/'
    html_dir = '../paper-html/'
    md_dir = '../paper-md/'
    files = os.listdir(xml_dir)
    # for f in files:
    #     fname = f[:-4]
    #     try:
    #         extract_single(xml_dir + fname + '.xml', html_dir + fname + '.html', md_dir + fname + '.md')
    #     except Exception as e:
    #         print(e)

    fname = 'P19-1036'
    extract_single(xml_dir + fname + '.xml', html_dir + fname + '.html', md_dir + fname + '.md')

    # with open('../paper-md/' + fname + '.md', 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         print(line)