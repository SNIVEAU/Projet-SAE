
"""
This module contains the views for the Flask application. It defines the routes and functions for rendering the HTML templates and handling user input. 

The routes include:
- home: renders the home page and displays all books in the database
- detail: renders the detail page for a specific book and displays its information, user rating, user comment, and all evaluations and comments for the book
- edit_author: renders the edit author page for a specific author and allows the user to edit the author's name
- save_author: saves the edited author's name to the database
- login: renders the login page and allows the user to log in with their username and password
- logout: logs the user out and redirects them to the home page
- rate_book: allows the user to rate a book and saves the rating to the database
- public_book_details: renders the public book details page for a specific book and displays all evaluations for the book
- comment_book: allows the user to comment on a book and saves the comment to the database
"""

from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Book, Commentaire, get_sample, get_author, Author, User,Evaluation

from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired

from hashlib import sha256

from flask_login import login_user, current_user, login_required, logout_user
from flask import request


@app.route("/")
def home():
    """home page

    Returns:
        html: home page
    """
    return render_template (
        "home.html",
        books = Book.query.all())


@app.route('/detail/<int:id>')
def detail(id):
    """page de détail d'un livre

    Args:
        id (int): book id

    Returns:
        html: page de détail d'un livre
    """
    book = Book.query.get(id)

    # Ajoutez ici le code pour récupérer la note de l'utilisateur pour ce livre
    user_rating = None  
    user_commentaire = None
    # Ajoutez ici le code pour récupérer le commentaire de l'utilisateur pour ce livre
    if current_user.is_authenticated:
        user_rating = Evaluation.query.filter_by(user_id=current_user.username, book_id=book.id).first()
        user_commentaire = Commentaire.query.filter_by(user_id=current_user.username, book_id=book.id).first()

    # Ajoutez le code pour récupérer toutes les évaluations pour ce livre
    évaluations = Evaluation.query.filter_by(book_id=book.id).all()
    commentaires = Commentaire.query.filter_by(book_id=book.id).all()

    return render_template(
        "detail.html",
        book=book,
        user_rating=user_rating,
        user_commentaire=user_commentaire,
        evaluations=évaluations,
        commentaires=commentaires)



class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()]) # Doit obligatoirement remplir le champs 

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    """Page d'édition d'un auteur
    Args:
        id (int): author id

    Returns:
        html: page d'édition d'un auteur
    """
    a = get_author(id)
    f = AuthorForm(id = a.id, name = a.name)
    return render_template(
        "edit-author.html",
        author = a,
        form = f)


@app.route("/save/author/", methods=["POST",]) # Uniquement accessible par cette méthode POST
def save_author():
    """Sauvegarde d'un auteur
        Returns:
        html: page d'édition d'un auteur
    """
    a = None
    f = AuthorForm() # Formulaire
    if f.validate_on_submit(): # Vérifie si formulaire valide -> champs bien remplit, trouver token, etc ...
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(        # Rediriger l'utilisateur vers une page
            url_for("home"))
    a = get_author(int(f.id.data))
    return render_template(
        "edit-author.html",
        author=a,
        form=f)


class LoginForm(FlaskForm):
    # Création des deux formulaires
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct

        Returns:
            user: l'utilisateur
        """
        user = User.query.get(self.username.data) # Récupérer l'utilisateur entré dans le formulaire
        if user is None:
            return None
        
        # Hashage
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()

        return user if passwd == user.password else None # Vérifier si le mot de passe de l'utilisateur entré est le bon


# Création du login
@app.route("/login/", methods=["GET", "POST" ,])
def login():
    """Login

    Returns:
        html: page de login
    """
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html",form=f)


@app.route("/register/", methods=["GET", "POST"])
def register():
    """s'inscrire"""
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = User.query.get(f.username.data)
        if user:
            f.next.data = request.args.get("hidden")
            print("L'utilisateur existe déjà.", "error")
        else:
            m = sha256()
            m.update(f.password.data.encode())
            passwd = m.hexdigest()
            user = User(username=f.username.data, password=passwd)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("home"))
    return render_template("register.html", form=f)


@app.route("/logout/")
def logout():
    """Logout
    Returns:
        html: page de home
    """
    logout_user()
    return redirect(url_for("home"))


@app.route('/rate-book/<int:id>', methods=['POST'])
@login_required
def rate_book(id):
    """
    Cette fonction permet à un utilisateur de noter un livre.
    Args:
        id (int): L'ID du livre à noter.
    Renvoie:
        Une redirection vers la page de détail du livre avec un message de réussite.
    """
    book = Book.query.get(id)
    rating = request.form.get('rating')

    # Assurez-vous que la note est un nombre entre 0 et 20
    try:
        rating = int(rating)
        if rating < 0 or rating > 20:
            # Si ce n'est pas le cas, affichez un message d'erreur et redirigez l'utilisateur vers la page de détails du livre.
            print('La note doit être comprise entre 0 et 20.', 'error')
            return redirect(url_for('detail', id=book.id))
    except ValueError:
        print('La note doit être un nombre entier entre 0 et 20.', 'error')
        return redirect(url_for('detail', id=book.id))

    # Vérifiez si l'utilisateur a déjà noté ce livre, auquel cas, mettez à jour la note.
    existing_rating = Evaluation.query.filter_by(user_id=current_user.username, book_id=book.id).first()
    if existing_rating:
        existing_rating.note = rating
    else:
        # Sinon, créez une nouvelle évaluation.
        new_rating = Evaluation(user_id=current_user.username, book_id=book.id, note=rating)
        db.session.add(new_rating)
    db.session.commit()

    print(f'Vous avez noté le livre "{book.title}" avec {rating}/20.', 'success')
    return redirect(url_for('detail', id=book.id))


@app.route('/public_book_details/<int:id>')
def public_book_details(id):
    """Cette fonction permet à un utilisateur de voir les détails d'un livre.

    Args:
        id (int): L'ID du livre à noter.

    Returns:
        Une redirection vers la page de détail du livre avec un message de réussite.
    """
    book = Book.query.get(id)
    
    # Récupérez toutes les évaluations pour ce livre
    evaluations = Evaluation.query.filter_by(book_id=id).all()
    
    return render_template("public_book_details.html", book=book, evaluations=evaluations)


@app.route('/comment-book/<int:id>', methods=['POST'])
@login_required
def comment_book(id):
    """
    Cette fonction permet à un utilisateur de commenter un livre.

    Args:
        id (int): L'ID du livre sur lequel commenter.

    Renvoie:
        Une redirection vers la page de détail du livre avec un message de réussite.
    """
    book = Book.query.get(id)
    commentaire = request.form.get('comment')
    
    existing_commentaire = Commentaire.query.filter_by(user_id=current_user.username, book_id=book.id).first()

    if existing_commentaire:
        existing_commentaire.commentaire = commentaire
    else:
        new_commentaire = Commentaire(user_id=current_user.username, book_id=book.id, commentaire=commentaire)
        db.session.add(new_commentaire)
    db.session.commit()

    print(f'Vous avez commenté le livre "{book.title}" avec "{commentaire}".', 'success')
    return redirect(url_for('detail', id=book.id))

    
@app.route('/public_book_details_comment/<int:id>')
def public_book_details_comment(id):
    """Cette fonction permet à un utilisateur de voir les détails d'un livre.
    Args:
        id (int): L'ID du livre à noter.
    Returns:
        Une redirection vers la page de détail du livre avec un message de réussite.
    """
    book = Book.query.get(id)
    
    # Récupérez tous les commentaires pour ce livre
    commentaires = Commentaire.query.filter_by(book_id=id).all()
    
    return render_template("public_book_details_comment.html", book=book, commentaires=commentaires)