#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load push_in_git.py
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd
import csv
import Supervised_model
import Keyword_extraction
import Text_Summarization
def post_issue_git():
    Supervised_model.classification_model()
    dataset = pd.read_csv("dataset_output.csv")
    keywords = Keyword_extraction.keyword_extraction()
    #print(dataset.shape)    
    for i in range(3):
        #print(i)
        label = dataset['Label'][i]
        if label!="Uninteresting Comment":
            review = dataset['Review'][i]
            #print(label)
            #print(review)
            #print(keywords[i])
            title = "Issue regarding "+keywords[i]
            description = "As a user I feel that "+review+"\n\n"+"Labels: "+label+"\n"

            link = "https://github.com/cs17b005/Test/issues/new"
            driver = webdriver.Firefox()
            driver.get(link)

            login = driver.find_element_by_xpath("//input[@id='login_field']")
            login.send_keys('Rishitha2003')

            password = driver.find_element_by_xpath("//input[@id='password']")
            password.send_keys('E76BtZwcQEiURvr')

            driver.find_element_by_xpath("//input[@class='btn btn-primary btn-block']").click()

            inputElement = driver.find_element_by_xpath("//input[@class='form-control input-lg input-block input-contrast required title js-session-resumable js-similar-issues-search']")
            inputElement.send_keys(title)

            desc = driver.find_element_by_xpath("//textarea[@id='issue_body']")
            desc.send_keys(description)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

            # label = driver.find_element_by_xpath("//details[@id='labels-select-menu']/summary[@class='text-bold discussion-sidebar-heading discussion-sidebar-toggle hx_rsm-trigger']")
            # label.click()
            # label_type = driver.find_element_by_xpath("//input[@data-label-name='bug']")
            # label_type.click() #error here
            sleep(1)
            submit_button = driver.find_element_by_xpath("//div[@class='flex-items-center flex-justify-end mx-2 mb-2 px-0 d-none d-md-flex']/button[@type='submit']")
            submit_button.click()
            sleep(1)
            driver.close()
    driver.quit()


