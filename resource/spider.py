import requests
from lxml import html
import urllib3

# 从acl上爬取论文,计算机语言协会第57届论文集
if __name__ == '__main__':
    url = 'https://www.aclweb.org/anthology/events/acl-2019/'
    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    links = tree.xpath(
        '//div[@id="p19-1"]/p[@class="d-sm-flex align-items-stretch"]/span[@class="d-block mr-2 text-nowrap list-button-row"]/a[@class="badge badge-primary align-middle mr-1"]/@href')

    dir = '../paper-pdf/'

    http_conn = urllib3.PoolManager()
    for i in range(len(links)):  # 661 papers
        if i == 0:  # 第一个是目录，排除
            continue
        if i == 101:
            break
        response = http_conn.request('GET', links[i])
        with open(dir + links[i].split('/')[-1] + '.pdf', 'wb')as of:
            of.write(response.data)
        print(links[i])
