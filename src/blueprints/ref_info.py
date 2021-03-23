#!/usr/bin/python3
import os
# from cwriter import CWriter
from parsers.bibtexparser import BibtexParser
from parsers.latexparser import LatexParser
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

		# CWriter(
		# 	os.path.join(file_path, bib_file.filename),
		# 	os.path.join(file_path, tex_file.filename),
		# 	os.path.join(file_path, tex_file.filename + ".c")
		# )

		return render_template('reference_info.html', refs=bibtex_refs, lp=latex_parser)
