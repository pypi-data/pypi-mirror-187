from ._version import version_info, __version__

from .ipyxturtle import *


def _jupyter_labextension_paths():
    return [{
        'src': 'labextension',
        'dest': 'ipyxturtle',
    }]


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'ipyxturtle',
        'require': 'ipyxturtle/extension'
    }]
