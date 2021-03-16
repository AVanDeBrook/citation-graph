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
		cstrings = self.create_cstrings(bibtex_parser.dict_entries)
		cfile = open(out_file, 'w')
		cfile.writelines(cstrings)
		cfile.close()

	"""
	Assembles the results of the BibTex and LaTex parsers into C-like function strings.
	"""
	def create_cstrings(self, bib_dicts):
		cstrings = []

		for bib_dict in bib_dicts:
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
			cstrings.append(self.STR_END_COMMENT)
			cstrings.append(self.STR_METHOD_SIGNATURE.replace("%function_name%", bib_dict["ID"]))
            # TODO use latex_parser for citations
			# for citation in citations:
			# 	cstrings.append(self.CALL_METHOD.replace("%function_name%", citation["ID"]))
			cstrings.append(self.STR_CALL_METHOD.replace("%function_name%", 'somePaper'))
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
        'data/paper/channelModel/ANoteOnChannelModel_TVT.tex',
		'data/out/c/cfordoxygen.c'
    )

if __name__ == "__main__":
	main()