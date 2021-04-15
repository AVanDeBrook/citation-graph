#!/usr/bin/python3
import os
from cwriter import CWriter
from parsers.bibtexparser import BibtexParser
from parsers.latexparser import LatexParser
from db import *

from flask import *
from multiprocessing import Process

bp = Blueprint('papers', __name__, url_prefix='/papers')

@bp.route('/')
def papers_home():
	return render_template('inputPaper.html')

@bp.route('/new', methods=('GET', 'POST'))
def new_paper():
	if request.method == 'POST':
		tex_file = request.files['texFile']
		bib_file = request.files['bibFile']
		file_path = os.path.join(current_app.config['USER_PAPERS'], tex_file.filename.split('.')[0])
		bibtex_refs = []

		try:
			os.makedirs(file_path)
		except OSError:
			# if folder already exists we can use the database to fill out the form data
			pass

		tex_file.save(os.path.join(file_path, tex_file.filename))
		bib_file.save(os.path.join(file_path, bib_file.filename))

		latex_parser = LatexParser(os.path.join(file_path, tex_file.filename))
		bibtex_parser = BibtexParser(
			bib_file=os.path.join(file_path, bib_file.filename),
			keys_list={
				"ID",
				"title",
				"author",
				"year"
			}
		)

		for entry in bibtex_parser.dict_entries:
			if entry['ID'] in latex_parser.get_citation_list():
				bibtex_refs.append(entry)

		execute_db('INSERT INTO paper (paper_id, has_bib, has_tex, title_tex, author_tex) VALUES (?, ?, ?, ?, ?)',
			[latex_parser.id, True, True, latex_parser.get_document_title(), str(latex_parser.get_author_info())])

		resp = query_db('SELECT * FROM paper')
		print(resp)

		session['paper_id'] = latex_parser.id
		session['bibtex_filename'] = bib_file.filename
		session['tex_filename'] = tex_file.filename

		return render_template('reference_info.html', refs=bibtex_refs, lp=latex_parser)

@bp.route('/doxygen', methods=('GET', 'POST'))
def doxygen():
	if request.method == 'POST':
		file_path = os.path.join(current_app.config['USER_PAPERS'], session['paper_id'])

		CWriter(
			os.path.join(file_path, session['bibtex_filename']),
			os.path.join(file_path, session['tex_filename']),
			os.path.join(file_path, session['tex_filename'] + ".c")
		)

		run_doxygen(file_path, session['paper_id'])

		with open(os.path.join(file_path, "html", "index.html"), "r") as doxy_index:
			return doxy_index.read()

@bp.route('/<path:file>')
def doxygen_files(file):
	@after_this_request
	def add_header(response):
		if file.endswith('.js'):
			response.headers['Content-Type'] = 'application/javascript'
		elif file.endswith('.css'):
			response.headers['Content-Type'] = 'text/css'
		return response
	with open(os.path.join(current_app.config['USER_PAPERS'], session['paper_id'], "html", escape(file)), "rb") as doxygen_file:
		return doxygen_file.read()

def run_doxygen(path, paper_id):
	doxy_cmd = "doxygen"

	with open(os.path.join(path, "Doxyfile"), "w") as dox_cfg:
		dox_cfg.write(render_template(
			"Doxyfile",
			paper_title=paper_id,
			out_path=path,
			input_dir=path,
			readme="../README.md"
		))

	os.system(" ".join([doxy_cmd, os.path.join(path, "Doxyfile")]))
