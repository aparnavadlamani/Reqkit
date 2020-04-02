from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd

# chrome_options = webdriver.ChromeOptions()


# chrome_options.binary_location = "C:\\Users\\SA31\\Downloads\\dt\\Win_337026_chrome-win32\\chrome-win32\\chrome.exe"

# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
link = "https://play.google.com/store/apps/details?id=org.videolan.vlc&hl=en&showAllReviews=true"
driver.get(link)

Ptitle = driver.find_element_by_css_selector('.AHFaub span').text

print(Ptitle)


sleep(1)

# f = open("sample.txt","a")
# f.write(driver.page_source)
# f.close()

# print("File written")

# print(driver.page_source)
# avg_rating = driver.find_element_by_css_selector('.pf5lIe').text

# print(avg_rating)
# driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()

# sleep(2)

# driver.find_element_by_css_selector('.U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d').click()

# reviewer_name = driver.find_element_by_css_selector('span.X43Kjb')
# print(reviewer_name.text)
Name = []
Review  = []
date = []
rating = []
upvotes = []

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
	lastCount = lenOfPage
	sleep(1)
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	if lastCount==lenOfPage:
		match=True
count = 1
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
	print(count)
	count+=1
	rev = review.text
	Review.append(rev)
	# print(rev)

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

print(Name,len(Name))
print(Review,len(Review))
print(date,len(date))
print(rating,len(rating))
print(upvotes,len(upvotes))

# driver.find_element_by_css_selector('.displayed-child').click()

# driver.execute_script("document.querySelectorAll('button.dropdown-child')[0].click()")
# reviews_df = []
# for i in range(1,5):
#     try:
#         for elem in driver.find_elements_by_class_name('single-review'):
#             print(str(i))
#             content = elem.get_attribute('outerHTML')
#             soup = BeautifulSoup(content, "html.parser")
#             date = soup.find('span',class_='review-date').get_text()
#             rating = soup.find('div',class_='tiny-star')['aria-label'][6:7]
#             title = soup.find('span',class_='review-title').get_text()
#             txt = soup.find('div',class_='review-body').get_text().replace('Full Review','')[len(title)+1:]
#             print(soup.get_text())
#             temp = pd.DataFrame({'Date':date,'Rating':rating,'Review Title':title,'Review Text':txt},index=[0])
#             print('-'*10)
#             reviews_df.append(temp)
#     except:
#         print('s')
#     driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()
# reviews_df = pd.concat(reviews_df,ignore_index=True)

# reviews_df.to_csv(Ptitle+'_reviews_list.csv', encoding='utf-8')
	

