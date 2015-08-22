from runipy.notebook_runner import NotebookRunner
from IPython.nbformat import read, write
# from IPython.nbconvert.exporters.html import HTMLExporter
import nbformat
from nbconvert import HTMLExporter

from flask import Flask, render_template, Markup
app = Flask(__name__)

@app.route('/')
def render_nb():
	# need ipynb v3 to play nice with runipy
	notebook = read(open("stock_infos.ipynb"), 3)

	nb = NotebookRunner(notebook, pylab=True)
	nb.run_notebook()
	
	# need ipynb v4 to play nice with Jupyter
	nb = nbformat.convert(nb.nb, 4)

	html_exporter = HTMLExporter()
	body, resources = html_exporter.from_notebook_node(nb)
	# body = Markup.escape(body)
	html_file= open("static/stock_infos.html","w")
	html_file.write(body.encode('utf8', 'ignore'))
	html_file.close()


	# render_template('stock_infos.html')
	return app.send_static_file('stock_infos.html')

if __name__ == '__main__':
    app.run(debug=True)