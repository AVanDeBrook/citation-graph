import os, webbrowser
from flask import *
from blueprints import ref_info, lookup_paper

# generate the doxygen configuration file
# os.system("doxygen -g ../data/out/doxygen/config/Doxyfile")

# generate HTML documentation from config file
# os.system("doxygen ../data/out/doxygen/config/Doxyfile")

# open HTML in browser
# webbrowser.open("../data/out/doxygen/html/index.html")

def create_app(test_config=None):
	app = Flask(
		__name__,
		instance_relative_config=True,
	)


	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)


	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/favicon.ico')
	def favicon():
		with open('static/images/favicon.ico', 'rb') as ffavicon:
			return ffavicon.read()

	app.register_blueprint(ref_info.bp)
	app.register_blueprint(lookup_paper.bp)

	return app
