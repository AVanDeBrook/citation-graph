#!/usr/bin/python3
import bibtexparser
import re
from parsers.latex-parser import LatexParser
from parsers.bibtex-parser import BibtexParser

"""
Wrapper/storage class for the bibtexparser API. Stores dictionaries of the bibliographies parsed by the bibtexparser.
"""
class BibtexParser(object):
	STR_BEGIN_COMMENT = "\n/*!"
	STR_PARAM = "\n\param %param_name% %description%"
	STR_END_COMMENT = "\n*/"
	STR_METHOD_SIGNATURE = "\nvoid %function_name%(void) {"
	STR_CALL_METHOD = "\n    %function_name%();"
	STR_CLOSE_METHOD = "\n};"
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
	YEAR_1900_2099 = re.compile("^(19|20)\d{2}$")

	"""
	Assembles all the parts of the bibtex entries into C-like function strings
	that can be stored in a file and processed later by Doxygen.
	"""
	def create_cstrings(self):
		cstrings = []

		for entry in self.dict_entries:
			cstrings.append(self.STR_BEGIN_COMMENT)
			for key in self.BIB_KEYS:
				if (key == "ID"):
					continue
				elif (key == "year"):
					if self.YEAR_1900_2099.fullmatch(entry[key]):
						cstrings.append(self._create_param_string(key.title(), entry[key]))
					else:
						cstrings.append(self._create_param_string(key.title(), self.STR_UNAVAILABLE))
				else:
					cstrings.append(self._create_param_string(key.title(), entry[key]))
			cstrings.append(self.STR_END_COMMENT)
			cstrings.append(self.STR_METHOD_SIGNATURE.replace("%function_name%", entry["ID"]))
			# for citations in entry:
			# 	cstrings.append(self.CALL_METHOD.replace("%function_name%", citations["ID"]))
			cstrings.append(self.STR_CLOSE_METHOD)
			cstrings.append("\n")

		return cstrings
	
	def _create_param_string(self, param_name, description):
		cstring = self.STR_PARAM.replace("%param_name%", param_name)
		cstring = cstring.replace("%description%", description)
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