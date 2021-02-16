#!/usr/bin/python3
from pylatexenc.latexwalker import *

"""
Main class for the latex parsing routines.

Serves as more or less of a wrapper for the pylatexenc LaTeX parser API.

Add functions here as needed to work around the weird logic of the API.

See 'main' for some examples of usage.
"""
class LatexParser(object):
	NODE_LIST_POS = 2

	def __init__(self, latex_str):
		latex_walker = LatexWalker(latex_str)
		(self.nodes, _, _) = latex_walker.get_latex_nodes()

		for node in self.nodes:
			if node.isNodeType(LatexEnvironmentNode) and node.environmentname == 'document':
				self.document_nodes = node.nodelist

	"""
	Add all 'sections' (\section{...}) found within the document to a dictionary with their
	respective contents (and strip heading and trailing whitespace).

	Returns a dictionary of section names and their values. For example:
	{
		"Abstract": "...",
		"Important Contributions": "...",
		...
	}
	"""
	def parse_sections(self, document_nodes):
		section_dict = {}

		for i in range(len(document_nodes)):
			if document_nodes[i].isNodeType(LatexMacroNode) and document_nodes[i].macroname == 'section':
				section_dict[document_nodes[i].nodeargd.argnlist[self.NODE_LIST_POS].nodelist[0].chars.strip()] = document_nodes[i + 1].chars.strip()

		return section_dict

def main():
	# TODO: Add example usage

if __name__ == "__main__":
	main()