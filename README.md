# Citation Graph
ERAU DB EECS Senior Design Project. Generates the citation graph of research papers.

## Application background
When researchers do research, they read a lot of papers. It is really a good idea to be able to how one paper is dependent on a couple of other papers. That is why they have to have a list of references at the end of the paper. When they want to track the dependencies of the papers, using the paper-based or pdf-based approach is awkward. There are some tools currently on the market to display the citation/dependency graphs of the papers. They are usually web-based, which is good for navigation.

However, the current produces lack an important function: adding necessary info to the citation graph. This info includes the summary of important contributions of the paper, how each contribution is related to a specific citation, the names of authors, the affiliation of the authors at the time of publishing the paper (which means there can be a list of affiliations for a single author). It is our contribution to implement the dependency/citation graph with the added information.

## Cloning, Building, etc.
To clone:
```bash
git clone https://github.com/AVanDeBrook/citation-graph.git
```
To build:
The following dependencies are needed:

Python v3.x Dependencies:
* `bibtexparser`
* `flask`
* `pylatexenc`
* `re` (if not provided by default w/ python 3.x)

System Dependencies:
* `graphviz`
* `doxygen`

Use the following script to download the dependencies listed above
```bash
pip install bibtexparser flask pylatexenc re
```

Non-Python Dependencies:
* [Doxygen](https://www.doxygen.nl/index.html) [(GitHub,](https://github.com/doxygen/doxygen) [man pages)](https://docs.oracle.com/cd/E88353_01/html/E37839/doxygen-1.html)
