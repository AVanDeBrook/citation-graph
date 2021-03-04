#!/usr/bin/python3
import bibtexparser
import re

"""
Wrapper/storage class for the bibtexparser API. Stores dictionaries of the bibliographies parsed by the bibtexparser.

Some of the functions in this class remain unfinished until we know the specific data that we need for each data point.

See 'main' for some examples of usage.
"""
class BibtexParser(object):
	BEGIN_COMMENT = "\n/*!"
	PARAM = "\n\param %param_name% %description%"
	END_COMMENT = "\n*/"
	METHOD_SIGNATURE = "\nvoid %function_name%(void) {"
	CALL_METHOD = "\n    %function_name%();"
	CLOSE_METHOD = "\n};"
	YEAR = re.compile("[0-9]+")
	YEAR_1900_2099 = re.compile("^(19|20)\d{2}$")

	"""
	Simple class constructor.
	Params: bib_file - file to parse BibTeX entries from.
	Loads the bibtex file into the bibtexparser and grabs the common entires between each bib entry.
	"""
	def __init__(self, bib_file):
		with open(bib_file) as bibtex_file:
			self.bib_entries = bibtexparser.load(bibtex_file)

		self.dict_entries = self.parse_entries(self.bib_entries)
		cstrings = self.create_cstrings()
		cfile = open('data/out/c/cfordoxygen.c', 'w')
		cfile.writelines(cstrings)
		cfile.close()

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

		for entry in self.dict_entries:
			cstrings.append(self.BEGIN_COMMENT)
			cstrings.append(self._create_title_param_string(entry))
			cstrings.append(self._create_year_param_string(entry))
			cstrings.append(self._create_author_param_string(entry))
			cstrings.append(self.END_COMMENT)
			cstrings.append(self.METHOD_SIGNATURE.replace("%function_name%", entry["ID"]))
			# for citations in entry:
			# 	cstrings.append(self.CALL_METHOD.replace("%function_name%", citations["ID"]))
			cstrings.append(self.CLOSE_METHOD)
			cstrings.append("\n")

		return cstrings

	def _create_title_param_string(self, entry):
		cstring = self.PARAM.replace("%param_name%", "Title")
		cstring = cstring.replace("%description%", entry["title"])
		return cstring

	def _create_year_param_string(self, entry):
		cstring = self.PARAM.replace("%param_name%", "Year")
		if self.YEAR_1900_2099.fullmatch(entry["year"]):
			cstring = cstring.replace("%description%", entry["year"])
		else:
			cstring = cstring.replace("%description%", "Unavailable")
		return cstring
	
	def _create_author_param_string(self, entry):
		cstring = self.PARAM.replace("%param_name%", "Author")
		cstring = cstring.replace("%description%", entry["author"])
		return cstring

	# def _create_author_list(self, entry):
	# 	authors = entry["author"].split("and")
	# 	for i in range(len(authors)):
	# 		# I am too lazy to make this read any better. It just works.
	# 		authors[i] = "CAuthor " + re.sub(r"[\\s\\.~{}\\\"\\']+", "", authors[i]).replace(" ", "").replace("\uFFFD", "")
	# 	return authors

def main():
	bibtex_parser = BibtexParser('data/commonFiles/all.bib')

if __name__ == "__main__":
	main()