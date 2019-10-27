Jupyter Notebook
Untitled
Autosave Failed!
Current Kernel Logo
Visit repo
Copy Binder link
Python 3 errorNot Trusted
File
Edit
View
Insert
Cell
Kernel
Widgets
Help
Run
Book Crossing Recommendation System
Author: Eleni Zarogianni October 2019
Objective: to implement a Book Recommender system that utilizes some sort of collaborative filtering using the online-available Book-Crossing Data set (http://www2.informatik.uni-freiburg.de/~cziegler/BX/)
In [ ]:

# import libraries
# for data manipulation
import pandas as pd
import numpy as np
# for plotting
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pylab
import seaborn as sns
​
plt.style.use('classic')
plt.style.use('seaborn-whitegrid')
Load Data The readily available Book Crossing Data set is used here. This dataset has been compiled by Cai-Nicolas Ziegler in 2004, and it comprises of three tables for users, books and ratings.
BX-Users : Contains the users. User IDs (User-ID) have been anonymized and map to integers. Demographic data is provided (Location, Age) if available.
BX-Books : Books are identified by their respective ISBN. Invalid ISBNs have already been removed from the dataset. Moreover, some content-based information is given (Book-Title, Book-Author, Year-Of-Publication, Publisher), obtained from Amazon Web Services. Note that in case of several authors, only the first is provided. URLs linking to cover images are also given, appearing in three different flavours (Image-URL-S, Image-URL-M, Image-URL-L), i.e., small, medium, large.
BX-Book-Ratings : Contains the book rating information. Ratings (Book-Rating) are either explicit, expressed on a scale from 1-10 (higher values denoting higher appreciation), or implicit, expressed by 0.
Let's jump straight into reading the csv files as pandas Dataframes (Dfs).
In [ ]:

users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1"
Inspect and clean the data In general, data inspection and cleaning prosedures include visually inspecting the data, through the use of graphs and plots, and figuring out any inconsistencies or peculiarities in the data sets. These might include, on a first-level, any duplicate entries or missing values, any wrongly assigned data types, and on a second-level any outliers. We will explore and handle each aspect of these below.
Let's have a first glance at the data and check the Df's shape.
In [ ]:

# print the shape of the data
print users.shape
print books.shape
print ratings.shape
That looks fine. On itinial inspection, all 3 Df's contain column names with a '-'.That will lead to problems accessing the dataframes,so let's change them.
In [ ]:

# remove middle slash  
users.columns = ['userID', 'Location', 'Age']
books.columns = ['ISBN', 'BookTitle', 'BookAuthor', 'YearOfPublication', 'Publisher', 'ImageUrlS', 'ImageUrlM', 'imageUrlL']
ratings.columns = ['userID', 'ISBN', 'BookRating']
Also on a first-look basis, we can already spot missing values (e.g. in the users.Age variable), but let's have a closer look and address each dataframe's idiosynchracies separately.
USERS DataFrame
In [ ]:

# Check 5 first entries
users.head(5)
# Get basic info first.
users.info()
# Describe numerical variables
users.describe()
# Describe categorical variables
users.describe(include=['O'])
In [ ]:

# check for missing values
users.Location.isnull().any()
# check for for duplicate entries
users.Location.nunique()
​
# split users.Location into 3 subparts
location_expanded = users.Location.str.split(',', 2, expand=True)
location_expanded.columns = ['Town', 'State', 'Country']
users = users.join(location_expanded)
# Drop the initial Location variable.
users.drop('Location', axis=1, inplace = True)

So, Location has no missing values and there are non-unique entries (duplicates), which is certainly OK. We've splitted up into 3 sub-parts as described and dropped the initial, corresponding variable.
​
Now, let's go an extra mile here, by having a look at some descriptives for location and some plots.
In [ ]:

# Again, check on missing values and duplicates.
print(users.Town.isnull().any())
print(users.State.isnull().any())
print(users.Country.isnull().any())
​
​
# How many unique towns, states and countries do I have?
nTowns=users.Town.nunique()
nStates=users.Town.nunique()
nCountries=users.Country.nunique()
​
print("There are {} unique towns, {} unique states and {} unique coutries.".format(nTowns, nStates, nCountries))
print("In comparison to unique countries, total number of user entries is {}".format(users.shape[0]))
# users.userID.nunique()

There are missing values for State and Country, which is problematic and requires to be dealt with. 
There are 32770 unique town and state entries, and 1276 unique coutries, in contrast to 278858 unique user entries (unique userIDs).
In [ ]:

# How many missing states and how many missing countries?
print(users.State.isnull().sum())
print(users.Country.isnull().sum())

There are 1 missing value for State and 2 for the Country variable. 
Let's do barplots for each.
In [ ]:

# State
# Count number of users per each state
states = users.State.value_counts()
# Show the top 10 states based on their corresponding book users:
users.State.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 States/Provinces per Book Users', alpha=.70)

A closer visual inspection of the states Df revealed other inconsistences too. For example, there are 'n/a' or '\n/a\"'instances. I've also spotted a '.' instance, so there might as well exist other english stopwords. The best solution I think would be to throw all these instances in an 'Other' bin.
​
In [ ]:

# Replace any instance of n/a, with 'other'
sum(users.State==' n/a') #  12527
users['State'].replace(r'[\s]n/a', 'other', regex = True, inplace=True)
In [ ]:

# Replace any instances of '.' or othe punctuation signs with 'other'.
import string
sum(users.State == ' .') # 15
users['State'].replace(r'[\s]\.', 'other', inplace =True, regex= True)
​
In [ ]:

# replace empty-string instances
users.State.replace('', 'other', inplace=True)

Finally, there are some interesting double-letter or three-letter acronyms that my guess is they might correspond to US/other state or province acronyms. A visit to https://www.fs.fed.us/database/feis/format.html revealed the accuracy of my hunch for some of these, like the 'ca', 'nh', 'mi', 'df' etc. Others, like 'zh', 'sp' or 'rm' did not correspond to any of these states/provinces.
​
I've downloaed the US/Canada province dictionary from here: http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/ and saved them all in py called provinces_mapping.py.
​
In [ ]:

# Replace state/province acronyms with their full names.
from provinces_mapping import provinces
# lower-case dictionary key-value pairs to match ours
dict((k.lower(), v.lower()) for k,v in provinces.iteritems())
# map the dictionary to the State column
users['State'].map(provinces)  
​
In [ ]:

# Missing Values
sum(users.State.isnull()) # 1
# Replace Null values with 'other'
df['State'] = df['State'].fillna('other')
In [ ]:

#plot again
users.State.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 States/Provinces per Book Users', alpha=.70)
In [ ]:

# Country
# Count number of users per each country
countries = users.Country.value_counts()
# Show the top 10 countries according to their corresponding book users:
users.Country.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Countries per Book Users', alpha=.70)

USA is number one on books, with over 130.000 users, with Canada falling second with sixth below the amount of US. Interestingly, we observe in the 9th position an 'empty-string-country'. 
In [ ]:

# How many countries are string-empty?
print(users[users.Country == ''].Country.value_counts())
# Replace empty string with 'Other' string.
users.Country.replace('', 'other', inplace=True)

Upon closer inspection of the countries Df (series actually), we observe a bunch of inconsistencies with misplaced strings, such as: ',' ,'n/a', 'scotland/uk','uk,united kingdom', 'illinois, usa'
In [ ]:

# #   Checking for other inconsistencies
# countries.Country contains the following inconsistences : ',' ,'n/a', 'scotland/uk','uk,united kingdom', 'illinois, usa'
​
sum(users.Country == ' n/a') #16
users['Country'].replace(r'[\s]n/a', 'other', regex = True, inplace=True) 
​
users['Country'].replace(r'[\s][,.]', 'other', inplace =True, regex= True)
​
In [ ]:

# Replace missing Value
sum(users.Country.isnull())
users['Country'] = users['Country'].fillna('other')
In [ ]:

# # # # # # # # # Checking for other inconsistencies, 'scotland/uk','uk,united kingdom', 'illinois, usa'
​
# Groupby functions and Plots
# groupby function  by location levels.
In [ ]:

# Town
​
# Count number of users per each state
towns = users.Town.value_counts()
# Show the top 10 states based on their corresponding book users:
users.Town.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Towns per Book Users', alpha=.70)
​
In [ ]:

users.Town.nunique()   # 32770
print(users.Country.isnull().sum()) # 2
​
# Revove null values and replace with 'other'
users['Town'] = users['Town'].fillna('other')
​
​
# any n/a values?
sum(users.Town == 'n/a')
# Replace n/a with other
users['Town'].replace(r'n/a', 'other', regex = True, inplace=True)
 
# Replace punctuation marks with 'other'
users['Town'].replace(r'[,.?]', 'other', inplace =True, regex= True)
​
 # # # # Checking for other inconsistencies, acronyms? 'c', b, ny, nis, !!!!!!!
    
    
    
    
In [ ]:

#plot again
users.Town.value_counts()[:10].plot(kind='bar', stacked = 'True', title='Top 10 Towns per Book Users', alpha=.70)
​

AGE
In [ ]:

users.Age.describe()
​
​
​
# remove null values
users.Age.isnull().any()).sum() #1
users.Age.nunique()   # 165
​
​
# observe a lot of nan
# mask out nan values
mask= ~np.isnan(users.Age)
​
​
​
###############
## create bins for Age values
In [ ]:

​
In [ ]:

​
