from fastapi import FastAPI
from Recommender import Recommender
from functools import lru_cache
from setup import setup
from pydantic import BaseModel


app = FastAPI()

interactions_file = "./users_interactions.csv"
articles_file = "./shared_articles.csv"

recommender = Recommender(interactions_file, articles_file)


ids = {"A": 4142810830429822977,
       "B": -6502100706127527925,
       "C": -8694104221113176052,
       "D": 1234688818012827660,
       "E": -1678759546322702318,
       "F": 1455185896278818838}


@lru_cache(maxsize=32)
def get_recommendations(person_id):
    res = recommender.get_recommendations(person_id, 30)
    return res


@app.get("/with_cache")
def index(id: str = "D", limit: int = 30):
    user_id = ids[id]
    return get_recommendations(user_id)['titles'][:limit]


@app.get("/without_cache")
def index(id: str = "D", limit: int = 30):
    setup()
    user_id = ids[id]
    res = recommender.get_recommendations(user_id, 30)
    return res['titles'][:limit]


# app.run(host="0.0.0.0", port=8000)
