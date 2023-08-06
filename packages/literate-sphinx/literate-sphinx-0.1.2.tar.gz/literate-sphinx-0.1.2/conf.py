# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from literate_sphinx import __doc__ as description
from literate_sphinx import __version__ as release

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Literate Sphinx'
copyright = '2023, Hubert Chathi'
author = 'Hubert Chathi'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'literate_sphinx',
    'myst_parser',
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv', 'LICENSES', 'public']

myst_heading_anchors = 3

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = []

html_theme_options = {
    'description': description,
    'extra_nav_links': {
        'Source': 'https://gitlab.com/uhoreg/literate-sphinx'
    }
}
