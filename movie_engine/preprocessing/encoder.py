from typing import List
from movie_engine.preprocessing.encoder_models import Languages, Genres


class LanguageEncoder(object):

    def __init__(self, languages: Languages) -> None:
        self.languages = languages.__dict__

    def encode(self, value: str) -> dict:
        return {language_name: int(value == language_id)
                for language_id, language_name in self.languages.items()}
    

class GenreEncoder(object):

    def __init__(self, genres: Genres) -> None:
        self.genres = genres.__dict__

    def encode(self, values: List[str]) -> dict:
        return {genre_name: int(genre_id in values)
                for genre_id, genre_name in self.genres.items()}
    

class PopularityEncoder(object):

    def __init__(self) -> None:
        pass

    def encode(self, value: float) -> int:
        if value < 5:
            return 0
        if value < 10:
            return 1
        if value < 15:
            return 2
        if value < 20:
            return 3
        if value < 25:
            return 4
        return 5