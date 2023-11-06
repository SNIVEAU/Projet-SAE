import click
from .app import app,db
import yaml
from .models import Musicien
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
@click.argument('filename')
def admin(filename:str) -> None:
    """ permet la creation dde la base de donnée"""
    f=yaml.safe_load(open(filename))
    for musicien in f:
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