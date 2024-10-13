# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql
from flask_mysqldb import MySQLdb
from functools import wraps

# Parent route
admin = Blueprint('admin', __name__)

# Login required decorator
def login_required(trust_level_required=1, admin_only=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # if the user is not logged in, return him to login page
            if "user" not in session:
                return redirect(url_for("home.login"))
            else:
                # fetch the user's name
                user = session['user']

                # Only admin can see this page
                if admin_only:
                    if user == "admin":
                        return func(*args, **kwargs)
                    else:
                        abort(403)
                # The page is available for others
                else:
                    # fetch the user's trust level
                    cursor = mysql.connection.cursor()
                    cursor.execute("SELECT trust_level FROM users WHERE name = %s", (user,))
                    user_trust_level = cursor.fetchone()[0]
                    cursor.close()

                    # users under required trust level cannot see this page
                    if user_trust_level < trust_level_required:
                        abort(403)

                    return func(*args, **kwargs)
        return wrapper
    return decorator


def fetch_columns(table_name):
    """Helper function to fetch column names for a given table."""
    cursor = mysql.connection.cursor()
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    cursor.close()
    return columns

def fetch_all_users():
    """Helper function to fetch all users."""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users




# Routes
@admin.route('/')
def admin_home_page():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            return render_template('admin/index.html')
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/quotes')
@login_required(trust_level_required=3)
def admin_quotes():
    # Fetch quotes
    cursor = mysql.connection.cursor()
    cursor.execute("""
    SELECT q.id, q.content, q.date, q.context, CONCAT(a.first_name, a.middle_name, a.last_name) AS 'author name'
    FROM quotes q
    LEFT OUTER JOIN authors a ON q.author_id = a.id""")
    quotes = cursor.fetchall()
    cursor.close()
    columns = fetch_columns("quotes")
    return render_template("admin/quotes.html", data=quotes, columns=columns)
    # if "user" in session:
    #     cursor = mysql.connection.cursor()
    #     cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
    #     trust_level = cursor.fetchone()[0]
    #     cursor.close()
    #     if trust_level >= 3:
    #         cursor = mysql.connection.cursor()
    #         cursor.execute("""
    #         SELECT q.id, q.content, q.date, q.context, CONCAT(a.first_name, a.middle_name, a.last_name) AS 'author name'
    #         FROM quotes q
    #         LEFT OUTER JOIN authors a ON q.author_id = a.id""")
    #         quotes = cursor.fetchall()
    #         cursor.execute("DESCRIBE quotes")
    #         columns = cursor.fetchall()
    #         cursor.close()
    #         return render_template("admin/quotes.html", data=quotes, columns=columns)
    #     else:
    #         abort(403)
    # else:
    #     return redirect(url_for('home.login'))


@admin.route('/users/')
def admin_users():
    if "user" in session:
        if session['user'] == "admin":
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            cursor.execute('DESCRIBE users')
            columns = cursor.fetchall()
            cursor.close()
            return render_template("admin/users.html", data=users, columns=columns)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/users/<user>', methods=['GET', 'POST'])
def admin_user_detail(user):
    if "user" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = %s', (session['user'],))
        usr = cursor.fetchone()
        cursor.close()
        print(usr)
        if usr['name'] == "admin" and session['user'] == "admin":
            if request.method == 'GET':
                cursor = mysql.connection.cursor()
                cursor.execute('''SELECT * FROM users WHERE name = %s''', (user,))
                user_data = cursor.fetchone()
                cursor.close()
                return render_template("admin/user.html", user=user_data)
            elif request.method == 'POST':
                username = request.form['name']
                email = request.form['email']
                trust_level = request.form['trust']
                cursor = mysql.connection.cursor()
                cursor.execute("""
                UPDATE users SET name = %s, email = %s, trust_level = %s
                WHERE name = %s""", (username, email, trust_level, user))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('admin.admin_users'))
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/nicknames')
@login_required(trust_level_required=3)
def admin_nicknames():
    return "add /author_id to see details about author's nicknames"
    # if "user" in session:
    #     cursor = mysql.connection.cursor()
    #     cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
    #     trust_level = cursor.fetchone()[0]
    #     cursor.close()
    #     if trust_level >= 3:
    #         return "add /author_id to see details about author's nicknames"
    #     else:
    #         abort(403)
    # else:
    #     return redirect(url_for('home.login'))

@admin.route('/nicknames/<author_id>')
def admin_nickname(author_id):
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            cursor = mysql.connection.cursor()
            cursor.execute("""
            SELECT nicknames.nick
            FROM 
                authors a
                LEFT JOIN authorsnicknames on a.id = authorsnicknames.Authors_id
                RIGHT JOIN nicknames on nicknames.id = authorsnicknames.Nicknames_id
            WHERE a.id = cast(%s AS int)
            """, (author_id,))
            nicknames = cursor.fetchall()
            cursor.execute("""
            SELECT a.id, CONCAT(a.first_name, ' ', a.last_name) AS 'author name' 
            FROM authors a
            WHERE a.id = cast(%s AS int)""", (author_id,))
            author = cursor.fetchone()
            cursor.close()
            return render_template("admin/nicknames.html", author=author, data=nicknames)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/nicknames/<author_id>/add', methods=['GET', 'POST'])
def admin_nickname_add(author_id):
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            if request.method == "GET":
                cursor = mysql.connection.cursor()
                cursor.execute("""
                SELECT a.id AS 'id', CONCAT(a.first_name, ' ', a.last_name) AS 'author_name' 
                FROM authors a
                WHERE a.id = cast(%s AS int)""", (author_id,))
                author = cursor.fetchone()
                cursor.execute("""
                SELECT a.id AS 'id', CONCAT(a.first_name, ' ', a.last_name) AS 'author_name' 
                FROM authors a""")
                authors = cursor.fetchall()
                cursor.close()
                return render_template("admin/add_nicknames.html", author=author, authors=authors)
            elif request.method == "POST":
                nickname = request.form['nick']
                author_id = request.form['author']
                cursor = mysql.connection.cursor()
                cursor.execute("""
                INSERT INTO nicknames (nick) VALUES (%s)
                """, (nickname, ))
                mysql.connection.commit()
                cursor.execute("""
                SELECT id
                FROM nicknames
                WHERE nick = %s
                ORDER BY id DESC
                LIMIT 1
                """, (nickname,))
                nick_id = cursor.fetchone()[0]
                cursor.execute("""
                INSERT INTO AuthorsNicknames (Authors_id, Nicknames_id) VALUES (%s, %s)
                """, (author_id, nick_id))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('admin.admin_nickname_add', author_id=author_id))
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/authors')
def admin_authors():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM authors")
            authors = cursor.fetchall()
            cursor.execute("DESCRIBE authors")
            columns = cursor.fetchall()
            cursor.close()
            return render_template("admin/authors.html", data=authors, columns=columns)
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/authors/add', methods=['GET', 'POST'])
def admin_authors_add():
    if "user" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT trust_level FROM users WHERE name = %s", (session['user'],))
        trust_level = cursor.fetchone()[0]
        cursor.close()
        if trust_level >= 3:
            if request.method == 'GET':
                return render_template("admin/add_author.html")
            elif request.method == 'POST':
                first_name = request.form['first_name']
                middle_name = request.form['middle_name'] if request.form['middle_name'] else None
                last_name = request.form['last_name']
                cursor = mysql.connection.cursor()
                cursor.execute("""
                INSERT INTO authors (first_name, middle_name, last_name) VALUES (%s, %s, %s)
                """, (first_name, middle_name, last_name))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('admin.admin_authors'))
        else:
            abort(403)
    else:
        return redirect(url_for('home.login'))

@admin.route('/database', methods=['GET', 'POST'])
def admin_database():
    if request.method == 'GET':
        if "user" in session:
            if session["user"] == "admin":
                return render_template("admin/database.html", data=None, query_value="")
            else:
                abort(403)
        else:
            return redirect(url_for('home.login'))
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute(request.form['query'])
        data = cursor.fetchall()
        cursor.close()
        return render_template("admin/database.html", data=data, query_value=request.form['query'])