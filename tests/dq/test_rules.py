import pandas as pd



def has_missing(df):
    return df.isnull().sum().sum() > 0


def has_duplicates(df):
    return df.duplicated().sum() > 0


def negative_sales(df):
    return (df["sales"] < 0).any()


def negative_profit(df):
    return (df["profit"] < 0).any()


def invalid_year(df):
    return (~df["year"].between(2015, 2035)).any()


# =====================================================
# DATA QUALITY TESTS
# =====================================================


def test_missing_values():
    df = pd.DataFrame({"a": [1, None]})
    assert has_missing(df)


def test_no_missing_values():
    df = pd.DataFrame({"a": [1, 2]})
    assert not has_missing(df)


def test_duplicates():
    df = pd.DataFrame({"a": [1, 1]})
    assert has_duplicates(df)


def test_no_duplicates():
    df = pd.DataFrame({"a": [1, 2]})
    assert not has_duplicates(df)


def test_negative_sales():
    df = pd.DataFrame({"sales": [-100]})
    assert negative_sales(df)


def test_positive_sales():
    df = pd.DataFrame({"sales": [100]})
    assert not negative_sales(df)


def test_negative_profit():
    df = pd.DataFrame({"profit": [-50]})
    assert negative_profit(df)


def test_positive_profit():
    df = pd.DataFrame({"profit": [50]})
    assert not negative_profit(df)


def test_invalid_year():
    df = pd.DataFrame({"year": [1990]})
    assert invalid_year(df)


def test_valid_year():
    df = pd.DataFrame({"year": [2024]})
    assert not invalid_year(df)
