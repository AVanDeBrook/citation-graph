import os, webbrowser, sqlite3
from flask import *
from blueprints import ref_info, lookup_paper

# generate the doxygen configuration file
# os.system("doxygen -g ../data/out/doxygen/config/Doxyfile")

# generate HTML documentation from config file
# os.system("doxygen ../data/out/doxygen/config/Doxyfile")

# open HTML in browser
# webbrowser.open("../data/out/doxygen/html/index.html")

DATABASE = 'citation_graph.db'
QUERY_GET_PAPER_BY_ID = 'SELECT * FROM paper WHERE paper_id = ?' # working
QUERY_INSERT_PAPER = 'INSERT INTO paper (paper_id, has_bib, has_tex) VALUES (?, ?, ?)' # working
QUERY_UPDATE_ATTRIBUTE_ABSTRACT = 'UPDATE paper SET abstract = ? WHERE paper_id = ?' # working
QUERY_GET_PAPERS_BY_ATTRIBUTE = 'SELECT * FROM paper WHERE ? = ?' # untested
QUERY_GET_ATTRIBUTE_BY_ID = 'SELECT ? FROM paper WHERE paper_id = ?' # untested
QUERY_GET_CITATIONS_BY_ID = 'SELECT reference_paper_id FROM citation WHERE paper_id = ?' # untested
QUERY_INSERT_CITATION = 'INSERT INTO citation (paper_id, reference_paper_id) VALUES (?, ?)' # untested

def create_app(test_config=None):
	if os.path.abspath(os.curdir).find(" ") != -1:
		raise Exception("Path name contains spaces. Please move the installation folder to one without spaces in the path name.")

	app = Flask(
		__name__,
		instance_relative_config=True,
	)

	app.config.from_object("config.Config")
	app.config['USER_PAPERS'] = os.path.join(app.instance_path,'user_files', 'papers')

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

	def get_db():
		db = getattr(g, '_database', None)
		if db is None:
			db = g._database = sqlite3.connect(DATABASE)
		return db

	def init_db(app):
		with app.app_context():
			db = get_db()
			with app.open_resource('schema.sql', mode='r') as f:
				db.cursor().executescript(f.read())
			db.commit()

	init_db(app)

	# for getting results from database
	# param one True if you only want one result
	def query_db(query, args=(), one=False):
		cur = get_db().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv
	
	# for executing a query on the database
	def execute_db(query, args=()):
		try:
			with sqlite3.connect(DATABASE) as con:
				cur = con.cursor()
				cur.execute(query, args)
				con.commit()
		except:
			print('Failed to execute query.')
			con.rollback()
		finally:
			con.close()

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

