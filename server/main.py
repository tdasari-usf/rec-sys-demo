from fastapi import FastAPI
from Recommender import Recommender
from functools import lru_cache


app = FastAPI()

interactions_file = "./users_interactions.csv"
articles_file = "./shared_articles.csv"

recommender = Recommender(interactions_file, articles_file)


@lru_cache(maxsize=32)
def get_recommendations(person_id):
    res = recommender.get_recommendations(person_id, 30)
    return res


@app.get("/with_cache")
def index(id: int = -1032019229384696495, limit: int = 30):
    return get_recommendations(id)['titles'][:limit]


@app.get("/without_cache")
def index(id: int = -1032019229384696495, limit: int = 30):
    res = recommender.get_recommendations(id, 30)
    return res['titles'][:limit]


# app.run(host="0.0.0.0", port=8000)
