from runipy.notebook_runner import NotebookRunner
from IPython.nbformat import read, write
import nbformat
from nbconvert import HTMLExporter

from flask import Flask, render_template, Markup
# from flask.ext.github import GitHub
app = Flask(__name__)

# app.config['GITHUB_CLIENT_ID'] = 'XXX'
# app.config['GITHUB_CLIENT_SECRET'] = 'YYY'

# # For GitHub Enterprise
# app.config['GITHUB_BASE_URL'] = 'https://HOSTNAME/api/v3/'
# app.config['GITHUB_AUTH_URL'] = 'https://HOSTNAME/login/oauth/'

# github = GitHub(app)

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

	html_file= open("static/stock_infos.html","w")
	html_file.write(body.encode('utf8', 'ignore'))
	html_file.close()

	return app.send_static_file('stock_infos.html')

if __name__ == '__main__':
    app.run(debug=False)