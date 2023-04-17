"""This module defines the configuration for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys
from datetime import datetime

import tomli

sys.path.insert(0, os.path.join(os.path.abspath(".."), "src"))


# Project information.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

with open(file="../pyproject.toml", mode="rb") as f:
    pyproject = tomli.load(f)

project = pyproject["project"]["name"]
author = pyproject["project"]["authors"][0]["name"]
release = pyproject["project"]["version"]
copyright = f"{datetime.now().year}, {author}"

# General configuration.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.napoleon",
    "sphinx_click.ext",
]

autosummary_generate = True
napoleon_google_docstring = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Options for HTML output.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
