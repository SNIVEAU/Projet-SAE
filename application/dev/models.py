from .app import db
from flask_login import UserMixin
from .app import db, login_manager
from datetime import *


class Musicien(db.Model, UserMixin):
    idMusicien = db.Column(db.Integer, primary_key=True)
    nomMusicien = db.Column(db.String(50))
    prenomMusicien = db.Column(db.String(50))
    password = db.Column(db.String(50))
    ageMusicien = db.Column(db.Integer)
    adressseMail = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    img = db.Column(db.String(50))

    def get_id(self):
        return self.idMusicien

    def __repr__(self) -> str:
        return self.nomMusicien + " " + self.prenomMusicien
    def get_id(self):
        return self.idMusicien
    def generate_username(self):
        return f"{self.nomMusicien}.{self.prenomMusicien}"

def get_max_idMusicient():
    return Musicien.query.order_by(Musicien.idMusicien.desc()).first().idMusicien
    

@login_manager.user_loader
def load_user(user_id):
    return Musicien.query.get(int(user_id))

def get_musicien()->list:
    return Musicien.query.all()

def get_musicien_by_id(id)->Musicien:
    return Musicien.query.filter_by(idMusicien=id).first()

class Repetition(db.Model):
    idRepetition = db.Column(db.Integer, primary_key=True)
    dateRepetition = db.Column(db.DateTime)
    dureeRepetition = db.Column(db.Integer)
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        return self.dateRepetition+" "+self.dureeRepetition+" "+self.idRepetition
    
def get_repetitions()->list:
    return Repetition.query.all()

def get_repetition_by_idRep(id)->Repetition:
    return Repetition.query.filter_by(idRepetition=id).first()

class Sortie(db.Model):
    idSortie = db.Column(db.Integer, primary_key=True)
    dateSortie = db.Column(db.DateTime)
    dureeSortie = db.Column(db.Integer)
    description = db.Column(db.String(100))
    lieu = db.Column(db.String(50))
    type= db.Column(db.String(50))
    tenue = db.Column(db.String(50))
    def __repr__(self) -> str:
        return str(self.dateSortie)+" "+str(self.dureeSortie)+" "+str(self.idSortie)
    
def get_sorties()->list:
    return Sortie.query.all()

def get_sortie_by_id(id)->Sortie:
    return Sortie.query.filter_by(idSortie=id).first()

def get_max_id_sortie()->int:
    if Sortie.query.count()==0:
        return 0
    return Sortie.query.order_by(Sortie.idSortie.desc()).first().idSortie

class Sondage(db.Model):
    idSondage = db.Column(db.Integer, primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'))
    message = db.Column(db.String(100))
    dateSondage = db.Column(db.DateTime)
    dureeSondage = db.Column(db.Integer)

    def get_sortie(self)->Sortie:
        return Sortie.query.filter_by(idSortie=self.idSortie).first()
    
    def temps_restant(self)->(int,int,int):
        """Retourne le temps restant avant la fin du sondage"""
        temps_second=self.dureeSondage*3600*24
        jour = (self.dureeSondage - (datetime.now() - self.dateSondage).days)
        heure = (temps_second - (datetime.now() - self.dateSondage).seconds)//3600%24
        minute = (temps_second - (datetime.now() - self.dateSondage).seconds)//60%60
        seconde = (temps_second - (datetime.now() - self.dateSondage).seconds)%60
        return jour,heure,minute,seconde

    def __repr__(self) -> str:
        return str(self.dateSondage)+" "+str(self.dureeSondage)+" "+str(self.idSondage)

def get_sondages()->list:
    return Sondage.query.all()

def get_max_id_sondage()->int:
    if Sondage.query.count()==0:
        return 0
    return Sondage.query.order_by(Sondage.idSondage.desc()).first().idSondage

def get_sondage_by_id(id)->Sondage:
    return Sondage.query.filter_by(idSondage=id).first()

def get_sondage_by_sortie(id)->Sondage:
    return Sondage.query.filter_by(idSortie=id).first()

def get_sondage_by_musicien(id)->Sondage:
    participation=[]
    sondages=[]
    for sorti in get_sortie_by_musicien(id):
        participation.append(get_sondage_by_id(sorti.idSortie))
    for part in participation:
        for sondage in get_sondage_by_sortie(part.idSortie):
            sondages.append(sondage)
    return sondages

class participer_repetition(db.Model):
    idMusicien = db.Column(db.Integer, db.ForeignKey('musicien.idMusicien'), primary_key=True)
    idRepetition = db.Column(db.Integer, db.ForeignKey('repetition.idRepetition'), primary_key=True)
    

    def __repr__(self) -> str:
        return self.idMusicien+" "+self.idRepetition
def get_participer_repetitions()->list:
    return participer_repetition.query.all()

def get_musicien_by_repetition(id)->list:
    return participer_repetition.query.filter_by(idRepetition=id).all()
def get_repetition_by_musicien(id)->list:
    return participer_repetition.query.filter_by(idMusicien=id)
class participer_sortie(db.Model):
    idMusicien = db.Column(db.Integer, db.ForeignKey('musicien.idMusicien'), primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'), primary_key=True)

    def get_sortie(self)->Sortie:
        return Sortie.query.filter_by(idSortie=self.idSortie).first()

    def __repr__(self) -> str:
        return self.idMusicien+" "+self.idSortie
    
def get_participer_sorties()->list:
    return participer_sortie.query.all()

def get_sortie_by_musicien(id)->list:
    return participer_sortie.query.filter_by(idMusicien=id).all()

def get_musicien_by_sortie(id)->list:
    return participer_sortie.query.filter_by(idSortie=id).all()

class Demi_journee(db.Model):
    date = db.Column(db.Date,primary_key=True)

def get_demi_journees()->list:
    return Demi_journee.query.all()
    
class disponibilite(db.Model):
    idMusicien = db.Column(db.Integer,db.ForeignKey('musicien.idMusicien'),primary_key=True)
    date = db.Column(db.Date,db.ForeignKey('demi_journee.date'),primary_key=True)

def get_disponibilites()->list:
    return disponibilite.query.all()

def get_disponibilite_by_musicien(id)->list:
    return disponibilite.query.filter_by(idMusicien=id).all()