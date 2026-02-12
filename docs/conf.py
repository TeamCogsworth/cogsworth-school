# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cogsworth school'
copyright = '2026, Tom Wagg'
author = 'Tom Wagg'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'cogsworth': ('https://cogsworth.readthedocs.io/en/latest/', None),
    'gala': ('https://gala.adrian.pw/en/latest/', None),
    'cosmic': ('https://cosmic-popsynth.github.io/COSMIC/', None),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ["new_font.css", "custom.css"]
html_title = "cogsworth school"
html_favicon = "_static/cog.ico"

html_theme_options = {
    "use_sidenotes": True,
    "logo": {
        "text": "cogsworth school",
        "image_light": "_static/cogsworth-logo.png",
        "image_dark": "_static/cogsworth-logo-darkmode.png",
    },
    "use_download_button": False,
    "icon_links": [
        {
            "name": "cogsworth repo",
            "url": "https://github.com/TomWagg/cogsworth",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "cogsworth docs",
            "url": "https://cogsworth.readthedocs.io/",
            "icon": "fa-solid fa-book",
            "type": "fontawesome",
        },
        {
            "name": "ask a question",
            "url": "https://github.com/TomWagg/cogsworth/issues/new?template=question.md",
            "icon": "fa-solid fa-comment-dots",
            "type": "fontawesome",
        }
   ]
}
