#!/usr/bin/python3

from flask import *

bp = Blueprint('papers', __name__, url_prefix='/papers')

@bp.route('/')
def papers_home():
	return render_template('inputPaper.html')

@bp.route('/new', methods=('GET', 'POST'))
def new_paper():
	if request.method == 'POST':
		return request.form['texFile']
