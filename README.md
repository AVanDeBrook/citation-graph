# Citation Graph
ERAU DB EECS Senior Design Project. Generates the citation graph of research papers.

## Application background
When researchers do research, they read a lot of papers. It is really a good idea to be able to how one paper is dependent on a couple of other papers. That is why they have to have a list of references at the end of the paper. When they want to track the dependencies of the papers, using the paper-based or pdf-based approach is awkward. There are some tools currently on the market to display the citation/dependency graphs of the papers. They are usually web-based, which is good for navigation.

However, the current produces lack an important function: adding necessary info to the citation graph. This info includes the summary of important contributions of the paper, how each contribution is related to a specific citation, the names of authors, the affiliation of the authors at the time of publishing the paper (which means there can be a list of affiliations for a single author). It is our contribution to implement the dependency/citation graph with the added information.

## Building and Running
### To Build (Option 1: Automatic)
Run the following command (from within the cloned repo) to automatically install the project's dependencies
```bash
pip install -e .
```
For a sanity check, you can run the following to make sure the app (and its dependencies) have been installed:
```bash
pip list | grep citation-graph
```
There should be an output similar to below (your installation path and version number may be different):
```bash
Package                Version         Location
---------------------- --------------- --------------------------------------------
citation-graph         0.2.0           /home/avandebrook/Programming/citation-graph
```
### To Build (Option 2: Manual)
The following dependencies are needed:

Python v3.x Dependencies:
* [`bibtexparser`](https://bibtexparser.readthedocs.io/en/master/)
* [`flask`](https://flask.palletsprojects.com/)
* [`pylatexenc`](https://pylatexenc.readthedocs.io/en/latest/index.html)

System Dependencies:
* [`graphviz`](https://graphviz.org/)
* [`doxygen`](https://www.doxygen.nl/)

Use the following script to download the dependencies listed above
```bash
pip install bibtexparser flask pylatexenc
```
### To Run
The server needs a configuration file to setup a few options that the server needs to run properly.

Create a file, `src/config.py`, that follows a structure similar to below:
```python3
class Config(object):
	DEBUG=True
	TESTING=False
	SECRET_KEY='something secret'
```
Note that the secret key should, ideally, be some sort of randomly generated string. It is needed to sign cookies that the server needs to operate properly.

Finally, run either `run.bat` (Windows) or `run` (Linux) to start the server and go the [https://127.0.0.1:5000](https://127.0.0.1:5000) to view the index page.
