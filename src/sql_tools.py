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
    """
    This function returns all the character names in a list of dictionaries to make it possible to convert to a panda
    """
    query = f"""
    SELECT Name 
    FROM mydb.Character 
    """

    personajes = list(engine.execute(query))
    lista = [{'Name': personaje[0]} for personaje in personajes]
    return lista

def getfilms():
    """
    This function returns all the films in the database in a list of dictionaries to make it possible to convert to a panda
    """
    queryf = f"""
    SELECT Name 
    FROM mydb.Film;
    """

    pelis = pd.read_sql_query(queryf,engine)
    lista = [{'Film': peli} for peli in pelis['Name']]
    return lista

def dameId(que,string):
    """
    Devuelve el ID de lo que le pidamos sabiendo que ese elemento EXISTE
    """
    if que == "Character":
        return list(engine.execute(f"SELECT characterID FROM `Character` WHERE Name ='{string}';"))[0][0]
    elif que == "Film":
        return list(engine.execute(f"SELECT FilmID FROM Film WHERE Name ='{string}';"))[0][0]

def obtenerfrases(nombre):
    """
    This function returns all the lines in the database in a list of dictionaries to make it possible to convert to a panda
    """
    id = dameId('Character', nombre)
    
    query2= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Character_characterID = {id};
    """
    lines = pd.read_sql_query(query2, engine)
    lista = [{'Line': line} for line in lines['line']]
    return lista

def obtenerfrasespeli(peli):
    """
    This function returns all the lines in a specified film in a list of dictionaries to make it possible to convert to a panda
    """
    
    id = dameId('Film', peli)

    query2= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Film_FilmID = {id};
    """
    lines = pd.read_sql_query(query2, engine)
    lista = [{'Line': line} for line in lines['line']]
    return lista

def obtenerfrasespelinombre(peli, nombre):
    """
    This function returns all the lines in a specified film in a list of dictionaries to make it possible to convert to a panda
    """
    idname = dameId('Character', nombre)
    idfilm = dameId('Film', peli)

    query3= f"""
    SELECT line
    FROM mydb.Lines
    WHERE Film_FilmID = {idfilm}
    AND Character_characterID = {idname};
    """
    lines = pd.read_sql_query(query3, engine)
    lista = [{'Line': line} for line in lines['line']]
    return lista

def newline(line,character,film, year):
    """
    This function insert a line in Lines table, receiving the line, the character that says it, the film in which it is said
    and the year of the film
    """
    cid = dameId('Character', character)
    fid = dameId('Film', film)
    engine.execute(f"""
    INSERT INTO `Lines` (line,year, Character_characterID, Film_FilmID)
    VALUES ('{line}', {year}, {cid}, {fid});
    """)
    
    return f"Se ha introducido correctamente: {line} {character} {film}"

def newfilm(film,year):
    """
    This function insert a new film in Film table receiving the name of the film and the year
    """
    engine.execute(f"""
    INSERT INTO `Film` (Name,year)
    VALUES ('{film}', {year});
    """)
    return "Se ha introducido correctamente una peli"

def newcharacter(character):
    """
    This function insert a character in Character table receiving the name of the character
    """
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