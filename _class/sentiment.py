#Sentiment analysis imports
import textblob as tb # type: ignore
from textblob import TextBlob # type: ignore

# Type imports
from _class.types import UrlText, TextGroup, Words
from typing import List, Union, Optional, Literal

# Other imports
from numpy import mean, floating, array
from pandas import Series
import matplotlib.pyplot as plt
from plotly import express as px
import plotly.graph_objects as go # type: ignore
from _class.utils import Utils

plt.style.use('bmh')

class Sentiment:
    """TextBlob wrapper class to setniment analysis methods.
    """
    def __init__(self) -> None:
        pass
    
    # Large-body sentiment analysis
    @staticmethod
    def analyze(text: UrlText) -> floating:
        """Analyze the sentiment of a body of text.

        Args:
            text (UrlText): Text to analyse (retireved from a URL)

        Returns:
            floating: Sentiment polarity of the text
        """
        blob = TextBlob(text)
        return blob.sentiment.polarity
    
    @staticmethod
    def group_average(group: TextGroup, combine: bool = True) -> Union[floating, List[floating]]:
        """Calculate the average sentiment of a group of texts.

        Args:
            group (TextGroup): Group of texts to analyze (retrieved from a URL)
            combine (bool, optional): Combine the sentiment of all texts in the group. Defaults to True.

        Returns:
            Union[floating, List[floating]]: Average sentiment of the group or list of sentiment values
        """
        analyzed: List[floating] = [Sentiment.analyze(text) for text in group]
        
        if combine:
            analyzed = [x for x in analyzed if x != '']
            return mean(analyzed)
        else:
            return analyzed
    
    @staticmethod
    def moving_average_sentiment(group: TextGroup, window: int = 500, 
                                 plot: bool = False, 
                                 plot_engine: Literal['pyplot', 'plotly'] = 'pyplot', 
                                 story_title: Optional[str] = None) -> Optional[List[floating]]:
        """Calculate the moving average sentiment of a group of texts.

        Args:
            group (TextGroup): Group of texts to analyze (retrieved from a URL)
            window (int, optional): Span of the moving average windiw. Defaults to 500.
            plot (bool, optional): Plot the moving average, returns None when True. Defaults to False.
            story_title (Optional[str], optional): Title of the story/news article to include in the plot title. Defaults to None.

        Returns:
            Optional[List[floating]]: List of moving average sentiment values.
        """
        assert window > 0, "Window must be greater than 0"
        word_split: Words = ' '.join(group).split(' ')
        
        moving_average: List[floating] = []
        for i in range(len(word_split) - window + 1):
            window_sentiment = Sentiment.wordlist_sentiment(word_split[i:i + window])
            moving_average.append(window_sentiment)
            
        if plot:
            _, x, y = Utils.slope(moving_average)
            if plot_engine == 'plotly':
                fig = px.line(Series(moving_average, name='Moving Average'), 
                              title=f'{story_title}: {window}-Word Moving Average Sentiment', 
                              labels={'index': 'Window Index', 'value': 'Average Polarity (Standardized)'})
                
                fig.update_traces(name='Moving Average', line=dict(color='rgba(0,0,0,.66)'))

                
                fig.add_scatter(x=x, y=y, mode='lines', line=dict(color='orange'), name='Slope')
                
                mean_value = mean(moving_average)
                min_value = min(moving_average)
                max_value = max(moving_average)
                
                fig.add_hline(y=mean_value, line=dict(color='red', dash='dash'), name=f'Mean = {mean_value:.2f}')
                fig.add_hline(y=min_value, line=dict(color='blue', dash='dash'), name=f'Min = {min_value:.2f}')
                fig.add_hline(y=max_value, line=dict(color='green', dash='dash'), name=f'Max = {max_value:.2f}')
                
                
                
                # Create horizontal lines and add them to the legend
                fig.add_trace(go.Scatter(x=[0, len(moving_average)], y=[mean_value, mean_value],
                                        mode='lines', line=dict(color='red', dash='dash'),
                                        name=f'Mean = {mean_value:.2f}'))
                
                fig.add_trace(go.Scatter(x=[0, len(moving_average)], y=[min_value, min_value],
                                        mode='lines', line=dict(color='blue', dash='dash'),
                                        name=f'Min = {min_value:.2f}'))
                
                fig.add_trace(go.Scatter(x=[0, len(moving_average)], y=[max_value, max_value],
                                        mode='lines', line=dict(color='green', dash='dash'),
                                        name=f'Max = {max_value:.2f}'))
                
                fig.update_layout(showlegend=True, legend=dict(x=1.05, y=1))
            
                fig.show()
                return None
            elif plot_engine == 'pyplot':
                _, ax = plt.subplots()
                plt.plot(array(moving_average), color='black', alpha=.66,label='Moving Average')
                
                plt.plot(x, y, color='orange', label=f'Slope')
                
                plt.hlines(mean(moving_average), 0, len(moving_average), colors='r', linestyles='dashed', label=f'Mean = {mean(moving_average):.2f}')
                plt.hlines(min(moving_average), 0, len(moving_average), colors='b', linestyles='dashed', label=f'Min = {min(moving_average):.2f}')
                plt.hlines(max(moving_average), 0, len(moving_average), colors='g', linestyles='dashed', label=f'Max = {max(moving_average):.2f}')
                
                plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
                
                plt.title(f'{window}-Word Moving Average Sentiment') if not story_title else plt.title(f'{story_title}: {window}-Word Moving Average Sentiment')
                
                # Hide the all but the bottom spines (axis lines)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["top"].set_visible(False)

                # Only show ticks on the left and bottom spines
                ax.yaxis.set_ticks_position("left")
                ax.xaxis.set_ticks_position("bottom")
                ax.spines["bottom"].set_bounds(min(x), max(x))
                
                plt.xlabel('Window Index')
                plt.ylabel('Average Polarity (Standardized)')
                
                plt.show()
                return None
            else:
                return moving_average
    
    # Single-word sentiment analysis
    @staticmethod
    def word_sentiment(word: str) -> floating:
        """Analyze the sentiment of a single word.

        Args:
            word (str): Word to analyze

        Returns:
            floating: Sentiment polarity of the word
        """
        return TextBlob(word).sentiment.polarity
    
    @staticmethod
    def wordlist_sentiment(group: TextGroup) -> floating:
        """Calculate the average sentiment of a group of words.

        Args:
            group (TextGroup): Group of words to analyze

        Returns:
            floating: Average sentiment of the group
        """
        groups: List[Words] = [[tb.TextBlob(text).words] for text in group]
        sentiments = []
        
        for text in groups:
            sentiment = [Sentiment.word_sentiment(str(word)) for word in text]
            sentiments.append(mean(sentiment))
        
        return mean([mean(sentiment) for sentiment in sentiments])