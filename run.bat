#!/usr/bin/sh
set FLASK_APP=server.py
# Change this for demos, otherwise there will be debugger stack traces written to the web page
set FLASK_ENV=development

cd src && flask run && cd ..
