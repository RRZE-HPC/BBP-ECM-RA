from .models import *
from .ecm import *

matplotlib_config = {
    'lines.linewidth': 2.5,
    'lines.markersize': 10,
    'font.size': 12.,
    #'font.sans-serif': ['Helvetica'],
    #'font.family' : 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'legend.fancybox': False,
#    'figure.figsize': (10., 10.),
    'savefig.bbox': 'tight',
    'axes.grid' : True
    }

import matplotlib
for key, value in matplotlib_config.items():
    matplotlib.rcParams[key] = value
