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
    test.genre2 = "action"
    test.genre3 = None
    test.release_year = 2000
    test.runtime = 100
    test.language = None

    recommended = model.predict(test)

    print(recommended)