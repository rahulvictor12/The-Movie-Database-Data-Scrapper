# -*- coding: utf-8 -*-
"""Web scraping of The Movie Database movie data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F-A5xcC4cvmi9PFXNE4qgSBGsFt4I_B5

The imports we need :-
1. Requests :- to make an http request to the web page.
2. BeautifulSoup :- for parsing the html response and then work with it.
3. Pandas :- for data manipulation and analysis.
4. pprint :- The pprint module provides a capability to “pretty-print” arbitrary Python data structures in a form which can be used as input to the interpreter

**1.
Sending an HTTP GET request to "https://www.themoviedb.org/movie" using the 'requests' library.
The 'verify' parameter is set to True, enabling SSL certificate verification.
A timeout of 30 seconds is specified for the request, and custom headers ('needed_headers') are included.**
"""

# Importing Necessary Libraries
import requests
from pprint import pprint

# Adding Needed Headers to mitigate HTTP Status code Error 403 Error.
needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                  'Cache-Control': 'max-age=0','Connection': 'keep-alive'}

# Formulating a get request .
response =requests.get(("https://www.themoviedb.org/movie"),verify=True, timeout=30,headers = needed_headers)

if response.status_code == requests.codes.ok :
    print(f'Request Executed Succesfully {response.status_code}')

    # Save the contents in a variable
    page_contents = response.text

    # Print the contents of the page
    print(page_contents)

    # Infering the type of the variable
    variable_type = type(page_contents)

    # Display the first 200 characters of the content
    print("First 200 Characters of Content:")
    print(page_contents[:200])
else :
    response.raise_for_status()

"""**Parse the content of HTML response using the BeautifulSoup library and execute the tasks
specified in the guidelines mentioned below.**
"""

# Importing the Necessary Libraries.
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import time

if response.status_code == requests.codes.ok :
    # Creating an instance of BeautifulSoup Class.
    soup=BeautifulSoup(page_contents,'html.parser')
    soup.prettify()

# Extracting the Title from webpage content
title = soup.title.string
print(f"Title: {title}")

# User Defined Function to generalize the Instance creation
def createBeautifulSoupInstanceFromURL(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url, timeout=120, headers = needed_headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Wait for Some Time
        time.sleep(1)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # soup.prettify()

        return soup

    except requests.exceptions.RequestException as e:
          # Handle exceptions such as malformed URLs or non-existent pages
          raise Exception(f"An Error Occured while accessing the URL: {e}")

"""**Test Cases to check the functionality**"""

print("Running Test Cases : ")
# Test Case 1: Working URL
working_url = 'https://www.themoviedb.org/movie'
try:
    result_soup = createBeautifulSoupInstanceFromURL(working_url)
    print(f"Successfully Created an Soup Instance and retrieved content from {working_url}")
except Exception as e:
    print(f"Test Case failed: {e}")

# Test Case 2: URL with 404 response
nonexistent_url = 'https://www.example.com/nonexistent'
try:
    result_soup = createBeautifulSoupInstanceFromURL(nonexistent_url)
    print(f"Test Case failed: The function did not raise an exception for {nonexistent_url}")
except Exception as e:
    print(f"Error Occured, Exception raised for {nonexistent_url} - {e}")

"""**Defining Base Url of TMDB.**"""

# Base URL for TMDB Website.
base_url = 'https://www.themoviedb.org/'

"""As we have gathered all the Data Required in the Cache. We are taking the Retrieved Details of the First Movie."""

soupInstance = createBeautifulSoupInstanceFromURL('https://www.themoviedb.org/movie')

# Gathering the Required Details.
FirstMovie_HTMLContent = soupInstance.find('div', {'class': 'card style_1'})
firstMovieTitle = FirstMovie_HTMLContent.find('h2').text.strip() if FirstMovie_HTMLContent else np.nan
firstMovieRating = "{:.2f}".format(float(FirstMovie_HTMLContent.find('div', {'class': 'user_score_chart'})['data-percent'])) if FirstMovie_HTMLContent else np.nan
firstMovieLink= FirstMovie_HTMLContent.a['href'] if FirstMovie_HTMLContent else np.nan


print(f"The HTML Content for Most Popular Movie from the Website is : {FirstMovie_HTMLContent}")
print(f"The Most Popular Movie from the Website is : {firstMovieTitle}")
print(f"Rating of The Most Popular Movie from the Website is : {firstMovieRating}")
print(f"Extracted Part of The URL of The Most Popular Movie is : {firstMovieLink[1:]}")

"""# Extension methods

**Methods to Use Incase of Requests Failure Due to Exceeded Redirects of any Unknown Requests**
"""

# Required Headers , Can be Removed
apiheaders = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNWE0NDI4NjlmZWFkMzU0M2MwOWU3ZTkzYWExNGYxYSIsInN1YiI6IjY1ZGM0OTU5YTM1YzhlMDE0YTEzYjkxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YD3tjMP1vSBYMKdjhNLVKNmw42G-0obCNNTuAhLEg9I"
}

def getCastListFromAPI(Movie):
    casturl = f"https://api.themoviedb.org/3/{Movie}/credits?language=en-US"
    # Connect to TMDB API and Get the Response.
    response = requests.get(casturl, headers=apiheaders)
    castData = response.json()

    #Gather the Required Cast Members.
    acting_names = []
    for person in castData['cast'] + castData['crew']:
        if person['known_for_department'] == 'Acting':
            acting_names.append(person['original_name'])

    return acting_names

def getGenreListFromAPI(Movie):
    apiurl = f'https://api.themoviedb.org/3/{Movie}?language=en-US'
    # Make a GET request to the API URL using the Above Headers.
    response = requests.get(apiurl, headers=apiheaders)

    # Get the Json Containing the Data.
    genreData = response.json()['genres']

    # Extract names of genres
    genre_names = [genre['name'] for genre in genreData]

    return genre_names

"""# User Defined Functions:

**User Defined Functions to Extract Movie Titles,Ratings,Html Content, Genres and Cast of all the Movies**
"""

# Function to Get the Titles of All Movies.
def getMovieTitlesList(soupObject):
    Movie_List = []
    for soup in soupObject:
        movie_names = [tag.string for tag in soup.select('h2')]
        # Extend Movie_List with the extracted movie names
        Movie_List.extend(movie_names)

    return Movie_List

# Function to Get the Ratings of All Movies.
def getRatingsList(soupObject):
    Rating_List = []
    All_Ratings = soupObject.find_all('div', {'class': 'user_score_chart'})
    for Rating in All_Ratings:
        # Gets the Rating for the Movie and Shows it as a two digit decimal.
        rating = "{:.2f}".format(float(Rating['data-percent']))
        Rating_List.append(rating if rating != 0.0 else 'not rated')

    return Rating_List

# Function to Get the Movie Link(End part of the url) of All Movies.
def getMovieLinksList(soupObject):
    MovieLinksList = []
    for movie_link in soupObject:
        hyperlinks = movie_link.select('h2 a')
        # Extract 'href' attribute from each <a> tag and append to MovieLinksList
        MovieLinksList.extend(h['href'][1:] for h in hyperlinks)

    return MovieLinksList

# Function to Get the Cast of All Movies.
def getEntireCastList(MovieLinksList):
    Cast_ListNew = []
    # Gathering HTML Content,Cast and Genre for Every Movie.
    for Movie in MovieLinksList:
        #Base URL + the Movie's Href link+/cast
        CastURL = base_url+Movie+'/cast'

        # Try Making a Get Request through Requests, If any Error Occurs , Use the API and Gather the Data.
        try:
            # Make a GET request to the URL
            response = requests.get(CastURL, verify=True, timeout=120, headers = needed_headers)
            time.sleep(1) # Wait for Some Time
            # Parse the HTML content using BeautifulSoup
            castSoup = BeautifulSoup(response.text, 'html.parser')
            castSoup.prettify()

            # Cast:
            MovieWiseCastList = []
            OrderedCastList = castSoup.find_all('ol', {'class': 'people credits'})
            for CastList in OrderedCastList:
                TotalCastParas = CastList.find_all('div', {'class':'info'})
                for all_cast in TotalCastParas:
                    TotalCastLinks = all_cast.find_all('a')
                    MovieWiseCastList.extend(cast.text for cast in TotalCastLinks)

            Cast_ListNew.append(MovieWiseCastList)

        except requests.exceptions.RequestException as e:
              try:
                cast = getCastListFromAPI(Movie)
                Cast_ListNew.append(cast)
              except:
                print(f'Redirect Error Occured While Accessing {CastURL}, So Appending Null Value to Cast List.')
                # Add NaN to the List and Continue the Proccess.
                Cast_ListNew.append(['Nan'])
                pass

    return Cast_ListNew


# Function to Get the Genres of All Movies.
def getGenreList(MovieLinksList):
    GenreListNew = []
    # Gathering HTML Content,Cast and Genre for Every Movie.
    for Movie in MovieLinksList:
        #Base URL + the Movie's Href link
        modifiedUrl = base_url+Movie

        # Try Making a Get Request through Requests, If any Error Occurs , Use the API and Gather the Data.
        try:
            # Make a GET request to the URL
            response = requests.get(modifiedUrl, timeout=120, headers = needed_headers)
            time.sleep(1) # Wait for Some Time
            # Parse the HTML content using BeautifulSoup
            responseSoup = BeautifulSoup(response.content, 'html.parser')
            responseSoup.prettify()

            Genres_span = responseSoup.find('span', class_='genres')
            Genres = [a.text for a in Genres_span.find_all('a')]
            GenreListNew.append(Genres)

        except requests.exceptions.RequestException as e:
              try:
                  genres = getGenreListFromAPI(Movie)
                  GenreListNew.append(genres)
              except:
                  print(f'Redirect Error Occured While Accessing {modifiedUrl}, So Appending Null Value to Genre List')
                  # Add NaN to the List and Continue the Proccess.
                  GenreListNew.append(['NaN'])
                  pass

    return GenreListNew

"""**User Defined Function to Return a Pandas Data Frame with Titles,Ratings,Genres and Cast of movies listed on the Page.**"""

def getDataFrameForEveryPageUsingSoupResponse(response, HTMLContentList):
    ColumnNames = ['Title', 'Rating', 'Genre', 'Cast']

    # Restricting the Search Area.
    movieListSoupObject = response.find_all('section', {'id': 'media_results'})

    # Gather the Titles and Ratings of the Movies.
    Movie_List = getMovieTitlesList(movieListSoupObject)
    Rating_List = getRatingsList(response)

    # Gather the Genres and Cast of the Movies.
    GenreList = getGenreList(HTMLContentList)
    Cast_List = getEntireCastList(HTMLContentList)

    # Creating a DataFrame for the Provided List of Data
    df = pd.DataFrame({ColumnNames[0]: Movie_List,ColumnNames[1]: Rating_List,ColumnNames[2]: GenreList,ColumnNames[3]: Cast_List})
    return df

def convertDataFrametoCSV(fileName, dataFrame):
    # Exporting the Data Frame to CSV
    dataFrame.to_csv(str(fileName)+'_ScrapedData.csv', mode='w', index=False)

"""**Scraping the data from the first 6 pages of the website and combining data into dataframes**"""

def scrapeAndCreateDataFrames():
    # List to Store DataFrames for all the pages, to Create a combined DataFrame.
    DataFrames = []

    for i in range(1,6):
        page_url = f'https://www.themoviedb.org/movie?page={i}'
        try:
            # Get the BeautifulSoup Response for Every Page
            response = createBeautifulSoupInstanceFromURL(page_url)

            # Restricting the Search Area.
            movieListSoupObject = response.find_all('section', {'id': 'media_results'})

            # Gather the HTML Content List.
            HTMLContentList = getMovieLinksList(movieListSoupObject)

            # Get the DataFrame.
            dataFrame = getDataFrameForEveryPageUsingSoupResponse(response, HTMLContentList)

            # Convert the DataFrames into CSV.
            convertDataFrametoCSV('DataFrame_Page_'+str(i),dataFrame)

            # Appending the DateFrame of the Respective Page to the List.
            DataFrames.append(dataFrame)

        except Exception as e:
              print(f"Other Type of Error had occured with Exception: {e}")
    return DataFrames

"""# Call the Main Method and Gather DataFrames"""

# Gathering All The DataFrames, With Data of all the Pages.
DataFrames = scrapeAndCreateDataFrames()

# Append the DataFrame to CombinedDataFrame
CombinedDataFrame = pd.concat(DataFrames, ignore_index=True)

# Display the DataFrame.
CombinedDataFrame

# Convert the combined DataFrame to CSV
convertDataFrametoCSV('Combined_Data', CombinedDataFrame)