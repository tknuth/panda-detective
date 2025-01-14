from data_signals import signals
from data_signals.collection import SignalCollection
from data_signals.testing import load_people
from pandas.testing import assert_series_equal, assert_frame_equal
import numpy as np
import pandas as pd

# TODO: test with other data types (datetime)


def test_range():
    df = load_people()
    signal = signals.RangeSignal(["age"], [18, 25])
    assert signal.config == "[18, 25]"
    assert_series_equal(
        signal.active(df),
        pd.Series(
            {
                "a": False,
                "b": True,
                "c": False,
                "d": True,
                "e": False,
            },
            name="age",
            dtype="boolean",
        ),
    )
    result = SignalCollection(df, signals=[signal]).evaluate(df)
    assert_series_equal(
        result.show().description,
        pd.Series(
            {
                "b": "Value 32 is outside [18, 25].",
                "d": "Value 47 is outside [18, 25].",
            },
            name="description",
        ),
    )
    assert_frame_equal(
        result.summarize(),
        pd.DataFrame(
            {
                "column": ["age"],
                "type": ["range"],
                "config": ["[18, 25]"],
                "ratio": [0.4],
                "description": ["40% of values are outside [18, 25]."],
            }
        ),
    )


def test_non_numeric_value():
    df = load_people()
    df.loc["a", "age"] = np.nan
    signal = signals.RangeSignal(["age"], [18, 25])
    assert signal.config == "[18, 25]"
    assert_series_equal(
        signal.active(df),
        pd.Series(
            {
                "a": False,
                "b": True,
                "c": False,
                "d": True,
                "e": False,
            },
            name="age",
            dtype="boolean",
        ),
    )
    result = SignalCollection(df, signals=[signal]).evaluate(df)
    assert_series_equal(
        result.show().description,
        pd.Series(
            {
                "b": "Value 32 is outside [18, 25].",
                "d": "Value 47 is outside [18, 25].",
            },
            name="description",
        ),
    )
    assert_frame_equal(
        result.summarize(),
        pd.DataFrame(
            {
                "column": ["age"],
                "type": ["range"],
                "config": ["[18, 25]"],
                "ratio": [0.4],
                "description": ["40% of values are outside [18, 25]."],
            }
        ),
    )
