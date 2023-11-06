from .app import db

class Musicien(db.Model):
    idMusicien = db.Column(db.Integer, primary_key=True)
    nomMusicien = db.Column(db.String(50))
    prenomMusicien = db.Column(db.String(50))
    password = db.Column(db.String(50))
    ageMusicien = db.Column(db.Integer)
    adresseMail = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    img = db.Column(db.String(50))


    def __repr__(self) -> str:
        return self.nomMusicien + " " + self.prenomMusicien
    
def get_musicien()->list:
    return Musicien.query.all()

def get_musicien_by_id(id)->Musicien:
    return Musicien.query.filter_by(idMusicien=id).first()

class Repetition(db.Model):
    idRepetition = db.Column(db.Integer, primary_key=True)
    dateRepetition = db.Column(db.Date)
    dureeRepetition = db.Column(db.Integer)
    tenue = db.Column(db.String(50))

    def __repr__(self) -> str:
        return self.dateRepetition+" "+self.dureeRepetition+" "+self.idRepetition
    
def get_repetitions()->list:
    return Repetition.query.all()

def get_repetition_by_id(id)->Repetition:
    return Repetition.query.filter_by(idRepetition=id).first()

class Sortie(db.Model):
    idSortie = db.Column(db.Integer, primary_key=True)
    dateSortie = db.Column(db.Date)
    dureeSortie = db.Column(db.Integer)
    lieu = db.Column(db.String(50))
    type= db.Column(db.String(50))
    tenue = db.Column(db.String(50))
    def __repr__(self) -> str:
        return self.dateSortie+" "+self.dureeSortie+" "+self.idSortie
    
def get_sorties()->list:
    return Sortie.query.all()

def get_sortie_by_id(id)->Sortie:
    return Sortie.query.filter_by(idSortie=id).first()

class Sondage(db.Model):
    idSondage = db.Column(db.Integer, primary_key=True)
    idSortie = db.Column(db.Integer, db.ForeignKey('sortie.idSortie'))
    dateSondage = db.Column(db.Date)
    dureeSondage = db.Column(db.Integer)

    def __repr__(self) -> str:
        return self.dateSondage+" "+self.dureeSondage+" "+self.idSondage

def get_sondages()->list:
    return Sondage.query.all()

def get_sondage_by_id(id)->Sondage:
    return Sondage.query.filter_by(idSondage=id).first()

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

    def __repr__(self) -> str:
        return self.idMusicien+" "+self.idSortie
    
def get_participer_sorties()->list:
    return participer_sortie.query.all()

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
