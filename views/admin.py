# Imports
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from db import mysql

# Parent route
admin = Blueprint('admin', __name__)

# Routes
@admin.route('/')
def admin_home_page():
    return "admin homepage"

@admin.route('/quotes')
def admin_quotes():
    return "list of quotes here, with full access to add, modify, delete and update"

@admin.route('/users')
def admin_users():
    return "list of users here, with full access to add, modify, delete and update"

@admin.route('/nicknames')
def admin_nicknames():
    return "list of nicknames here, with full access to add, modify, delete and update"

@admin.route('/authors')
def admin_authors():
    return "list of authors here, with full access to add, modify, delete and update"