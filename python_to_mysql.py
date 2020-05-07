#!/usr/bin/env python
# coding: utf-8

# In[4]:


#conda install -c conda-forge pymysql


# In[2]:


import csv
import pymysql
import vlc_scraper_1
def store_in_db(name, appid, git):
	mydb = pymysql.connect(host='localhost',
		user='root',
		passwd='Alekhya#1',
		db='ReqkitDB')

	cursor = mydb.cursor()
	cursor.execute("SHOW TABLES")

	for x in cursor:
		print(x)    
	try:
		cursor.execute("""CREATE TABLE VLCdb(Name VARCHAR(255),
										   Review VARCHAR(2048) NOT NULL, 
										   UpVotes VARCHAR(255), 
										   Rating VARCHAR(255), 
										   Date VARCHAR(255),
										   UNIQUE(Name, Review, UpVotes, Rating, Date))""")
	except Exception as e:
		print(e)
	try:
		with open('processed.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, skipinitialspace=True)
			row_count = 0
			for row in reader:
				if(row_count==0):
					row_count+=1
				else:
					print(len(row),row)
					try:
						cursor.execute('INSERT INTO VLCdb(Name, Review, UpVotes, Rating, Date ) VALUES("%s", "%s", "%s", %s, %s)',row)
					except Exception:
						continue
	except:
		vlc_scraper_1.scrape_all_reviews(name,appid,git)
	mydb.commit()
	cursor.close()
	print("Done")

