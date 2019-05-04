from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

def get_article_list(i):
    page_url = 'https://www.rfa.org/mandarin/zhuanlan/yehuazhongnanhai/story_archive?b_start:int=' + str(i*30)
    html = requests.get(page_url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    sections = soup.find_all(attrs={'class': 'sectionteaser'})
    for sec in sections:
        title = sec.h2.a.get_text()
        date = sec.find(attrs={'id': 'story_date'}).string
        url = sec.h2.a['href']
        with open('article_list.txt', 'a', encoding='utf-8') as f:
            f.write('%s, %s, %s\n' % (title, date, url))
        with open('urls.txt', 'a', encoding='utf-8') as u:
            u.write(url + '\n')
    print('Index page %d saved!' % i)

def get_article(url):
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    main = soup.find(attrs={'id': 'storypagemaincol'})
    title = main.h1.string
    storytext = main.find(attrs={'id': 'storytext'})
    entry = ''
    for child in storytext.children:
        if child.string:
            entry = entry + child.string.strip('\n') + '\n'
    entry = entry.strip('\n').replace("'", '"')
    insert_sql = """INSERT INTO yehua_articles (title, entry) VALUES ('%s', '%s');\n""" % (title, entry)
    with open('yehua.sql', 'a', encoding='utf-8') as w:
        w.write(insert_sql)
    print('Article %s saved!' % title)

if __name__ == '__main__':
    for i in range(0, 28):
        get_article_list(i)
    r = open('urls.txt', 'r', encoding='utf-8')
    urls = r.readlines()
    for url in urls:
        get_article(url)
    r.close()
