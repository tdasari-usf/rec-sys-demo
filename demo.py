from main import Recommender

interactions_file = "./users_interactions.csv"
articles_file = "./shared_articles.csv"

recommender = Recommender(interactions_file, articles_file)

person_id = -1032019229384696495
res = recommender.get_recommendations(person_id, 30)

print(res)