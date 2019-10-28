# Book-Recommnder-System

Introduction 

Wikipedia defines recommender systems too narrowly, as “a subclass of information filtering systems that seeks to predict the ‘rating’ or ‘preference’ that a user would give to an item”. Recommender systems are active information filtering systems that personalize the information coming to a user based on his interests, relevance of the information, etc. Recommender systems are used widely for recommending movies, articles, restaurants, places to visit, items to buy, and more. 

Types of recommender systems:
- correlation based, subset of which is 
    - Collaborative filtering. 
- Content-based.  
- Hybrid of the two. 
- Socio-demographic-based. 
- Contextual-based. 
 
 
As per requested, in the EXUS task description, I am going to get my hands on some sort of Collaborative Filtering (CF) method. Before, we begin with the implementation part, allow me to introduce you to the methodology first. 

In general, CF methods make automatic predictions (filtering) about the interests of a user by collecting preferences from many users (collaborating). The underlying assumption of the collaborative filtering approach is that if a person A has the same opinion as a person B on a set of items, A is more likely to have B's opinion for a given item than that of a randomly chosen person. Collaborative Filtering (CF) has two main implementation strategies: 
 
    Memory-based: This approach uses the memory of previous users interactions to compute users similarities based on items         they've interacted with (user-based approach) or compute items similarities based on the users that have interacted with them       (item-based approach). 
    A typical example of this approach is User Neighbourhood-based CF, in which the top-N similar users (usually computed using Pearson correlation) for a user are selected and used to recommend items those similar users liked, but the current user have not interacted yet. This approach is very simple to implement, but usually do not scale well for many users.  
 
    Model-based: in this approach, models are developed using different machine learning algorithms to recommend items to users. There are many model-based CF algorithms, like neural networks, bayesian networks, clustering models, and latent factor models, such as Singular Value Decomposition (SVD) and probabilistic latent semantic analysis.

We will engane with the first, memory-based CF approach only.


Set-up

I have implemented the python code uwing theAnaconda distribution, Python version 2.7 , running on MacOS Mojave, version 10.14.6.
 
Technologies used: 
   - local editor: Spyder 3.1.4.
   - Jupyter notebook 4.3.1.(web based interactive environment) 
   - https://hub.gke.mybinder.org/ (to turn Git repo into interactive python notebook.)


Work Flow

Please check the EXUS_ML_REPORT.doc for a thorough description of the work-flow process. Also, thorough description of the steps and methodology used can be found on the Book_Recommender.ipynb.

I hope you enjoy browsing through my python notebook! Thank you for your time!
