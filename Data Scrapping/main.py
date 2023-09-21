import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import time
import multiprocessing
from datetime import datetime


def convert_to_sqlite_date(date_str):
    try:
        dt_obj = datetime.strptime(date_str, '%d %b %Y')
        sqlite_date = dt_obj.strftime('%Y-%m-%d')
        return sqlite_date
    except ValueError:
        return None
def data_scrape(site):
    # r=requests.get(url)
    # #print(r) if the output is (<Response [200]> then you can scrape the website)
    # soup= BeautifulSoup(r.text,"lxml")
    # table=soup.find("table",class_=Class)
    # #print(table)
    # header=[]
    # head=table.findAll("th")
    # for i in head:
    #     i=i.text
    #     header.append(i)
    # df=pd.DataFrame(columns=header)
    # rows=table.findAll("tr")
    # n=0
    # for i in rows[1:]:
    #     data = i.findAll("td")
    #     row_data=[tr.text for tr in data]
    #     if len(row_data)==1:
    #         continue
    #     while n<len(row_data):
    #         row_data[n]=row_data[n].replace('\n'or '\t','')
    #         row_data[n] = row_data[n].replace('   ', '')
    #         row_data[n] = row_data[n].replace("'", ' ')
    #         row_data[n]=row_data[n].strip()
    #         n+=1
    #
    #     # if row_data[1].find('('):
    #     #     row_data[1]=row_data[1].split('(')[1].strip(')')
    #     #     row_data[1]=convert_to_sqlite_date(row_data[1])
    #     # if row_data[2].find('('):
    #     #     row_data[2]=row_data[2].split('(')[1].strip(')')
    #     row_data[5] = convert_to_sqlite_date(row_data[5])
    #
    #
    #     n=0
    #     l=len(df)
    #     df.loc[l+1]=row_data
    #
    # if len(df.columns) == 3:
    #     lst=[]
    #     for i in range (0,len(df)):
    #         lst.append('-')
    #     df['Extra']=lst
    df = pd.read_html('https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates')
    df=df[0]
    conn=sqlite3.connect('final.db')
    c=conn.cursor()
    create_table=("CREATE TABLE IF NOT EXISTS {}(Product TEXT,EOS TEXT,\
                   EOL TEXT) ".format(site))
    c.execute(create_table)
    for d in df.itertuples():
        insert_table=("INSERT INTO {} VALUES('{}','{}','{}')".format(site,d[1],d[2],d[3]))
        c.execute(insert_table)
    conn.commit()



p1=multiprocessing.Process(target=data_scrape,args=['paloalto'])
#p2=multiprocessing.Process(target=data_scrape,args=['https://endoflife.date/panos','Palo_cortex','lifecycle'])
if __name__== '__main__':
    p1.start()
  #  p2.start()
    p1.join()
   # p2.join()

finish=time.perf_counter()
print("time taken to complete :",finish)