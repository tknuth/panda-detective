import pandas as pd
from dataclasses import dataclass, field
from typing import Iterable, Optional
import numpy as np
import json


@dataclass
class Histogram:
    series: pd.Series
    bins: int
    range: Optional[Iterable[int]]

    def evaluate(self):
        y, x = np.histogram(self.series.dropna(), self.bins, self.range)
        x = map(float, x)
        y = map(int, y)
        return [{"x": round(x, 2), "y": y} for x, y in zip(x, y)]


@dataclass
class NumericVariable:
    series: pd.Series = field(repr=False)
    components: dict = field(default_factory=dict)
    description: str = None

    def histogram(self, bins=10, range=None):
        self.components["histogram"] = Histogram(self.series, bins, range)
        return self

    def evaluate(self):
        return {k: v.evaluate() for k, v in self.components.items()}
