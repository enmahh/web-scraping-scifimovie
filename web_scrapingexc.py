import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

# Initialize empty lists to store the scraped data
titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []

# URL parameters
base_url = "https://www.imdb.com/search/title?genres=sci-fi&start={}&explore=title_type,genres&ref_=adv_prv"
start_page = 1
end_page = 9951  # Set the number of pages you want to scrape
page_step = 50  # Number of movies per page

# User-agent header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Scraping loop
for page in range(start_page, end_page, page_step):
    url = base_url.format(page)
    response = requests.get(url, headers=headers, timeout=(10, 30))
    
    if response.status_code != 200:
        print(f"Request failed for page {page}. Skipping...")
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = soup.find_all('div', class_='lister-item mode-advanced')

    for container in movie_containers:
        title = container.h3.a.text
        titles.append(title)
        
        year = container.h3.find('span', class_='lister-item-year').text.strip('()')
        years.append(year)
        
        rating = container.p.find('span', class_='certificate')
        ratings.append(rating.text if rating else "")
        
        genre = container.p.find('span', class_='genre').text.strip()
        genres.append(genre)
        
        # Check if the runtime element exists
        runtime_tag = container.p.find('span', class_='runtime')
        runtime = runtime_tag.text.strip(' min') if runtime_tag else None
        runtimes.append(runtime)
        
        imdb_tag = container.find('div', class_='ratings-imdb-rating')
        imdb = float(imdb_tag.strong.text) if imdb_tag else None
        imdb_ratings.append(imdb)
        
        metascore_tag = container.find('span', class_='metascore')
        metascore = int(metascore_tag.text) if metascore_tag else None
        metascores.append(metascore)
        
        votes_tag = container.find('span', attrs={'name': 'nv'})
        votes_value = int(votes_tag['data-value']) if votes_tag else None
        votes.append(votes_value)

    # Sleep to avoid overloading the server
    sleep(randint(8, 15))

# Create a DataFrame
df = pd.DataFrame({
    'Title': titles,
    'Year': years,
    'Rating': ratings,
    'Genre': genres,
    'Runtime (min)': runtimes,
    'IMDb Rating': imdb_ratings,
    'Metascore': metascores,
    'Votes': votes
})

# Data transformation: Convert 'Year' column to integers
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Save the scraped data to an Excel file
df.to_excel('movie_data.xlsx', index=False, engine='openpyxl')


