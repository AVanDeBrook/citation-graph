#!/usr/bin/python3
from db import *
from flask import *

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/')
def search():
	return render_template('lookUpPaper.html')

@bp.route('/paper', methods=('GET', 'POST'))
def find_paper():
	if request.method == 'POST':
		return render_template('reference_info.html',
			paper=query_db("SELECT * FROM paper WHERE paper_id = ?", args=[request.form['search']], one=True)
		)