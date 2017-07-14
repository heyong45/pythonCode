import requests
from requests import Request, Session
from bs4 import BeautifulSoup
import os

reqHeader = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept': 'image/webp,image/*,*/*;q=0.8'}
def getMeiZiTu(path=None,startPage=1,endPage=2):
    """
    get girl picture from mzitu.com
    :param path: the path you choice to save picture
    :param startPage: the start page
    :param endPage: the end page
    :return: None
    """
    savePath='E:\\picture\\'
    if None != path:
        savePath = path
    if not os.path.exists(savePath):
        os.mkdir(savePath)

    url = "Http://mzitu.com/page/"
    # mainPage = requests.get(url, headers = reqHeader)
    # print (mainPage.text)
    for curPage in range(int(startPage),int(endPage)):
        curURL = url + str(curPage)
        curContext = requests.get(curURL,headers = reqHeader)
        soup = BeautifulSoup(curContext.text,'html.parser')
        preViewList = soup.find(id = 'pins').find_all('a',target='_blank')[1::2]
        for linkItem in preViewList:
            linkHref = linkItem['href']
            try:
                soup = BeautifulSoup(requests.get(linkHref).text,'html.parser')
                picCount = soup.find('div',class_='pagenavi').find_all('a')[4].get_text()
            except:
                continue
            print("URL:",linkHref," pageCount:",picCount)
            for picIndex in range(1,int(picCount)):
                picLink = linkHref + "/" + str(picIndex)
                try:
                    picPage = requests.get(picLink,headers = reqHeader)
                    soup = BeautifulSoup(picPage.text,'html.parser')
                    picPath = soup.find('div',class_='main-image').find('img')['src']
                    print(picPath)
                    picName = picPath.split('/')[-1]
                    f = open(os.path.join(savePath, picName), 'wb')
                    f.write(requests.get(picPath, headers=reqHeader).content)
                    f.flush()
                    f.close()
                except:
                    print("except")
                    continue

def getQiuShiBaiKe(file=None):
    """
    from QiuShiBaiKe get joke
    :param file: the file to save
    :return:
    """
    if None != file:
        saveFile = file
    else:
        saveFile = "xiaohua.txt"
    url = "https://www.qiushibaike.com/8hr/page/"
    mySesion = requests.Session()
    f = open(saveFile, '+a')
    for page in range(1,35):
        curURL = url + str(page)
        try:
            mainPage = mySesion.get(curURL,headers=reqHeader)
            soup = BeautifulSoup(mainPage.text,'html.parser')
            contentList = soup.find_all('div',class_='content')
            for item in contentList:
                print(item.span.get_text())
                txt=item.span.get_text()
                f.write(txt + '\n\n')
        except:
            continue
    f.close()

if __name__ == "__main__":
    #getMeiZiTu('E:\\2',3,4)
    getQiuShiBaiKe()