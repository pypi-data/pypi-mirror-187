
__module_name__ = "__init__.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# import API ------------------------------------------------------------------
from . import _construction as build
from . import _style as style
from . import _utilities as ut

# import main API functions ---------------------------------------------------
from ._plot._Plot import _Plot as Plot
from ._plot._quick_plot import _quick_plot as quick_plot
from ._construction._save_figure import _save_figure as save

# fetch color palettes --------------------------------------------------------
from ._color_palettes._ColorPalettes import _ColorPalettes

colors = _ColorPalettes()
