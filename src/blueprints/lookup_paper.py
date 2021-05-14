#!/usr/bin/python3
import csv
from db import *
from flask import *

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/')
def search():
	return render_template('lookUpPaper.html')

@bp.route('/paper', methods=('GET', 'POST'))
def find_paper():
	if request.method == 'POST':
		bibtex_refs = []
		#paper is a dictionary with the query results
		paper = query_db("SELECT * FROM paper WHERE paper_id = ?", args=[escape(request.form['search'])], one=True)
		#iterate through each item in the list after the brackets are stripped
		#access the dictionary by using paper["what i am looking for"]
		for citations in csv.reader([paper['bib_references'].strip('[]')]):
			for citation in citations:
				print(citation)
				bibtex_refs.append(query_db('SELECT * FROM paper WHERE paper_id = ?', args=[citation.strip().replace('\'', '')], one=True))


		#for i in range(len(bibtex_refs)):
		#	print(bibtex_refs[i]['bib_references'])

		return render_template('reference_info.html',
			paper=paper,
			refs=bibtex_refs
		)