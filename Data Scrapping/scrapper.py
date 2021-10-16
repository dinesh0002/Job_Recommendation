# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint

# Function to initialize beautiful soup and get response from requests
def extract(position, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    url = f'https://in.indeed.com/jobs?q={position}&l=India&start={page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

# Function for Parsing and extracting data
def transform(soup):
    div_tags = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in div_tags:
        # Position Tag
        try:
            job_tag = item.find('table', class_ = 'jobCard_mainContent').div.text.strip()
            if job_tag[0:3] == 'new':
                job_tag = job_tag[3:]
            else:
                job_tag = job_tag
        except AttributeError:
            job_tag = ''
        # Company Tag
        try:
            comp_tag = item.find('div', class_ = 'heading6 company_location tapItem-gutter').span.text.strip()
        except AttributeError:
            comp_tag = ''
        # Company Rating
        try:
            comp_rating = item.find('span', class_ = 'ratingsDisplay withRatingLink').text.strip()
        except AttributeError:
            comp_rating = ''
        # Company Location
        try:
            comp_loc = item.find('div', class_ = 'companyLocation').text.strip()
        except AttributeError:
            comp_loc = ''
        # Salary
        try:
            sal = item.find('div', class_ = 'heading6 tapItem-gutter metadataContainer').text.strip()
        except AttributeError:
            sal = ''
        # Company Summary
        try:
            comp_summ = item.find('tr', class_ = 'underShelfFooter').text.strip().replace('\n', '')
        except AttributeError:
            comp_summ = ''
        # Job Dict
        job = {
            'title': job_tag,
            'company': comp_tag,
            'rating': comp_rating,
            'location': comp_loc,
            'salary': sal,
            'summary': comp_summ
        }
        joblist.append(job)
    return

# empty list
joblist = []

# input from user
position = input('enter job position name for scrapping')

# looping through the pages of the site which are in increment of 10
for i in range(0, 5000, 10):
    try:
        print(f'Scrapping Page, {i}')
        c = extract(position ,i)
        transform(c)
    except AttributeError:
        break

# Making an CSV File
df = pd.DataFrame(joblist)
print(df.head())
df.to_csv(f'{position}.csv')

