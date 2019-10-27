#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:22:56 2019

@author: elenizarogianni

24/10/2010 EXUS ML INTERVIEW ASSIGNMENT

Recommender System using the Book Crossing Data set



"""


# import libraries
# for data manipulation
import pandas as pd
import numpy as np
# for plotting
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pylab
import seaborn as sns

plt.style.use('classic')
plt.style.use('seaborn-whitegrid')

# find and change working directory
from os import chdir, getcwd
wd=getcwd()

# /Users/elenizarogianni/Desktop/Python/Kaggle/Titanic
chdir('/Users/elenizarogianni/Desktop/EXUS_ML_Task')


# Load Data 

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!! Remember! Adjust to Ipython running working space !!!!!


users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")

# print the shape of the data
print users.shape
print books.shape
print ratings.shape

# remove middle slash  
users.columns = ['userID', 'Location', 'Age']
books.columns = ['ISBN', 'BookTitle', 'BookAuthor', 'YearOfPublication', 'Publisher', 'ImageUrlS', 'ImageUrlM', 'imageUrlL']
ratings.columns = ['userID', 'ISBN', 'BookRating']


#users2 = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
#users2.columns = ['userID', 'Location', 'Age']
#BookLocation = users2.Location



# Get basic info from all 3 dataframes 
# Users
users.info()

# Describe numerical variables
users.describe()

# Describe categorical variables
users.describe(include=['O'])

# Check 5 first entries
users.head(5)




#check for missing value
users.isnull().any().any()





# LOCATION
# check for missing values
users.Location.isnull().any()
# check for mduplicate entries
users.Location.nunique()

# Check for invalid entries under users.Location
# split users.Location into 3 subparts
location_expanded = users.Location.str.split(',', 2, expand=True)
location_expanded.columns = ['Town', 'State', 'Country']
users = users.join(location_expanded)

users.drop('Location', axis=1, inplace = True)



# Again, check on missing values and duplicates.
print(users.Town.isnull().any())
print(users.State.isnull().any())
print(users.Country.isnull().any())

# How many unique towns, states and countries do I have?
nTowns=users.Town.nunique()
nStates=users.Town.nunique()
nCountries=users.Country.nunique()


print("There are {} unique towns, {} unique states and {} unique coutries.".format(nTowns, nStates, nCountries))
print("In comparison to unique countries, total number of user entries is {}".format(users.shape[0]))


# How many missing states and how many missing countries?
print(users.State.isnull().sum())
print(users.Country.isnull().sum())



# State

un_state=state.unique()
un_state = sorted(un_state)


# Count number of users per each state
states = users.State.value_counts()
# Show the top 10 states based on their corresponding book users:
users.State.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 States/Provinces per Book Users', alpha=.70)


# Replace any instance of ' n/a'  'with 'other'

import re
sum(users.State==' n/a') #  12527
users['State'].replace(r'[\s]n/a', 'other', regex = True, inplace=True)

users.State.replace(' n/a', 'other', inplace=True)
# sum(users.State==' n/a') #  0


users.State.str.replace(r'[\s]*(n/a)[\s]*', 'other', regex=True)  # inplace=True)



# works
re.sub(r' n/a','other',users.State[30])
re.sub(r'[\s]*(n/a)[\s]*','other', users.State[30])


def replace_na(series):
    new_series = re.sub(r'[\s]*(n/a)[\s]*','other',series)
    return new_series

new_State = re.sub(r'[\s]*(n/a)[\s]*','other',users.State) 

state = pd.Series(users['State'])
state.apply(replace_na)

users['State2']=users['State'].apply(replace_na) 


# Replace any instances of '.' or othe punctuation signs with 'other'.
import string
sum(users.State == ' .') # 15
users['State'].replace(r'[\s]\.', 'other', inplace =True, regex= True)

users['State'].str.replace('[{}]'.format(string.punctuation), 'other')


# replace empty-string instances
users.State.replace('', 'other', inplace=True)


'''Finally, there are some interesting double-letter or three-letter acronyms that my guess is they might correspond to US/other state or province acronyms. A visit to https://www.fs.fed.us/database/feis/format.html revealed the accuracy of my hunch for some of these, like the 'ca', 'nh', 'mi', 'df' etc. Others, like 'zh', 'sp' or 'rm' did not correspond to any of these states/provinces.

I've downloaed the US/Canada province dictionary from here: http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/ and saved them all in py called provinces_mapping.pyc.

'''

# Replace state/province acronyms with their full names.
from provinces_mapping import provinces

# Replace state/province acronyms with their full names.
from provinces_mapping import provinces
# lower-case dictionary key-value pairs to match ours
dict((k.lower(), v.lower()) for k,v in provinces.iteritems())
# map the dictionary to the State column
users['State'].map(provinces)  

outdict = {}
for k, v in {'My Key': 'My Value'}.iteritems():
    outdict[k.lower()] = v.lower()


# Missing Values
sum(users.State.isnull()) # 1
# Replace Null values with 'other'
df['State'] = df['State'].fillna('other')


#plot again
users.State.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 States/Provinces per Book Users', alpha=.70)


# Country

countries = users.Country.value_counts()

# Show the top 10 countries according to their corresponding book users:
users.Country.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Countries per Book Users', alpha=.70)


# How many countries are string-empty?
print(users[users.Country == ''].Country.value_counts())
# Replace empty string with 'other' string.
users.Country.replace('', 'other', inplace=True)


# countries.Country contains the following inconsistences : ',' ,'n/a', 


sum(users.Country == ' n/a') #16
users['Country'].replace(r'[\s]n/a', 'other', regex = True, inplace=True) 


# work 
#users['Country'].replace(r'[\s]\,', 'other', inplace =True, regex= True)
users['Country'].replace(r'[\s][,.]', 'other', inplace =True, regex= True)


# Replace missing Value
sum(users.Country.isnull())
users['Country'] = users['Country'].fillna('other')


# # # # # # # # # Checking for other inconsistencies, 'scotland/uk','uk,united kingdom', 'illinois, usa'

# Groupby functions and Plots
# groupby function  by location levels.

#plot again
users.Country.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Countries per Book Users', alpha=.70)






# Town


users.Town.nunique()   # 32770

# Count number of users per each state
towns = users.Town.value_counts()
# Show the top 10 states based on their corresponding book users:
users.Town.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Towns per Book Users', alpha=.70)


print(users.Country.isnull().sum()) # 2

# Revove null values and replace with 'other'
users['Town'] = users['Town'].fillna('other')


# any n/a values?
sum(users.Town == 'n/a')
# Replace n/a with other
users['Town'].replace(r'n/a', 'other', regex = True, inplace=True)
 
# Replace punctuation marks with 'other'
users['Town'].replace(r'[,.?]', 'other', inplace =True, regex= True)

# any acronyms? 'c', b, ny, nis,

#plot again
users.Town.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Towns per Book Users', alpha=.70)




# AGE

users.Age.describe()
# remove null values
users.Age.isnull().any()).sum() #1
users.Age.nunique()   # 165


# visual inspection observe a lot of nan
# mask out nan values
mask= ~np.isnan(users.Age) # What to do with those?




###############
## Show range of Age values


users.loc[(users.age<5) | (users.age>100), 'age'] = np.nan

################

# alternatively with sns
# distplot can't handle missing values
sns.distplot(users.Age[~np.isnan(users.Age)])



# Observe values outside normal range. Spot which are, and/or remove
mask_out=users[users.Age>100]
pylab.hist(users.Age[mask_out])
pylab.show()





#  Duplicate entries, missing entries, wrong data types ofr users.userID




# joint plots of Age with Town/State/COuntry



# Books
books.info()
# Describe numerical variables
books.describe()

# Describe categorical variables
books.describe(include=['O'])

# Check 5 first entries
books.head(5)

#check for missing value
books.isnull().any().any()



# do i need ImageUrl??? If not drop them using
books.drop(['ImageUrlS', 'ImageUrlM', 'ImageUrlL'], axis=1, inplace=True)

books.dtypes

# BookTitle, !!!!!!
top_titles = books.book_title.value_counts()[:10]
print('The 10 book titles with the most entries in the books table are:\n{top_titles}')
# tsekare me allon tropo pws vriskw unique entries se string.
books[books.book_title=='Jane Eyre']
'''

It looks like each ISBN assigned to the book 'Jane Eyre' has different Publisher and Year of Publication values also.
It might be more useful for our model if we simplified this to give each book a unique identifier, independent of the book format, as our recommendations will be for a book, not a specific version of a book. Therefore, all values in the Jane Eyre example above would stay the same,
except all of the Jane Eyre entries would additionally be assigned a unique ISBN code as a new field.
'''

# Convert years to float
books.year_of_publication = pd.to_numeric(books.year_of_publication, errors='coerce')
# Check for 0's or NaNs in Year of Publication
zero_yr = books[books.year_of_publication == 0].year_of_publication.count()
nan_yr = books.year_of_publication.isnull().sum()
print('There are {zero_yr} entries as \'0\', and {nan_yr} NaN entries in the Year of Publication field')
# Replace all years of zero with NaN
books.year_of_publication.replace(0, np.nan, inplace=True)


# BookAuthor, des posoi unique einai kai kane ena groupby me autous. Kai antistoixa plots
uniq_authors=books.BookAuthor.nunique()
top_authors = books.book_author.value_counts()[:10]
print('The 10 authors with the most entries in the books table are:\n{top_authors}')


uniq_books = books.isbn.nunique()
all_books = books.isbn.count()
top_publishers = books.publisher.value_counts()[:10]
print('The 10 publishers with the most entries in the books table are:\n{top_publishers}')



# YearofPublication, posa unique entries exw, kane groupby, kai des pws sunduazetai me BookAuthor, kai Publisher,
# kane plots kai des an mporeis na eksageis asfales sumperasma.
# how to handle weird/outlier entries for yearofPublication. Omit them (that's what most did)


# Publisher, empty strings in publisher??




# Ratings

ratings.info()
# Describe numerical variables
ratings.describe()

# Describe categorical variables
ratings.describe(include=['O'])

# Check 5 first entries
ratings.head(5)

# Check datatypes

book_ratings.dtypes

# check for missing value
ratings.isnull().any().any()

#  




super_users = book_ratings.groupby('user_id').isbn.count().sort_values(ascending=False)
print('The 20 users with the most ratings:\n{super_users[:20]}')


# plot histograms, e.g ratings-counts, 

'''Seems like most of the entries have a rating of zero!
After doing some research on the internet regarding this (and similar) datasets, it appears that the rating scale is actually from 1 to 10, and a 0 indicates an 'implicit' rather than an 'explicit' rating. An implicit rating represents an interaction (may be positive or negative) between the user and the item. Implicit interactions usually need to be handled differently from explicit ones.
For the modeling step we'll only be looking at explicit ratings, and so the 0 rating entry rows will be removed.
'''

# remove entries with ratings of 0. E.g.
book_ratings = book_ratings[book_ratings.book_rating != 0]



# TABLE JOINS
# join books and ratings on ISBN
books_with_ratings = book_ratings.join(books.set_index('isbn'), on='isbn')

books_with_ratings.book_title.isnull().sum()
len(books_with_ratings)/books_with_ratings.book_title.isnull().sum()

books_with_ratings.dropna(subset=['book_title'], inplace=True) # remove rows with missing title/author data

# inspect new table, info and shape


# Let's see which books have the highest cumulative book rating values.

#  What about the highest average ratings (with a minimum of at least 50 ratings recieved)?


# How about the lowest-rated books?


# Now I'd like to tackle the challenge of the same book potentially having multiple ISBN numbers (for the different formats it is available in). We should clean that up here before we add the 'user' table.
# Restrict books to a "single ISBN per book" (regardless of format)

print('There are {len(has_mult_isbns)} book titles with multiple ISBN numbers which we will try to re-assign to a unique identifier')






# Join the 'users' table on the 'user_id' field

books_users_ratings = books_with_ratings.join(users.set_index('user_id'), on='user_id')

# inspect new table, info and shape




# # #  RECOMMENDER SYSTEM

# 1. Simple recommendations based on rating counts
rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
rating_count.sort_values('bookRating', ascending=False).head()

# 1. Recommendation based on correlation. We use Pearsons’R correlation coefficient to measure the linear correlation between two variables, in our case, the ratings for two books.
# First, we need to find out the average rating, and the number of ratings each book received.

average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
average_rating.sort_values('ratingCount', ascending=False).head() # more on this on datascienceplus.com



# 3. Collaborative Filtering Using k-Nearest Neighbors (kNN) -  code: datascienceplus

# 4. Collaborative Filtering Using Matrix Factorization -  code: datascienceplus

# 5. User-based CF OR item-based CF, check towardsdatascience and Github/fellowshipai


# Think about how to evaluate results? recall/precision?



# Suprise library 
# where Several common model-based algorithms including SVD, KNN, and non-negative matrix factorization are built-in!







# Results 
 
# Plots-Visualization of results 
 
# Conclusions – Discussion 






