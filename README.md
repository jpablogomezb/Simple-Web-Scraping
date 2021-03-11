# Simple-Web-Scraping

A simple python script to scrape a url, parse text, count and store words into a local CSV file.

This python script used Requests and BeautifulSoup.
Python Stop Words is used to get list of common stop words in order to omit them from the counting.

- Update with your **domain of interest** and an specific **html tag** for your case (e.g. main-container, content-area) in line 48.
- Specify the **language of the stop words package** (e.g. en, es) in line 28.
- You can include your **own defined stop words** in line 29.
