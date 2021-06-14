import os
import sys
import flaskcode

from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.config.from_object(flaskcode.default_config)
app.register_blueprint(flaskcode.blueprint, url_prefix='/pythonlogin/flaskcode')
app.config['FLASKCODE_RESOURCE_BASEPATH'] = '/'

app.secret_key = 'lubie_placki'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'pythonlogin'

app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11417642'
app.config['MYSQL_PASSWORD'] = 'AeBsPYMgbu'
app.config['MYSQL_DB'] = 'sql11417642'

mysql = MySQL(app)

@app.route('/')
def hello():
    return redirect(url_for('home'))

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account and sha256_crypt.verify(password, account['password']):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['group_id'] = 0
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('group_id', None)

    return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            password_hashed = sha256_crypt.encrypt(password)
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password_hashed, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])

    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account=account)

    return redirect(url_for('login'))

@app.route('/pythonlogin/create_group', methods=['GET','POST'])
def create_group():
    msg = ''
    if 'loggedin' in session:

        if request.method == 'POST' and 'group_name' in request.form:
            group_name = request.form['group_name']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM app_groups WHERE group_name = %s', (group_name,))
            account = cursor.fetchone()

            if account:
                msg = 'Group already exists!'
            elif not group_name:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO app_groups VALUES (NULL, %s, %s, %s)', (group_name, 1, session['id'],))
                cursor.execute('SELECT max(Group_ID) as id FROM app_groups')
                grp_id = cursor.fetchone()
                cursor.execute('INSERT INTO memberships VALUES (NULL, %s, %s, %s)', (session['id'], grp_id['id'], 'Administrator',)) 
                mysql.connection.commit()
                msg = 'Group has been successfully created!'

        elif request.method == 'POST':
            msg = 'Please fill out the form!'

        return render_template('create_group.html', msg=msg)

    return redirect(url_for('login'))

@app.route('/pythonlogin/groups', methods=['GET','POST'])
def groups():
    if 'loggedin' in session:
        
        if request.method == 'POST' and 'group_id' in request.form:
            grp_id = request.form.get("group_id","")
            session['group_id'] = grp_id
            return redirect(url_for('groups_menu'))
            
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT app_groups.Group_ID, app_groups.Group_name, app_groups.Liczba_uczestnikow, memberships.Member_ID'
                        ' FROM app_groups JOIN memberships ON app_groups.Group_ID = memberships.Group_ID'
                        ' WHERE Member_ID = %s', (session['id'],))
            groups = cursor.fetchall()
            return render_template('groups.html', groups=groups)

    return redirect(url_for('login'))

@app.route('/pythonlogin/groups_menu', methods=['GET','POST'])
def groups_menu():
    msg = ''

    if 'loggedin' in session:
        if request.method == 'POST' and 'dodaj_do_grupy' in request.form:
            username = request.form['username']
            type = request.form['type']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accounts.username, memberships.Member_type, app_groups.Group_name'
                            ' FROM accounts, memberships, app_groups'
                            ' WHERE app_groups.Group_ID = %s AND accounts.id = memberships.Member_ID AND app_groups.Group_ID = memberships.Group_ID', (session['group_id'], ))
            users = cursor.fetchall()

            cursor.execute('SELECT accounts.username'
                            ' FROM accounts'
                            ' WHERE accounts.username = %s', (username, ))
            system_user = cursor.fetchall()

            cursor.execute('SELECT accounts.username FROM accounts, memberships, app_groups'
                            ' WHERE accounts.username = %s AND app_groups.Group_ID = %s AND accounts.id = memberships.Member_ID AND app_groups.Group_ID = memberships.Group_ID', (username, session['group_id'], ))
            user_in_group = cursor.fetchall()

            if not(system_user):
                msg="Użytkownik nie istnieje w systemie"
                return render_template('groups_menu.html', users=users, msg=msg)
            elif not(user_in_group):
                msg="Pomyślnie dodano użytkownika"
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM accounts WHERE accounts.username = %s', (username, ))
                add_user = cursor.fetchone()
                cursor.execute('INSERT INTO memberships VALUES (NULL, %s, %s, %s)', (add_user['id'], session['group_id'], type, ))
                mysql.connection.commit()
                cursor.execute('UPDATE app_groups SET app_groups.Liczba_uczestnikow = app_groups.Liczba_uczestnikow+1 WHERE app_groups.Group_ID = %s', (session['group_id']))
                mysql.connection.commit()
                session.pop('group_id', None)
                return render_template('groups_menu.html', users=users, msg=msg)
            else:
                msg="Użytkownik istnieje w grupie"

            return render_template('groups_menu.html', users=users, msg=msg)
        
        elif request.method == 'POST' and 'usun_z_grupy' in request.form:
            username = request.form['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accounts.username, memberships.Member_type, app_groups.Group_name'
                            ' FROM accounts, memberships, app_groups'
                            ' WHERE app_groups.Group_ID = %s AND accounts.id = memberships.Member_ID AND app_groups.Group_ID = memberships.Group_ID', (session['group_id'], ))
            users = cursor.fetchall()

            cursor.execute('SELECT accounts.username'
                            ' FROM accounts'
                            ' WHERE accounts.username = %s', (username, ))
            system_user = cursor.fetchall()

            cursor.execute('SELECT accounts.username FROM accounts, memberships, app_groups'
                            ' WHERE accounts.username = %s AND app_groups.Group_ID = %s AND accounts.id = memberships.Member_ID AND app_groups.Group_ID = memberships.Group_ID', (username, session['group_id'], ))
            user_in_group = cursor.fetchall()

            if not(system_user):
                msg="Użytkownik nie istnieje w systemie"
                return render_template('groups_menu.html', users=users, msg=msg)
            elif user_in_group:
                msg="Pomyślnie usunięto użytkownika"
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM accounts WHERE accounts.username = %s', (username, ))
                del_user = cursor.fetchone()
                cursor.execute('DELETE FROM memberships WHERE memberships.Member_ID = %s', (del_user['id'],))
                mysql.connection.commit()
                cursor.execute('UPDATE app_groups SET app_groups.Liczba_uczestnikow = app_groups.Liczba_uczestnikow-1 WHERE app_groups.Group_ID = %s', (session['group_id']))
                mysql.connection.commit()
                session.pop('group_id', None)
                return render_template('groups_menu.html', users=users, msg=msg)
            else:
                msg="Użytkownik nie istnieje w grupie"

            return render_template('groups_menu.html', users=users, msg=msg)

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accounts.username, memberships.Member_type, app_groups.Group_name'
                            ' FROM accounts, memberships, app_groups'
                            ' WHERE app_groups.Group_ID = %s AND accounts.id = memberships.Member_ID AND app_groups.Group_ID = memberships.Group_ID', (session['group_id'], ))
            users = cursor.fetchall()
            return render_template('groups_menu.html', users=users)

    return redirect(url_for('login'))

@app.route('/pythonlogin/flaskcode')
def editor():
    if 'loggedin' in session:
        pass
    return redirect(url_for('login'))