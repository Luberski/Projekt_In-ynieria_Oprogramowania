1. Zainstalować dependencies:
https://www.python.org/downloads/ //Zainstaluj python 3
Uruchom komendy w konsoli:
Run command: pip install flaskcode
Run command: pip install passlib
Run command: pip install flask
Run command: pip install flask-mysqldb

2. Sklonować cały projekt

3. Otwórz cmd w folderze SkyCode

4. Uruchomić te komendy
Run command: set FLASK_APP=app.py
Run command: set FLASK_DEBUG=1
Run command: flask run

5. Otworzyć stronę http://127.0.0.1:5000/pythonlogin/

#####################################

app.config['FLASKCODE_RESOURCE_BASEPATH'] = 'Ścieżka/do/folderu/z/zasobami'
