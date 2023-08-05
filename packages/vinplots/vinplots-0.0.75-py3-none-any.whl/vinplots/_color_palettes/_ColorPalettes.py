
__module_name__ = "_ColorPalettes.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"

# import packages -------------------------------------------------------------
import os
import pydk
import matplotlib as mpl
import numpy as np


# static ----------------------------------------------------------------------
PalettePathDict = {
    "warm": "warm_palette.pkl",
    "share_seq": "share_seq_palette.pkl",
    "BuOr": "BuOr_palette.pkl",
    "BlueSand": "BlueSand_palette.pkl",
    "LARRY_in_vitro": "LARRY_in_vitro_palette.pkl",
    "pbmc3k":"pbmc3k_palette.pkl",
}


# supporting function ---------------------------------------------------------
def _load_palette(key):
    
    pkl_path = os.path.join("_palette_pkl_src", PalettePathDict[key])
    fpath = os.path.join(os.path.dirname(__file__), pkl_path)
    
    return pydk.load_pickled(fpath)


# main class ------------------------------------------------------------------
class _ColorPalettes:
    PathDict = PalettePathDict
    _mpl_pallettes = ["BuOr"]

    def __init__(self):

        self.available = list(self.PathDict.keys())
        self._setup()

    def _setup(self):

        for key in self.available:
            self.__setattr__(key, self._load(key))

    def _process_mpl_cmap(self, cmap, n=None):
        """
        cmap
            type: np.ndarray
        n
            type: int or NoneType
            default: None
        """
        if n:
            return np.linspace(1, len(cmap) - 1, n).astype(int) / 255
        else:
            return mpl.colors.ListedColormap(cmap / 255)

    def _load(self, key, n=None):

        cmap = _load_palette(key)

        if key in self._mpl_pallettes:
            return self._process_mpl_cmap(cmap=cmap, n=n)
        else:
            return cmap

    def load_mpl(self, key, n=None):
        return self._load(key, n)
