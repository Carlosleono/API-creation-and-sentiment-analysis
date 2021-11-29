# API-creation-and-sentiment-analysis
## 


#### In this project we are going to analyze the scripts of all the Marvel movies from 2008 to 2019. In order to do so, we are going to download a Kaggle [dataset](https://www.kaggle.com/pdunton/marvel-cinematic-universe-dialogue) containing all the Lines of the characters in the films. 
#### Then we are going to create a SQL database and insert all the information in three tables: Characters, Films and Lines. After that, we a re going to create an API connected to this SQL database that have access to all the information and allow the user to insert new lines, characters or films, as well as doing sentiment analysis with the selected lines.
#### 

#
# API

#### The API has the following GET endpoints:
- '/characters': returns all the characters
- '/films': returns all the films
- '/characterlines/\<name>': returns all the lines of a character in all movies
- '/filmlines/\<film>': returns all the lines of a film
- '/filmcharacterlines/\<film>/\<name>': returns all the lines of a character in a specified film

#### And the following POST endpoint:
- '/newline': receives line, character, film name and year
- '/newfilm': receives film name and year
- '/newcharacter': receives character

#
# Sentiment analysis

#
# Libraries

[requests](https://pypi.org/project/requests/2.7.0/)

[pandas](https://pandas.pydata.org/)

[re](https://docs.python.org/3/library/re.html)

[Flask](https://flask.palletsprojects.com/en/2.0.x/)

[Markdown](https://pypi.org/project/Markdown/)

[json](https://docs.python.org/3/library/json.html)

[sqlalchemy](https://docs.sqlalchemy.org/en/14/)

[nltk](https://www.nltk.org/)

[textblob](https://textblob.readthedocs.io/en/dev/)

[spacy](https://spacy.io/)


