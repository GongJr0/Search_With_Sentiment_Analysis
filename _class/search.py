import googlesearch as gs # type: ignore
import requests # type: ignore
import pandas as pd

from typing import List, Optional
from _class.types import Url, Result, ResultSeries

class Search:
    """Class to search for URLs using Google search.
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def run(query: str, num: int = 10, lang: str = 'en', **kwargs) -> Result:
        """Search for URLs using Google search.

        Args:
            query (str): Query to search for
            num (int, optional): Number of results to return. Defaults to 10.
            lang (str, optional): Language of the search. Defaults to 'en' (English).

        Returns:
            Result: List of URLs found in the search
        """
        result = gs.search(query, stop=num, lang=lang, **kwargs)
        
        out: Result = [Url(x) for x in result]
        return out
    
    @staticmethod
    def series(query: str, num: int = 10, lang: str = 'en', name: Optional[str] = None, **kwargs) -> ResultSeries:
        """Search for URLs using Google search and return a pandas Series.

        Args:
            query (str): Query to search for
            num (int, optional): Number of results to return. Defaults to 10.
            lang (str, optional): Language of the search. Defaults to 'en' (English).
            name (Optional[str], optional): Name of the Series. Defaults to None.

        Returns:
            ResultSeries: Pandas Series of URLs found in the search
        """
        name = name if name else query
        return pd.Series(Search.run(query, num, lang, **kwargs), name=name)
    
    @staticmethod
    def series_from_list(queries: Result, name: Optional[str] = None) -> ResultSeries:
        """Generate a pandas Series from a list of URLs.

        Args:
            queries (Result): List of URLs
            name (Optional[str], optional): Name of the Series. Defaults to None.

        Returns:
            ResultSeries: Pandas Series of URLs
        """
        name = name if name else None
        return pd.Series(queries, name=name)