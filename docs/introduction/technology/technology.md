# Plugin
NodeNote supports hot plugin.

Manager will load, registry, unload plugin.
The api version invoked by plugin must be provided.
Meta data file or Internal code.
Plugins run in a separate progress and communicate with the core api through IPC channel.
Load plugins by different symbols.

## Core api
init
free
registry

# Custom Widgets
## package.component.base_component.BaseComponent class

# Logging system.
Qt logging system.



# Document generation tool.
https://www.sphinx-doc.org/en/master/

Sphinx is a good tool to generate different format of document. In our project, I use html generator to parse google style document string.

First, type `sphinx-quickstart` command in `src/docs` which is used to generate document and the configuration of document will show.

Second, add `autoapi.extension` extension into `conf.py/extensions`. This extension will parse document string into different format.

Third, I change the `BUILDDIR` of `make.bat/Makefile` into `docs/api`. Then We can use `make html` to generator html pages of api.

# Spell check tool.
https://github.com/streetsidesoftware/vscode-spell-checker.git

I use `Code Spell Checker` extension to check the spell of words. The settings is in .vscode/settings which excludes some specific words.