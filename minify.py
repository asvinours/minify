#! /usr/bin/python
# -*- coding: utf-8 -*-

#############
#
#	WARNING
# Before using this script please verify that you have installed uglify-js
# https://github.com/mishoo/UglifyJS
# Before using this script please verify that you have installed uglifycss
# https://github.com/fmarcia/UglifyCSS
#
# Date: 11/27/2013
# Author: Fabrice Baumann <fabrice.baumann@mindgeek.com>
# Usage: minify.py [-h] [--cacheKey CACHEKEY]
#
# Compress JS files of a specific folder
#
# optional arguments:
#  -h, --help            				show this help message and exit
#  --cacheKey CACHEKEY, -c CACHEKEY		Used to create the filename with the cache key
#  --folder FOLDER, -f FOLDER           The folder where the files are
#  --type TYPE, -t TYPE                 The type of files to compress (css, js)
#  --auto, -a                           Detect automatically the type of file
#
##############

import os, os.path, subprocess, fnmatch, argparse
from os.path import join, getsize

###########################
#
# Settings
#
###########################

# you can exclude some specific files
excludedFiles = []
# or use a pattern to exclude multiples files at the same time
excludedPattern = '*[-._]min[-._]*'
#folder to exclude from the walk
excludedFolders = ['.svn', '.git']

###########################
#
# Function
#
###########################

# this function is just to format the size of the folder.
def prettySize(size):
    suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            return round(size/float(lim/2**10),2).__str__()+suf

def diff(a, b):
  b = set(b)
  return [aa for aa in a if aa not in b]


def compressCss(f):
    if not fnmatch.fnmatch(f, '*.uglify') and fnmatch.fnmatch(f, '*.css') and not fnmatch.fnmatch(f, excludedPattern) and f not in excludedFiles:
        fullPath = os.path.join(root, f)
        fullPathUg = os.path.join(root, f+".uglify")
        print fullPath+" will be compressed"
        subprocess.call("uglifycss "+fullPath+" > "+fullPathUg, shell=True)
        if args.cachekey is not False and args.cachekey is not None:
            fullVersionPath = os.path.join(root, args.cachekey+"-"+f)
            subprocess.call("uglifycss "+fullPath+" > "+fullVersionPath, shell=True)
        os.remove(fullPath)
        os.rename(fullPathUg, fullPath)
    else:
        print "Skip: "+f

def compressJs(f):
    # if the file is a JS file, not already compressed, if it is not in the list of excluded files
    #       and is not matching the exclude pattern
    if not fnmatch.fnmatch(f, '*.uglify') and fnmatch.fnmatch(f, '*.js') and not fnmatch.fnmatch(f, excludedPattern) and f not in excludedFiles:
        # We compute the two file names we need, the original one, and the destination for the compressed file
        fullPath = os.path.join(root, f)
        fullPathUg = os.path.join(root, f+".uglify")
        print fullPath+" will be compressed"

        # We call uglify to compress the file
        subprocess.call("uglifyjs "+fullPath+" > "+fullPathUg, shell=True)

        # If the cache key has been passed as argument, we also create a compressed file with the key in the name
        if args.cachekey is not False and args.cachekey is not None:
            fullVersionPath = os.path.join(root, args.cachekey+"-"+f)
            subprocess.call("uglifyjs "+fullPath+" > "+fullVersionPath, shell=True)

        # We remove the original file
        os.remove(fullPath)
        # We rename the compressed file to the original name
        os.rename(fullPathUg, fullPath)
    else:
        print "Skip: "+f

##############################
#
# Script
#
##############################



# we check if the cache key is passed as an argument
parser = argparse.ArgumentParser(description='Compress JS files of a specific folder', prog='minify.py')
parser.add_argument('--cacheKey', '-c', dest='cachekey', action='store', default=False, help='Used to create the filename with the cache key')
parser.add_argument('--folder', '-f', dest='folder', action='store', help='The folder where the files are')
parser.add_argument('--type', '-t', dest='type', choices=['css', 'js'], action='store', help='The type of files to compress (css, js)')
parser.add_argument('--auto', '-a', dest='auto', action="store_true", help='Let the script check the type of file')

args = parser.parse_args()

if not (args.folder):
        parser.error('No folder specified. Please add a folder with --folder')

# we create the real path of the folder
if os.path.isabs(args.folder):
    folder = args.folder
else:
    folder = os.path.dirname(__file__)+"/"+args.folder
print folder

# for each file in each folder of the specified root
for root, dirs, files in os.walk(folder):

    # We retrieve the full size of the folder
    fullSize = sum(getsize(join(root, name)) for name in files)

    # We don't want to go trough the svn folder, so we remove it
    dirs = diff(dirs, excludedFolders)

    # for each file in this folder
    for f in files:
        if(args.auto):
            fileName, fileExtension = os.path.splitext(f)
            if(fileExtension == '.css'):
                compressCss(f)
            elif(fileExtension == '.js'):
                compressJs(f)
            else:
                print "Unknown extesnion. Skipping file"
        elif(args.type == 'css'):
            compressCss(f)
        elif(args.type == 'js'):
            compressJs(f)
        else:
            print "You need to chose something to compress"

    # We retrieve the total size of the folder after compression of each file
    compressedSize = sum(getsize(join(root, name)) for name in files)

    print root, "went from",
    print prettySize(fullSize), "to", prettySize(compressedSize),
    print "in", len(files), "non-directory files\n"
