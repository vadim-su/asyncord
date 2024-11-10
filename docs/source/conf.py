# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Asyncord'
copyright = '2024, Vadim Suharnikov'
author = 'Vadim Suharnikov'
release = '0.12.0b4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_material'
html_theme_options = {
    'nav_title': 'Asyncord',
    'base_url': 'https://asyncord.dev',
    'color_primary': 'space-blue',
    'color_accent': 'vibran-orange',
    'repo_url': 'https://github.com/vadim-su/asyncord',
    'repo_name': 'vadim-su/asyncord',
}
html_static_path = ['static']
