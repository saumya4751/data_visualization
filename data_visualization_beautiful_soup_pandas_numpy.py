# Description: This program aims to get some information from different URL of Movie and Weather, and then
#              clean and extract the data of that website. After getting the HTML data of the URL, 
#              information is gathered for Movies and Weather. Once the required data is gathered, a dataframe
#              is created of that data and it's stored to an Excel (CSV) file. Data Visualization is done
#              by creating the graph and comparing the data of Movies and Weather.


# requests library to get the URL
import requests
# beautifulsoup, a library for fetching the HTML data from the URL
from bs4 import BeautifulSoup
# regular expression module for finding specific data from a string
import re
# numpy library for mathematical operations
import numpy as np
# using pandas for creating dataframe of the data
import pandas as pd
# matplotlib for creating graph and data visualization
import matplotlib.pyplot as mpl


# Class for getting the data of movies 
class Movies:
    # Constructor for initializing some variables and getting the URL(s)
    def __init__(self):
        # URL for 1-50 movies
        self.URL1 = requests.get('https://www.imdb.com/search/title/?groups=top_100')
        # URL for 51-100 movies
        self.URL2 = requests.get('https://www.imdb.com/search/title/?groups=top_100&start=51&ref_=adv_nxt')
        # Lists for storing the data
        self.movie_name = []
        self.release_year = []
        self.movie_runtime = []
        self.movie_genre = []
        self.movie_rating = []
        self.movie_metascore = []
        self.movie_desc = []
        self.movie_votes = []

    # Function for fetching HTML data and finding a class that contains all the data
    def beautifulsoup(self):
        # For movies 1-50
        self.soup1 = BeautifulSoup(self.URL1.content, 'html.parser')
        self.content1 = self.soup1.find_all(class_ = 'lister-item-content')
        # For movies 51-100
        self.soup2 = BeautifulSoup(self.URL2.content, 'html.parser')
        self.content2 = self.soup2.find_all(class_ = 'lister-item-content')

    # Function for getting the data and storing it into lists
    def get_data(self):
        # Loop for storing data of movies from 1-50
        for details in self.content1:
            # Getting movie name
            movie = details.find('a')
            self.movie_name.append(movie.text)

            # Getting released year of the movie
            year = details.find(class_= 'lister-item-year')
            # Using re, getting digits from the string containing numbers and alphabets
            y = re.search('([0-9]+)', year.text)
            self.release_year.append(int(y[0]))

            # Getting movie runtime
            runtime = details.find(class_= 'runtime')
            # Using re, getting digits from the string containing numbers and alphabets
            r = re.search('([0-9]+)', runtime.text)
            self.movie_runtime.append(r[0])

            # Getting genre of the movie
            genre = details.find(class_= 'genre')
            # strip function for removing '\n' from the string
            self.movie_genre.append(genre.text.strip())

            # Getting the ratings of the movie
            ratings = details.find(class_= 'ratings-imdb-rating')
            # Getting data from an attribute of the tag
            rating_value = ratings.attrs['data-value']
            self.movie_rating.append(float(rating_value))

            # Getting metascore of the movie
            metascore = details.find(class_= 'metascore')
            # Using error handling routines for metascore
            # if metascore in not there for any movie, then store 0 in the list
            try:
                self.movie_metascore.append(int(metascore.text))
            except:
                self.movie_metascore.append(0)

            # Getting description of the movie
            description = details.find_all(class_='text-muted')
            # strip function for removing '\n' from the string
            self.movie_desc.append(description[2].text.strip())

            # Getting votes of the movie
            votes = details.find(class_='sort-num_votes-visible')
            votes_tag = votes.find_all('span')
            votes_value = votes_tag[1].text
            # removing ',' from the string, to convert it to int
            v = votes_value.replace(",", "")
            self.movie_votes.append(int(v))

        # Loop for storing data of movies from 51-100
        for details in self.content2:
            # Getting movie name
            movie = details.find('a')
            self.movie_name.append(movie.text)

            # Getting released year of the movie
            year = details.find(class_= 'lister-item-year')
            # Using re, getting digits from the string containing numbers and alphabets
            y = re.search('([0-9]+)', year.text)
            self.release_year.append(int(y[0]))

            # Getting movie runtime
            runtime = details.find(class_= 'runtime')
            # Using re, getting digits from the string containing numbers and alphabets
            r = re.search('([0-9]+)', runtime.text)
            self.movie_runtime.append(r[0])

            # Getting genre of the movie
            genre = details.find(class_= 'genre')
            # strip function for removing '\n' from the string
            self.movie_genre.append(genre.text.strip())

            # Getting the ratings of the movie
            ratings = details.find(class_= 'ratings-imdb-rating')
            # Getting data from an attribute of the tag
            rating_value = ratings.attrs['data-value']
            self.movie_rating.append(float(rating_value))

            # Getting metascore of the movie
            metascore = details.find(class_= 'metascore')
            # Using error handling routines for metascore
            # if metascore in not there for any movie, then store 0 in the list
            try:
                self.movie_metascore.append(int(metascore.text))
            except:
                self.movie_metascore.append(0)

            # Getting description of the movie
            description = details.find_all(class_='text-muted')
            # strip function for removing '\n' from the string
            self.movie_desc.append(description[2].text.strip())

            # Getting votes of the movie
            votes = details.find(class_='sort-num_votes-visible')
            votes_tag = votes.find_all('span')
            votes_value = votes_tag[1].text
            # removing ',' from the string, to convert it to int
            v = votes_value.replace(",", "")
            self.movie_votes.append(int(v))

    # Function for creating the dataframe from the data stored in the lists
    def dataframe(self):
        data = {
        "Movie_name": self.movie_name,
        "Release_year": self.release_year, 
        "Movie_genre": self.movie_genre, 
        "Movie_runtime": self.movie_runtime, 
        "Movie_metascore": self.movie_metascore,
        "Movie_rating": self.movie_rating,
        "Movie_desc": self.movie_desc,
        "Movie_votes": self.movie_votes
        }
        self.movie_info = pd.DataFrame(data)

    # Function for printing some major data of the movies
    def print_data(self):
        print('Movie(s) with hightest rating:\n', self.movie_info[self.movie_info['Movie_rating'] == self.movie_info['Movie_rating'].max()], '\n')
        print('Movie(s) with lowest rating:\n', self.movie_info[self.movie_info['Movie_rating'] == self.movie_info['Movie_rating'].min()], '\n')
        print('Movie(s) with hightest metascore:\n', self.movie_info[self.movie_info['Movie_metascore'] == self.movie_info['Movie_metascore'].max()], '\n')
        print('Movie(s) with lowest metascore:\n', self.movie_info[self.movie_info['Movie_metascore'] == self.movie_info['Movie_metascore'].min()], '\n')
        print('Movie(s) with Most Votes:\n', self.movie_info[self.movie_info['Movie_votes'] == self.movie_info['Movie_votes'].max()], '\n')

    # Function for storing the whole data in an excel file
    def create_csv(self):
        self.movie_info.to_csv('Movie Information.csv')

    # Function for creating the graph of some data
    def create_graph(self):
        # Graph of top 10 movies
        top_10_ratings = self.movie_info.nlargest(10, ['Movie_rating'])
        # Comparing Release year, Ratings, and Metascore
        ax = top_10_ratings.sort_values(by= ['Release_year']).plot(x= 'Release_year', y= 'Movie_rating', kind= 'bar', title= 'Top 10 movies with Release Year and Movie Ratings')
        ax1 = top_10_ratings.sort_values(by= ['Release_year']).plot(x= 'Release_year', y= 'Movie_metascore', kind= 'bar', title= 'Top 10 movies with Release Year and Movie Metascore')
        ax.set_xlabel('Release Year')
        ax.set_ylabel('Ratings')
        ax1.set_xlabel('Release Year')
        ax1.set_ylabel('Metascore')
        mpl.show()

# Class for getting the data of Weather 
class Weather:
    # Constructor for initializing some variables and getting the URL(s)
    def __init__(self):
        self.URL = requests.get('https://forecast.weather.gov/MapClick.php?lat=39.7592&lon=-84.1938#.YbA1G9DMJPY')
        self.days = []
        self.temperature_list = []
        self.temperature_list_int = []
        self.description = []
    
    # Function for fetching HTML data and finding a class that contains all the data
    def beautifulsoup(self):
        # For data of next 5 days
        self.soup = BeautifulSoup(self.URL.content, 'html.parser')
        self.seven_days_content = self.soup.find(id= 'seven-day-forecast-container')
        self.content = self.seven_days_content.find_all(class_= 'tombstone-container')
        # For current information
        self.current_information_content = self.soup.find_all('td')
        self.current_condition_content = self.soup.find(class_='myforecast-current')

    # Function for getting the data about current information
    def current_information(self):
        self.humidity = self.current_information_content[1].text
        self.windspeed = self.current_information_content[3].text
        self.dewpoint = self.current_information_content[7].text
        self.visibility = self.current_information_content[9].text
        self.current_condition = self.current_condition_content.text.strip()

    # Function for getting the data for next 5 days
    def get_data(self):
        for information in self.content:
            # Getting the temperature 
            temp = information.find(class_='temp')
            # Splitting a string the contains 'High/Low: 30 F'
            split_temp = temp.text.split(':')
            # Storing just value and the degree
            self.temperature_list.append(split_temp[1]) 
            # Finding the digits from string such as '30 F'
            t = re.search('([0-9]+)', split_temp[1])
            # Storing just the numbers in a list 
            self.temperature_list_int.append(int(t[0]))

            # Getting the data about the day\period and description of that day/period
            full_description = information.find('img')
            description_text = full_description.attrs['title']
            days_and_description = description_text.split(':')
            self.days.append(days_and_description[0])
            self.description.append(days_and_description[1])

    # Function for creating the dataframe from the data stored in the lists
    def dataframe(self):
        data = {
            'Day': self.days,
            'Temperature': self.temperature_list,
            'Temperature_int': self.temperature_list_int,
            'Description': self.description
        }
        self.weather_info = pd.DataFrame(data)
    
    # Function for printing some data of the weather
    def print_data(self):
        print('Current Weather Information:')
        print('Current Condition:', self.current_condition)
        print('Dewpoint:', self.dewpoint)
        print('Humidity:', self.humidity)
        print('Windspeed:', self.windspeed)
        print('Visibility:', self.visibility)

        print('\nSome Information about next 5 days:')
        print('Average temperature for next 5 days would be:', int(np.mean(np.array(self.temperature_list_int))), 'F\n')
        print('Low temperature will be on:\n', self.weather_info.loc[self.weather_info['Temperature_int'] == self.weather_info['Temperature_int'].min()], '\n')
        print('High temperature will be on:\n', self.weather_info[self.weather_info['Temperature_int'] == self.weather_info['Temperature_int'].max()], '\n')

    # Function for storing the whole data in an excel file
    def create_csv(self):
        self.weather_info.to_csv('Weather Information.csv')

    # Function for creating the graph of some data
    def create_graph(self):
        mpl.plot(self.weather_info['Day'], self.weather_info['Temperature_int'])
        mpl.title('Temperature on a Day/Period')
        mpl.xlabel('Period of Days')
        mpl.ylabel('Temperature')
        mpl.show()        

# Main function
def main():
    print("Here, you can find the information about Top 100 movies till now and also about weather.")
    # Loop for providing menu to the user
    while True:
        # Providing menu to the user
        print('1. Movies \n2. Weather \n3. Exit')
        # Error handling routines, for taking the input from the user
        try:
            user_choice = int(input('Please select one of the option listed above for getting some information: '))
            # If user select movies
            if user_choice==1:
                # Creating object of class Movies and calling it's functions
                movies = Movies()
                movies.beautifulsoup()
                movies.get_data()
                movies.dataframe()
                movies.print_data()
                movies.create_csv()
                movies.create_graph()

            # If user select weather  
            elif user_choice==2:
                # Creating object of class Weather and calling it's functions
                weather = Weather()
                weather.beautifulsoup()
                weather.current_information()
                weather.get_data()
                weather.dataframe()
                weather.print_data()
                weather.create_csv()
                weather.create_graph()

            # If user selects exit
            elif user_choice==3:
                break

            # If user enters some other digit
            else:
                print('Please select an option within listed above')

        except:
            print('Please select an option within listed above')

if __name__=="__main__":
    main()