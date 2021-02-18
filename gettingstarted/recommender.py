
from random import choice

MOVIES = [
    'Shrek',
    'Ex Machina',
    'Star Trek',
    'Pulp Fiction'
]

def get_movie_recommendation(name, rating):
    print("*** doing ML magic ***")
    print("name  : ", name)
    print("rating: ", rating)
    return choice(MOVIES)


if __name__ == '__main__':
    # only gets executed when running recommender.py 
    # directly but not when importing
    print(get_movie_recommendation("Kung Fu Panda", 5))
