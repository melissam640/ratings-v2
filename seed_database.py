"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')
model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie.get('title')
    overview = movie.get('overview')
    release_date = movie.get('release_date')
    format_date = "%Y-%m-%d"
    poster_path = movie.get('poster_path')
    movies_in_db.append(crud.create_movie(title, overview, datetime.strptime(release_date, format_date), poster_path))

model.db.session.add_all(movies_in_db)
model.db.session.commit()
# TODO: create a movie here and append it to movies_in_db

users_in_db = []

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)

    # TODO: create a user here
    users_in_db.append(user)

    # TODO: create 10 ratings for the user
    ratings = []

    for j in range(10):
        movie = choice(movies_in_db)
        score = randint(1,5)
        rating = crud.create_rating(movie,user,score)
        ratings.append(rating)
    
    model.db.session.add_all(ratings)

model.db.session.add_all(users_in_db)
model.db.session.commit()
