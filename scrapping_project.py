from warnings import filterwarnings
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup
import random 
from time import sleep

original_url = "https://quotes.toscrape.com"
url = "/page/1"

page = 1

all_quotes = []
all_authors = []
about_authors = {}

while url: # Iterate while we have next button (next page)
    response = requests.get(f"{original_url}{url}").text # Returns HTML as text(string)
    soup = BeautifulSoup(response, features = "html.parser") # Creates BeatifulSoup object for scrapping data 

    quotes = soup.find_all(class_ = 'quote')
    for quote in quotes:
        
        quote_text = list(quote.children)[1].get_text()  # Gets text of quotes
        author = list(quote.children)[3].find('small').get_text() # Gets author of this quote
        # print(list(quote.children))
        link_to_bio = list(quote.children)[3].find('a')['href']
        
        all_quotes.append(quote_text) # Adds quote into list 
        all_authors.append(author) # Adds author of quote into list

        if author not in about_authors.keys(): # For every author that still isn't in the dicitonary
            bio_response = requests.get(original_url + link_to_bio).text # Returns HTML as text(string)
            bio_soup = BeautifulSoup(bio_response, features = "html.parser") # Creates BeatifulSoup object for scrapping data
            about_authors[author] = {}
            about_authors[author]['date'] = bio_soup.find(class_ = 'author-born-date').get_text() # 
            about_authors[author]['location'] = bio_soup.find(class_ = 'author-born-location').get_text()
            about_authors[author]['bio'] = bio_soup.find(class_ = 'author-description').get_text()


    next_btn =  soup.find(class_ = 'next') # If we have next page -> page += 1
    url = next_btn.find('a')['href'] if next_btn else None

# print(about_authors)

# Game Starts


wants_again = True
while wants_again:
    i = random.choice(range(len(all_quotes)))
    quote = all_quotes[i]
    author = all_authors[i]
    num_guesses = 5

    print("Here's quote:\n")
    print(quote)

    while num_guesses:
        guess = input(f"\nWho said this? Guesses remaining : {num_guesses}. ")
        num_guesses -= 1
        if guess.lower() !=  author.lower():
            if num_guesses == 4:
                date = about_authors[author]['date']
                location = about_authors[author]['location']
                print(f"False :( Here is hint: The author was born in {date} {location}")
            elif num_guesses == 3:
                names = author.split(' ')
                first_name = names[0]
                print(f"False :( Here is hint: The author's first name starts with {first_name[0]}")
            elif num_guesses == 2:
                last_name = names[-1]
                print(f"False :( Here is hint: The author's last name starts with {last_name[0]}")

            elif num_guesses == 1:
                bio_words = about_authors[author]['bio'].split()
                stop_words = (first_name, last_name, first_name + "'s", last_name + "'s")
                stop_words = tuple(map(lambda x: x.lower(), stop_words))
                
                result_words = [word if word.lower() not in stop_words else "..." for word in bio_words] 
                result = ' '.join(result_words)
                print(f"{result}")

            else: 
                print(f"GAME IS OVER!!! The right author is {author}")
            
        else:
            print('Correct! Congratulations')
            break
    wants_again = input('Would you like to play again (y/n)?  ')
    wants_again = wants_again[0].lower()
    wants_again = True if wants_again == 'y' else False

    print()
        



