import requests, os
from bs4 import BeautifulSoup

class GetAll:
    def format_target(self, target):    #用于解析所给页面的url
        req = requests.get(target)
        req.encoding = 'GBK'
        html = req.text
        bs = BeautifulSoup(html, 'lxml')
        return bs

    def get_title_url(self, target):    #获取所给页面的url和标题的generator
        res = self.format_target(target)
        urls = res.find_all('dt', class_ = 'xs2')
        for mass in urls:
            title = mass.find('a')
            url = title.get('href')
            if title.string.find('?') != -1:
                title.string = title.string.replace('?', '？')
            yield title.string, url

    def get_contents(self, target):  #返回内容页面内容所在的标签整体
        res = self.format_target(target)
        contents = res.find('td', id = 'article_content')
        return contents

    def get_title_text_url(self, target):   #返回页面的大标题以及对应的url的generator
        res = self.format_target(target)
        urls = res.find_all('span', class_ = 'titletext')
        for mass in urls:
            title = mass.find('a')
            url = title.get('href')
            yield title.string, url

    def get_page_num(self, target): #返回页面总数
        res = self.format_target(target)
        pages = res.find('div', class_ = 'pg')
        pages = pages.label.span['title']
        pages = pages[1:-2]
        return int(pages)

class WriteSomething(GetAll):
    def write_contents(self, title, contents, path = '.'):  #创建以title为名，content为内容，path为路径的.txt文件（默认为当前路径）
        if path != '.':
            try:
                os.makedirs(path)
            except FileExistsError:
                pass
        with open(path + '/' + title + '.txt', 'w+', encoding = 'UTF-8') as f1:
            for content in contents.strings:    #contents.strings用于提取标签中的多个字符串
                f1.write(str(content))
                f1.write('\n')