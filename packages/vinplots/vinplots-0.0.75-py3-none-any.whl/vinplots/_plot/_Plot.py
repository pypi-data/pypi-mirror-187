

__module_name__ = "_Plot.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# import packages -------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt


# import local dependencies ---------------------------------------------------
from .._construction._construct_plot_layout import _construct_plot_layout
from .._style._modify_axis_spines import _modify_axis_spines, _modify_all_ax_spines
from .._construction._linearize_axes import _linearize_axes


# main class ------------------------------------------------------------------
class _Plot:
    def __init__(self, tight=True, grid=True):

        """Instantiates a general plot space"""

    def construct(
        self,
        nplots,
        ncols=4,
        figsize_width=1,
        figsize_height=1,
        figsize=False,
        hspace=0.18,
        wspace=0,
        width_ratios=False,
        height_ratios=False,
    ):

        """
        Setup figure layout.
        nplots
        ncols
        figsize_width
        figsize_height
        """
        
        assert nplots >= ncols, print("nplots must be >= ncols")
        
        self._nplots = nplots
        self._hspace = hspace
        self._wspace = wspace
        self._ncols = ncols
        
        if figsize:
            self._figsize_width = self._figsize_height = figsize
        else:
            self._figsize_width = figsize_width
            self._figsize_height = figsize_height
        
        if width_ratios:
            self._width_ratios = width_ratios
        else:
            self._width_ratios = np.ones(min(self._nplots, self._ncols))

        self.fig, self.AxesDict = _construct_plot_layout(
            nplots=self._nplots,
            ncols=self._ncols,
            figsize_width=self._figsize_width,
            figsize_height=self._figsize_height,
            grid_hspace=self._hspace,
            grid_wspace=self._wspace,
            width_ratios=self._width_ratios,
            height_ratios=height_ratios,
        )
        
    def linearize(self):
        
        return _linearize_axes(self.AxesDict)
        
    def modify_spines(self,
                      ax,
                      color=False,
                      spines_to_color=False,
                      spines_to_delete=False,
                      spines_to_move=False,
                      spines_positioning="outward",
                      spines_positioning_amount=0,):
        
        """
        
        """
        
            
        if ax=="all":
            mod_func = _modify_all_ax_spines
            ax=self.AxesDict
        else:
            mod_func = _modify_axis_spines
            
        mod_func(ax, 
                 color, 
                 spines_to_color, 
                 spines_to_delete,
                 spines_to_move,
                 spines_positioning,
                 spines_positioning_amount,)
        