import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle as pkl

from movie_engine.preprocessing.scaler import Scaler
from movie_engine.preprocessing.encoder import (
    GenreEncoder, LanguageEncoder, PopularityEncoder)
from movie_engine.preprocessing.encoder_models import Languages, Genres
from movie_engine.models.DAO import InputPredict



class MovieModel(object):

    def __init__(self, data: pd.DataFrame, metadata: pd.DataFrame) -> None:
        self.movies = data.set_index("tmdb_id")
        self.metadata = metadata.set_index("tmdb_id")

        self.release_year_scaler = Scaler()
        self.runtime_scaler = Scaler()
        self.vote_average_scaler = Scaler()

        self.languages_encoder = LanguageEncoder(Languages())
        self.genres_encoder = GenreEncoder(Genres())
        self.popularity_encoder = PopularityEncoder()

    def fit(self):
        self.release_year_scaler.fit(self.movies["release_year"])
        self.runtime_scaler.fit(self.movies["runtime"])
        self.vote_average_scaler.fit(self.movies["vote_average"])

        self.movies["release_year"] = self.release_year_scaler.\
            transform(self.movies["release_year"])
        self.movies["runtime"] = self.runtime_scaler.\
            transform(self.movies["runtime"])
        self.movies["vote_average"] = self.vote_average_scaler.\
            transform(self.movies["vote_average"])

    def predict(self, inputPredict: InputPredict, n_predictions=5):

        genres = [inputPredict.genre1, inputPredict.genre2, inputPredict.genre3]
        predict_dict = self.genres_encoder.encode(genres)

        predict_dict.update(self.languages_encoder.encode(inputPredict.language))

        predict_dict.update({"popularity_class": self.popularity_encoder.encode(inputPredict.popularity)})

        predict_dict.update({"release_year": self.release_year_scaler.transform(inputPredict.release_year)})
        predict_dict.update({"runtime": self.runtime_scaler.transform(inputPredict.runtime)})
        predict_dict.update({"vote_average": self.vote_average_scaler.transform(inputPredict.vote_average)})

        predict_df = pd.DataFrame([predict_dict])
        predict_df = predict_df[list(self.movies.columns)]

        X = self.movies.values
        idx = self.movies.index
        y = predict_df.values
        similarity = cosine_similarity(X, y)
        similarity = pd.Series(similarity.reshape(1, -1)[0], idx)
        similarity.sort_values(ascending=False, inplace=True)

        most = similarity.head(n_predictions).index

        recommended = self.metadata.loc[most, :]
        recommended["probability"] = similarity[:n_predictions]
        return recommended
    

    def save(self, path: str):
        with open(path, "wb") as fp:
            pkl.dump(self, fp)

    @staticmethod
    def load(path):
        with open(path, "rb") as fp:
            model = pkl.load(fp)
        return model