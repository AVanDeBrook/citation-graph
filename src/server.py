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
QUERY_GET_PAPER_BY_ID = 'SELECT * FROM paper WHERE paper_id = ?'
QUERY_GET_PAPERS_BY_ATTRIBUTE = 'SELECT * FROM paper WHERE ? = ?'
QUERY_GET_ATTRIBUTE_BY_ID = 'SELECT ? FROM paper WHERE paper_id = ?'
QUERY_GET_CITATIONS_BY_ID = 'SELECT reference_paper_id FROM citation WHERE paper_id = ?'
QUERY_INSERT_PAPER = 'INSERT INTO paper (paper_id, has_bib, has_tex) VALUES (?, ?, ?)'
QUERY_INSERT_CITATION = 'INSERT INTO citation (paper_id, reference_paper_id) VALUES (?, ?)'
QUERY_UPDATE_ATTRIBUTE = 'UPDATE paper SET ? = ? WHERE paper_id = ?'

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

	# TODO if (database doesn't exist yet):
	init_db(app)

	def query_db(query, args=(), one=False):
		cur = get_db().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv

	# @app.route('/exAddPaper', methods = ['POST', 'GET'])
	@app.route('/exAddPaper')
	def exAddPaper():
		# if request.method == 'POST':
		try:
			# paperId = request.form['paperId']
			paperId = 'Corrina2020'

			with sqlite3.connect(DATABASE) as con:
				cur = con.cursor()
				cur.execute(QUERY_INSERT_PAPER, (paperId, 0, 0))
				con.commit()
		except:
			print('Failed to add paper')
			con.rollback()
		finally:
			con.close()
		return render_template('index.html')

	@app.route('/exGetPapers')
	def exGetPapers():
		rows = query_db('SELECT * FROM paper')
		print(rows)
		# return render_template("newpage.html", rows = rows)
		return render_template('index.html')

	# @app.route('/exDatabaseUsage', methods = ['POST', 'GET'])
	@app.route('/exDatabaseUsage')
	def exDatabaseUsage():
		# if request.method == 'POST':
		# paperId = request.form['paperId']
		paperId = 'Corrina2020'

		paper = query_db(QUERY_GET_PAPER_BY_ID, [paperId], one=True)
		if paper is None:
			print('No such paper' + paperId)
			return
		else:
			print('Retrieved whole paper, can access attributes:' + paper[1])

		# papers = query_db(QUERY_GET_PAPERS_BY_ATTRIBUTE, ['month', 'December'], one=True)
		# print('Retrieved all papers with attribue month = December' + papers.len)

		# paper = query_db(QUERY_GET_ATTRIBUTE_BY_ID, ['title_bib', paperId], one=True)
		# print('Retrieved only attribute title from paper:' + paper['title_bib'])

		# for citation in query_db(QUERY_GET_CITATIONS_BY_ID, paperId):
		# 	print(paperId + 'references' + citation['reference_paper_id'])

		# paper = query_db(QUERY_GET_ATTRIBUTE_BY_ID, ['title_bib', paperId], one=True)
		# print('Retrieved only attribute title from paper:' + paper['title_bib'])

		# for citation in query_db(QUERY_GET_CITATIONS_BY_ID, paperId):
		# 	print(paperId + 'references' + citation['reference_paper_id'])

		# query_db(QUERY_INSERT_CITATION, [paperId, 'DelGreco2021'])

		# query_db(QUERY_UPDATE_ATTRIBUTE, ['last_accessed', 'right now!', paperId])

		return render_template('index.html')

	'''
	@app.route('/exUpdateAttribute', methods = ['POST', 'GET'])
	def exUpdateAttribute():
		if request.method == 'POST':
			try:
				paperId = request.form['paperId']
				attributeName = 'title_bib' # TODO determine which attribute
				attributeValue = request.form[attributeName]

				with sqlite3.connect(DATABASE) as con:
					cur = con.cursor()
					cur.execute(QUERY_UPDATE_ATTRIBUTE, (attributeName, attributeValue, paperId))
					con.commit()
			except:
				con.rollback()
			finally:
				con.close()

	@app.teardown_appcontext
	def close_connection(exception):
		db = getattr(g, '_database', None)
		if db is not None:
			db.close()
	'''
	
	return app

