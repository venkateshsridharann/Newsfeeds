import os
import sys 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

sys.path.append(os.path.abspath("../labeling"))
from ml_label import *

sys.path.append(os.path.abspath("../source_scripts"))
from axios import *
from finSME import *
from prnews import *
from VCNews import *
from cb_news import *
from fortune import *
from benzinga import *
from vcaonline import *
from pehub_new import *
from techcrunch import *
from venturebeat import *
from businesswire import *
from globenewswire import *
from PEprofessional import *
from businessjournals import *

sys.path.append(os.path.abspath("../boto3"))
from download_from_aws import *
from upload_to_aws import *

options = Options()
options.headless = True

# linux (after getting geckodriver place in main file)
# driver = webdriver.Firefox(executable_path="./geckodriver.exe", options=options)

# windows 
driver = webdriver.Firefox(executable_path="./geckodriver.exe", options=options)

today_date = str(datetime.now())[:10]
data_set = set()

if not os.path.exists('../tmp'):
    os.makedirs('../tmp')
    
filename = '../tmp/previously_seen_{}.csv'.format(today_date[:7])
database = '../tmp/database_{}.csv'.format(today_date)
bankruptcy_ipo = '../tmp/bankruptcy_ipo_{}.csv'.format(today_date)

download_from_s3(today_date)

# calculating batch number based on previous runs
if os.path.isfile(database):
    file = open(database, 'r') 
    data = file.read()
    data = [x for x in data.split('\n') if x!=''][-1]
    batch = [x for x in data.split(',') if x!=''][-1]
    batch = str(int(batch)+1)
else :
    batch = '1'

# adding previously seen as a set
if os.path.isfile(filename):
    file = open(filename, 'r') 
    data = file.read().split('\n')
    # for tab seperated inputs 
    for x in data:
        x= x.split(',')
        if isinstance(x, list) and len(x)== 3:
            x = x[2]
        elif isinstance(x, list) and len(x)>3:
            x = ",".join(x[2:])
        else:
            continue
        data_set.add(x)
    file.close()

# making blank file with headers for start of day
if not os.path.isfile(database):
        file = open(database, 'w')
        file.write("Date_Collected,Date_Published,Source,Article_Name,Article_Link,Description,Keyword_label_article_name,Keyword_label_description,ER_Spacy,ML_label_Article_Name,Batch\n")
        file.close() 
if not os.path.isfile(bankruptcy_ipo):
        file = open(bankruptcy_ipo, 'w')
        file.write("Date_Collected,Date_Published,Source,Article_Name,Article_Link,Description,Keyword_label_article_name,Keyword_label_description,ER_Spacy,ML_label_Article_Name,Batch\n")
        file.close() 

# calling all source scripts sequentially
main_FinSME(data_set,today_date,filename,database,batch)
main_businesswire(data_set,today_date,filename,database,batch)
main_techcrunch(data_set,today_date,filename,database,batch)
main_VCN(data_set,today_date,filename,database,batch)
main_venturebeat(data_set,today_date,filename,database,batch)
main_prnews(data_set,today_date,filename,database,batch)
main_businessjournals(data_set,today_date,filename,database,batch)
main_vcaonline(data_set,today_date,filename,database,batch)    
main_globenewswire(data_set,today_date,filename,database,batch)
main_pehub_new(driver,data_set,today_date,filename,database,batch)
        # ## benzinga needs fixes
        # ## main_benzinga(data_set,today_date,filename,database)
        # # if first_time_today == True:
main_cb_news(driver,data_set,today_date,filename,database,batch)
        # ## not working needs changes
        # ## main_fortune(driver,today_date,database)
        # ## peprofessonal changed
        # ## main_pep(driver,data_set,today_date,filename,database)
        # # axios changed
        # ## main_axios(driver,data_set,today_date,filename,database)    
ml_label(today_date)
upload_to_s3(today_date)
driver.quit()
