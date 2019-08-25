from bs4 import BeautifulSoup
import requests
import webbrowser
import threading
from multiprocessing.pool import ThreadPool


def BBCCyberNews():
    res = requests.get("https://www.bbc.com/news/topics/cz4pr2gd85qt/cyber-security")
    soup = BeautifulSoup(res.text,'lxml')

    news_box = soup.find('div', {'class' : 'gel-layout__item gel-3/5@l'})
    news_article = news_box.find_all('article')                                      #The top headline objects

    file_to_insert_text = open("BBCnews.txt","w+")                                   #file that I will write into
    file_to_insert_text.write("                 Latest Cyber News From BBC: \n\n")
    i=1

    for news in news_article:
        z = str(i)+". "
        file_to_insert_text.write(z)
        headline = news.find('header')

        file_to_insert_text.write((headline.text).encode("utf-8"))
        file_to_insert_text.write("\n\n")

        body = news.find('div', {'class' : 'gel-layout__item gel-5/8@l'})
        inner_body = body.find('p', {'class' : 'qa-sty-summary'})
        file_to_insert_text.write((inner_body.text).encode("utf-8"))
        file_to_insert_text.write("\n\n\n\n\n\n\n")
        i+=1
        if(i>3):
                break

    return 'BBCnews.txt'


def CywareNews():

    res = requests.get("https://cyware.com/cyber-security-news-articles")
    soup = BeautifulSoup(res.text, 'lxml')

    news_box = soup.find('div', {'class': 'col-sm-12 animated fadeInUp'})
    news_article = soup.findAll('div', {'class': 'post post-v2 format-image news-card get-id'}) #all headline objects

    file_to_insert_text = open("Cyware.txt", "w+")                       # file that I will write into
    file_to_insert_text.write("                 Latest Cyber News From CywareNews: \n\n")
    i = 1

    for news in news_article:
        z = str(i) + ". "
        file_to_insert_text.write(z)
        headline = news.find('h2', {'class': 'post-title post-v2-title text-image'})

        file_to_insert_text.write((headline.text).encode("utf-8"))

        file_to_insert_text.write("\n\n\n\n\n\n\n")
        i += 1
        if (i > 3):
            break

    return 'Cyware.txt'


def ThreatPostVulnarbilities():
    res = requests.get("https://threatpost.com/category/vulnerabilities/")
    soup = BeautifulSoup(res.text, 'lxml')

    news_box = soup.find('div', {'class': 'o-row c-border-layout@md'})
    news_article = soup.findAll('div', {'class': 'o-col-4@md'})  # all headline objects

    file_to_insert_text = open("Vulnerbilities.txt", "w+")  # file that I will write into
    file_to_insert_text.write("                 Latest Vulnerbility News From ThreatPost: \n\n")
    i = 1
    for news in news_article:
        z = str(i) + ". "
        file_to_insert_text.write(z)
        headline = news.find('h2', {'class': 'c-card__title'})

        file_to_insert_text.write((headline.text).encode("utf-8"))
        file_to_insert_text.write("\n\n")


        inner_body = news.find('p')
        file_to_insert_text.write((inner_body.text).encode("utf-8"))

        file_to_insert_text.write("\n\n\n\n\n\n\n")
        i += 1
        if (i > 3):
            break

    return 'Vulnerbilities.txt'


def Combine_files(filenames):

    with open('CyberNews.txt', 'w') as CyberNews:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    CyberNews.write(line)

if __name__== "__main__":
    results = []
    pool = ThreadPool(3)

    results.append(pool.apply_async(BBCCyberNews,()))
    results.append(pool.apply_async(CywareNews,()))
    results.append(pool.apply_async(ThreatPostVulnarbilities,()))
    results = [r.get() for r in results]

    pool.close()
    pool.join()

    Combine_files(results)
    SendNewsByMail()