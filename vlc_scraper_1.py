from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd
import csv

def scrape_all_reviews(Name, ID1, URL):
	print(Name, ID1, URL)
	l1 = "https://play.google.com/store/apps/details?id="
	id_1 = l1+ID1
	link = id_1+"&hl=en&showAllReviews=true"
	print("Final URL: ", link)

	driver = webdriver.Firefox()
	driver.get(link)

	Ptitle = driver.find_element_by_css_selector('.AHFaub span').text

	print(Ptitle)


	sleep(1)

	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		sleep(1)
		lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		if lastCount==lenOfPage:
			try:
				n = 20
				driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
				while(n>0):
					n = n -1
					lastCount = lenOfPage
					sleep(2)
					lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
					if(lenOfPage==lastCount):
						driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
			except NameError: 
				print("here3")
			else:
				match=True
	Name = []
	Review = []
	upvotes = []
	rating = []
	date = []
	count = 1

	people = driver.find_elements_by_xpath('//span[@class="X43Kjb"]')
	for person in people:
		name = person.text
		Name.append(name)
		count+=1
	print(count)

	count = 1
	
	reviews_full = driver.find_elements_by_xpath('//div[@jscontroller="LVJlx"]/span[@jsname="fbQN7e"]')
	reviews_half = driver.find_elements_by_xpath('//span[@jsname="bN97Pc"]')
	print(len(reviews_half), len(reviews_full))

	for i in range(len(reviews_full)):
		print(i)
		print(reviews_full[i].get_attribute('innerText'))
		print(reviews_half[i].text)
		try:
			if reviews_full[i].get_attribute('innerText') == "":
				Review.append(reviews_half[i].text)
			else:
				Review.append(reviews_full[i].get_attribute('innerText'))
		except:
			Review.append("")
			continue

	dates = driver.find_elements_by_xpath('//span[@class="p2TkOb"]')
	for d in dates:
		d1 = d.text
		date.append(d1)

	stars = driver.find_elements_by_xpath('//div[@class="pf5lIe"]/div')
	for s in stars:
		s1 = s.get_attribute('aria-label')
		rating.append(s1)

	thumps_up = driver.find_elements_by_xpath('//div[@class="jUL89d y92BAb"]')
	for t in thumps_up:
		t1 = t.text
		upvotes.append(t1)

	a = []
	a.append(Name)
	a.append(Review)
	a.append(upvotes)
	a.append(rating)
	a.append(date)
	print(len(a[0]))

	with open("test1.csv", "w", encoding = 'utf-8') as f:
	    writer = csv.writer(f)
	    writer.writerows(a)

# scrape_all_reviews("VLC", "org.videolan.vlc", "-")
