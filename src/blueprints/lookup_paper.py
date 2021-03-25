#!/usr/bin/python3
from flask import *

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/')
def search():
	return render_template('lookUpPaper.html')

@bp.route('/paper', methods=('GET', 'POST'))
def find_paper():
	if request.method == 'POST':
		return request.form['search']
