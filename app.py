from flask import Flask
import requests
import json
import time

app = Flask(__name__)


@app.route('/movies', methods=['GET'])
def movies():
    tic = time.perf_counter()
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    movies = [{'endpoint': 'https://api.themoviedb.org/3/discover/tv?api_key=' + TMDB_API_KEY + '&with_networks=213',
               'key': 'netflix'},
              {'endpoint': 'https://api.themoviedb.org/3/movie/top_rated?api_key=' + TMDB_API_KEY + '&language=en-US',
               'key': 'topRated'},
              {'endpoint': 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=28',
               'key': 'action'},
              {'endpoint': 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=35',
               'key': 'comedy'},
              {'endpoint': 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=27',
               'key': 'horror'},
              {'endpoint': 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=10749',
               'key': 'romance'},
              {'endpoint': 'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=99',
               'key': 'documentaries'},
              {'endpoint': 'https://api.themoviedb.org/3/trending/all/week?api_key=' + TMDB_API_KEY + '&language=en-US',
               'key': 'trending'},
              ]
    imageUrl = "https://image.tmdb.org/t/p/w500"
    movies_result = {'netflix': [], 'action': [], 'comedy': [], 'romance': [], 'documentaries': [], 'horror': [],
                     'trending': [], 'topRated': []}
    for obj in movies:
        url = obj["endpoint"]
        response = requests.get(url).json()
        for movie in response["results"]:
            movies_result[obj["key"]].append(movie)
    toc = time.perf_counter()
    print(f"netflix movies got in {toc - tic:0.4f} seconds")
    return json.dumps(movies_result)


@app.route('/person', methods=['GET'])
def person():
    person_id = '7467'
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    person_details = requests.get(
        'https://api.themoviedb.org/3/person/' + person_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    person_movies = requests.get(
        'https://api.themoviedb.org/3/discover/movie' + '?api_key=' + TMDB_API_KEY + '&with_people=' + person_id).json()
    average_movies_rating = 0
    for movie in person_movies['results']:
        average_movies_rating += movie['vote_average']
    top_5 = sorted(person_movies['results'], key=lambda x: x['vote_average'], reverse=True)
    average_movies_rating = round(average_movies_rating / len(person_movies['results']), 1)
    person_response = {'details': person_details, 'average_movies_rating': average_movies_rating, 'top_5': top_5[:5]}
    return json.dumps(person_response)


@app.route('/movie', methods=['GET'])
def movie():
    movie_id = '460465'
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    movie_details = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_credits = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '/credits?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_videos = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '/videos?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    print(movie_videos['results'])
    trailer = None
    for video in movie_videos['results']:
        if video['type'] == 'Trailer':
            trailer = video
    movie_response = {'details': movie_details, 'credits': movie_credits, 'trailer': trailer}
    return json.dumps(movie_response)


if __name__ == '__main__':
    app.run()
