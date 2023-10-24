from .app import db, login_manager
from flask_login import UserMixin # Permet une authentification 

class Author(db.Model):
    """Représentation de la table Author dans la base de données

    Args:
        db : la base de données associée
    """
    id = db.Column(db.Integer, primary_key=True) # Indique la clé primaire de la table
    name = db.Column(db.String(100))

    def __repr__(self):
        """  Redéfinit l'équivalent du toString en java  """
        return "%s" % self.name
        
class Book(db.Model):
    """Représentation de la table Book dans la base de données

    Args:
        db : la base de données associée
    """
    id = db.Column(db.Integer, primary_key =True) # Indique la clé primaire de la table
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(250))
    img = db.Column(db.String(200))

    # Partie foreign key 
    author_id = db.Column(db.Integer, db.ForeignKey("author.id")) # Indique la foreign key dans la table associée
    author = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        """  Redéfinit l'équivalent du toString en java  """
        return "%s" % self.title

class User(db.Model, UserMixin): # Héritage de UserMixin
    """Représentation de la table User dans la base de données

    Args:
        db : la base de données associée
    """
    username = db.Column(db.String(50), primary_key =True)
    password = db.Column(db.String(64))

    def get_id(self):
        """Retour l'id actuel du User"""
        return self.username
    
    def __repr__(self):
        """  Redéfinit l'équivalent du toString en java  """
        return "%s" % self.username
    
class Evaluation(db.Model):
    """Représentation de la table Evaluation dans la base de données"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    note = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """  Redéfinit l'équivalent du toString en java  """
        return "%s" % self.note
    
class Commentaire(db.Model):
    """Représentation de la table Commentaire dans la base de données"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    commentaire = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        """  Redéfinit l'équivalent du toString en java  """
        return "%s" % self.commentaire
    
# ================================================ #


def get_sample():
    """  Retourne les 10 premiers livres  """
    return Book.query.all() # S'apparente au "select * from Book;"


def get_author(id: int): 
    """Retourne l'auteur avec l'id associé

    Args:
        id : l'id associé
    """
    return Author.query.get(id)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

