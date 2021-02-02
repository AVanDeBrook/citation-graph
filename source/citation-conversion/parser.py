#!/usr/bin/python3
import bibtexparser
import re

CSTRING_REF = "void %function_name%(%parameters%);"
YEAR_RE = re.compile("[0-9]+")

def main():
	dict_list = parse_entries()
	cstrings = create_cstrings(dict_list)

	for string in cstrings:
		print(string)

def parse_entries():
	dict_list = []

	with open('bibs/all.bib') as bibtex_file:
		bib_entries = bibtexparser.load(bibtex_file)

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

def create_cstrings(dict_list):
	cstrings = []

	for dict in dict_list:
		cstring = CSTRING_REF.replace("%function_name%", dict["ID"])
		cstring = cstring.replace("%parameters%", "void")#assemble_param_string(dict['author'], dict['year']))
		cstrings.append(cstring)

	return cstrings

def assemble_param_string(authors, year):
	params = []
	author_str = create_author_string(authors)
	year_str = create_year_string(year)

	for author in author_str:
		params.append(author)

	params.append(year_str)

	return ", ".join(params)

def create_author_string(author_str):
	authors = author_str.split("and")

	for i in range(len(authors)):
		# I am too lazy to make this read any better. It just works.
		authors[i] = "CAuthor " + re.sub(r"[\\s\\.~{}\\\"\\']+", "", authors[i]).replace(" ", "").replace("\uFFFD", "")

	return authors

def create_year_string(year_str):
	if YEAR_RE.fullmatch(year_str):
		return "CYear " + year_str
	else:
		return "CYear Unavilable"

if __name__ == "__main__":
	main()
