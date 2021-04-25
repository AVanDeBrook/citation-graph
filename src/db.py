#!/usr/bin/python3

from flask import *
import sqlite3

QUERY_GET_PAPER_BY_ID = 'SELECT * FROM paper WHERE paper_id = ?' # working
QUERY_INSERT_PAPER = 'INSERT INTO paper (paper_id, has_bib, has_tex) VALUES (?, ?, ?)' # working
QUERY_UPDATE_ATTRIBUTE_ABSTRACT = 'UPDATE paper SET abstract = ? WHERE paper_id = ?' # working
QUERY_GET_PAPERS_BY_ATTRIBUTE = 'SELECT * FROM paper WHERE ? = ?' # untested
QUERY_GET_ATTRIBUTE_BY_ID = 'SELECT ? FROM paper WHERE paper_id = ?' # untested
QUERY_GET_CITATIONS_BY_ID = 'SELECT reference_paper_id FROM citation WHERE paper_id = ?' # untested
QUERY_INSERT_CITATION = 'INSERT INTO citation (paper_id, reference_paper_id) VALUES (?, ?)' # untested

def get_db():
		db = getattr(g, '_database', None)
		if db is None:
			db = g._database = sqlite3.connect(current_app.config['DATABASE'])
		return db

def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

# for getting results from database
# param one True if you only want one result
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (create_dict_db(rv[0]) if rv else None) if one else [create_dict_db(row) for row in rv]

# for executing a query on the database
def execute_db(query, args=()):
	try:
		with sqlite3.connect(current_app.config['DATABASE']) as con:
			cur = con.cursor()
			cur.execute(query, args)
			con.commit()
	except Exception as ex:
		# print('Failed to execute query.')
		print(ex)
		con.rollback()
	finally:
		con.close()

def create_dict_db(db_row: list):
	paper_row = {
		"paper_id": db_row[0],
		"title": db_row[1],
		"author": db_row[2],
		"year": db_row[3],
		"abstract": db_row[4],
		"bib_references": db_row[5]
	}

	return paper_row
