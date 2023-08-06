faerun-notebook
===============================

A widget for visualising *large* data sets.

Installation
------------

To install use pip:

    $ pip install faerun_notebook

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com//faerun-notebook.git
    $ cd faerun-notebook
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix faerun_notebook
    $ jupyter nbextension enable --py --sys-prefix faerun_notebook

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite faerun_notebook

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
