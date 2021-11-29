import re
import os
from dotenv import load_dotenv
import sqlalchemy as alch
import pandas as pd
# from Configuration.configuration import engine
# import random
from nltk.corpus import stopwords
import string
import spacy
import en_core_web_sm
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

load_dotenv()

password = os.getenv('pass')

db_name = "mydb"
conec = f"mysql+pymysql://root:{password}@localhost/{db_name}"
engine = alch.create_engine(conec)

def getcharacters():
    query = f"""
    SELECT Name 
    FROM mydb.Character 
    """

    personajes = list(engine.execute(query))
    lista = [{'Name': personaje[0]} for personaje in personajes]
    return lista

def getfilms():
    query = f"""
    SELECT Name 
    FROM mydb.Film 
    """

    pelis = pd.read_sql_query(query,engine)
    
    return pelis.to_json(orient='records')

def dameId(que,string):
    """
    Devuelve el ID de lo que le pidamos sabiendo que ese elemento EXISTE
    """
    if que == "Character":
        return list(engine.execute(f"SELECT characterID FROM `Character` WHERE Name ='{string}';"))[0][0]
    elif que == "Film":
        return list(engine.execute(f"SELECT FilmID FROM Film WHERE Name ='{string}';"))[0][0]

def obtenerfrases(nombre):
    
    id = dameId('Character', nombre)
    
    query2= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Character_characterID = {id};
    """
    lines = pd.read_sql_query(query2, engine)
    return lines.to_json(orient='records')

def obtenerfrasespeli(peli):
    
    id = dameId('Film', peli)

    query2= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Film_FilmID = {id};
    """
    lines = pd.read_sql_query(query2, engine)
    return lines.to_json(orient='records')

def obtenerfrasespelinombre(peli, nombre):
    
    idname = dameId('Character', nombre)
    idfilm = dameId('Film', peli)

    query3= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Film_FilmID = {idfilm}
    AND Character_characterID = {idname};
    """
    lines = pd.read_sql_query(query3, engine)
    return lines.to_json(orient='records')

def newline(line,character,film, year):

    cid = dameId('Character', character)
    fid = dameId('Film', film)
    engine.execute(f"""
    INSERT INTO `Lines` (line,year, Character_characterID, Film_FilmID)
    VALUES ('{line}', {year}, {cid}, {fid});
    """)
    
    return f"Se ha introducido correctamente: {line} {character} {film}"

def newfilm(film,year):
    engine.execute(f"""
    INSERT INTO `Film` (Name,year)
    VALUES ('{film}', {year});
    """)
    return "Se ha introducido correctamente una peli"

def newcharacter(character):
    engine.execute(f"""
    INSERT INTO `Character` (Name)
    VALUES ('{character}');
    """)
    return "Se ha introducido correctamente un personaje"

def sentiment_analysis(name,film):
    idname = dameId('Character', name)
    idfilm = dameId('Film', film)

    query= f"""
    SELECT line
    FROM `Lines`
    WHERE Film_FilmID = {idfilm}
    AND Character_characterID = {idname};
    """
    data = pd.read_sql_query(query,engine)
    return data

def tokenizer(txt):
    nlp = spacy.load("en_core_web_sm")
    tokens = nlp(txt)
    filtered = []  
    for token in tokens:
        if not token.is_stop:
            lemma = token.lemma_.lower().strip()
            if re.search('^[a-zA-Z]+$',lemma): 
                filtered.append(lemma)
    return " ".join(filtered)

def sentiment(quote):
    sia = SentimentIntensityAnalyzer()
    polarity = sia.polarity_scores(quote)
    pol = polarity["compound"]
    return pol