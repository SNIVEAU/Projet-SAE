from .app import *
from flask import render_template, url_for, redirect, request,jsonify
from .models import *
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField , HiddenField, PasswordField,EmailField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange
from flask_login import login_user, current_user, login_required, logout_user
from hashlib import sha256
import plotly.graph_objs as go
import calendar
import email_validator

MOIS=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']


@login_manager.user_loader
def load_user(user_id):
    """Charger l'utilisateur actuel
    Args:
        user_id (int): id de l'utilisateur
    Returns:
        user: l'utilisateur actuel"""
    return Musicien.query.get(user_id)

@app.route("/")
def home():
    """home page
    Returns:
        html: home page"""
    musiciens = Musicien.query.all()
    return render_template("home.html", musiciens=musiciens)

@app.route("/calendrier", methods=["GET"])
def calendrier():
    if current_user.is_authenticated:
        print("ydgyfseubfuhesbfiesbifjbsejifbjsbvjbdsbfjsbjifbsjbfjdsbf")
        num_mois=datetime.now().month
        moisActuelle=datetime.now().month
        if request.args.get("mois")!=None:
            if(int(request.args.get("mois"))>0 and int(request.args.get("mois"))<13):
                num_mois=int(request.args.get("mois"))
        c=calendar.HTMLCalendar(firstweekday=0)
        c.cssclasses_weekday_head=["jour", "jour", "jour", "jour", "jour", "jour", "jour"]
        c.cssclass_month_head="mois"
        num_day=datetime.now().day
        mois=MOIS[num_mois-1]+" "+str(datetime.now().year)
        return render_template("calendrier.html",moisActuelle=moisActuelle,numMois=num_mois,get_sortie_by_id=get_sortie_by_id,calendrier=c.formatmonth(datetime.now().year,num_mois),num_day=num_day, mois=mois,dispo = get_disponibilite_by_musicien(current_user.idMusicien),dispo_musicien = get_disponibilites())
    return redirect(url_for("login"))


@app.route('/get_val_dico_mois/<day>/<month>')
def get_val_dico_mois_route(day,month):
    result = get_val_dico_mois(day,month)
    if result is None:
        return jsonify({})
    dict={}
    for i in range(len(result)):
        if i==0 and result[i] is not None:
            dict["sortie"]=result[i]
        if i==1 and result[i] is not None:
            dict["repetition"]=result[i]
    return jsonify(dict)


@app.route("/sortie/<idSortie>")
def sortie(idSortie):
    sortie = get_sortie_by_id(idSortie)
    print(get_musicien_by_sortie(idSortie))
    liste_musicien = []
    for i in get_musicien_by_sortie(idSortie):
        liste_musicien.append(get_musicien_by_id(i.idMusicien))
    return render_template("sortie.html", sortie=sortie,participation=liste_musicien)
@app.route("/repetition/<idRepetition>")
def repetition(idRepetition):
    rep = get_repetition_by_idRep(idRepetition)
    liste_musicien = []
    for i in get_musicien_by_repetition(idRepetition):
        liste_musicien.append(get_musicien_by_id(i.idMusicien))
    return render_template("repetition.html", rep=rep,participation=liste_musicien)

class LoginForm(FlaskForm):
    """Formulaire de connexion
    Attributes:
        nomMusicien (StringField): Nom de l'utilisateur
        prenomMusicien (StringField): Prénom de l'utilisateur
        password (PasswordField): Mot de passe de l'utilisateur
        next (HiddenField): Page suivante"""
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

        # Vérifier si l'utilisateur existe
        musicien = Musicien.query.filter_by(nomMusicien=nom, prenomMusicien=prenom).first()
        if musicien is None:
            return None
        
        # Vérifier si le mot de passe est correct
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return musicien if passwd == musicien.password else None

@app.route("/login/", methods=["GET", "POST"])
def login():
    """Login page
    Returns:
        html: login page
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
            f.password.errors += ("Nom d'utilisateur ou mot de passe incorrect",)
    return render_template("login.html", form=f)


@app.route("/logout/")
def logout():
    """Logout
    Returns:
        html: home page
    """
    logout_user()
    return redirect(url_for("home"))

def is_valid_email(email):
    """Vérifie si l'adresse e-mail est valide
    Returns:
        bool: True si l'adresse e-mail est valide"""
    try:
        # Vérifie si l'adresse e-mail a le bon format
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False

def is_valid_age(age):
    """Vérifie si l'âge est valide
    Returns:
        bool: True si l'âge est valide"""
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
    """Valider un sondage
    Returns:
        html: page de sondage
    """
    if len(request.form)==0:
        return redirect(url_for("page_sondage"))
    id=int(request.form.get("idsondage"))
    if request.form.get("choix"+str(id))=="True":
        reponse=True
    else:
        reponse=False
    idMusicien=current_user.idMusicien
    if(request.form.get("idMusicien")!=None):
        idMusicien=int(request.form.get("idMusicien"))
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if get_sondage_by_id(id).idRepetition!=None:
        rs=participer_repetition(idRepetition=get_sondage_by_id(id).idRepetition,
                            idMusicien=idMusicien,
                            dateReponse=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
                            presence=reponse)
    elif get_sondage_by_id(id).idSortie!=None:
        rs=participer_sortie(idSortie=get_sondage_by_id(id).idSortie,
                            idMusicien=idMusicien,
                            dateReponse=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
                            presence=reponse)
    db.session.add(rs)
    db.session.commit()
    return redirect(url_for("page_sondage"))

@app.route("/annuler_sondage/", methods=["POST","GET"])
def annuler_sondage():
    if len(request.form)==0:
        return redirect(url_for("page_sondage"))
    id=int(request.form.get("idsondage"))
    idMusicien=current_user.idMusicien
    if(request.form.get("idMusicien")!=None):
        idMusicien=int(request.form.get("idMusicien"))
    if get_sondage_by_id(id).idRepetition!=None:
        rs=participer_repetition.query.filter_by(idRepetition=get_sondage_by_id(id).idRepetition,idMusicien=idMusicien).first()
    elif get_sondage_by_id(id).idSortie!=None:
        rs=participer_sortie.query.filter_by(idSortie=get_sondage_by_id(id).idSortie,idMusicien=idMusicien).first()
    else:
        rs=Reponse.query.filter_by(idQuestion=get_question_by_idSondage(id).idQuestion,idMusicien=idMusicien).first()
    db.session.delete(rs)
    db.session.commit()
    return redirect(url_for("page_sondage"))

@app.route("/ajoute_dispo/", methods=["POST","GET"])
def ajoute_dispo():
    datedebut = request.form.get("date_debut")
    datefin = request.form.get("date_fin")
    if datedebut == "" or datefin == "":
        return redirect(url_for("calendrier"))
    datedebut = datetime.strptime(datedebut, '%Y-%m-%d').date()
    datefin = datetime.strptime(datefin, '%Y-%m-%d').date()
    # on supprime les anciennes dates
    dispo = get_disponibilite_by_musicien(current_user.idMusicien)
    for d in dispo:
        if d in get_disponibilite_by_musicien(current_user.idMusicien) and d.date >= datedebut and d.date <= datefin:
            db.session.delete(d)
    db.session.commit()
    # si date debut deja passer on la met a aujourd'hui
    if datedebut < datetime.now().date():
        datedebut = datetime.now().date()
    # on ajoute les nouvelles dates
    for i in range((datefin - datedebut).days + 1):
        print(datedebut + timedelta(days=i))
        d = disponibilite(idMusicien=current_user.idMusicien, date=datedebut + timedelta(days=i))
        db.session.add(d)
    db.session.commit()
    return redirect(url_for("calendrier"))



@app.route("/supprime_dispo/<date>", methods=["POST","GET"])
def supprime_dispo(date):
    d=disponibilite.query.filter_by(idMusicien=current_user.idMusicien,date=date).first()
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for("calendrier"))




class RegistrationForm(FlaskForm):
    """Formulaire d'inscription
    Attributes:
        nomMusicien (StringField): Nom de l'utilisateur
        prenomMusicien (StringField): Prénom de l'utilisateur
        password (PasswordField): Mot de passe de l'utilisateur
        confirm_password (PasswordField): Confirmation du mot de passe de l'utilisateur
        ageMusicien (IntegerField): Age de l'utilisateur
        isAdmin (BooleanField): Admin ou non
        next (HiddenField): Page suivante"""
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
    """Register page
    Returns:
        html: register page
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if not current_user.admin:
        return render_template('error_pages.html'), 403
    
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
    liste_idtutele=tutele_by_idTuteur(current_user.idMusicien)
    liste_tutele=[]
    for id in liste_idtutele:
        liste_tutele.append(get_musicien_by_id(id.idTutele))
    all_type_instrument = get_type_instruments()
    mes_instruments = get_instruments_by_musicien(current_user.idMusicien)
    return render_template("profil.html", form=form,liste_tutele=liste_tutele, all_type_instrument=all_type_instrument, mes_instruments=mes_instruments)


class maj_profile(FlaskForm):
    """Formulaire de mise à jour du profil
    Attributes:
        nomMusicien (StringField): Nom de l'utilisateur
        prenomMusicien (StringField): Prénom de l'utilisateur
        password (PasswordField): Mot de passe de l'utilisateur
        confirm_password (PasswordField): Confirmation du mot de passe de l'utilisateur
        ageMusicien (IntegerField): Age de l'utilisateur
        isAdmin (BooleanField): Admin ou non
        next (HiddenField): Page suivante
    """
    nomMusicien = StringField('Nom')
    prenomMusicien = StringField('Prénom')
    telephone = StringField('Télephone')
    adresseMail = EmailField('Email', validators=[DataRequired(), Email()])
    ageMusicien = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])    
    isAdmin = BooleanField('Admin')
    type_instrument = StringField('Type Instrument')

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
             # verifie si le nom et le prenom existe deja
        m=Musicien.query.filter_by(nomMusicien=nom, prenomMusicien=prenom).first()
        if m is not None and id != m.idMusicien  :
            self.nomMusicien.errors += ("Un utilisateur avec ce nom et prénom existe déjà.",)
            return False
        return True


@app.route("/delete_instrument/", methods=["GET", "POST"])
def delete_instrument():
    id_instrument = request.form.get("idInstrument")
    delete_instrument_by_id = Jouer.query.filter_by(idMusicien=current_user.idMusicien,idTypeInstrument=id_instrument).first()
    db.session.delete(delete_instrument_by_id)
    db.session.commit()
    return redirect(url_for("profil"))



@app.route("/maj_profil/", methods=["GET", "POST"])
@login_required
def maj_profil():
    """Mise à jour du profil
    Returns:
        html: page de mise à jour du profil
    """
    form = maj_profile()
    if request.method == "POST" and form.validate():
        # Récupérer les données du formulaire
        nom = form.nomMusicien.data
        prenom = form.prenomMusicien.data
        telephone = form.telephone.data
        adresseMail = form.adresseMail.data
        age = request.form.get('ageMusicien')
        admin = current_user.admin
        type_instrument = request.form.get('type-instrument')


        # Mettez à jour l'utilisateur actuel
        current_user.nomMusicien = nom
        current_user.prenomMusicien = prenom
        current_user.telephone = telephone
        current_user.adresseMail = adresseMail
        current_user.ageMusicien = age
        current_user.admin = admin
        instrument = Jouer.query.filter_by(idMusicien=current_user.idMusicien,idTypeInstrument=type_instrument).first()
        if instrument is None:
            add_jouer(current_user.idMusicien, type_instrument)
        else:
            instrument.idTypeInstrument = type_instrument

        
                    
        # Enregistrez les modifications dans la base de données
        db.session.commit()

        return redirect(url_for("profil"))

    return render_template("profil.html", form=form)

@app.route("/crea_sortie/", methods=["GET", "POST"])
def crea_sortie(erreur=False):
    date=datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template("crea_sortie.html" ,date=date , erreur=erreur )

@app.route("/save_sortie/", methods=["GET", "POST"])
def save_sortie():
    date_str=request.form.get("date")
    if date_str=="" or request.form.get("lieu")=="" or request.form.get("type")=="" or request.form.get("tenue")=="" or request.form.get("duree")=="":
        return crea_sortie(erreur=True)
    
    date=date_str.split("T")[0]+" "+date_str.split("T")[1]+":00"

    date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    idSorti=get_max_id_sortie()+1
    s=Sortie(idSortie=idSorti,
                dateSortie=date,
                dureeSortie=int(request.form.get("duree")),
                lieu=request.form.get("lieu"),
                type=request.form.get("type"),  
                tenue=request.form.get("tenue")
               )

    sondage=Sondage(idSondage=get_max_id_sondage()+1,
                    idSortie=idSorti,
                    idRepetition=None,
                    message="Sortie à "+request.form.get("lieu"),
                    dateSondage=datetime.now(),
                    dureeSondage=int(request.form.get("duree")))
    date_jour=datetime.strftime(date,"%Y-%m-%d")
    date_jour=datetime.strptime(date_jour,"%Y-%m-%d").date()
    print(date_jour)
    liste_dispo=get_disponibilite_by_date(date_jour)
    print(liste_dispo)
    for dispo in liste_dispo:
        musicien=get_musicien_by_id(dispo.idMusicien)
        ps=participer_sortie(idSortie=idSorti,
                            idMusicien=musicien.idMusicien,
                            dateReponse=date,
                            presence=True)
        db.session.add(ps)
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
    if date_str=="" or request.form.get("lieu")=="" or request.form.get("tenue")=="" or request.form.get("duree")=="" or request.form.get("date")=="":
        return crea_repetition(erreur=True)
    date=date_str.split("T")[0]+" "+date_str.split("T")[1]+":00"

    date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    id_repetition=get_max_id_repetition()+1
    r=Repetition(idRepetition=id_repetition,
                dateRepetition=date,
                dureeRepetition=int(request.form.get("duree")),
                lieu=request.form.get("lieu"),
                tenue=request.form.get("tenue"))
    sondage=Sondage(idSondage=get_max_id_sondage()+1,
                    idSortie=None,
                    idRepetition=id_repetition,
                    message="repetition à "+request.form.get("lieu"),
                    dateSondage=datetime.now(),
                    dureeSondage=int(request.form.get("duree")))
    date_jour=datetime.strftime(date,"%Y-%m-%d")
    date_jour=datetime.strptime(date_jour,"%Y-%m-%d").date()
    print(date_jour)
    liste_dispo=get_disponibilite_by_date(date_jour)
    print(liste_dispo)
    for dispo in liste_dispo:
        musicien=get_musicien_by_id(dispo.idMusicien)
        pr=participer_repetition(idRepetition=id_repetition,
                            idMusicien=musicien.idMusicien,
                            dateReponse=date,
                            presence=True)
        db.session.add(pr)
    db.session.add(r)
    db.session.add(sondage)
    db.session.commit()
    return redirect(url_for("home"))
    
@app.route("/crea_sondage_standard/", methods=["GET", "POST"])
def crea_sondage_standard():
    return render_template("crea_sondage_standard.html")

@app.route("/save_sondage_standard/", methods=["GET", "POST"])
def save_sondage_standard():
    if request.form.get("intitule")=="" or request.form.get("duree")=="" or request.form.get("type_question")=="":
        return crea_sondage_standard()
    else:
        print(request.form.get("duree"))
        sondage=Sondage(idSondage=get_max_id_sondage()+1,
                        idSortie=None,
                        idRepetition=None,
                        message=request.form.get("intitule"),
                        dateSondage=datetime.now(),
                        dureeSondage=int(request.form.get("duree")))
        reponse="type:"+request.form.get("type_question")+"|"
        for i in range(1,int(request.form.get("nbreponse"))+1):
            reponse+=request.form.get("reponse"+str(i))+";"
        question=Question(idQuestion=get_max_id_question()+1,
                        idSondage=sondage.idSondage,
                        reponsesQuestion=reponse,
                        intitule=request.form.get("intitule"),
                        dateFin=datetime.now() + timedelta(days=int(request.form.get("duree"))))
        db.session.add(sondage)
        db.session.add(question)
        db.session.commit()

        return redirect(url_for("page_sondage"))
        
@app.route("/page_reponse_question/<idQuestion>", methods=["GET", "POST"])
def page_reponse_question(idQuestion):
    question=get_question_by_id(int(idQuestion))
    questions=question.reponsesQuestion.split("|")
     
    type=questions[0].split(":")[1]
    liste_reponse=questions[1].split(";")
    liste_reponse.pop()
    return render_template("page_reponse_question.html",question=question,listeReponse=liste_reponse,type=type)
    
@app.route("/save_reponse_question/", methods=["GET", "POST"])
def save_reponse_question():
    reponse_sondage=""
    questions=get_question_by_id(int(request.form.get("idQuestion"))).reponsesQuestion.split("|")
    type=questions[0].split(":")[1]
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reponse_sondage+="type:"+type+"|"
    print("test")
    if type=="radio":
        reponse_sondage+="reponse"+":"+request.form.get("reponse")
    else:
        liste_reponse=questions[1].split(";")
        liste_reponse.pop()
        for reponse in liste_reponse:
            reponse_sondage+=reponse+":"+request.form.get(reponse)+";"
    print(request.form.get("reponseSpeciale"))
    reponse=Reponse(
                    idQuestion=int(request.form.get("idQuestion")),
                    idMusicien=current_user.idMusicien,
                    reponseQuestion=reponse_sondage,
                    reponseSpeciale=request.form.get("reponseSpeciale"),
                    dateReponse=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
    db.session.add(reponse)
    db.session.commit()
    return redirect(url_for("page_sondage"))


@app.route("/stat/")
def stat():
    """Statistiques
    Returns:
        html: page de statistiques
    """
    if current_user.is_authenticated and current_user.admin:
        data = [go.Bar(x=[], y=[])]
        data2 = [go.Bar(x=[], y=[])]
        data_jour_dispo = [go.Bar(x=[], y=[])]
        data_reponse_sondage = [go.Bar(x=[], y=[])]
        mus=get_musicien()
        layout = go.Layout(title='Nombre de participation par musicien')
        layout2 = go.Layout(title='Pourcentage de participation par activité')
        layout_jour_dispo = go.Layout(title='Jour de disponibilité')
        layout_reponse = go.Layout(title="Taux de réponse à un sondage")
    
        for musicien in mus:
            data.append(go.Bar(x=[musicien.nomMusicien], y=[len(get_sortie_by_musicien(musicien.idMusicien))]))
        for sort in get_sorties():
            pourcent = len(get_musicien_by_sortie(sort.idSortie)) / len(get_musicien())*100
            data2.append(go.Bar(x=[sort.dateSortie], y=[pourcent]))
        deja_parcouru = []
        for dispo in get_disponibilites():
            if get_musicien_by_id(dispo.idMusicien).nomMusicien not in deja_parcouru:
                deja_parcouru.append(get_musicien_by_id(dispo.idMusicien).nomMusicien)
                data_jour_dispo.append(go.Bar(x=[get_musicien_by_id(dispo.idMusicien).nomMusicien], y=[len(get_disponibilite_by_musicien(dispo.idMusicien))]))
        for musicien in get_musicien():
            print(musicien.nomMusicien)
            print(len(get_sondage_by_musicien(musicien.idMusicien)))
            # get_sondage_by_musicien(musicien.idMusicien)
            data_reponse_sondage.append(go.Bar(x=[musicien.nomMusicien], y=[len(get_sondage_by_musicien(musicien.idMusicien))]))
        #  catégorie de personne présente
        #pourcentage de personne présente à une activité
        #vérifier le pourcentage de réponse à un sondage
        # graphique affichatn les jours avec le plus de disponibilité
        #pourceentage h/f
        fig = go.Figure(data=data, layout=layout)
        fig2 = go.Figure(data=data2, layout=layout2)
        fig_jour_dispo = go.Figure(data=data_jour_dispo, layout=layout_jour_dispo)
        fig_reponse = go.Figure(data=data_reponse_sondage, layout=layout_reponse)
        return render_template("stat.html",question = get_questions(),musiciens=get_musicien(),plot=fig.to_html(),pourcentage=fig2.to_html(),jour_dispo=fig_jour_dispo.to_html(),reponse=fig_reponse.to_html())
    return render_template("error_pages.html"), 403

@app.route("/sondage/", methods=["GET", "POST"])
def page_sondage(erreur=False):
    if current_user.is_authenticated:
        idMusicien=current_user.idMusicien
        if(request.form.get("idMusicienSondage")!=None):
            idMusicien=int(request.form.get("idMusicienSondage"))
        liste_idtutele=tutele_by_idTuteur(current_user.idMusicien)
        liste_tutele=[]
        for id in liste_idtutele:
            liste_tutele.append(get_musicien_by_id(id.idTutele))
        s=get_sondage_non_rep(current_user.idMusicien)
        if s is None:
            s=[]
        participation=get_sondage_by_musicien(int(idMusicien))
        return render_template("sondage.html",liste_tutele=liste_tutele,idActuelle=idMusicien,get_participation_by_musicien_and_sortie=get_participation_by_musicien_and_sortie,get_participation_by_musicien_and_repetition=get_participation_by_musicien_and_repetition,get_reponse_by_id=get_reponse_by_id,len=len,get_question_by_idSondage=get_question_by_idSondage,sondages=s,get_sortie_by_id=get_sortie_by_id,get_sondage_by_sortie=get_sondage_by_sortie,participation=participation,sondage_rep=get_sondage_by_musicien(current_user.idMusicien),erreur=erreur,p_r=participer_repetition,p_s=participer_sortie,isinstance=isinstance,get_sondage_by_repetition=get_sondage_by_repetition,get_repetition_by_id=get_repetition_by_idRep,get_question_by_id=get_question_by_id,get_sondage_by_question=get_sondage_by_question)
    return redirect(url_for("login"))

@app.route('/update_temps<idSondage>')
def update_temps(idSondage:Sondage.idSondage):
    new_content = get_sondage_by_id(idSondage).temps_restant()
    if new_content =="0j 0h 0m 0s":
        new_content="Sondage terminé"
        db.session.delete(get_sondage_by_id(idSondage))
        db.session.commit()
    return jsonify({'content': new_content})

@app.route('/Sondage/verif_reponse/<idQuestion>', methods=['GET'])
def verif_reponse(idQuestion):

    question=get_question_by_id(int(idQuestion))
    questions=question.reponsesQuestion.split("|")
    type=questions[0].split(":")[1]
    liste_reponse=questions[1].split(";")
    liste_reponse.pop()

    reponseMusicien=get_reponse_by_id(idQuestion,current_user.idMusicien).reponseQuestion.split("|")[1].split(";")
    if type!="radio":
        reponseMusicien.pop()
    for i in range(len(reponseMusicien)):
        reponseMusicien[i]=reponseMusicien[i].split(":")
    reponseSpecial=get_reponse_by_id(idQuestion,current_user.idMusicien).reponseSpeciale
    print(reponseSpecial)


    return render_template("page_verif_reponse.html",question=question,type=type,reponseMusicien=reponseMusicien,reponseSpecial=reponseSpecial)

@app.route('/Sondage/verif_toute_reponse/<idQuestion>/<idMusicien>', methods=['GET'])
def verife_reponse(idQuestion,idMusicien):
    
    question=get_question_by_id(idQuestion)
    questions=question.reponsesQuestion.split("|")
    type=questions[0].split(":")[1]
    liste_reponse=questions[1].split(";")
    liste_reponse.pop()

    reponseMusicien=get_reponse_by_id(idQuestion,idMusicien).reponseQuestion.split("|")[1].split(";")
    if type!="radio":
        reponseMusicien.pop()
    for i in range(len(reponseMusicien)):
        reponseMusicien[i]=reponseMusicien[i].split(":")
    reponseSpecial=get_reponse_by_id(idQuestion,idMusicien).reponseSpeciale
    print(reponseSpecial)


    return render_template("page_verif_reponse.html",question=question,type=type,reponseMusicien=reponseMusicien,reponseSpecial=reponseSpecial)

@app.route('/detail_question/',methods=['POST','GET'])
def detail_question():
    idQuestion = int(request.form.get("reponse"))
    question=get_question_by_id(idQuestion)
    listemusicien = []
    for rep in get_Reponse_by_idQuestion(idQuestion):
        print(rep.idMusicien)
        listemusicien.append(get_musicien_by_id(rep.idMusicien))
        print(listemusicien)
    return render_template("detail_question.html",musiciens = listemusicien,questions = question)

@app.route('/inscription_tutore',methods=["GET", "POST"])
def inscription_tutore():
    f = LoginForm()
    db.session.rollback()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            if(Tutorer.query.filter_by(idTuteur=current_user.idMusicien,idTutele=user.idMusicien).first() is None and user.idMusicien!=current_user.idMusicien):
                db.session.add(Tutorer(idTuteur=current_user.idMusicien,idTutele=user.idMusicien))
                db.session.commit()
                return redirect(url_for("profil"))
            elif(user.idMusicien==current_user.idMusicien):
                return render_template("inscription_tutore.html",form=f,Vous=True)
            else:
                return render_template("inscription_tutore.html",form=f,DejaTutorer=True)
        else:
            f.password.errors += ("Nom d'utilisateur ou mot de passe incorrect",)
    return render_template("inscription_tutore.html",form=f,DejaTutorer=False,Vous=False)

