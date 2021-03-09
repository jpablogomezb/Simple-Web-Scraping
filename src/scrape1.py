import os
import datetime
import csv
import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words
#driver = webdriver.Chrome(ChromeDriverManager().install())

def clean_word(word):
	word = word.replace("!", "")
	word = word.replace("?", "")
	word = word.replace(".", "")
	word = word.replace(",", "")
	word = word.replace(":", "")
	word = word.replace(";", "")
	word = word.replace("(", "")
	word = word.replace(")", "")
	word = word.replace("-", "")
	word = word.replace("--", "")
	return word

def clean_up_words(words):
	new_words = []
	pkg_stop_words = get_stop_words('en')
	my_stop_words = ['the', 'is', 'and', 'to']
	for word in words:
		word = word.lower()
		cleaned_word = clean_word(word)
		if cleaned_word in my_stop_words or cleaned_word in pkg_stop_words:
			pass
		else:
			new_words.append(cleaned_word)
	return new_words

def create_csv_path(csv_path):
	if not os.path.exists(csv_path):
		with open(csv_path, 'w') as csvfile:
			header_columns = ['word', 'count', 'timestamp']
			writer = csv.DictWriter(csvfile, fieldnames=header_columns)
			writer.writeheader()


saved_domains = {
	"www.domain-of-interest.com": "main-container-block",
	"tim.blog":"content-area"
}

my_url = input("Enter the ulr to scrape: ")
print("Requesting...", my_url)
#driver.get(my_url)
domain = urlparse(my_url).netloc #domain name
print("domain", domain)

response = requests.get(my_url)
if response.status_code != 200:
	print("You can't scrape this. Status is", response.status_code)
else:
	print("Starting the scraping...")
	#html = driver.page_source
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	if domain in saved_domains:
		div_class = saved_domains[domain]
		body_ = soup.find("div", {"class": div_class})
	else:
		body_ = soup.find("body")
	#print(body_.text)
	words = body_.text.split()
	#removing stop words and punctation
	clean_words = clean_up_words(words)
	word_counts = Counter(clean_words)
	#print(word_counts.most_common(30))
	filename = domain.replace(".", "-") + '.csv'
	path = 'csv/' + filename
	timestamp = datetime.datetime.now()
	create_csv_path(path)
	with open(path, 'a') as csvfile:
			header_columns = ['word', 'count', 'timestamp']
			writer = csv.DictWriter(csvfile, fieldnames=header_columns)
			for word, count in word_counts.most_common(30):
				writer.writerow({
						"word": word,
						"count": count,
						"timestamp": timestamp
					})
