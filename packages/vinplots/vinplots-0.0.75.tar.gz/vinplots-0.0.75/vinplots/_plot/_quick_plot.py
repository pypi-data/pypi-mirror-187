
__module_name__ = "_quick_plot.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# import local dependencies ---------------------------------------------------
from ._Plot import _Plot


# main function ---------------------------------------------------------------
def _quick_plot(nplots=1, ncols=1, spines_to_delete=['top', 'right'], rm_ticks=False, **construct_kwargs):
    
    if spines_to_delete == "all":
        spines_to_delete = ['top', 'bottom', 'left', 'right']
    
    fig = _Plot()
    fig.construct(nplots=nplots, ncols=ncols, **construct_kwargs)
    fig.modify_spines(ax="all", spines_to_delete=spines_to_delete)
    axes = fig.linearize()
    
    if rm_ticks:
        for ax in axes:
            ax.set_xticks([])
            ax.set_yticks([])

    return fig, axes