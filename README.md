# Book-Recommnder-System

Introduction 

Wikipedia defines recommender systems too narrowly, as “a subclass of information filtering systems that seeks to predict the ‘rating’ or ‘preference’ that a user would give to an item”. Recommender systems are active information filtering systems that personalize the information coming to a user based on his interests, relevance of the information, etc. Recommender systems are used widely for recommending movies, articles, restaurants, places to visit, items to buy, and more. //Give your own explanation of what is a recommender system OR find one that you find mostly appealing/relevant 
Types of recommender systems 
correlation based 
Collaborative filterin 
Content-based  
Hybrid of the two 
Socio-demographic-based 
Contextual-based. 
 
 
 
As per requested, in the EXUS task description, I am going to get my hands on some sort of Collaborative filtering method. Before, we begin with the implementation part, allow me to introduce you to the methodology first. 
Collaborative Filtering (CF) has two main implementation strategies: 
 
Memory-based: This approach uses the memory of previous users interactions to compute users similarities based on items they've interacted with (user-based approach) or compute items similarities based on the users that have interacted with them (item-based approach). 
A typical example of this approach is User Neighbourhood-based CF, in which the top-N similar users (usually computed using Pearson correlation) for a user are selected and used to recommend items those similar users liked, but the current user have not interacted yet. This approach is very simple to implement, but usually do not scale well for many users.  
 
Model-based: This approach, models are developed using different machine learning algorithms to recommend items to users. There are many model-based CF algorithms, like neural networks, bayesian networks, clustering models, and latent factor models such as Singular Value Decomposition (SVD) and, probabilistic latent semantic analysis. //αυτο μένει εδώ ή μπορείς να το πας στα enhancements/future directions 
 
 
Set-up 
 
Technologies used: Python, version? Anaconda 
                   Jupyter notebook (web based interactive environment) 



Work Flow

Report


