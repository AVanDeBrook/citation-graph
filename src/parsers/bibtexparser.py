#!/usr/bin/python3
import bibtexparser
import re

"""
Wrapper/storage class for the bibtexparser API. Stores dictionaries of the bibliographies parsed by the bibtexparser.
"""
class BibtexParser(object):
	BIB_KEYS = {
		"ID",
		"title",
		"author",
		"year",
		"month",
		"volume",
		"number",
		"pages",
		"publisher",
		"journal",
		"last accessed",
		"address"
		}
	STR_UNAVAILABLE = "UNAVAILABLE"

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
			temp_dict = dict.fromkeys(self.BIB_KEYS)

			for key in temp_dict.keys():
				try:
					temp_dict[key] = bib_entries.entries[entry][key]
				except KeyError:
					temp_dict[key] = self.STR_UNAVAILABLE

			dict_list.append(temp_dict)

		return dict_list

def main():
	bibtex_parser = BibtexParser('data/commonFiles/all.bib')

if __name__ == "__main__":
	main()