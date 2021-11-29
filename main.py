
from os import name
from flask import Flask, request, jsonify
import markdown.extensions.fenced_code
import src.sql_tools as sqlt
import json
app = Flask(__name__)

@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template

@app.route("/characters")
def personajes():
    personajes= sqlt.getcharacters()
    return json.dumps(personajes)

@app.route("/films")
def pelis():
    pelis= sqlt.getfilms()
    return jsonify(pelis)

@app.route("/characterlines/<name>")
def frasesnombre(name):
    frasespersonaje= sqlt.obtenerfrases(name)
    return jsonify(frasespersonaje)

@app.route("/filmlines/<film>")
def frasespeli(film):
    frasespeli= sqlt.obtenerfrasespeli(film)
    return jsonify(frasespeli)


@app.route("/filmcharacterlines/<film>/<name>")
def frasespelinombre(film,name):
    
    frasespelinombre = sqlt.obtenerfrasespelinombre(film, name)
    return jsonify(frasespelinombre)

@app.route("/newline", methods=["POST"])
def insertline():
    line = request.form.get("line")
    char_ = request.form.get("character")
    film = request.form.get("film")
    year = request.form.get('year')
    return sqlt.newline(line, char_, film, year)

@app.route("/newfilm", methods = ["POST"])
def insertfilm():
    film = request.form.get('film')
    year = request.form.get('year')

    return sqlt.newfilm(film, year)

@app.route("/newcharacter", methods = ["POST"])
def insertcharacter():
    name = request.form.get('name')

    return sqlt.newcharacter(name)


@app.route("/sentiment/<name>/<film>")
def sentiment_author(name,film):
    df = sqlt.sentiment_analysis(name,film)
    df['Tokenized'] = df['line'].apply(sqlt.tokenizer)
    df['Sentiments'] = df['Tokenized'].apply(sqlt.sentiment)
    return str(df.Sentiments.mean())


app.run(debug=True)