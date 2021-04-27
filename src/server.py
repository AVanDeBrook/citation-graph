import os, webbrowser
from flask import *
from blueprints import ref_info, lookup_paper
from db import *

# generate the doxygen configuration file
# os.system("doxygen -g ../data/out/doxygen/config/Doxyfile")

# generate HTML documentation from config file
# os.system("doxygen ../data/out/doxygen/config/Doxyfile")

# open HTML in browser
# webbrowser.open("../data/out/doxygen/html/index.html")

def create_app(test_config=None):
	if os.path.abspath(os.curdir).find(" ") != -1:
		raise Exception("Path name contains spaces. Please move the installation folder to one without spaces in the path name.")

	app = Flask(
		__name__,
		instance_relative_config=True,
	)

	app.config.from_object("config.Config")
	app.config['USER_PAPERS'] = os.path.join(app.instance_path,'user_files', 'papers')
	app.config['DATABASE'] = 'citation_graph.db'

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(os.path.join(app.instance_path, 'user_files', 'papers'))
	except OSError as e:
		pass

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/favicon.ico')
	def favicon():
		with open('static/images/favicon.ico', 'rb') as ffavicon:
			return ffavicon.read()

	app.register_blueprint(ref_info.bp)
	app.register_blueprint(lookup_paper.bp)

	init_db(app)

	# the commented out lines allow the data to come from the front-end
	# @app.route('/exampleAddPaper', methods = ['POST', 'GET'])
	@app.route('/exampleAddPaper')
	def exampleAddPaper():
		# if request.method == 'POST':
		paperId = 'Corrina2020' # paperId = request.form['paperId']
		execute_db(QUERY_INSERT_PAPER, (paperId, 0, 0))
		return render_template('index.html') # render whatever page you want, index is just a placeholder

	@app.route('/exampleGetPapers')
	def exampleGetPapers():
		rows = query_db('SELECT * FROM paper')
		print(rows)
		# this commented out line shows how you would send the data to the front-end (in rows)
		# return render_template("newpage.html", rows = rows)
		return render_template('index.html') # render whatever page you want, index is just a placeholder

	# the commented out lines allow the data to come from the front-end
	# @app.route('/exampleGetPaperById', methods = ['POST', 'GET'])
	@app.route('/exampleGetPaperById')
	def exampleGetPaperById():
		# if request.method == 'POST':
		paperId = 'Corrina2020' # paperId = request.form['paperId']
		paper = query_db(QUERY_GET_PAPER_BY_ID, [paperId], one=True)
		if paper is None:
			print('No such paper' + paperId)
			return
		else:
			print('Retrieved whole paper, can access attributes like this:' + paper[1])
		return render_template('index.html') # render whatever page you want, index is just a placeholder

	# the commented out lines allow the data to come from the front-end
	# @app.route('/exampleUpdateAttribute', methods = ['POST', 'GET'])
	@app.route('/exampleUpdateAttribute')
	def exampleUpdateAttribute():
		# if request.method == 'POST':
		paperId = 'Corrina2020' # paperId = request.form['paperId']
		abstract = 'The new abstract' # abstract = request.form['abstract']
		execute_db(QUERY_UPDATE_ATTRIBUTE_ABSTRACT, (abstract, paperId))
		return render_template('index.html') # render whatever page you want, index is just a placeholder

	return app
