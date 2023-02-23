import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import random

URL_TEMPLATE = "https://kinovezha.com/films/comedy/"

def get_amount_of_pages():
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "html.parser")
    all_pages_with_movies = soup.find_all('div', class_='pagination__inner d-flex jc-center')
    a = all_pages_with_movies[0].find_all('a')
    return int(a[-1].text)


def random_movie():
    page = np.random.randint(1,get_amount_of_pages())
    movie_url = URL_TEMPLATE+'page/'+str(page)
    return movie_url

def random_comedy():
    page = random_movie()
    # poster_url = 'https://kinovezha.com'
    # print(page)
    r = requests.get(page)
    soup = bs(r.text, "html.parser")
    # comedy = soup.find_all('div', class_='movie-item__title')
    movies = soup.find_all('div', class_='movie-item__inner')
    list_of_movies = []
    for i in range(len(movies)):
        movie = movies[i]
        year = movie.find('div', class_='movie-item__meta ws-nowrap').text.replace('\n', ' ').split(' ')[1]
        title = movie.find('div', class_='movie-item__title').text
        link = movie.find('a', class_='movie-item__link')
        # poster_link = movie.find('img')

        # list_of_movies.append((title, year, poster_url+poster_link['data-src']))
        list_of_movies.append((title, year, link['href']))
    
    return random.choice(list_of_movies)

if __name__ == "__main__":
    print(random_comedy())