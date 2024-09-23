from typing import NewType, Sequence
from pandas import Series
from textblob import Word # type: ignore

# Search Return Types
Url = NewType('Url', str)
Result = Sequence[Url]
ResultSeries = Series # type: ignore

# Scrape Return Types
UrlText = NewType('UrlText', str)
TextGroup = Sequence[UrlText]

# Sentiment Return Types
Words = Sequence[Word]
