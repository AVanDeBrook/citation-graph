#!/usr/bin/python3
from flask import *

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
	with open('html/index.html') as index_page:
		return index_page.read()

@flask_app.errorhandler(404)
def page_not_found(error):
	return "Page not found", 404
