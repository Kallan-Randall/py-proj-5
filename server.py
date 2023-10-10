"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "super secret"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route("/")
def homepage():
    
    return render_template("homepage.html")

@app.route("/movies")
def all_movies():
    """A view of all movies."""
    
    movies = crud.get_movies()
    
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show the info about a specific movie."""
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users", methods=["GET"])
def all_users():
    """A view for all the users."""
    users = crud.get_users()
    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Creates a new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if user:
            flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created! Welcome {user.email}")

    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """Login for user"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if user:
        session["email"] = user.email
        flash(f"Welcome Back {user.email}")
    else:
        flash("This email is not currently registered!")
        
    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show the info about a specific user."""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route("/rating/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    user = crud.get_user_by_email(session["email"])
    movie = crud.get_movie_by_id(movie_id)
    score = int(request.form["rating"])
    
    new_rating = crud.create_rating(user, movie, score)
    db.session.add(new_rating)
    db.session.commit()
    return redirect(f"/movies/{movie.movie_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)