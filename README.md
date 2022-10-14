# Hashtable Behind the Scenes
Team - Ben Chen, Jessica Wang, Tejaswi Samrat Dasari.  

## Application of Hashtable
### Motivation: how do we enjoy the speed of hash functions in our daily python work?
We can cache the function results for future usage to avoid repeated computation and use the data structure of hashtable to speed up the lookup process. 
Caching is a process to store data or files in a temporary storage location - cache, so they can be accessed faster. 

### Case 1: Find the nth number in in Fibonacci Sequence
The following methods were applied:
* Use a recursive function to find the nth number
* Established a decorator to cache the function result
* Apply the cache function from the python package of functools   
It is proved that caching the result in hashtable can improve the efficiency (run-time) significantly. 

### Case 2: Recommender application

#### Implementation of Recommendation Engine: 

The objective of a Recommendation system is to recommend relevant items for users, based on their preference. Preference and relevance are subjective, and they are generally inferred by items users have consumed previously.

We build 2 models in this project 1. Semantic and 2. Popular model.

Semantic - To recommend users the items similar to thier past interactions.
Popular - To recommend users the items that are liked/shared/bookmarked/commented by majority of the users. 

Other models like collaborative filtering can also be used but for now we are only considering Semantic, and popular.

#### Encoding For Semantic vectorization

We used sentence_transformers, a library used to encode sentences to higher dimensions to capture the contextual meaning of the sentences. The dimension is of 768. For similar articles we have used cosine similarity. Cosine similarity is the angle between two vectors, parallel vectors have a cosine similarity of 1 and the ones in the opposite have a value of -1. 1 corresponds to how equal sentences. 

#### Hash Tables usage in Recommendations:

We created a Hash table using keys as the ids of the titles in the dataset. Each key has been paired to a value of lists containing top K similar sentences.

#### Recommendations serving

Given a user, we extract all the previously interacted items by the user and serve the similar items, along with popular/trending content.

#### Serving

We have used FASTAPI library to create end points, containerized using docker.

#### Furthuer improvements
1. Collaborative Filtering model could be added to make the recommendations more diverse
2. Avoid seen content to keep the user hooked.
3. Build a monitoring system to see how the performance of the models, and to guage how good the recommendations are.
4. Make use of additional features in the dataset.


#### Conclusion:

Here we leveraged the fast search of Hashtables to serve the recommendations by pre calculating the similarities in the titles of the articles.
In many situations, hash tables turn out to be more efficient than search trees or any other table lookup structure. For this reason, they are widely used in many kinds of computer softwares, particularly for associative arrays, database indexing, caches and sets.


