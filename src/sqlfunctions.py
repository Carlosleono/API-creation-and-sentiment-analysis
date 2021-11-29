import re
import os
from dotenv import load_dotenv
import sqlalchemy as alch

load_dotenv()

password = os.getenv('pass')

db_name = "mydb"
conec = f"mysql+pymysql://root:{password}@localhost/{db_name}"
engine = alch.create_engine(conec)

def nombres(marvel):
    for row in marvel:
        if re.match('.*TONY.*', row):
            row = 'TONY STARK'
        if re.match('.*STEVE.*', row):
            row = 'STEVE ROGERS'
        if re.match('.*NATASHA.*', row):
            row = 'NATASHA ROMANOFF'
        if re.match('.*FURY.*', row):
            row = 'FURY'
        if re.match('.*THOR.*', row):
            row = 'THOR'
        if re.match('.*CLINT.*', row):
            row = 'CLINT BARTON'
        if re.match('.*HULK.*', row):
            row = 'HULK'
        if re.match('.*LOKI.*', row):
            row = 'LOKI'
    return marvel

    

def check(tabla, valor):
    '''
    Función que comprueba si el elemento llamado existe en la tabla.
    DEvuelve True si existe y False si no
    '''
    if tabla == 'Character':
        query = list(engine.execute(f"SELECT Name FROM `Character` WHERE Name = '{valor}'"))
        if len(query) > 0:
            return True
        else:
            return False

    if tabla == 'Film':
        query = list(engine.execute(f"SELECT Name FROM Film WHERE Name = '{valor}'"))
        if len(query) > 0:
            return True
        else:
            return False

    if tabla == 'Lines':
        query = list(engine.execute(f"SELECT line FROM `Lines` WHERE line = '{valor}'"))
        if len(query) > 0:
            return True
        else:
            return False

def insertCharacter(value):
    """
    Llama a la función check para comprobar si existe el personaje
    Inserta personaje si no existe
    """
    if check("Character", value):
        return "Character already exists"
    else:
        engine.execute(f"INSERT INTO `Character` (Name) VALUES ('{value}');")

def insertFilm(value):
    """
    Llama a la función check para comprobar si existe la película
    Inserta película si no existe
    """
    if check("Film", value):
        return "Film already exists"
    else:
        engine.execute(f"INSERT INTO Film (Name) VALUES ('{value}');")

def dameId(que,string):
    """
    Devuelve el ID de lo que le pidamos sabiendo que ese elemento EXISTE
    """
    if que == "Character":
        return list(engine.execute(f"SELECT characterID FROM `Character` WHERE Name ='{string}';"))[0][0]
    elif que == "Film":
        return list(engine.execute(f"SELECT FilmID FROM Film WHERE Name ='{string}';"))[0][0]

def insertLine(fila, indice):
    """
    La función final 
    """
    try:
        if check("Lines", fila["line"]):
            return "line already exists"
        else:
            if check("Character", fila["character"]):
                character_id = dameId("Character", fila["character"])
            else:
                insertCharacter(fila["character"])
                character_id = dameId("Character", fila["character"])
            
            if check("Film", fila["movie"]):
                film_id = dameId("Film", fila["movie"])
            else:
                insertFilm(fila["movie"])
                film_id = dameId("Film", fila["movie"])
                
            engine.execute(f"""
            INSERT INTO `Lines` (line, Year, Character_characterID, Film_FilmID) VALUES
            ("{fila['line']}", "{fila['year']}", "{character_id}", "{film_id}");
            """)
    except Exception as e:
        print('Error en la fila: ', indice, '\nError: ', e)

def sustituye(x):
    x = str(x).replace('"', "`")
    x = str(x).replace("'", "`")
    return x