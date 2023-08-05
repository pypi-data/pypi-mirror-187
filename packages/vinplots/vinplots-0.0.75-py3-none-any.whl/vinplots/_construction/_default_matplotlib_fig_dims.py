
__module_name__ = "_default_matplotlib_fig_dims.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# import packages -------------------------------------------------------------
import matplotlib
import numpy as np


# primary function ------------------------------------------------------------
def _default_matplotlib_fig_dims():

    """
    Return default height and width of matplotlib figures.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    w, h
        array of shape: (2,) containing elements: [width, height]
        of the default matplotlib figure size
        type: numpy.ndarray
        
    Notes:
    ------
    (1) 
    """

    default_wh = matplotlib.rcParams["figure.figsize"]  # w x h
    w, h = default_wh[0], default_wh[1]

    return np.array([w, h])