
__module_name__ = "_linearize_axes.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# single function -------------------------------------------------------------
def _linearize_axes(AxesDict):

    axes = []

    for i, row in AxesDict.items():
        for j, col in row.items():
            axes.append(AxesDict[i][j])
    return axes