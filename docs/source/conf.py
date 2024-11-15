# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_material

import asyncord

project = 'Asyncord'
copyright = '2024, Vadim Suharnikov'
author = 'Vadim Suharnikov'
release = asyncord.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
]

autosummary_generate = True
autoclass_content = 'class'


templates_path = ['templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions.append('sphinx_material')
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = 'sphinx_material'


html_theme_options = {
    'nav_title': 'Asyncord',
    'base_url': 'https://asyncord.dev',
    'color_primary': 'space-blue',
    'color_accent': 'vibran-orange',
    'repo_url': 'https://github.com/vadim-su/asyncord',
    'repo_name': 'vadim-su/asyncord',
}


html_sidebars = {
    '**': ['logo-text.html', 'globaltoc.html', 'localtoc.html', 'searchbox.html'],
}
