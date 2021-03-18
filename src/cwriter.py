#!/usr/bin/python3
import bibtexparser
import re
from parsers.bibtexparser import BibtexParser
from parsers.latexparser import LatexParser

"""
Doxygen generates graphs and documentation from source files, but LaTex and BibTex are not supported input file types.
This class uses the parsers to convert info from LaTex and BibTex files into C-like functions, and then writes a C file that Doxygen can interpret.
"""
class CWriter(object):
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
	STR_BEGIN_COMMENT = "\n/*!"
	STR_PARAM = "\n\param %param_name% %description%"
	STR_END_COMMENT = "\n*/"
	STR_METHOD_SIGNATURE = "\nvoid %function_name%(void) {"
	STR_CALL_METHOD = "\n    %function_name%();"
	STR_CLOSE_METHOD = "\n};"
	YEAR_1900_2099 = re.compile("^(19|20)\d{2}$")

	"""
	Class constructor. Uses the BibtexParser and LatexParser and writes a C file that can later be processed by Doxygen.
	"""
	def __init__(self, bib_file, tex_file, out_file):
		bibtex_parser = BibtexParser(bib_file, self.BIB_KEYS)
		latex_parser = LatexParser(tex_file)
		cstrings = self.create_cstrings(bibtex_parser.dict_entries, latex_parser)
		cfile = open(out_file, 'w')
		cfile.writelines(cstrings)
		cfile.close()

	"""
	Assembles the results of the BibTex and LaTex parsers into C-like function strings.
	"""
	def create_cstrings(self, bib_dicts, latex_parser):
		cstrings = []

		for bib_dict in bib_dicts:

			# param comments aka paper attributes
			cstrings.append(self.STR_BEGIN_COMMENT)
			for key in self.BIB_KEYS:
				if (key == "ID"):
					continue
				elif (key == "year"):
					if self.YEAR_1900_2099.fullmatch(bib_dict[key]):
						cstrings.append(self._create_param_string(key.title(), bib_dict[key]))
					else:
						cstrings.append(self._create_param_string(key.title(), self.STR_UNAVAILABLE))
				else:
					cstrings.append(self._create_param_string(key.title(), bib_dict[key]))
			if (latex_parser.id == bib_dict['ID']):
				cstrings.append(self._create_param_string("Title(LaTex)", latex_parser.get_document_title()))
				cstrings.append(self._create_param_string("AuthorInfo", ', '.join(latex_parser.get_author_info())))
				cstrings.append(self._create_param_string("Abstract", latex_parser.get_abstract()))
				cstrings.append(self._create_param_string("BibliographyFiles", ', '.join(latex_parser.get_bibtex_file())))
			cstrings.append(self.STR_END_COMMENT)

			# method signature aka paper id
			cstrings.append(self.STR_METHOD_SIGNATURE.replace("%function_name%", bib_dict["ID"]))

			# call methods aka references to other papers
			if (latex_parser.id == bib_dict['ID']):
				for citation_id in latex_parser.get_citation_list():
					cstrings.append(self.STR_CALL_METHOD.replace("%function_name%", citation_id))
			
			cstrings.append(self.STR_CLOSE_METHOD)
			cstrings.append("\n")

		return cstrings
	
	def _create_param_string(self, param_name, description):
		cstring = self.STR_PARAM.replace("%param_name%", param_name)
		cstring = cstring.replace("%description%", description)
		return cstring

"""
Example usage
"""
def main():
	cwriter = CWriter(
        'data/commonFiles/all.bib',
        'data/graph/Liu2008.tex',
		'data/out/c/cfordoxygen.c'
    )

if __name__ == "__main__":
	main()
