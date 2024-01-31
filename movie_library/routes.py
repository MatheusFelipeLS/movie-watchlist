import uuid
import datetime 
from dataclasses import asdict

from flask import (
    Blueprint,
    current_app, 
    flash,
    redirect,
    render_template, 
    session,
    url_for, 
    request,
)
from movie_library.forms import RegisterForm, LoginForm, MovieForm, ExtendedMovieForm
from movie_library.models import User, Movie
from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index(): 
    movie_data = current_app.db.movies.find({}) #o movies n obrigatoriamente é o nome da pasta do db. Se na hora de inserir um filme fosse movie, nessa linha deveria ser movie
    movies = [Movie(**movie) for movie in movie_data]
    
    return render_template(
        "index.html",
        title="Movies watchlist",
        movies_data=movies
    )
    

@pages.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )
        
        current_app.db.user.insert_one(asdict(user))
        
        flash("User registered sucessfully", "sucess")
        
        return redirect(url_for(".login"))
    
    return render_template(
        "register.html", title="Movies Watchlist - Registrar", form=form
    )
    

@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        users_data = current_app.db.user.find_one({"email": form.email.data})
        if not users_data:
            flash("Credenciais não estão corretas", category="danger")
            return redirect(url_for(".login"))
        
        user = User(**users_data)
        
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email
            
            return redirect(url_for(".index"))
        
        flash("Credenciais não estão corretas", category="danger")
        
    return render_template("login.html", title="Movie Watchlist - Login", form=form)
            
    
    
@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()
    
    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )
        
        current_app.db.movies.insert_one(asdict(movie))
        
        return redirect(url_for(".movie", _id=movie._id))
    
    return render_template(
        "new_movie.html", title="Movie Watchlist - Add Movie", form=form
    )
    
    
@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie = Movie(**current_app.db.movies.find_one({"_id": _id}))
    return render_template("movie_details.html", movie=movie)


@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
def edit_movie(_id: str):
    movie = Movie(**current_app.db.movies.find_one({"_id": _id}))
    form = ExtendedMovieForm(obj=movie) #obj faz com que os campos correspondentes sejam iguais. title = title, director = director...
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.tags = form.tags.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data
        
        print("d ", asdict(movie))
        current_app.db.movies.update_one({"_id": movie._id}, {"$set": asdict(movie)})
        print("b ", asdict(movie))
        return redirect(url_for(".movie", _id=movie._id))
    
    print("c ", asdict(movie))
    return render_template("movie_form.html", movie=movie, form=form)


@pages.get("/movie/<string:_id>/rate")
def rate_movie(_id):
    rating = int(request.args.get("rating"))
    current_app.db.movies.update_one({"_id": _id}, {"$set": {"rating": rating}})
    
    return redirect(url_for(".movie", _id=_id))


@pages.get("/movie/<string:_id>/watch")
def watch_today(_id):
    current_app.db.movies.update_one({"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}})
    return redirect(url_for(".movie", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == 'dark':
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
        
    return redirect(request.args.get("current_page"))