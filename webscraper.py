import string
import requests
from bs4 import BeautifulSoup
import os


# title editor
def file_name(title):
    title = title.strip()
    new_title = ''
    for letter in title:
        if letter == ' ':
            new_title += '_'
        elif letter not in string.punctuation:
            new_title += letter
    new_title += '.txt'
    return new_title


# directory check
def dir_check(num, path):
    if not os.access(f'{path}/Page_{num}', os.F_OK):
        os.mkdir(f'{path}/Page_{num}')
        os.chdir(f'{path}/Page_{num}')
    else:
        os.chdir(f'{path}/Page_{num}')


# user inputs and path head
n_pages = int(input('Enter number of pages: '))
art_type = input('Enter article type: ')
path = os.getcwd()


for page_num in range(1, n_pages + 1):

    # getting response and making folder
    inp_url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    r = requests.get(inp_url, params={'page': str(page_num)})
    dir_check(page_num, path)

    # checking response
    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        all_articles = soup.find_all('article')
        spec_arts = []

        # searching for articles
        for article in all_articles:
            a_type = article.find('span', {'data-test': 'article.type'}).text
            if a_type.strip() == art_type:
                a_link = article.find('a', {'data-track-action': 'view article'})
                spec_arts.append(a_link)

        # working with news articles
        for a_link in spec_arts:
            # creating title and filename
            a_title = file_name(a_link.text)
            # working with file and url
            article_file = open(a_title, 'wb')
            a_url = 'https://www.nature.com' + a_link.get('href')
            r2 = requests.get(a_url)
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            # writing byte body to file
            body = soup2.find('div', {'class': 'c-article-body'}).text
            b_body = bytes(body, encoding='utf-8')
            article_file.write(b_body)
            article_file.close()

    # error with link
    else:
        print('The URL returned ' + str(r))

# outputting confirmation
print('Saved all articles.')

