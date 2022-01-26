from flask import Flask, render_template, request, url_for, redirect, session
from mangas import Mangas
import secrets


app = Flask(__name__)
HEX = secrets.token_hex(16)
app.secret_key = HEX 
mangas = Mangas()


def shape_list(lista, colums=3):
	out = []
	for i in range(0, len(lista), colums):
		out.append(lista[i: i + colums])

	return out


@app.route('/', methods=["POST", "GET"])
def raiz():
	if request.method == "POST":
		manga_title = request.form["manga_title"]
		return redirect(url_for("results", manga_title=manga_title))
	
	# cookie = request.cookies['session']
	# if not cookie in session:
	# 	session['cookie'] = {}

	return render_template('pesquisa.html')


@app.route('/results/<manga_title>')
def results(manga_title):
	if manga_title:
		lista = mangas.search(manga_title)
		lista = shape_list(lista['Mangas'])
		return render_template('resultados.html', RESULTADOS=lista)
	
	return 'Verifique se passou algum título'


@app.route('/chapters', methods=['POST', 'GET'])
def chapters():
	if request.method == 'POST':
		manga_url = request.get_json()['manga_url']
		capitulos = mangas.get_last_chapter(manga_url)
		grupo_de_capitulos = shape_list(capitulos, colums=4)

		return render_template('capitulos.html', GRUPOS=grupo_de_capitulos, URL=manga_url)

	return 'Não conseguimos acessar os capítulos'


@app.route('/pages', methods=['POST', 'GET'])
def pages():
	if request.method == 'POST':
		DATA = request.get_json()
		session['CAP_URL'] = DATA['CAP_URL']
		return ('ok', 200)

	if 'CAP_URL' in session:
		url_capitulo = session['CAP_URL']
		pages = mangas.get_pages(url_capitulo)
		return render_template('pagina.html', PAGINAS=pages, FIRST=pages[0])

	return 'Erro ao acessar páginas'


app.run(host='0.0.0.0', port=5000, debug=True)