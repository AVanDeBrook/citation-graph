#!/usr/bin/python3
from flask import *

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
	with open('html/index.html') as index:
		return index.read()

@flask_app.route('/favicon.ico')
def favicon():
	try:
		with open('images/favicon.ico', "rb") as logo:
			response = make_response(logo.read())
	except FileNotFoundError:
		response = make_response()
		response.status_code = 404
	return response

@flask_app.route('/stylesheets/<path:stylesheet>')
def stylesheets(stylesheet):
	try:
		with open('stylesheets/' + escape(stylesheet)) as style_file:
			response = make_response(style_file.read(), 200)
			response.headers['Content-Type'] = 'text/css'
	except FileNotFoundError:
		response = make_response()
		response.status_code = 404
	return response

@flask_app.route('/scripts/<path:script>')
def scripts(script):
	try:
		with open('scripts/' + escape(script)) as script_file:
			response = make_response(script_file.read(), 200)
			response.headers['Content-Type'] = 'application/javascript'
	except FileNotFoundError:
		response = make_response()
		response.status_code = 404
	return response

@flask_app.errorhandler(404)
def page_not_found(error):
	return "Page not found", 404
