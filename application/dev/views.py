
"""

"""

from .app import *
from flask import render_template, url_for, redirect, request
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, current_user, login_required, logout_user
from flask import request


@login_manager.user_loader
def load_user(user_id):
    return Musicien.query.get(user_id)

@app.route("/")
def home():
    """home page

    Returns:
        html: home page
    """
    return render_template("home.html", musiciens=get_musicien(), sorties=get_sorties(), repetitions=get_repetitions())

@app.route("/sondage/")
def page_sondage():
    print("test")
    participations = participer_sortie.query.filter_by(idMusicien=current_user.idMusicien).all()
    return render_template("sondage.html",sondages=get_sondages(),get_sortie_by_id=get_sortie_by_id,participer_sortie=get_sortie_by_musicien(current_user.idMusicien))

@app.route("/log/")

def page_log():

    return render_template("home.html")

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


