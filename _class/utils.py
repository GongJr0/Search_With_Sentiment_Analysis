import numpy as np
from typing import Sequence, Tuple

class Utils:
    """Utility class for general-purpose methods.
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def slope(arr: Sequence) -> Tuple[float, np.ndarray, np.ndarray]:
        """Calculate the slope of a sequence of values using polyfit.

        Args:
            arr (Sequence): Sequence of values

        Returns:
            Tuple[float, np.ndarray, np.ndarray]: Slope, indices, and fitted values
        """
        indices = np.arange(len(arr))
        slope, intercept = np.polyfit(indices, arr, 1)
        fitted_values = slope * indices + intercept
        
        return (slope, indices, fitted_values)