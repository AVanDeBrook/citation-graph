#!/usr/bin/python3
from pylatexenc.latexwalker import *

"""
Main class for the latex parsing routines.

Serves as more or less of a wrapper for the pylatexenc LaTeX parser API.

Add functions here as needed to work around the weird logic of the API.

See 'main' for some examples of usage.
"""
class LatexParser(object):

	document_macros = {
		"title": [],
		"bibliography": [],
		"author": [],
		# "section": [],
		# "cite": [],
		# "ref": [],
		# "label": []
	}

	def __init__(self, latex_str):
		latex_walker = LatexWalker(latex_str)
		(self.nodes, _, _) = latex_walker.get_latex_nodes()

		try:
			for node in self.nodes:
				if node.isNodeType(LatexEnvironmentNode):
					self.document_node_pos = node.pos
					(self.document_environment, _, _) = latex_walker.get_latex_environment(node.pos, environmentname="document")
		except LatexWalkerParseError:
			print(LatexWalkerParseError.msg)

		for node in self.document_environment.nodelist:
			if node.isNodeType(LatexMacroNode) and node.macroname in self.document_macros.keys():
				self.document_macros[node.macroname].append(node)

	def get_document_environemtn_nodes(self):
		try:
			return self.document_environment.nodelist
		except Exception:
			raise Exception("Could not find document nodes")

	def get_latex_nodes(self):
		return self.nodes

	def get_document_title(self):
		title = ""

		for title_node in self.document_macros["title"]:
			for group_node in title_node.nodeargd.argnlist:
				for node in group_node.nodelist:
					if node.isNodeType(LatexCharsNode):
						title += node.chars.replace("\n", "") + " "

		return title.strip()

	def get_bibtex_file(self):
		possible_files = []

		for index in self.document_macros["bibliography"]:
			for parsed_node in index.nodeargd.argnlist:
				for node in parsed_node.nodelist:
					possible_files.append(node.chars)

		return possible_files

	def get_author_info(self):
		author_info = []

		for author in self.document_macros["author"]:
			for arg in author.nodeargd.argnlist:
				for node in arg.nodelist:
					if node.isNodeType(LatexGroupNode):
						for subnode in node.nodelist:
							if subnode.isNodeType(LatexCharsNode):
								author_info.append(subnode.chars.replace("\n", ""))
					elif node.isNodeType(LatexCharsNode):
						author_info.append(node.chars.replace("\n", ""))

		for item in author_info:
			if item == '':
				author_info.remove(item)

		return author_info

if __name__ == "__main__":
	lp = LatexParser(open("citationGraph/ourPapers/channelModel/ANoteOnChannelModel_TVT.tex").read())

	# for key, values in lp.document_macros.items():
	# 	print("--------\n%s\n--------" % key)
	# 	for v in values:
	# 		print(v, end="\n\n")
	# 	print("\n\n\n")

	print("Title:\t", lp.get_document_title())
	print("Bib:\t", lp.get_bibtex_file())
	print("Author:\t", lp.get_author_info())
