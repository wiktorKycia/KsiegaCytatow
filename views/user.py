from flask import Blueprint, render_template, request, redirect, url_for, abort, session, g
from config import mysql, send_change_password_email, generate_token, send_email_with_url, verify_token
from flask_mysqldb import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
profile = Blueprint('profile', __name__)


# URL Preprocessor to fetch user by slug
@profile.url_value_preprocessor
def get_profile_owner(endpoint, values):
    user_url_slug = values.pop('user_url_slug')  # Extract the slug from the URL

    # Execute SQL query to fetch the user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM users WHERE name = %s', (user_url_slug,))

    user = cur.fetchone()
    cur.close()

    if user is None:
        return "User not found", 404


    if "user" in session:
        g.profile_owner = user  # Store the user info in the 'g' object
    else:
        return redirect(url_for("home.login"))



# TODO: change nickname preferences
# TODO: display favourite quotes

# Route to display the user profile
@profile.route('/')
def user_profile():
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT trust_level, email FROM users WHERE name = %s', (user['name'],))
            trust, email = cursor.fetchone()
            cursor.close()
            if trust < 1:
                session['user_email'] = email
                return render_template("profile/index.html", username=user['name'], canverify=True)

            return render_template("profile/index.html", username=user['name'], canverify=False)
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))

@profile.route('/send_email')
def send_email():
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner
            print(user)
            email = user.get("email")
            token = generate_token(email)
            send_email_with_url(
                email, url_for("profile.change_password", token=token, user_url_slug=session['user'], _external=True),
                "Password change",
                "Click the link here to change your password {url}",
            )
            return "Check your email inbox for a link"
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))

@profile.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token): # tutaj potrzebny jest parametr <token> i jego weryfikacja jak w home.py
    if "user" in session:
        if g.profile_owner.get('name') == session['user']:
            user = g.profile_owner

            try:
                email = verify_token(token)
            except:
                print('The verification link is invalid or has expired.')
                # flash('The verification link is invalid or has expired.', 'danger')
                return redirect(url_for('index'))

            if request.method == 'GET':
                return render_template("profile/change_password.html", password_not_match=False)
            elif request.method == 'POST':
                password = request.form['password']
                password_confirm = request.form['password2']
                if password != password_confirm:
                    return render_template("profile/change_password.html", password_not_match=True)
                else:
                    password = generate_password_hash(password)
                    cursor = mysql.connection.cursor()
                    cursor.execute('UPDATE users SET user_password = %s WHERE name = %s', (password, user['name']))
                    mysql.connection.commit()
                    cursor.close()
                    return redirect(url_for('profile.user_profile', user_url_slug=session['user']), code=302)
        else:
            return redirect(url_for("profile.user_profile", user_url_slug=session['user']), code=302)
    else:
        return redirect(url_for("home.login"))

# pierwsze zapytanie: dostępni autorzy i ich dostępne nicki
# 3 tabele: authors, AuthorsNicknames, nicknames
# przetransformować do formy: (pętla for i po kolei dodawanie autorów i cytatów do słownika)
# dictionary = {
#     "author_1" : [
#         ("nick_1", False),
#         ("nick_2", False) # <- jak będzie True, to znaczy, że ta opcja w html-u będzie selected
#     ],
#     "author_2" : [
#         ("nick_3", False),
#         ("nick_4", False)
#     ]
# }
# print(dictionary)

# drugie zapytanie: wybrane nicki przez użytkownika
# id_autorów, id_nickname  tam gdzie user_id == profileowner[id]
# do tych id-ków, dołączyć author_name, nickname
# przetransformować do listy tupli: (nawet sql-em można wybrać, żeby były tylko stringi, w sensie bez id-ków)
# jeśli id_nickname jest NULL to znaczy, że użytkownik nie wybrał nicku i trzeba (w html-u) wstawić author_name
# lista = [
#     ('author_name', 'nick'),
#     ('author_name_2', 'nick_2')
# ]
# print(lista)

# porównanie słownika i listy:
# dla każdego <autor> w liście:
# patrzymy do podlisty o kluczu <autor> w słowniku
# tam gdzie nick w podliście w słowniku  równa się  nick w liście,
#   tam wstawiamy True
# print(dictionary)

# sprawdzenie, czy w każdej podliście jest tylko jedno True (lub 0)
# przekazanie słownika do html-a