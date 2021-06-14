1. Zainstaluj dependencies:
pip install flaskcode
pip install passlib
pip install flask
pip install flask-mysqldb

2. Sklonuj cały projekt

3. Otwórz cmd w folderze SkyCode

4. Uruchom te komendy
Run command: set FLASK_APP=app.py
Run command: set FLASK_DEBUG=1
Run command: flask run

5. Otwórz stronę http://127.0.0.1:5000/pythonlogin/

#####################################

app.config['FLASKCODE_RESOURCE_BASEPATH'] = 'Ścieżka/do/folderu/z/zasobami'
