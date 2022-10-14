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

### Case 3: API Interactive showcase
