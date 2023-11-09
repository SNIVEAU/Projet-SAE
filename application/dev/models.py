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
    adresseMail = db.Column(db.String(50))
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
    if Musicien.query.count()==0:
        return 0
    return Musicien.query.order_by(Musicien.idMusicien.desc()).first().idMusicien

def get_musicien()->list:
    return Musicien.query.all()

def get_musicien_by_id(id)->Musicien:
    return Musicien.query.filter_by(idMusicien=id).first()

class Repetition(db.Model):
    idRepetition = db.Column(db.Integer, primary_key=True)
    dateRepetition = db.Column(db.DateTime)
    dureeRepetition = db.Column(db.Integer)
    lieu = db.Column(db.String(50))
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        return str(self.dateRepetition)+" "+str(self.dureeRepetition)+" "+str(self.idRepetition)
    
    def to_dict(self)->dict:
        return {"idRepetition":self.idRepetition,"dateRepetition":self.dateRepetition,"dureeRepetition":self.dureeRepetition,"lieu":self.lieu,"tenue":self.tenue}
    
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
    
    def to_dict(self)->dict:
        return {"idSortie":self.idSortie,"dateSortie":self.dateSortie,"dureeSortie":self.dureeSortie,"description":self.description,"lieu":self.lieu,"type":self.type,"tenue":self.tenue}
    
def get_sorties()->list:
    return Sortie.query.all()

def get_sortie_by_id(id)->Sortie:
    return Sortie.query.filter_by(idSortie=id).first()

def get_max_id_sortie()->int:
    if Sortie.query.count()==0:
        return 0
    return Sortie.query.order_by(Sortie.idSortie.desc()).first().idSortie


def get_eve_by_mois(mois)->list:
    eve={}
    for sortie in get_sorties():
        if sortie.dateSortie.month==mois:
            eve[str(sortie.dateSortie.day)]=[sortie.idSortie]
            eve[str(sortie.dateSortie.day)].append(None)
    keys=eve.keys()
    for repetition in get_repetitions():
        if repetition.dateRepetition.month==mois:
            if str(repetition.dateRepetition.day) in keys:
                eve[str(repetition.dateRepetition.day)].pop()
                eve[str(repetition.dateRepetition.day)].append(repetition.idRepetition)
            else:
                eve[str(repetition.dateRepetition.day)]=[None]
                eve[str(repetition.dateRepetition.day)].append(repetition.idRepetition)
    keys=eve.keys()
    cle_trier=sorted(keys)
    eve_trier={}
    for cle in cle_trier:
        eve_trier[cle]=eve[cle]
    return eve_trier

def get_val_dico_mois(num_jour)->Sortie:
    dict=get_eve_by_mois(datetime.now().month)
    if str(num_jour) not in dict.keys():
        return None
    return dict[str(num_jour)]

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
        jour = ((datetime.now() - self.dateSondage).days)
        print((datetime.now() - self.dateSondage).days)
        heure = (temps_second - (datetime.now() - self.dateSondage).seconds)//3600%24
        minute = (temps_second - (datetime.now() - self.dateSondage).seconds)//60%60
        seconde = (temps_second - (datetime.now() - self.dateSondage).seconds)%60
        return f"{jour}j {heure}H {minute}m {seconde}s"

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

def get_sondage_non_rep(idMusicien)->list:
    sondages=get_sondages()
    participations=get_sondage_by_musicien(idMusicien)
    s=[]
    for sondage in sondages:
        if sondage not in participations:
            s.append(sondage) 
    print(sondages)  
    return s

def get_sondage_by_sortie(id)->Sondage:
    return Sondage.query.filter_by(idSortie=id).first()

def get_sondage_by_musicien(id)->list:
    participation=[]
    sondages=[]
    for sorti in get_sortie_by_musicien(id):
        participation.append(get_sondage_by_id(sorti.idSortie))
    for part in participation:
        sondages.append(get_sondage_by_sortie(part.idSortie))
    return sondages

class participer_repetition(db.Model):
    idMusicien = db.Column(db.Integer, db.ForeignKey('musicien.idMusicien'), primary_key=True)
    idRepetition = db.Column(db.Integer, db.ForeignKey('repetition.idRepetition'), primary_key=True)
    dateReponse = db.Column(db.DateTime)
    presence = db.Column(db.Boolean)
    
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
    dateReponse = db.Column(db.DateTime)
    presence = db.Column(db.Boolean)

    def get_sortie(self)->Sortie:
        return Sortie.query.filter_by(idSortie=self.idSortie).first()

    def __repr__(self) -> str:
        return str(self.idMusicien)+" "+str(self.idSortie)
    
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

def get_max_id_repetition()->int:
    if Repetition.query.count()==0:
        return 0
    return Repetition.query.order_by(Repetition.idRepetition.desc()).first().idRepetition