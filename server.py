"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def run_homepage():
    """Create the homepage"""

    return render_template('homepage.html')

@app.route('/movies')
def show_movies():
    """Show all the movies"""

    movies = crud.return_all_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie_details(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def show_users():

    users = crud.return_all_users()

    return render_template('all_users.html', users=users)

@app.route('/users', methods=['POST'])
def create_account():
    """Creates a user account"""
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email) is not None:
        flash('Account already exists with that email addres. Try again.')
    else:
        flash('Account created, please log in.')
        user = crud.create_user(email,password)
        db.session.add(user)
        db.session.commit()

    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    """Log a user into their account"""
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user is not None:
        if crud.check_user_match_password(email,password):
            flash('Logged in!')
            session['current_user'] = user.user_id
            return redirect('/')
    
    flash('Email or password incorrect, please try again.') 
    return redirect('/')


@app.route('/users/<user_id>')
def show_user_details(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/movies/<movie_id>/rating', methods = ['POST'])
def make_new_rating(movie_id):
    rating = int(request.form.get('rating'))

    rating = crud.create_rating(crud.get_movie_by_id(movie_id), crud.get_user_by_id(session['current_user']),rating)

    db.session.add(rating)
    db.session.commit()

    return redirect('/movies')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
