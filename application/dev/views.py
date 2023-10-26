
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
from wtforms import BooleanField, StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired

from hashlib import sha256

from flask_login import login_user, current_user, login_required, logout_user
from flask import request


@app.route("/")
def home():
    musiciens = Musicien.query.all()
    return render_template("home.html", musiciens=musiciens)

class LoginForm(FlaskForm):
    # Création des deux formulaires
    nomMusicien = StringField('Nom')
    prenomMusicien = StringField('Prénom')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct

        Returns:
            user: l'utilisateur
        """
        nom = self.nomMusicien.data
        prenom = self.prenomMusicien.data
        username = f"{nom}.{prenom}"  # Utiliser le username généré

        musicien = Musicien.query.filter_by(nomMusicien=nom, prenomMusicien=prenom).first()
        if musicien is None:
            return None
        # Vérifier si le mot de passe est correct
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return musicien if passwd == musicien.password else None


# Création du login
@app.route("/login/", methods=["GET", "POST"])
def login():
    """Login

    Returns:
        html: page de login
    """
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
        else:
            print("Identifiants incorrects. Veuillez réessayer.", "danger")
    return render_template("login.html", form=f)


class RegistrationForm(FlaskForm):
    nomMusicien = StringField('Nom')
    prenomMusicien = StringField('Prénom')
    telephone = StringField('Télephone')
    adresseMail = StringField('Email')
    password = PasswordField('Mot de passe')
    confirm_password = PasswordField('Confirmer le mot de passe')
    isAdmin = BooleanField('Admin')  # Ajout du champ pour la case à cocher
    next = HiddenField()

    def validate(self):
        """Vérifie si le formulaire est valide

        Returns:
            bool: True si le formulaire est valide
        """
        # Vérifier si le mot de passe est correct
        if self.password.data != self.confirm_password.data:
            self.password.errors.append("Les mots de passe ne correspondent pas")
            return False
        # Vérifier si l'utilisateur existe déjà
        nom = self.nomMusicien.data
        prenom = self.prenomMusicien.data
        username = f"{nom}.{prenom}"

        # Vérifier si isAdmin est coché
        admin = self.isAdmin.data  # Récupère la valeur de la case à cocher

        return True





@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST" and form.validate():
        # Récupérer les données du formulaire
        nom = form.nomMusicien.data
        prenom = form.prenomMusicien.data
        telephone = form.telephone.data
        adresseMail = form.adresseMail.data
        password = form.password.data
        admin = form.isAdmin.data 


        # Hasher le mot de passe
        m = sha256()
        m.update(password.encode())
        hashed_password = m.hexdigest()
        # Ajouter l'utilisateur à la base de données
        user = Musicien(
            idMusicien=get_max_idMusicient() + 1,
            nomMusicien=nom,
            prenomMusicien=prenom,
            password=hashed_password,
            telephone=telephone,
            adresseMail=adresseMail,
            admin=admin
        )
        db.session.add(user)
        db.session.commit()

        # Rediriger l'utilisateur vers une page de confirmation ou de connexion
        return redirect(url_for("login"))

    return render_template("register.html", form=form)



@app.route("/logout/")
def logout():
    """Logout
    Returns:
        html: page de home
    """
    logout_user()
    return redirect(url_for("home"))


