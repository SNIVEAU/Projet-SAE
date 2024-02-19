import click
from .app import app,db
import yaml
from .models import *
from datetime import *
from hashlib import sha256

@app.cli.command()
def destroydb():
    """Destruction de toutes les tables."""
    db.drop_all()

@app.cli.command()
def syncdb():
    """Création de toutes les tables."""
    db.create_all()

@app.cli.command()
def resetdb():
    """Destruction et recréation de toutes les tables."""
    db.drop_all()
    db.create_all()

@app.cli.command()
@click.argument('filename')
def crea_musicien(filename:str) -> None:
    """ permet l'injection de données (de musicien) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for musicien in fy:
        print(musicien)
        m = sha256()
        m.update(musicien["password"].encode())
        hashed_password = m.hexdigest(),
        m=Musicien(idMusicien=int(musicien["idMusicien"]),
                   nomMusicien=musicien["nomMusicien"],
                   prenomMusicien=musicien["prenomMusicien"],
                   
                   password=str(hashed_password[0]),
                   ageMusicien=int(musicien["ageMusicien"]),
                   adresseMail=musicien["adresseMail"],
                   telephone=musicien["telephone"],
                   admin=musicien["admin"],
                   img=None)
        db.session.add(m)
        db.session.commit()

@app.cli.command()
@click.argument('filename')
def ajoute_disponibilite(filename:str) -> None:
    """ permet l'injection de données ( de disponibilité ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for disp in fy:
        datedispo=datetime.strptime(disp["date"], '%Y-%m-%d %H:%M:%S')
        d=disponibilite(idMusicien=int(disp["idMusicien"]),
                        date=datedispo)
        db.session.add(d)
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
def crea_participe_sortie(filename:str) -> None:
    """ permet l'injection de données ( de participation à une sortie ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for participation_sortie in fy:
        srt = participer_sortie(idMusicien=participation_sortie["idMusicien"],
                                   idSortie=participation_sortie["idSortie"])
        db.session.add(srt)
    db.session.commit()

@app.cli.command()
@click.argument('filename')
def crea_sortie(filename:str) -> None:
    def image_to_blob(chemin_image):
        with open(chemin_image, 'rb') as fichier_image:
            donnees_binaires = base64.b64encode(fichier_image.read())
        return donnees_binaires
    blob_data = image_to_blob("/home/iut45/Etudiants/o22204836/Documents/but2/SAE/Projet-SAE/application/dev/static/images/sortie1.jpg")
    # print(blob_data)
    
    print(str(blob_data))
    """ permet l'injection de données ( de sortie ) dans la base de données"""
    fy=yaml.safe_load(open(filename))
    for sortie in fy:
        date = datetime.strptime(sortie["dateSortie"], '%Y-%m-%d %H:%M:%S')
        srt=Sortie(idSortie=int(sortie["idSortie"]),
                   dateSortie=date,
                   dureeSortie=int(sortie["dureeSortie"]),
                   lieu=sortie["lieu"],
                   type=sortie["type"],
                   tenue=sortie["tenue"],
                   blob_data=str(blob_data))
        db.session.add(srt)
        db.session.commit()

@app.cli.command()
def tout_musicien():
    """Affiche tous les musiciens."""
    print(Musicien.query.all())

@app.cli.command()
def toute_sortie():
    """Affiche toutes les sorties."""
    print(Sortie.query.all())

@app.cli.command()
def tout_sondage():
    """Affiche tous les sondages."""
    print(Sondage.query.all())

@app.cli.command()
def tout_dispo():
    """Affiche toutes les disponibilités."""
    print(disponibilite.query.all())


@app.cli.command()
def sup_srt_sdg_part():
    """Supprime toutes les sorties, sondages et participations."""
    db.session.query(Sondage).delete()
    db.session.query(Sortie).delete()
    db.session.query(participer_sortie).delete()
    db.session.commit()

@app.cli.command()
def clean_sondage():
    """Supprime tous les sondages."""
    db.session.query(Sondage).delete()
    db.session.commit()
    
@app.cli.command()
def crea_type_instrument():
    """Création des types d'instruments."""
    db.session.add(TypeInstrument(idTypeInstrument=1, nomTypeInstrument="Guitare"))
    db.session.add(TypeInstrument(idTypeInstrument=2, nomTypeInstrument="Batterie"))
    db.session.add(TypeInstrument(idTypeInstrument=3, nomTypeInstrument="Basse"))
    db.session.add(TypeInstrument(idTypeInstrument=4, nomTypeInstrument="Clavier"))
    db.session.add(TypeInstrument(idTypeInstrument=5, nomTypeInstrument="Chant"))
    db.session.commit()
