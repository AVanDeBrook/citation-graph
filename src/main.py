#!/usr/bin/python3

import os
import subprocess

# generate the doxygen configuration file
os.system("doxygen -g data/out/doxygen/config/Doxyfile")

# generate HTML documentation from config file
os.system("doxygen data/out/doxygen/config/Doxyfile")