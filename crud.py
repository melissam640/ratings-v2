"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def return_all_users():
    """Return all user objects"""

    users = db.session.query(User).all()

    return users

def get_user_by_id(this_user_id):
    """Get user id."""

    user = User.query.filter_by(user_id=this_user_id).first()
    return user

def get_user_by_email(email):
    """Get user by email."""

    user = User.query.filter_by(email=email).first()
    if user ==[]:
        return None
    else:
        return user

def check_user_match_password(email, password):
    """Check if password matches user's password"""
    user_password = get_user_by_email(email).password
    if user_password == password:
        return True
    return False

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date,poster_path=poster_path)
    
    return movie

def return_all_movies():
    """Return all movie objects"""

    movies = db.session.query(Movie).all()

    return movies

def get_movie_by_id(this_movie_id):
    """Get movie id."""

    movie = Movie.query.filter_by(movie_id=this_movie_id).first()
    return movie

def get_movie_avg_score(movie):
    """Get movie average score"""
    all_ratings = movie.ratings

    score = 0
    if all_ratings != []:
        for rating in all_ratings:
            score = score + rating.score
        score = score/len(all_ratings)
        return str(score)
    else:
        return 'Not Rated'

def create_rating(movie, user, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)