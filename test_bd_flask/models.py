from .app import db
from sqlalchemy_imageattach import *

class Musicien(db.Model):
    idMusicien = db.Column(db.Integer, primary_key=True)
    nomMusicien = db.Column(db.String(50))
    prenomMusicien = db.Column(db.String(50))
    ageMusicien = db.Column(db.Integer)
    adresseMail = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    img = db.Column(db.String(50))  

    def __repr__(self) -> str:
        return self.nomMusicien + " " + self.prenomMusicien

class Repetition(db.Model):
    idRepetition = db.Column(db.Integer, primary_key=True)
    dateRepetition = db.Column(db.Date)
    dureeRepetition = db.Column(db.Integer)
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        return self.dateRepetition+" "+self.dureeRepetition+" "+self.idRepetition

class Sortie(db.Model):
    idSortie = db.Column(db.Integer, primary_key=True)
    dateSortie = db.Column(db.Date)
    dureeSortie = db.Column(db.Integer)
    lieu = db.Column(db.String(50))
    type= db.Column(db.String(50))
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        return self.dateSortie+" "+self.dureeSortie+" "+self.idSortie

class Sondage(db.Model):
    idSondage = db.Column(db.Integer, primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'))
    dateSondage = db.Column(db.Date)
    dureeSondage = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.dateSondage+" "+self.dureeSondage+" "+self.idSondage

class journal_repetition(db.Model):
    idMusicien = db.Column(db.Integer,primary_key=True)
    idRepetition = db.Column(db.Integer,primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    dateRepetition = db.Column(db.Date)
    dureeRepetition = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.nom+" "+self.prenom+" "+self.idRepetition

class journal_Sortie(db.Model):
    idMusicien = db.Column(db.Integer,primary_key=True)
    idSortie = db.Column(db.Integer,primary_key=True)
    intituleSortie = db.Column(db.String(50))   
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    dateSortie = db.Column(db.Date)
    dureeSortie = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.nom+" "+self.prenom+" "+self.idSortie

class participer_repetition(db.Model):
    idMusicien = db.Column(db.Integer,db.ForeignKey('musicien.idMusicien'),primary_key=True)
    idRepetition = db.Column(db.Integer,db.ForeignKey('repetition.idRepetition'),primary_key=True)

    def __repr__(self) -> str:
        return self.idMusicien+" "+self.idRepetition

class participer_sortie(db.Model):
    idMusicien = db.Column(db.Integer,db.ForeignKey('musicien.idMusicien'),primary_key=True)
    idSortie = db.Column(db.Integer,db.ForeignKey('sortie.idSortie'),primary_key=True)

    def __repr__(self) -> str:
        return self.idMusicien+" "+self.idSortie