import pandas as pd
import numpy as np
from typing import Union

class Scaler(object):

    def __init__(self) -> None:
        pass

    def fit(self, serie: pd.Series) -> None:
        self.max_ = serie.max()
        self.min_ = serie.min()

    def transform(self, value: Union[int, float, pd.Series]) -> Union[pd.Series, float]:
        return np.round((value - self.min_) / (self.max_ - self.min_), 3)