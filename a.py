import requests
from bs4 import BeautifulSoup
import json

# Define the tags to scrape
tags = ['Data Science', 'NLP', 'Deep Learning',
        'Machine Learning', 'Artificial Intelligence']

# Article
ARTICLE_TAG = 'article'

# Title
TITLE_TAG = 'h2'

# URL
URL_TAG = 'a'

# Author
AUTHOR_TAG = 'p'

# Date
DATE_SELECTOR = 'article > div > div > div > div > div > div.je.jf.jg.jh.ji.ab > div.jn.bg.ab.jo > div.l.ee > span > div > a > p > span:nth-child(2)'

# Initialize an empty list to store the scraped data
articles = []

# Loop through the tags and scrape the top articles for each tag
for tag in tags:
    # Construct the URL for the tag page
    url = f'https://medium.com/tag/{tag.lower().replace(" ", "-")}/top/all-time'

    print("Scraping data for tag: ", tag)
    # Make a request to the URL and get the page content
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f'Request failed with status code {response.status_code} for tag - {tag}')
    page_content = response.content
    print("Webpage content fetched successfully")

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find all the article elements on the page
    # Find all the article elements on the page
    article_elements = soup.find_all(ARTICLE_TAG)
    # article_elements = soup.select('.l .article')
    # Loop through the article elements and extract the relevant data
    print(f'Found {len(article_elements)} articles for tag - {tag}')
    print("Extracting article data")
    for i, article_element in enumerate(article_elements):
        # Extract the title
        title_element = article_element.find(TITLE_TAG)
        if title_element:
            title = title_element.text.strip()
        else:
            title = None

        # Extract the article URL
        url_element = article_element.find(URL_TAG)
        if url_element is not None:
            url = url_element['href']
        else:
            url = None

        # Extract the author name
        try:
            author = article_element.find(AUTHOR_TAG).text.strip()
        except AttributeError:
            author = 'No author listed'

        # Extract the date published
        date_element = article_element.select(DATE_SELECTOR)
        if date_element:
            date = date_element[0].text
        else:
            date = None

        # Add the article data to the list
        articles.append({
            'title': title,
            'url': url,
            'author': author,
            'date': date,
            'tag': tag
        })
    print('Finished extraction')
    print('----------------------')

# Write the scraped data to a JSON file
with open('medium_articles.json', 'w') as f:
    json.dump(articles, f)
