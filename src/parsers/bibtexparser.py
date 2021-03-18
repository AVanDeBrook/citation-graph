#!/usr/bin/python3
import bibtexparser
import re

"""
Wrapper/storage class for the bibtexparser API.
Stores dictionaries of the bibliographies parsed by the bibtexparser.
"""
class BibtexParser(object):
	STR_UNAVAILABLE = "UNAVAILABLE"

	"""
	Simple class constructor. Loads the BibTex file into the bibtexparser.
	Paramaters:
		bibtex_file - .bib file to parse BibTeX entries from.
		keys_list - the list of paper attributes to search for in the dictionary created by bibtexparser, for example { "ID", "title", "author", "year" }
	"""
	def __init__(self, bib_file, keys_list):

		with open(bib_file) as bibtex_file:
			self.bib_entries = bibtexparser.load(bibtex_file)

		self.dict_entries = self.parse_entries(self.bib_entries, keys_list)

	"""
	Since there are some specific fields that we want (given to this class in keys_list), we make template dictionary, fill in the fields (when able), and store back into a list. This list of dictionaries is returned from the function and stored as an attribute of the class.
	"""
	def parse_entries(self, bib_entries, keys_list):
		dict_list = []

		for entry in range(len(bib_entries.entries)):
			temp_dict = dict.fromkeys(keys_list)

			for key in temp_dict.keys():
				try:
					temp_dict[key] = bib_entries.entries[entry][key]
				except KeyError:
					temp_dict[key] = self.STR_UNAVAILABLE

			dict_list.append(temp_dict)

		return dict_list

"""
Example usage
"""
def main():
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
	bp = BibtexParser('data/commonFiles/all.bib', BIB_KEYS)
	print(bp.dict_entries)

if __name__ == "__main__":
	main()
