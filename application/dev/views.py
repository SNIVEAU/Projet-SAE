from .app import *
from flask import render_template, url_for, redirect, request,jsonify
from .models import *
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField , HiddenField, PasswordField,EmailField, IntegerField, DateTimeField  
from wtforms.validators import DataRequired, Email, NumberRange
from flask_login import login_user, current_user, login_required, logout_user
from flask import request
from hashlib import sha256
import plotly.graph_objs as go
from flask import Flask, render_template
import calendar

MOIS=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
import email_validator


@login_manager.user_loader
def load_user(user_id):
    return Musicien.query.get(user_id)

@app.route("/")
def home():
    musiciens = Musicien.query.all()
    return render_template("home.html", musiciens=musiciens)

@app.route("/calendrier/")
def calendrier():
    c=calendar.HTMLCalendar(firstweekday=0)
    c.cssclasses_weekday_head=["jour", "jour", "jour", "jour", "jour", "jour", "jour"]
    c.cssclass_month_head="mois"
    num_day=datetime.now().day
    num_mois=datetime.now().month
    mois=MOIS[num_mois-1]+" "+str(datetime.now().year)
    return render_template("calendrier.html",get_sortie_by_id=get_sortie_by_id,calendrier=c.formatmonth(datetime.now().year,datetime.now().month),num_day=num_day, mois=mois)


@app.route('/get_val_dico_mois/<day>')
def get_val_dico_mois_route(day):
    result = get_val_dico_mois(day)
    print(result)
    if result is None:
        return jsonify({})
    dict={}
    for i in range(len(result)):
        if i==0 and result[i] is not None:
            dict["sortie"]=result[i]
        if i==1 and result[i] is not None:
            dict["repetition"]=result[i]
    print(dict)
    return jsonify(dict)


@app.route("/sortie/<idSortie>")
def sortie(idSortie):
    sortie = get_sortie_by_id(idSortie)
    return render_template("sortie.html", sortie=sortie)

@app.route("/repetition/<idRepetition>")
def repetition(idRepetition):
    rep = get_repetition_by_idRep(idRepetition)
    return render_template("repetition.html", rep=rep)

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
        print(passwd)
        return musicien if passwd == musicien.password else None


# Création du login
@app.route("/login/", methods=["GET", "POST"])
def login():

    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
        else:
            f.password.errors += ("Nom d'utilisateur ou mot de passe incorrect",)
    return render_template("login.html", form=f)

@app.route("/stat/")
def stat():
    """home page

    Returns:
        html: home page
    """
    if current_user.is_authenticated and current_user.admin and len(get_sorties())!=0:
        data = [go.Bar(x=[], y=[])]
        data2 = [go.Bar(x=[], y=[])]
        data_jour_dispo = [go.Bar(x=[], y=[])]
        mus=get_musicien()
        layout = go.Layout(title='Nombre de participation par musicien')
        layout2 = go.Layout(title='Pourcentage de participation par activité')
        layout_jour_dispo = go.Layout(title='Jour de disponibilité')
    
        for musicien in mus:
            data.append(go.Bar(x=[musicien.nomMusicien], y=[len(get_sortie_by_musicien(musicien.idMusicien))]))
        for sort in get_sorties():
            print(sort.description)
            pourcent = len(get_musicien_by_sortie(sort.idSortie)) / len(get_musicien())*100
            data2.append(go.Bar(x=[sort.dateSortie], y=[pourcent]))
        deja_parcouru = []
        for dispo in get_disponibilites():
            if get_musicien_by_id(dispo.idMusicien).nomMusicien not in deja_parcouru:
                deja_parcouru.append(get_musicien_by_id(dispo.idMusicien).nomMusicien)
                data_jour_dispo.append(go.Bar(x=[get_musicien_by_id(dispo.idMusicien).nomMusicien], y=[len(get_disponibilite_by_musicien(dispo.idMusicien))]))
        #  catégorie de personne présente
        #pourcentage de personne présente à une activité
        #vérifier le pourcentage de réponse à un sondage
        # graphique affichatn les jours avec le plus de disponibilité
        #pourceentage h/f
        fig = go.Figure(data=data, layout=layout)
        fig2 = go.Figure(data=data2, layout=layout2)
        fig_jour_dispo = go.Figure(data=data_jour_dispo, layout=layout_jour_dispo)
        return render_template("stat.html",musiciens=get_musicien(),plot=fig.to_html(),pourcentage=fig2.to_html(),jour_dispo=fig_jour_dispo.to_html())
    return render_template("error_pages.html"), 403

@app.route("/sondage/")
def page_sondage(erreur=False):
    if current_user.is_authenticated:

        s=get_sondage_non_rep(current_user.idMusicien)
        if s is None:
            s=[]
        return render_template("sondage.html",len=len,sondages=s,get_sortie_by_id=get_sortie_by_id,get_sondage_by_sortie=get_sondage_by_sortie,participation=get_eve_by_musicien(current_user.idMusicien),sondage_rep=get_sondage_by_musicien(current_user.idMusicien),erreur=erreur,p_r=participer_repetition,p_s=participer_sortie,isinstance=isinstance,get_sondage_by_repetition=get_sondage_by_repetition,get_repetition_by_id=get_repetition_by_idRep)
    return redirect(url_for("login"))

@app.route('/update_temps<idSondage>')
def update_temps(idSondage:Sondage.idSondage):
    new_content = get_sondage_by_id(idSondage).temps_restant()
    return jsonify({'content': new_content})



def is_valid_email(email):
    try:
        # Vérifie si l'adresse e-mail a le bon format
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False

def is_valid_age(age):
    try:
        # Vérifie si l'âge est un nombre entre 18 et 100
        age = int(age)
        return 18 <= age <= 100
    except ValueError:
        return False

   

@app.route("/rep_ajoute/" , methods=["GET", "POST"])
def ajoute_rep():
    date_str=request.form.get("date")
    if date_str=="":
        return page_sondage(erreur=True)
    
    date=date_str.split("T")[0]+" "+date_str.split("T")[1]+":00"

    date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    r=Repetition(idRepetition=get_max_id_repetition()+1,
                dateRepetition=date,
                dureeRepetition=1,
                lieu="test",
                tenue="test")
    db.session.add(r)
    db.session.commit()
    return redirect(url_for("page_sondage"))


@app.route("/valid_sondage/", methods=["POST","GET"])
def validation_sondage():
    if len(request.form)==0:
        return redirect(url_for("page_sondage"))
    id=int(request.form.get("idsondage"))
    if request.form.get("choix"+str(id))=="True":
        reponse=True
    else:
        reponse=False
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if get_sondage_by_id(id).idRepetition is None:
        rs=participer_sortie(idSortie=get_sondage_by_id(id).idSortie,
                            idMusicien=current_user.idMusicien,
                            dateReponse=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
                            presence=reponse)
    if get_sondage_by_id(id).idSortie is None:
        rs=participer_repetition(idRepetition=get_sondage_by_id(id).idRepetition,
                            idMusicien=current_user.idMusicien,
                            dateReponse=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
                            presence=reponse)
    db.session.add(rs)
    db.session.commit()
    return page_sondage()

@app.route("/annuler_sondage/", methods=["POST","GET"])
def annuler_sondage():
    if len(request.form)==0:
        return redirect(url_for("page_sondage"))
    id=int(request.form.get("idsondage"))
    if get_sondage_by_id(id).idRepetition is None:
        rs=participer_sortie.query.filter_by(idSortie=get_sondage_by_id(id).idSortie,idMusicien=current_user.idMusicien).first()
    if get_sondage_by_id(id).idSortie is None:
        rs=participer_repetition.query.filter_by(idRepetition=get_sondage_by_id(id).idRepetition,idMusicien=current_user.idMusicien).first()
    db.session.delete(rs)
    db.session.commit()
    return page_sondage()



# class AuthorForm(FlaskForm):
#     id = HiddenField('id')
#     name = StringField('Nom', validators=[DataRequired()]) # Doit obligatoirement remplir le champs 
 
class RegistrationForm(FlaskForm):
    nomMusicien = StringField('Nom')
    prenomMusicien = StringField('Prénom')
    telephone = StringField('Télephone')
    adresseMail = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe')
    confirm_password = PasswordField('Confirmer le mot de passe')
    ageMusicien = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])    
    isAdmin = BooleanField('Admin')  # Ajout du champ pour la case à cocher
    next = HiddenField()

    def validate(self):
        """Vérifie si le formulaire est valide

        Returns:
            bool: True si le formulaire est valide
        """
        # Vérifier si le mot de passe est correct
        if self.password.data != self.confirm_password.data:
            self.password.errors += ("Les mots de passe ne correspondent pas.",)
            return False
        
        if not is_valid_email(self.adresseMail.data):
            self.adresseMail.errors += ("adresse mail non valide.",)
            return False

        if not is_valid_age(request.form.get('age')):
            self.ageMusicien.errors += ("L\'âge doit être un nombre entre 18 et 100 ans.",)
            return False

        # Vérifier si l'utilisateur existe déjà
        nom = self.nomMusicien.data
        prenom = self.prenomMusicien.data
        username = f"{nom}.{prenom}"
        if Musicien.query.filter_by(nomMusicien=nom, prenomMusicien=prenom).first() is not None:
            self.nomMusicien.errors += ("Un utilisateur avec ce nom et prénom existe déjà.",)
            return False
        return True


@app.route("/register/", methods=["GET", "POST"])
def register():
    # if not current_user.is_authenticated:
    #     return redirect(url_for("login"))

    # if not current_user.admin:
    #     return render_template('error_pages.html'), 403
    
    form = RegistrationForm()

    if request.method == "POST" and form.validate():
        # Récupérer les données du formulaire
        nom = form.nomMusicien.data
        prenom = form.prenomMusicien.data
        telephone = form.telephone.data
        adresseMail = form.adresseMail.data
        password = form.password.data
        ageMusicien = request.form.get('age')
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
            ageMusicien=int(ageMusicien),
            adresseMail=adresseMail,
            telephone=telephone,
            admin=admin,
            img=None
        )
        db.session.add(user)
        db.session.commit()

        # Rediriger l'utilisateur vers une page de confirmation ou de connexion
        return redirect(url_for("home"))

    return render_template("register.html", form=form)


@app.route("/profil/")
@login_required
def profil():
    """Profil

    Returns:
        html: page de profile
    """
    form = maj_profile()
    return render_template("profil.html", form=form)

@app.route("/logout/")
def logout():
    """Logout
    Returns:
        html: page de home
    """
    logout_user()
    return redirect(url_for("home"))


class maj_profile(FlaskForm):
    nomMusicien = StringField('Nom')
    prenomMusicien = StringField('Prénom')
    telephone = StringField('Télephone')
    adresseMail = EmailField('Email', validators=[DataRequired(), Email()])
    ageMusicien = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])    
    isAdmin = BooleanField('Admin')  

    def validate(self):
        """Vérifie si le formulaire est valide

        Returns:
            bool: True si le formulaire est valide
        """
        if not is_valid_email(self.adresseMail.data):
            self.adresseMail.errors += ("adresse mail non valide.",)
            return False

        if not is_valid_age(request.form.get('ageMusicien')):
            self.ageMusicien.errors += ("L\'âge doit être un nombre entre 18 et 100 ans.",)
            return False

        # Vérifier si l'utilisateur existe déjà
        nom = self.nomMusicien.data
        prenom = self.prenomMusicien.data
        id  = current_user.idMusicien
        username = f"{nom}.{prenom}"
        # verifie si le nom et le prenom existe deja
        m=Musicien.query.filter_by(nomMusicien=nom, prenomMusicien=prenom).first()
        if m is not None and id != m.idMusicien  :
            self.nomMusicien.errors += ("Un utilisateur avec ce nom et prénom existe déjà.",)
            return False
        return True




@app.route("/maj_profil/", methods=["GET", "POST"])
@login_required  # Assurez-vous que l'utilisateur est authentifié
def maj_profil():
    form = maj_profile()
    print("test")
    if request.method == "POST" and form.validate():
        print(request.form)
        # Récupérer les données du formulaire
        nom = form.nomMusicien.data
        prenom = form.prenomMusicien.data
        telephone = form.telephone.data
        adresseMail = form.adresseMail.data
        age = request.form.get('ageMusicien') # Ajout de l'âge
        admin = current_user.admin

        # Mettez à jour l'utilisateur actuel
        current_user.nomMusicien = nom
        current_user.prenomMusicien = prenom
        current_user.telephone = telephone
        current_user.adresseMail = adresseMail
        current_user.ageMusicien = age
        current_user.admin = admin


        # Enregistrez les modifications dans la base de données
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("profil.html", form=form)



@app.route("/crea_sortie/", methods=["GET", "POST"])
def crea_sortie(erreur=False):
    date=datetime.now().strftime("%Y-%m-%dT%H:%M")
    print(erreur)
    return render_template("crea_sortie.html" ,date=date , erreur=erreur )

@app.route("/save_sortie/", methods=["GET", "POST"])
def save_sortie():
    date_str=request.form.get("date")
    if date_str=="" or request.form.get("lieu")=="" or request.form.get("type")=="" or request.form.get("tenue")=="" or request.form.get("duree")=="":
        return crea_sortie(erreur=True)
    
    date=date_str.split("T")[0]+" "+date_str.split("T")[1]+":00"

    date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    s=Sortie(idSortie=get_max_id_sortie()+1,
                dateSortie=date,
                dureeSortie=int(request.form.get("duree")),
                lieu=request.form.get("lieu"),
                type=request.form.get("type"),  
                tenue=request.form.get("tenue"))
    sondage=Sondage(idSondage=get_max_id_sondage()+1,
                    idSortie=s.idSortie,
                    idRepetition=None,
                    message="sortie à "+request.form.get("lieu"),
                    dateSondage=datetime.now(),
                    dureeSondage=int(request.form.get("duree")))
    db.session.add(s)
    db.session.add(sondage)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/crea_repetition/", methods=["GET", "POST"])
def crea_repetition(erreur=False):
    date=datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template("crea_repetition.html",date=date , erreur=erreur )

@app.route("/save_repetition/", methods=["GET", "POST"])
def save_repetition():
    date_str=request.form.get("date")
    if date_str=="" or request.form.get("lieu")=="" or request.form.get("tenue")=="" or request.form.get("duree")=="":
        return crea_repetition(erreur=True)
    
    date=date_str.split("T")[0]+" "+date_str.split("T")[1]+":00"

    date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    r=Repetition(idRepetition=get_max_id_repetition()+1,
                dateRepetition=date,
                dureeRepetition=int(request.form.get("duree")),
                lieu=request.form.get("lieu"),
                tenue=request.form.get("tenue"))
    sondage=Sondage(idSondage=get_max_id_sondage()+1,
                    idSortie=None,
                    idRepetition=r.idRepetition,
                    message="repetition à "+request.form.get("lieu"),
                    dateSondage=datetime.now(),
                    dureeSondage=int(request.form.get("duree")))
    db.session.add(r)
    db.session.add(sondage)
    db.session.commit()
    return redirect(url_for("home"))