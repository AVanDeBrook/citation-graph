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
QUERY_INSERT_PAPER = 'INSERT INTO paper (paper_id) VALUES (?)'
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

	# TODO if (database doesn't exist yet):
	init_db(app)

	@app.route('/addpaper', methods = ['POST', 'GET'])
	def addpaper():
		if request.method == 'POST':
			try:
				paperId = request.form['paperId']

				with sqlite3.connect(DATABASE) as con:
					cur = con.cursor()
					cur.execute(QUERY_INSERT_PAPER, (paperId))
					con.commit()
			except:
				con.rollback()
			finally:
				con.close()

	return app

def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

# TODO delete later, here for reference and testing
def query_db_example_usage():
	myPaperId = 'LiuLi2008'
	print('EXAMPLE DB USAGE FOR PAPER ID' + myPaperId)

	paper = query_db(QUERY_GET_PAPER_BY_ID, [myPaperId], one=True)
	if paper is None:
		print('No such paper' + myPaperId)
		return
	else:
		print('Retrieved whole paper, can access attributes like title:' + paper['title_bib'])

	papers = query_db(QUERY_GET_PAPERS_BY_ATTRIBUTE, ['month', 'December'], one=True)
	print('Retrieved all papers with attribue month = December' + papers.len)

	paper = query_db(QUERY_GET_ATTRIBUTE_BY_ID, ['title_bib', myPaperId], one=True)
	print('Retrieved only attribute title from paper:' + paper['title_bib'])

	for citation in query_db(QUERY_GET_CITATIONS_BY_ID, myPaperId):
		print(myPaperId + 'references' + citation['reference_paper_id'])

	query_db(QUERY_INSERT_CITATION, [myPaperId, 'DelGreco2021'])

	query_db(QUERY_UPDATE_ATTRIBUTE, ['last_accessed', 'right now!', myPaperId])

@app.route('/addpaper', methods = ['POST', 'GET'])
def addpaper():
	if request.method == 'POST':
		try:
			paperId = request.form['paperId']

			with sqlite3.connect(DATABASE) as con:
				cur = con.cursor()
				cur.execute(QUERY_INSERT_PAPER, (paperId))
				con.commit()
		except:
			con.rollback()
		finally:
			con.close()

@app.route('/updateattribute', methods = ['POST', 'GET'])
def updateattribute():
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

'''
@app.route('/list')
def list():
	con = sqlite3.connect(DATABASE)
	con.row_factory = sqlite3.Row
   
	cur = con.cursor()
	cur.execute("SELECT * FROM paper")
   
	rows = cur.fetchall(); 
	return render_template("idk.html", rows = rows)
'''
