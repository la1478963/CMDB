from bs4 import BeautifulSoup
import requests


def get_title(url):
    response=requests.get(url)
    # print(response.text)
    obj=BeautifulSoup(response.text,'html.parser')
    title=obj.find('title').text
    meta=obj.find('meta',attrs={'name':'description'}).get('content')
    return(title,meta)


# JG=get_title('http://music.163.com/#/song?id=188057')

