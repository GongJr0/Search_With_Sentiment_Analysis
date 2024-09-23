import bs4 # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

from typing import List, Union, cast

from _class.types import Url, Result, ResultSeries, UrlText, TextGroup
import nltk # type: ignore

class Scrape:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_text(cls, url: Url) -> UrlText:
        try:
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Request on URL: {url} failed with status code: {response.status_code}")
                return cast(UrlText, '')
            
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            

            out: str = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])
            len_before = len(out)
            out = ' '.join([word for word in out.split() if word.lower() not in cls.STOPWORDS])
            len_after = len(out)
            
            print(f"Removed {len_before - len_after} stopwords from URL: {url}")
            return cast(UrlText, out)
        
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Request on URL: {url} failed with exception: {e}")
            return cast(UrlText, '')
            
    
    @staticmethod
    def textify_results(result: Union[Result, ResultSeries]) -> TextGroup:
        out: TextGroup = [Scrape.get_text(url) for url in result]
        return out
    
 
    STOPWORDS: List[str] = nltk.corpus.stopwords.words('english')