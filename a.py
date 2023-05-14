import requests
from bs4 import BeautifulSoup
import json

# Define the tags to scrape
tags = ['Data Science', 'NLP', 'Deep Learning', 'Machine Learning', 'Artificial Intelligence']

# Initialize an empty list to store the scraped data
articles = []

# Loop through the tags and scrape the top articles for each tag
for tag in tags:
    # Construct the URL for the tag page
    url = f'https://medium.com/tag/{tag.lower().replace(" ", "-")}/top/all-time'
    
    # Make a request to the URL and get the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Request failed with status code {response.status_code}')
        exit()
    page_content = response.content
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Find all the article elements on the page
    # Find all the article elements on the page
    article_elements = soup.find_all('div', {'class': 'l'})
    #article_elements = soup.select('.l .article')
    print(article_elements)


    # Loop through the article elements and extract the relevant data
    for article_element in article_elements:
        # Extract the title
        title_element = article_element.find('h2')
        if title_element:
            title = title_element.text.strip()
        else:
            title = None
        
        # Extract the article URL
        url_element = article_element.find('a')
        if url_element is not None:
            url = url_element['href']
        else:
            url = None

        
        # Extract the author name
        try:
            author = article_element.find('p').text.strip()
        except AttributeError:
            author = 'No author listed'
        
        # Extract the date published
        date_element = article_element.find('p', {'class': 'be b bf z dl'})
        if date_element:
            date_span_elements = date_element.find_all('span')
            date = ' '.join([d.text for d in date_span_elements])
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

# Write the scraped data to a JSON file
with open('medium_articles.json', 'w') as f:
    json.dump(articles, f)
