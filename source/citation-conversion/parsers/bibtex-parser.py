#!/usr/bin/python3
import bibtexparser
import re

"""
Wrapper/storage class for the bibtexparser API. Stores all the dictionaries of the bibliographies parsed by the bibtexparser.

See 'main' for some examples of usage.

Some of the functions in this class remain unfinished until we know the specific data that we need for each data point.
"""
class BibtexParser(object):
	CSTRING_REF = "void %function_name%(%parameters%);"
	YEAR_RE = re.compile("[0-9]+")

	"""
	Simple class constructor.
	Params: bib_file - file to parse BibTeX entries from.

	Loads the bibtex file into the bibtexparser and grabs the common entires between each bib entry.
	"""
	def __init__(self, bib_file):
		with open(bib_file) as bibtex_file:
			self.bib_entries = bibtexparser.load(bibtex_file)

		self.dict_entries = self.parse_entries(self.bib_entries)

	"""
	Since there are some specific fields that we want/need to create the C-like
	functions, we have a template dictionary that we make a copy of, fill in the
	fields (when able) and store back into a list. These are returned from the
	function and stored as an attribute of the class.
	"""
	def parse_entries(self, bib_entries):
		dict_list = []

		for entry in range(len(bib_entries.entries)):
			temp_dict = {
				"ID": "",
				"title": "",
				"year": "",
				"author": ""
			}

			for key in temp_dict.keys():
				try:
					temp_dict[key] = bib_entries.entries[entry][key]
				except KeyError:
					temp_dict[key] = "UNAVAILABLE"

			dict_list.append(temp_dict)

		return dict_list

	"""
	Assembles all the parts of the bibtex entries into C-like function strings
	that can be stored in a file and processed later by Doxygen.

	This function is subject to changez*
	"""
	def create_cstrings(self):
		cstrings = []

		for dict in self.dict_entries:
			cstring = CSTRING_REF.replace("%function_name%", dict["ID"])
			cstring = cstring.replace("%parameters%", "void")#assemble_param_string(dict['author'], dict['year']))
			cstrings.append(cstring)

		return cstrings

	def _assemble_param_string(self, authors, year):
		params = []
		author_str = _create_author_string(authors)
		year_str = _create_year_string(year)

		for author in author_str:
			params.append(author)

		params.append(year_str)

		return ", ".join(params)

	def _create_author_string(self, author_str):
		authors = author_str.split("and")

		for i in range(len(authors)):
			# I am too lazy to make this read any better. It just works.
			authors[i] = "CAuthor " + re.sub(r"[\\s\\.~{}\\\"\\']+", "", authors[i]).replace(" ", "").replace("\uFFFD", "")

		return authors

	def _create_year_string(self, year_str):
		if YEAR_RE.fullmatch(year_str):
			return "CYear " + year_str
		else:
			return "CYear Unavilable"

def main():
	bibtex_parser = BibtexParser('bibs/all.bib')

if __name__ == "__main__":
	main()
