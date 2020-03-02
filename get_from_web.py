import urllib
import urllib.request
import nltk
from bs4 import BeautifulSoup
import time

# 右键 审查元素 在console中输入
'''
for(var a of document.getElementsByTagName('a')){
console.log(a.href)
}
'''
# 抓取页面方法，调用该方法返回抓取到数据
def read_pageHtml(url):
    file = urllib.request.urlopen(url)
    data = file.read()
    return data

# 将数据生成txt文件方法 传入保存文件路径 storagePath 以及文件数据 data
def storageToLocalFiles(storagePath, data):
    fhandle = open(storagePath,"wb")
    fhandle.write(data)
    fhandle.close()


def get_text(url):        
    url = url.replace('\n','')
    n = url.split('/')[-1]
    html = read_pageHtml(url)  
    soup = BeautifulSoup(html, features="lxml")
    raw = soup.get_text()
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def get_sep_file_lofter():
    with open('links.txt', 'r') as f:
        links = f.readlines()

    counter = 0
    l = len(links)

    while counter<l:
        url = links[counter]
        counter +=1
        text = get_text(url)
        text = text.split('RSS')[-1]
        text = text.split('热度')[0]

        name = text.split('\n')[1].replace('|', '·').replace('/', '·').replace('*', '×')+".txt"
        print(name, url)

        try:
            with open(name, 'w+', encoding="utf-8") as f:
                f.write(text)
        except:            
            with open(str(time.time())+'.txt', 'w+', encoding="utf-8") as f:
                f.write(text)

        print('{}/{}'.format(counter, len(links)))

def get_links():    
    with open('links.txt', 'r') as f:
        links = f.readlines()
    o = []
    for i in links:
        if '.lofter.com/post/' in i:
            url = 'https' + i.split('https')[-1]
            o.append(url)
            #print(url)    
    with open('links.txt', 'w') as f:
        f.write(''.join(o))
    print("Clear.")


if __name__ == '__main__': 
    get_links()
    get_sep_file_lofter()


