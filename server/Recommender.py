
import pandas as pd
import numpy as np
import pickle
from time import sleep

# from sentence_transformers import SentenceTransformer
# from sentence_transformers.util import cos_sim


class Recommender:

    def __init__(self, interactions_file, articles_file):

        self.interactions_file = interactions_file
        self.articles_file = articles_file

        # self.all_articles = pd.read_csv(articles_file)
        # self.all_articles.set_index("contentId", inplace = True)

        self.articles = self.process_articles()
        self.interactions = self.process_interactions()

        # self.similar_db = self.create_similar_items()
        self.similar_db = self.load_similar_db()
        self.popular_items = self.create_popular_items()

    def process_articles(self):

        articles = pd.read_csv(self.articles_file)
        unique_articles = articles.drop_duplicates(
            subset="title", keep='first')
        articles_final = unique_articles[unique_articles.lang == 'en']
        articles_final = articles_final[['contentId', 'title']]
        articles_final.set_index('contentId', inplace=True)
        indexes = articles_final.index.tolist()

        self.idx_to_id = {idx: content_id for idx,
                          content_id in enumerate(indexes)}
        self.id_to_idx = {content_id: idx for idx,
                          content_id in enumerate(indexes)}

        self.titles = articles_final.title.tolist()
        return articles_final

    def process_interactions(self):
        # remove non english
        #
        interactions = pd.read_csv(self.interactions_file)
        articles = pd.read_csv(self.articles_file)
        filter_en = articles[articles['lang'] == 'en']['contentId'].tolist()

        interactions = interactions[["contentId", "personId", "eventType"]]
        interactions_english = interactions[interactions['contentId'].isin(
            filter_en)]

        return interactions_english

    def load_similar_db(self):

        pickle_in_path = "./sim_ht.pkl"
        pickle_in = open(pickle_in_path, "rb")
        return pickle.load(pickle_in)

    def create_similar_items(self):

        # initalize vector model

        model_name = "bert-base-nli-mean-tokens"
        model = SentenceTransformer(model_name)

        vect_dict = dict()

        sentences = self.articles.title.tolist()
        print(f"{len(sentences)} to be vectorized...")
        # create sent_vect id
        for idx, sentence in enumerate(sentences):
            if idx % 500 == 0:
                print(f"vectorizing status -- {idx}")
            vect_dict[idx] = model.encode(sentence)

        print(f"data vectorized")

        sim_dict = dict()

        del model

        for idx_1, _ in enumerate(sentences):
            if idx_1 % 100 == 0:
                print(f"similarity calculation status --- {idx_1}")
            sim_dict[idx_1] = dict()
            for idx_2, _ in enumerate(sentences):
                if idx_1 == idx_2:
                    continue
                sim_dict[idx_1][idx_2] = cos_sim(
                    vect_dict[idx_1], vect_dict[idx_2])

            sorted_items = sorted(
                sim_dict[idx_1].items(), key=lambda x: x[1], reverse=True)
            sim_dict[idx_1] = [item[0] for item in sorted_items][:50]

        del vect_dict

        return sim_dict

    def create_popular_items(self):

        event_type_strength = {
            'VIEW': 1.0,
            'LIKE': 2.0,
            'BOOKMARK': 2.5,
            'FOLLOW': 3.0,
            'COMMENT CREATED': 4.0, }

        self.interactions['score'] = self.interactions['eventType'].apply(
            lambda x: event_type_strength[x])
        scored_content = self.interactions.groupby('contentId').count()
        popular_content = scored_content.sort_values(
            'score', ascending=False).index.tolist()

        return popular_content

    def get_interactions(self, person_id):

        person_filter = self.interactions['personId'] == person_id
        return list(set(self.interactions[person_filter].contentId.tolist()))

    def get_similar_items(self, all_interactions):
        # get similar items from input interactions
        recommended_items = []
        ix = 0

        for item in all_interactions:
            if len(recommended_items) >= 10:
                break
            item_idx = self.id_to_idx[item]
            recommended_items.append(self.similar_db[item_idx][ix])
            ix += 1

        return recommended_items

    def get_popular(self, person_id, n):

        return [self.id_to_idx[item] for item in self.popular_items[:n]]

    def alternate(self, similar_items, popular_items, n):
        return list(set(similar_items + popular_items))[:n]

    def convert_to_text(self, ids_list):
        # takes in int(id) to give content id
        content_ids = [self.idx_to_id[id] for id in ids_list]
        return self.articles.loc[content_ids].title.tolist()

    def get_recommendations(self, person_id, n):

        all_interactions = self.get_interactions(person_id)
        similar_items = self.get_similar_items(all_interactions)
        popular_items = self.get_popular(person_id, n)
        # items = self.alternate(similar_items, popular_items, n)
        similar_texts = self.convert_to_text(similar_items)
        pop_texts = self.convert_to_text(popular_items)

        sleep(3)
        return {"titles": similar_texts + pop_texts}


if __name__ == '__main__':

    interactions_file = "./users_interactions.csv"
    articles_file = "./shared_articles.csv"

    recommender = Recommender(interactions_file, articles_file)

    print("model ini")
    person_id = -1032019229384696495
    res = recommender.get_recommendations(person_id, 20)

    print(res)
