from bs4 import BeautifulSoup

path = '../paper-html/P19-1001/test-1.html'
soup = BeautifulSoup(open(path, encoding='utf-8'), features='lxml')
css = str(soup.style)
# print(css)
font_array = css.split('.ft')
# class_hub = [[], [], []]  # 0表示小字部分，1表示正文，2表示标题
_dict = dict()
for s in font_array:
    index1 = s.find('font-size:')
    if index1 > 0:
        name = s[:index1 - 1]
        index2 = s.find('px;')
        size = int(s[index1 + 10:index2])
        _dict['ft' + name] = size
print(str(_dict))
body = soup.find_all('p')
_content = []  # 内容集合，加个md有的#号，我先做个样子，具体样式再商量看
temp_content = ''  # 暂时存储正文，以每次检测到标题为隔断，作者信息当成正文我觉得没啥问题（第一段；对于小字就忽略处理
# Todo 一些特殊部位字体大小会是个问题，作文本处理的时候从Abstract开始我觉得应该可以避免处理这个丑陋的东西
for p in body:
    # _str = str(p)
    # print(p.attrs['class'])
    size = _dict.get(p.attrs['class'][0])
    content = str(p.text)
    if size <= 11:
        continue
    if size >= 15:
        _content.append('###  ' + temp_content)
        _content.append('#  ' + content)
        temp_content = ''
        continue
    temp_content += content
    # index1 = max(0, content.find('>'))
    # index2 = max(-1, content.find('</'))
    # text = content[index1 + 1:index2]
    # if text <= 10:
    #     print("**********")
    # Todo 对content内容处理，连接，大小的安排
    # print(content[content.find('>'):])
    # print(_dict.get(p.attrs['class'][0]))
# print(css.index('ft00'))
_content.append('### ' + temp_content)
for c in _content:
    print(c)
