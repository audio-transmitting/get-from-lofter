import urllib
import urllib.request
import nltk
from bs4 import BeautifulSoup
import time
import glob
import codecs
import io
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

def get_sep_file_lofter(folder = "output/"):
    with open('links.txt', 'r') as f:
        links = f.readlines()

    counter = 0
    l = len(links)

    while counter<l:
        url = links[counter]
        counter +=1
        text = get_text(url)
        name = text.split('\n')[0].replace('|', '·').replace('/', '·').replace('*', '×').replace('<', '').replace('>', '')
        name = name.split('-')[0]
        text = text.split('归档\n')[-1]
        text = text.split('< 上一篇')[0]
        text = text.split('下一篇 >')[0]
        text = text.split('热度 (')[0]
        print(name, ": ", url)
        name = folder + name
        text = ''.join([url, '\n', '\n', text])
        try:
            with open(name+".txt", 'w+', encoding="utf-8") as f:
                f.write(text)

            paragraph_num = len(text.split('\n'))
            if paragraph_num<20:
                with open(name+".txt", 'r', encoding="utf-8") as f:
                    text = f.read()
                text = text.replace('　　', '\n')
                with open(name+".txt", 'w+', encoding="utf-8") as f:
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
            #url = 'https' + i.split('https')[-1]
            url = i.split(' ')[-1]
            o.append(url)
            #print(url)    
    with open('links.txt', 'w') as f:
        f.write(''.join(o))
    print("Clear, {} in total.".format(len(o)))

def convert_to_md(
    src_folder = "./output/"
    ):
    file_list = glob.glob(src_folder+"*.txt")
    print(len(file_list), "files in total.")
    for filename in file_list:
        try:
            with io.open(filename, 'r', encoding='utf8') as f:
                text = f.read()
            output_path = filename.replace(".txt", ".md")
            # process Unicode text
            with io.open(output_path, 'w+', encoding='utf8') as f:
                text = ''.join(text).replace('\n', '<br/>\n')
                text = text.replace('~', '——')
                f.write(text)
        except:
            print(filename) 
            print(output_path) 


if __name__ == '__main__': 
    #get_links()
    #get_sep_file_lofter()
    convert_to_md()


