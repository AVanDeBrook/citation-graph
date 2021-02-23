#!/usr/bin/python3

import os
import webbrowser

# generate the doxygen configuration file
os.system("doxygen -g data/out/doxygen/config/Doxyfile")

# generate HTML documentation from config file
os.system("doxygen data/out/doxygen/config/Doxyfile")

# open HTML in browser
webbrowser.open("data\out\doxygen\html\index.html")