import uuid
from flask import Blueprint, render_template,session, redirect, request, current_app, url_for
from dataclasses import asdict
from movie_library.forms import MovieForm
from movie_library.models import Movie

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
    
    
@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()
    
    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data
        )
        
        current_app.db.movies.insert_one(asdict(movie))
        return redirect(url_for(".index"))
    
    return render_template(
        "new_movie.html", 
        title="Movie Watchlist - Add Movie", 
        form=form
    )
    
    
@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie_data = current_app.db.movies.find_one({"_id": _id})
    movie = Movie(**movie_data)
    return render_template("movie_details.html", movie=movie)


@pages.get("/movie/<string:_id>/rate")
def rate_movie(_id):
    rating = int(request.args.get("rating"))
    current_app.db.movies.update_one({"_id": _id}, {"$set": {"rating": rating}})
    
    return redirect(url_for(".movie", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == 'dark':
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
        
    return redirect(request.args.get("current_page"))