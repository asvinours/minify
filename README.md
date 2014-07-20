minify
======


Usage: minify.py [-h] [--cacheKey CACHEKEY] [--folder FOLDER] [--type TYPE] [--auto]
Compress JS files of a specific folder

Required arguments:
+  --folder FOLDER, -f FOLDER           The folder where the files are

Optional arguments:
+  -h, --help            				show this help message and exit
+  --cacheKey CACHEKEY, -c CACHEKEY		Used to create the filename with the cache key
+  --type TYPE, -t TYPE                 The type of files to compress (css, js)
+  --auto, -a                           Detect automatically the type of file

Dependencies
============

+ NodeJS
+ Uglify-js: https://github.com/mishoo/UglifyJS
+ Uglifycss: https://github.com/fmarcia/UglifyCSS