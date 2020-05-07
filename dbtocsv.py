#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pymysql
import python_to_mysql

def fetch_table_data(table_name):
    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
    cnx = pymysql.connect(
        host='localhost',
        database='ReqkitDB',
        user='root',
        password='Alekhya#1'
    )
    cursor = cnx.cursor()
    try:
        cursor.execute('select * from ' + table_name)
        list1 = []
        for x in cursor:
            list1.append(x)
    except:
        python_to_mysql.store_in_db()
        
    cnx.close()

    return list1
    


# In[9]:


def export(table_name):
    list1 = fetch_table_data(table_name)
    with open(table_name+'.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['Name','Review','UpVotes','Rating','Date'])
        for row in list1:
            csv_out.writerow(row)


# In[10]:


# Tables to be exported
# export('VLCdb', name, appid, git)

