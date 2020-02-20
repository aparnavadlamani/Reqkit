from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd
import csv

driver = webdriver.Chrome()
link = "https://play.google.com/store/apps/details?id=org.videolan.vlc&hl=en&showAllReviews=true"
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
		# print("Here1")
		try:
			# print("here2")
			n = 20
			driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
			while(n>0):
				n = n -1
				lastCount = lenOfPage
				sleep(2)
				lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
				if(lenOfPage==lastCount):
					driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
		except NameError: #NoSuchElementException
			print("here3")
		else:
			# print("here4")
			match=True
Name = []
Review = []
upvotes = []
rating = []
date = []
count = 1

# print(n)
# big_tags = driver.find_elements_by_xpath('//div[@class="d15Mdf bAhLNe"]')
# for tag in big_tags:
# 	name = tag.find_element_by_xpath('//span[@class="X43Kjb"]').text
# 	Name.append(name)

# 	rev = tag.find_element_by_xpath('//div[@class="UD7Dzf"]/span').text.replace('"','')
# 	rev = rev.replace("'",'')
# 	Review.append(rev)

# 	d = tag.find_element_by_xpath('//span[@class="p2TkOb"]').text
# 	date.append(d)

# 	stars = tag.find_element_by_xpath('//div[@class="pf5lIe"]/div').get_attribute('aria-label')
# 	rating.append(stars)

# 	thumps_up = tag.find_element_by_xpath('//div[@class="jUL89d y92BAb"]')
# 	t = thumps_up.text
# 	upvotes.append(t)

# 	print(count," field done!!!")
# 	# print(name)
# 	count+=1

people = driver.find_elements_by_xpath('//span[@class="X43Kjb"]')
for person in people:
	name = person.text
	Name.append(name)
	# print(name)
	count+=1
print(count)

count = 1
reviews = driver.find_elements_by_xpath('//span[@jsname="bN97Pc"]')
for review in reviews:
	if(count==244):
		count+=1
	else:
		print(count)
		count+=1
		rev = review.text
		Review.append(rev)

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

with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(a)

# with open('vlc_reviews.csv', 'w', newline='') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(Name)
#     wr.writerow(Review)
#     wr.writerow(upvotes)
#     wr.writerow(rating)
#     wr.writerow(date)

print(Name)
print(Review)
print(upvotes)
print(rating)
print(date)