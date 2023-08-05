
__module_name__ = "_setup_matplotlib_params.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = 0.0.74


# import packages -------------------------------------------------------------
import os
import pydk
import matplotlib


# primary function ------------------------------------------------------------
def _setup_matplotlib_params(return_CLI=False):
    
    """install mscorefonts and clear the previous parameter cache file (should it exist)"""
    
    CLI = pydk.conda_package_installer("mscorefonts", "conda-forge")
    CLI.conda_list()
    CLI.install()

    _ = os.system("rm -rf ~/.cache/matplotlib")

    _font = {"size": 12}
    matplotlib.rc(_font)
    matplotlib.rcParams["font.sans-serif"] = "Arial"
    matplotlib.rcParams["font.family"] = "sans-serif"
    
    if return_CLI:
        return CLI