#!/usr/bin/python3

import os
from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs

# (unused) use LaTeXML to convert all.bib to XML (takes a while)
# os.system("latexmlc data/common/all.bib --destination=out/allbib.xml --bibtex")

# (unused) use LaTeXML to convert reduced paper (any .tex in graph folder) to XML
# os.system("latexmlc data/graph/liu2008.tex --destination=out/liu2008.xml")

# use LaTeXML to convert reduced paper (any .tex in graph folder) to HTML
os.system("latexmlc data/graph/liu2008.tex --destination=data/out/latexml/liu2008.html")

# remove white spaces from HTML and convert to a string, makes handle_data of HTMLParser happier
html = codecs.open("data/out/latexml/liu2008.html", encoding="utf8")
html_string = str(html.read())
html_string_no_whitespace = ' '.join(html_string.split())

# HTMLParser example to show what's going on
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        if (data != ' '):
            print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

parser = MyHTMLParser()
parser.feed(html_string_no_whitespace)