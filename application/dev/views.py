
"""

"""

from .app import *
from flask import render_template, url_for, redirect, request,jsonify
from .models import *
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
<<<<<<< HEAD
from hashlib import sha256
from flask_login import login_user, current_user, login_required, logout_user
from flask import request
=======
>>>>>>> origin/develop

from hashlib import sha256

from flask_login import login_user, current_user, login_required, logout_user
from flask import request
import plotly.graph_objs as go
from flask import Flask, render_template

@login_manager.user_loader
def load_user(user_id):
    return Musicien.query.get(user_id)

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

    Returns:    {% endblock %}
    {% block content%}
        html: home page
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

@app.route("/stat/")
def stat():
    """home page

    Returns:
        html: home page
    """
    
    data = [go.Bar(x=[], y=[])]
    data2 = [go.Bar(x=[1,2,3,4,5], y=[1,2,8])]
    data_jour_dispo = [go.Bar(x=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"], y=["Feur"])]
    mus=get_musicien()
    for musicien in mus:
        data.append(go.Bar(x=[musicien.nomMusicien], y=[musicien.ageMusicien]))
    layout = go.Layout(title='Nombre de participation par musicien')
    layout2 = go.Layout(title='Pourcentage de participation par activité')
    layout_jour_dispo = go.Layout(title='Jour de disponibilité')
    fig = go.Figure(data=data, layout=layout)
    fig2 = go.Figure(data=data2, layout=layout2)
    fig_jour_dispo = go.Figure(data=data_jour_dispo, layout=layout_jour_dispo)
    #  catégorie de personne présente
    #pourcentage de personne présente à une activité
    #vérifier le pourcentage de réponse à un sondage
    # graphique affichatn les jours avec le plus de disponibilité
    #pourceentage h/f
    return render_template("stat.html",musiciens=get_musicien(),plot=fig.to_html(),pourcentage=fig2.to_html(),jour_dispo=fig_jour_dispo.to_html())

@app.route("/sondage/")
def page_sondage():
    participations = participer_sortie.query.filter_by(idMusicien=current_user.idMusicien).all()
    return render_template("sondage.html",sondages=get_sondages(),get_sortie_by_id=get_sortie_by_id,participer_sortie=get_sortie_by_musicien(current_user.idMusicien))

<<<<<<< HEAD
@app.route('/update_temps<idSondage>')
def update_temps(idSondage:Sondage.idSondage):
    # Code to update the content
    new_content = get_sondage_by_id(idSondage).temps_restant()
    return jsonify({'content': new_content})

@app.route("/sondage_ajout")
def sondage_ajoute():
    s=Sondage(idSondage=get_max_id_sondage()+1,
                idSortie=1,
                message="test",
                dateSondage=datetime.now(),
                dureeSondage=1)
    db.session.add(s)
    db.session.commit()
    return page_sondage()

@app.route("/sortie_ajoute/" , methods=["GET", "POST"])
def ajoute_sortie():
    print(request.form)
    #date_str=request.form["date"]
    #print(date_str)
    #date=datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return page_sondage()

# class AuthorForm(FlaskForm):
#     id = HiddenField('id')
#     name = StringField('Nom', validators=[DataRequired()]) # Doit obligatoirement remplir le champs 
 
=======
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

>>>>>>> origin/develop




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


