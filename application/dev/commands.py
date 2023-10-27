import click
from .app import app,db
import yaml
from .models import Musicien,Sondage,Sortie
from datetime import *

# voir pour inserer des image en sql alchemy


@app.cli.command()
def destroydb():
    """Destroys the current database."""
    db.drop_all()

@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()

@app.cli.command()
def resetdb():
    """Destroys and creates all tables."""
    db.drop_all()
    db.create_all()

@app.cli.command()
@click.argument('filename')
def crea_musicien(filename:str) -> None:
    """ permet l'injection de données ( de musicien ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for musicien in fy:
        print(musicien)
        m=Musicien(idMusicien=int(musicien["idMusicien"]),
                   nomMusicien=musicien["nomMusicien"],
                   prenomMusicien=musicien["prenomMusicien"],
                   password=musicien["password"],
                   ageMusicien=int(musicien["ageMusicien"]),
                   adresseMail=musicien["adresseMail"],
                   telephone=musicien["telephone"],
                   admin=musicien["admin"],
                   img=None)
        db.session.add(m)
        db.session.commit()

@app.cli.command()
@click.argument('filename')
def crea_sondage(filename:str) -> None:
    """ permet l'injection de données ( de sondage ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for sondage in fy:
        date=datetime.strptime(sondage["dateSondage"], '%Y-%m-%d %H:%M:%S')
        s=Sondage(idSondage=int(sondage["idSondage"]),
                  idSortie=int(sondage["idSortie"]),
                  message=sondage["message"],
                  dateSondage=date,
                  dureeSondage=int(sondage["dureeSondage"]))
        db.session.add(s)
        db.session.commit()

@app.cli.command()
@click.argument('filename')
def crea_sortie(filename:str) -> None:
    """ permet l'injection de données ( de sortie ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for sortie in fy:
        date = datetime.strptime(sortie["dateSortie"], '%Y-%m-%d %H:%M:%S')
        srt=Sortie(idSortie=int(sortie["idSortie"]),
                   dateSortie=date,
                   dureeSortie=int(sortie["dureeSortie"]),
                   lieu=sortie["lieu"],
                   type=sortie["type"],
                   tenue=sortie["tenue"])
        db.session.add(srt)
        db.session.commit()

@app.cli.command()
def tout_musicien():
    print(Musicien.query.all())

@app.cli.command()
def toute_sortie():
    print(Sortie.query.all())

@app.cli.command()
def tout_sondage():
    print(Sondage.query.all())