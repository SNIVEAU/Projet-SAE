from .app import db
from flask_login import UserMixin
from .app import db, login_manager
from datetime import *


class Musicien(db.Model, UserMixin):
    """Classe Musicien"""
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
        """Retourne l'id du musicien
        Return:
            int : id du musicien"""
        return self.idMusicien

    def __repr__(self) -> str:
        """Retourne le nom et le prénom du musicien
        Return:
            str : nom et prénom du musicien"""
        return self.nomMusicien + " " + self.prenomMusicien
    
    def generate_username(self):
        """Retourne le nom et le prénom du musicien
        Return:
            str : nom et prénom du musicien"""
        return f"{self.nomMusicien}.{self.prenomMusicien}"

def get_max_idMusicient():
    """Retourne l'id du dernier musicien enregistré dans la base de données
    Return:
        int : id du dernier musicien enregistré dans la base de données"""
    if Musicien.query.count()==0:
        return 0
    return Musicien.query.order_by(Musicien.idMusicien.desc()).first().idMusicien

def get_musicien()->list:
    """Retourne la liste des musiciens
    Return:
        list : liste des musiciens"""
    return Musicien.query.all()

def get_musicien_by_id(id)->Musicien:
    """Retourne le musicien dont l'id est passé en paramètre
    Args:
        id (int): id du musicien
    Return:
        Musicien : musicien dont l'id est passé en paramètre"""
    return Musicien.query.filter_by(idMusicien=id).first()

class Repetition(db.Model):
    """Classe Repetition"""
    idRepetition = db.Column(db.Integer, primary_key=True)
    dateRepetition = db.Column(db.DateTime)
    dureeRepetition = db.Column(db.Integer)
    lieu = db.Column(db.String(50))
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        """Retourne la date, la durée et l'id de la répétition
        Return:
            str : date, durée et id de la répétition"""
        return self.dateRepetition+" "+self.dureeRepetition+" "+self.idRepetition
    
def get_repetitions()->list:
    """Retourne la liste des répétitions
    Return:
        list : liste des répétitions"""
    return Repetition.query.all()

def get_repetition_by_idRep(id)->Repetition:
    """Retourne la répétition dont l'id est passé en paramètre
    Args:
        id (int): id de la répétition
    Return:
        Repetition : répétition dont l'id est passé en paramètre"""
    return Repetition.query.filter_by(idRepetition=id).first()

class Sortie(db.Model):
    """Classe Sortie"""
    idSortie = db.Column(db.Integer, primary_key=True)
    dateSortie = db.Column(db.DateTime)
    dureeSortie = db.Column(db.Integer)
    description = db.Column(db.String(100))
    lieu = db.Column(db.String(50))
    type= db.Column(db.String(50))
    tenue = db.Column(db.String(50))
    def __repr__(self) -> str:
        """Retourne la date, la durée et l'id de la sortie
        Return:
            str : date, durée et id de la sortie"""
        return str(self.dateSortie)+" "+str(self.dureeSortie)+" "+str(self.idSortie)
    
    def to_dict(self)->dict:
        return {"idSortie":self.idSortie,"dateSortie":self.dateSortie,"dureeSortie":self.dureeSortie,"description":self.description,"lieu":self.lieu,"type":self.type,"tenue":self.tenue}
    
def get_sorties()->list:
    """Retourne la liste des sorties
    Return:
        list : liste des sorties"""
    return Sortie.query.all()

def get_sortie_by_id(id)->Sortie:
    """Retourne la sortie dont l'id est passé en paramètre
    Args:
        id (int): id de la sortie
    Return:
        Sortie : sortie dont l'id est passé en paramètre"""
    return Sortie.query.filter_by(idSortie=id).first()

def get_max_id_sortie()->int:
    """Retourne l'id de la dernière sortie enregistrée dans la base de données
    Return:
        int : id de la dernière sortie enregistrée dans la base de données"""
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
    """Classe Sondage"""
    idSondage = db.Column(db.Integer, primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'))
    idRepetition = db.Column(db.Integer, db.ForeignKey('repetition.idRepetition'))
    message = db.Column(db.String(100))
    dateSondage = db.Column(db.DateTime)
    dureeSondage = db.Column(db.Integer)

    def get_sortie(self)->Sortie:
        """Retourne la sortie associée au sondage
        Return:
            Sortie : sortie associée au sondage"""
        return Sortie.query.filter_by(idSortie=self.idSortie).first()
    
    def temps_restant(self)->(int,int,int):
        """Retourne le temps restant avant la fin du sondage
        Return:
            int : nombre de jours restants
            int : nombre d'heures restantes
            int : nombre de minutes restantes
            int : nombre de secondes restantes
        """
        temps_second=self.dureeSondage*3600*24
        jour = ((datetime.now() - self.dateSondage).days)
        print((datetime.now() - self.dateSondage).days)
        heure = (temps_second - (datetime.now() - self.dateSondage).seconds)//3600%24
        minute = (temps_second - (datetime.now() - self.dateSondage).seconds)//60%60
        seconde = (temps_second - (datetime.now() - self.dateSondage).seconds)%60
        return f"{jour}j {heure}H {minute}m {seconde}s"

    def __repr__(self) -> str:
        """Retourne la date, la durée et l'id du sondage
        Return:
            str : date, durée et id du sondage"""
        return str(self.dateSondage)+" "+str(self.dureeSondage)+" "+str(self.idSondage)

def get_sondages()->list:
    """Retourne la liste des sondages
    Return:
        list : liste des sondages"""
    return Sondage.query.all()

def get_max_id_sondage()->int:
    """Retourne l'id du dernier sondage enregistré dans la base de données
    Return:
        int : id du dernier sondage enregistré dans la base de données"""
    if Sondage.query.count()==0:
        return 0
    return Sondage.query.order_by(Sondage.idSondage.desc()).first().idSondage

def get_sondage_by_id(id)->Sondage:
    """Retourne le sondage dont l'id est passé en paramètre
    Args:
        id (int): id du sondage
    Return:
        Sondage : sondage dont l'id est passé en paramètre"""
    return Sondage.query.filter_by(idSondage=id).first()

def get_sondage_non_rep(idMusicien)->list:
    """Retourne la liste des sondages auxquels le musicien n'a pas encore répondu
    Args:
        idMusicien (int): id du musicien
    Return:
        list : liste des sondages auxquels le musicien n'a pas encore répondu"""
    sondages=get_sondages()
    participations=get_sondage_by_musicien(idMusicien)
    s=[]
    for sondage in sondages:
        if sondage not in participations:
            s.append(sondage) 
    print(sondages)  
    return s

def get_sondage_by_sortie(id)->Sondage:
    """Retourne le sondage associé à la sortie dont l'id est passé en paramètre
    Args:
        id (int): id de la sortie
    Return:
        Sondage : sondage associé à la sortie dont l'id est passé en paramètre"""
    return Sondage.query.filter_by(idSortie=id).first()

def get_sondage_by_repetition(id)->Sondage:
    return Sondage.query.filter_by(idRepetition=id).first()

def get_sortie_by_musicien(id)->list:
    return participer_sortie.query.filter_by(idMusicien=id).all()

def get_sondage_by_musicien(id)->list:
    """Retourne la liste des sondages auxquels le musicien a répondu
    Args:
        id (int): id du musicien
    Return:
        list : liste des sondages auxquels le musicien a répondu"""
    participation=[]
    sondages=[]
    for sorti in get_sortie_by_musicien(id):
        participation.append(get_sondage_by_sortie(sorti.idSortie))
    for repet in get_repetition_by_musicien(id):
        participation.append(get_sondage_by_repetition(repet.idRepetition))
    for part in participation:
        sondages.append(get_sondage_by_sortie(part.idSortie))
        sondages.append(get_sondage_by_repetition(part.idRepetition))
    return sondages

class participer_repetition(db.Model):
    """Classe participer_repetition"""
    idMusicien = db.Column(db.Integer, db.ForeignKey('musicien.idMusicien'), primary_key=True)
    idRepetition = db.Column(db.Integer, db.ForeignKey('repetition.idRepetition'), primary_key=True)
    dateReponse = db.Column(db.DateTime)
    presence = db.Column(db.Boolean)
    
    def __repr__(self) -> str:
        """Retourne l'id du musicien et l'id de la répétition
        Return:
            str : id du musicien et id de la répétition
        """
        return self.idMusicien+" "+self.idRepetition
    
    def get_repetition(self)->Repetition:
        return Repetition.query.filter_by(idRepetition=self.idRepetition).first()
    
def get_participer_repetitions()->list:
    """Retourne la liste des participations aux répétitions
    Return:
        list : liste des participations aux répétitions"""
    return participer_repetition.query.all()

def get_musicien_by_repetition(id)->list:
    """Retourne la liste des musiciens participant à la répétition dont l'id est passé en paramètre
    Args:
        id (int): id de la répétition
    Return:
        list : liste des musiciens participant à la répétition dont l'id est passé en paramètre"""
    return participer_repetition.query.filter_by(idRepetition=id).all()

def get_repetition_by_musicien(id)->list:
    """Retourne la liste des répétitions auxquelles le musicien participe
    Args:
        id (int): id du musicien
    Return:
        list : liste des répétitions auxquelles le musicien participe"""
    return participer_repetition.query.filter_by(idMusicien=id)

class participer_sortie(db.Model):
    """Classe participer_sortie"""
    idMusicien = db.Column(db.Integer, db.ForeignKey('musicien.idMusicien'), primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'), primary_key=True)
    dateReponse = db.Column(db.DateTime)
    presence = db.Column(db.Boolean)

    def get_sortie(self)->Sortie:
        """Retourne la sortie associée à la participation
        Return:
            Sortie : sortie associée à la participation"""
        return Sortie.query.filter_by(idSortie=self.idSortie).first()

    def __repr__(self) -> str:
        """Retourne l'id du musicien et l'id de la sortie
        Return:
            str : id du musicien et id de la sortie"""
        return str(self.idMusicien)+" "+str(self.idSortie)
    
def get_participer_sorties()->list:
    """Retourne la liste des participations aux sorties
    Return:
        list : liste des participations aux sorties"""
    return participer_sortie.query.all()

def get_eve_by_musicien(id)->list:
    return participer_sortie.query.filter_by(idMusicien=id).all()+participer_repetition.query.filter_by(idMusicien=id).all()

def get_musicien_by_sortie(id)->list:
    """Retourne la liste des musiciens participant à la sortie dont l'id est passé en paramètre
    Args:
        id (int): id de la sortie
    Return:
        list : liste des musiciens participant à la sortie dont l'id est passé en paramètre"""
    return participer_sortie.query.filter_by(idSortie=id).all()

class Demi_journee(db.Model):
    """Classe Demi_journee"""
    date = db.Column(db.Date,primary_key=True)

def get_demi_journees()->list:
    """Retourne la liste des demi-journées
    Return:
        list : liste des demi-journées"""
    return Demi_journee.query.all()
    
class disponibilite(db.Model):
    """Classe disponibilite"""
    idMusicien = db.Column(db.Integer,db.ForeignKey('musicien.idMusicien'),primary_key=True)
    date = db.Column(db.Date,db.ForeignKey('demi_journee.date'),primary_key=True)

def get_disponibilites()->list:
    """Retourne la liste des disponibilités
    Return:
        list : liste des disponibilités"""
    return disponibilite.query.all()

def get_disponibilite_by_musicien(id)->list:
    """Retourne la liste des disponibilités du musicien dont l'id est passé en paramètre
    Args:
        id (int): id du musicien
    Return:
        list : liste des disponibilités du musicien"""
    return disponibilite.query.filter_by(idMusicien=id).all()

def get_max_id_repetition()->int:
    if Repetition.query.count()==0:
        return 0
    return Repetition.query.order_by(Repetition.idRepetition.desc()).first().idRepetition

