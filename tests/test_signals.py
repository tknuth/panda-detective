from panda_detective import signals
from panda_detective.testing import load_people
from pandas.testing import assert_series_equal


def test_base():
    df = load_people()

    signal = signals.Signal(["age", "gender"])
    assert signal.config is None
    assert signal.column is None
    assert signal.type is None
    assert signal.value(df).isna().all()
    assert signal.__str__() == "<Signal>"

    signal = signals.Signal(["age"])
    assert signal.column == "age"
    assert_series_equal(signal.value(df), df.age)

    assert signals.Signal(["age"]) == signals.Signal(["gender"])


def test_range():
    df = load_people()
    signal = signals.RangeSignal(["age"], [18, 25])
    assert signal.config == "[18, 25]"
    assert signal.active(df).to_dict() == {
        "a": False,
        "b": True,
        "c": False,
        "d": True,
        "e": True,
    }


def test_notna():
    df = load_people()
    signal = signals.NotNASignal(["age", "gender"])
