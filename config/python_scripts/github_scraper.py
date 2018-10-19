from bs4 import BeautifulSoup as bs
import requests

def stars_count(url):
	html = requests.get(url).text
	soup = bs(html, 'lxml')
	stars_class = "social-count js-social-count"
	stars = soup.find('a', class_=stars_class).text.strip()
	return stars

repo = 'yourrepohere'
repo_next = 'yourgoalhere'
repo_last = 'yourpreviousgoalhere'
print(stars_count(repo))
print(stars_count(repo_next))
print(stars_count(repo_last))
