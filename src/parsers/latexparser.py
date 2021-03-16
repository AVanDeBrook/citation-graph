#!/usr/bin/python3
from pylatexenc.latexwalker import *

"""
Main class for the LaTex parsing routines.
Serves as more or less of a wrapper for the pylatexenc LaTeX parser API.
"""
class LatexParser(object):

	document_macros = {
		"title": [],
		"bibliography": [],
		"author": [],
		# "section": [],
		"cite": [],
	}

	"""
	Constructor to initialize the class fields and latex parser.
	"""
	def __init__(self, latex_file):
		self.latex_walker = LatexWalker(open(latex_file).read())
		(self.nodes, _, _) = self.latex_walker.get_latex_nodes()

		try:
			for node in self.nodes:
				if node.isNodeType(LatexEnvironmentNode):
					self.document_node_pos = node.pos
					(self.document_environment, _, _) = self.latex_walker.get_latex_environment(node.pos, environmentname="document")
		except LatexWalkerParseError:
			raise Exception("Could not find \\begin\{document\} symbol")

		for node in self.document_environment.nodelist:
			if node.isNodeType(LatexMacroNode) and node.macroname in self.document_macros.keys():
				self.document_macros[node.macroname].append(node)

	def get_document_environment_nodes(self):
		"""
		Returns the list of all nodes in the 'document' environment.
		E.g. all nodes between "\begin{document}" and "\end{document}"
		"""
		try:
			return self.document_environment.nodelist
		except Exception:
			raise Exception("Could not find document nodes")

	def get_latex_nodes(self):
		"""
		Returns all nodes in the latex file.
		"""
		return self.nodes

	def get_document_title(self):
		"""
		Finds and returns the document title, if specified in the file.
		"""
		title = ""

		for title_node in self.document_macros["title"]:
			for group_node in title_node.nodeargd.argnlist:
				for node in group_node.nodelist:
					if node.isNodeType(LatexCharsNode):
						title += node.chars.replace("\n", "") + " "

		return title.strip()

	def get_bibtex_file(self):
		"""
		Returns a list of possible bibtex files to parse citations and bibliographies from.
		"""
		possible_files = []

		for index in self.document_macros["bibliography"]:
			for parsed_node in index.nodeargd.argnlist:
				for node in parsed_node.nodelist:
					possible_files.append(node.chars)

		return possible_files

	def get_author_info(self):
		"""
		Returns a list of author information that was found in the document.
		"""
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

	def get_citation_list(self):
		"""
		Returns a list of bibtex IDs that were cited within the document.
		"""
		citation_list = []

		for citation in self.document_macros["cite"]:
			for arg in citation.nodeargd.argnlist:
				if arg != None and arg.isNodeType(LatexGroupNode):
					for node in arg.nodelist:
						if node.isNodeType(LatexCharsNode) and not node.chars in citation_list:
							citation_list.append(node.chars)

		return citation_list

	# I'm not religious, but may god forgive me for the mess I have created
	def get_abstract(self):
		"""
		Attempst to find and return the abstract from the latex file.
		"""
		for node in self.document_environment.nodelist:
			if node.isNodeType(LatexGroupNode):
				for subnode in node.nodelist:
					if subnode.isNodeType(LatexCharsNode) and subnode.chars.lower() == "abstract":
						(expr, _, _) = self.latex_walker.get_latex_expression(pos=(subnode.pos + subnode.len + 1))
						while not expr.isNodeType(LatexCharsNode):
							(expr, _, _) = self.latex_walker.get_latex_expression(pos=(expr.pos + expr.len))
						(abstract, _, _) = self.latex_walker.get_latex_nodes(pos=expr.pos, read_max_nodes=1)
						return abstract[0].chars.replace("\n","")

	def get_index_terms(self):
		# There is no easy way to parse the index terms for some reason, so it will not be finished in sprint 1.
		"""
		Not implemented
		"""
		raise NotImplementedError()


	def _print_dict_info(self):
		"""
		Prints the raw data from the document_macros dictionary.
		"""
		for key, values in self.document_macros.items():
			print("--------\n%s\n--------" % key)
			for v in values:
				print(v, end="\n\n")
			print("\n\n\n")

if __name__ == "__main__":
	lp = LatexParser(open("data/paper/channelModel/ANoteOnChannelModel_TVT.tex").read())

	# print("Abstract:\t", lp.get_abstract()) # commented just because abstracts are usually very long
	# print("Index terms:\t", lp.get_index_terms()) # not implemented
	print("Title:\t", lp.get_document_title())
	print("Bib:\t", lp.get_bibtex_file())
	print("Author:\t", lp.get_author_info())
	print("Cite:\t", lp.get_citation_list())