from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd
import csv

def post_issue_git():
    link = "https://github.com/Rishitha2003/SampleRepository/issues/new"
    driver = webdriver.Firefox()
    driver.get(link)

    login = driver.find_element_by_xpath("//input[@id='login_field']")
    login.send_keys('Rishitha2003')

    password = driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys('Alekhya#1')

    driver.find_element_by_xpath("//input[@class='btn btn-primary btn-block']").click()

    inputElement = driver.find_element_by_xpath("//input[@class='form-control input-lg input-block input-contrast required title js-session-resumable js-similar-issues-search']")
    inputElement.send_keys('New Test Issue')

    desc = driver.find_element_by_xpath("//textarea[@id='issue_body']")
    desc.send_keys("This test description is automatically written using geckodriver")

    label = driver.find_element_by_xpath("summary[@class='text-bold discussion-sidebar-heading discussion-sidebar-toggle hx_rsm-trigger']")
    label.click()

    


    # inputElement.send_keys(Keys.ENTER)
    
    sleep(1)
    
post_issue_git()
    
    