from spyder import GetAll, WriteSomething
from tqdm import tqdm

bass = GetAll() 
kick = WriteSomething()

root = 'http://www.zhongdi168.com/'
for large_title, href in tqdm(bass.get_title_text_url(root), desc = "总体爬取进度：", total = 8):
    if large_title != '种植资讯':
        target = 'http://www.zhongdi168.com/' + str(href)
        for i in tqdm(range(1, bass.get_page_num(target) + 1), desc = '子页面爬取进度'):
            targets = 'http://www.zhongdi168.com/' + str(href) + 'list-' + str(i)
            t_u = bass.get_title_url(target)
            for title, url in t_u:
                contents = bass.get_contents(url)
                path =  str(large_title) + '/' + 'page' + str(i)
                kick.write_contents(title, contents, path)
    else:
        break