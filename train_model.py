import pandas as pd
from movie_engine.models.recommender import MovieModel
from movie_engine.models.DAO import InputPredict


if __name__ == "__main__":
    data = pd.read_csv("./datasets/movies_dataset_model.csv", index_col=0)
    data_metadata = pd.read_csv("./datasets/movies_dataset_metadata.csv", index_col=0)

    model = MovieModel(data, data_metadata)

    model.fit()

    model.save("movie_model_fitted.mr")
    model = MovieModel.load("movie_model_fitted.mr")

    test = InputPredict()
    test.genre1 = "adventure"
    test.genre2 = "family"
    test.genre3 = "fantasy"
    test.release_year = 2001
    test.runtime = 152
    test.vote_average = 7.5
    test.popularity = 38
    test.language = "english"

    recommended = model.predict(test)

    print(recommended)