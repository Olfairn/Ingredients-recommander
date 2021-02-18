# pip install flask
# python -m pip install flask

from flask import Flask, request
from flask.templating import render_template
import recommender

app = Flask(__name__)

@app.route('/movie')  # <-- suffix of the URL
def get_movie():
    #TODO read URL parameters
    d = dict(request.args)
    name = d['movie1']
    rating = int(d['rating1'])
    movie = recommender.get_movie_recommendation(name, rating)
    return render_template('result.html', movie=movie, 
                           score=0.123,
                           title='your recommendations:')

@app.route('/')
def hello():
    return render_template('main.html') # in templates/


if __name__ == "__main__":
    app.run(debug=True, port=5000)

