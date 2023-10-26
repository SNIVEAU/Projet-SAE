
"""
This module contains the views for the Flask application. It defines the routes and functions for rendering the HTML templates and handling user input. 

The routes include:
- home: renders the home page and displays all books in the database
- detail: renders the detail page for a specific book and displays its information, user rating, user comment, and all evaluations and comments for the book
- edit_author: renders the edit author page for a specific author and allows the user to edit the author's name
- save_author: saves the edited author's name to the database
- login: renders the login page and allows the user to log in with their username and password
- logout: logs the user out and redirects them to the home page
- rate_book: allows the user to rate a book and saves the rating to the database
- public_book_details: renders the public book details page for a specific book and displays all evaluations for the book
- comment_book: allows the user to comment on a book and saves the comment to the database
"""

from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
# from flask_login import login_user, current_user, login_required, logout_user
from flask import request


@app.route("/")
def home():
    """home page

    Returns:    {% endblock %}
    {% block content%}
        html: home page
    """
    return render_template("home.html", musiciens=get_musicien(), sorties=get_sorties(), repetitions=get_repetitions())

@app.route("/stat/")
def stat():
    """home page

    Returns:
        html: home page
    """
    return render_template("stat.html",musiciens=get_musicien(), sorties=get_sorties(), repetitions=get_repetitions(),participe=get_participer_repetitions())



# class AuthorForm(FlaskForm):
#     id = HiddenField('id')
#     name = StringField('Nom', validators=[DataRequired()]) # Doit obligatoirement remplir le champs 





# class LoginForm(FlaskForm):
#     # Création des deux formulaires
#     username = StringField('Username')
#     password = PasswordField('Password')
#     next = HiddenField()

#     def get_authenticated_user(self):
#         """Vérifie si l'utilisateur existe et si le mot de passe est correct

#         Returns:
#             user: l'utilisateur
#         """
#         user = User.query.get(self.username.data) # Récupérer l'utilisateur entré dans le formulaire
#         if user is None:
#             return None
        
#         # Hashage
#         m = sha256()
#         m.update(self.password.data.encode())
#         passwd = m.hexdigest()

#         return user if passwd == user.password else None # Vérifier si le mot de passe de l'utilisateur entré est le bon


# # Création du login
# @app.route("/login/", methods=["GET", "POST" ,])
# def login():
#     """Login

#     Returns:
#         html: page de login
#     """
#     f = LoginForm()
#     if not f.is_submitted():
#         f.next.data = request.args.get("next")
#     elif f.validate_on_submit():
#         user = f.get_authenticated_user()
#         if user:
#             login_user(user)
#             return redirect(url_for("home"))
#     return render_template("login.html",form=f)


# @app.route("/register/", methods=["GET", "POST"])
# def register():
#     """s'inscrire"""
#     f = LoginForm()
#     if not f.is_submitted():
#         f.next.data = request.args.get("next")
#     elif f.validate_on_submit():
#         user = User.query.get(f.username.data)
#         if user:
#             f.next.data = request.args.get("hidden")
#             print("L'utilisateur existe déjà.", "error")
#         else:
#             m = sha256()
#             m.update(f.password.data.encode())
#             passwd = m.hexdigest()
#             user = User(username=f.username.data, password=passwd)
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             return redirect(url_for("home"))
#     return render_template("register.html", form=f)


# @app.route("/logout/")
# def logout():
#     """Logout
#     Returns:
#         html: page de home
#     """
#     logout_user()
#     return redirect(url_for("home"))


