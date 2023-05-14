# Development Guide

#### Note: My testing and build environment was on Windows. Some changes to guide below may be necesseary for Linux and MacOS environemnts.

## Testing:

`calibre-customize -b ./; calibre-debug -g`

or

`calibre-customize -b /folder/containing/plugin; calibre-debug -g`

Run to test changes to plugin. This updates plugin in calibre using files in this folder.
See [Debugging Calibre Plugins](https://manual.calibre-ebook.com/creating_plugins.html#id13) (if it doesn't auto scroll, scroll down to 'Debugging plugins').
I've removed the initial "calibre-debug -s" because the command line is open to see stdout and error from calibre, so shutdown is done manually by closing calibre.

## Building:

If you prefer to set up commands to compress plugin to a zip file, below are some examples. You can alternatively use any other program/method to compress the files into a zip folder.

### Powershell:

`Compress-Archive -LiteralPath '__init__.py','libgen_plugin.py','README.md','License','plugin-import-name-store_libgen.txt' -DestinationPath './libgenfiction_plugin.zip'`

### Bash

`zip libgenfiction_plugin.zip __init__.py libgen_plugin.py LICENSE README.md plugin-import-name-store_libgen.txt`

*"zip" package required*