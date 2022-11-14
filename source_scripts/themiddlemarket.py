import re
import os
import sys
import os.path
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath("../labeling"))
from labeling import *



def main_middlemarket(driver,data_set,today_date,filename,database,batch):
    url = 'https://www.themiddlemarket.com/latest-news'    
    driver.get(url)
    driver.implicitly_wait(100)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find('div',{'class':'latest-news__sidebar-list'})
    all_items = soup.find_all('a')
     
    all_articles = []
    article = {}
    
    for i in range(len(all_items)):
        header = all_items[i].find('span',{'class':'latest-news__sidebar-item--title'}).text
        article['title'] = cleanhtml(header)
        print(article['title'])
        try :
            pubDate =  all_items[i].find('span',{'class':'latest-news__sidebar-item--date meta-text'}).text
            pubDate = datetime.strptime(pubDate, '%B %d, %Y')
            pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
            
        except:
            break
        article['pubDate']=pubDate
        article['link'] = all_items[i]['href']
        article['description']  = article['title']
        article['source'] = "Middlemarket M&A"
        article['batch'] =batch
        all_articles.append(article)
        article = {}

    with open(database, "a", encoding='utf8') as rf:
        now = datetime.now()
        timenow = now.strftime("%m/%d/%Y %H:%M:%S")
        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']) :
                    article = label_creator(article)
                    nkw = '(No Keywords detect)'
                    if article['label_for_article_name'] == nkw and article['label_description'] == nkw:
                        pass
                    else:
                        arti = timenow+ ','+ article['pubDate'] + ',' +article['source'] +','+article['title']+","+ str(article['link']) + \
                        ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + ',' \
                        + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"]+','+article['batch']
                        
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
         
