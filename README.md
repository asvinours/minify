minify
======


Usage: minify.py [-h] [--cacheKey CACHEKEY] [--folder FOLDER] [--type TYPE] [--auto]
Compress JS files of a specific folder

 optional arguments:
  -h, --help            				show this help message and exit
  --cacheKey CACHEKEY, -c CACHEKEY		Used to create the filename with the cache key
  --folder FOLDER, -f FOLDER           The folder where the files are
  --type TYPE, -t TYPE                 The type of files to compress (css, js)
  --auto, -a                           Detect automatically the type of file

Dependencies
============

Before using this script please verify that you have installed uglify-js
https://github.com/mishoo/UglifyJS
Before using this script please verify that you have installed uglifycss
https://github.com/fmarcia/UglifyCSS