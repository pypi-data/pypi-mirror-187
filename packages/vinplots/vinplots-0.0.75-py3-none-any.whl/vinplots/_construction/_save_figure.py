
__module_name__ = "_save_figure.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])
__version__ = "0.0.75"


# import packages -------------------------------------------------------------
import licorice_font
import matplotlib.pyplot as plt
import os
import pydk


# supporting functions --------------------------------------------------------
def _get_file_extension(filename):
    return filename.split(".")[-1]


def _add_default_extension(filename):

    if filename.endswith("."):
        filename += "png"
    else:
        filename += ".png"

    return filename

def _format_file_extension(filename, extension_list=["png", "svg", "pdf"]):

    extension = _get_file_extension(filename)
    if not extension in extension_list:
        return _add_default_extension(filename)
    else:
        return filename

def _bool_to_str(user_savename):

    if not type(user_savename) == str:
        return ""
    else:
        return user_savename


def _format_figure_file_basename(
    program_prefix=False, user_savename=False, add_timestamp=False
):

    """Asserts a series of defaults in absence of any component of the save-path."""

    program_prefix = _bool_to_str(program_prefix)
    user_savename = _bool_to_str(user_savename)
    figure_name = ".".join([program_prefix, user_savename])

    if len(figure_name) > 1:
        if add_timestamp:
            figure_name = ".".join([figure_name, pydk.time()])
        if figure_name.startswith("."):
            figure_name = figure_name[1:]
        if figure_name.endswith("."):
            figure_name = figure_name[:-1]

        return figure_name
    else:
        return "saved_plot.{}".format(pydk.time())



def _echo(formatted_savename):

    print(
        "{}: {}".format(
            licorice_font.font_format("Saving figure to", ["BOLD"]), formatted_savename
        )
    )

def _format_figure_savename(
    program_prefix="my_program_prefix",
    user_savename="user_defined_plot_name",
    add_timestamp=True,
    extension_list=["png", "svg", "pdf"],
):

    formatted_basename = _format_figure_file_basename(
        program_prefix, user_savename, add_timestamp
    )
    formatted_savename = _format_file_extension(formatted_basename, extension_list)

    return formatted_savename


# primary function ------------------------------------------------------------
def _save_figure(
    program_prefix=False,
    user_savename=False,
    outpath="./",
    add_timestamp=False,
    extension_list=["png", "svg", "pdf"],
    dpi=250,
    echo=True,
):
    """
    program_prefix
        type: bool or str
        default: False
    
    user_savename
        type: bool or str
        default: False
    
    outpath
        type: bool or str
        default: "./"
    
    add_timestamp
        type: bool
        default: False
    
    extension_list
        List of acceptable image exensions.
        type: list
        default: ["png", "svg", "pdf"]
    
    dpi
        Image resolution.
        type: int
        default: 250
    
    echo
        Print the constructed filepath to console.
        type: bool
        default: True
    """

    pydk.mkdir_flex(outpath)

    formatted_figure_savename = _format_figure_savename(
        program_prefix, user_savename, add_timestamp, extension_list
    )
    figure_filepath = os.path.join(outpath, formatted_figure_savename)
    if echo:
        _echo(figure_filepath)

    if figure_filepath.endswith(".png"):
        plt.savefig(figure_filepath, dpi=dpi)
    else:
        plt.savefig(figure_filepath)
