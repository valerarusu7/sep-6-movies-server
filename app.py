from flask import Flask, request
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/movies', methods=['GET'])
def movies():
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    movie_type = request.args.get('type')
    page = request.args.get('page')
    movies_result = {'results': []}

    genre_ids = [{'type': 'drama', 'id': '18'}, {'type': 'action', 'id': '28'}, {'type': 'comedy', 'id': '35'},
                 {'type': 'horror', 'id': '27'}, {'type': 'romance', 'id': '10749'},
                 {'type': 'documentaries', 'id': '99'}, {'type': 'fantasy', 'id': '14'},
                 {'type': 'mystery', 'id': '9648'}]

    if movie_type == 'top-rated':
        movies_result = requests.get(
            'https://api.themoviedb.org/3/movie/top_rated?api_key=' + TMDB_API_KEY + '&language=en-US&page=' + page).json()
    elif movie_type == 'trending':
        movies_result = requests.get(
            'https://api.themoviedb.org/3/trending/all/week?api_key=' + TMDB_API_KEY + '&language=en-US&page=' + page).json()
    else:
        for genre in genre_ids:
            if genre['type'] == movie_type:
                genre_id = genre['id']
                movies_result = requests.get(
                    'https://api.themoviedb.org/3/discover/movie?api_key=' + TMDB_API_KEY + '&with_genres=' + genre_id + '&page=' + page).json()

    movies_response = {'movies': movies_result['results']}
    return json.dumps(movies_response)


@app.route('/person', methods=['GET'])
def person():
    person_id = request.args.get('id')
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    average_movies_rating = 0

    person_details = requests.get(
        'https://api.themoviedb.org/3/person/' + person_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    person_movies = requests.get(
        'https://api.themoviedb.org/3/discover/movie' + '?api_key=' + TMDB_API_KEY + '&with_people=' + person_id).json()

    for movie in person_movies['results']:
        average_movies_rating += movie['vote_average']
    top_5 = sorted(person_movies['results'], key=lambda x: x['vote_average'], reverse=True)
    average_movies_rating = round(average_movies_rating / len(person_movies['results']), 1)
    person_response = {'details': person_details, 'average_movies_rating': average_movies_rating, 'top_5': top_5[:5]}

    return json.dumps(person_response)


@app.route('/movie', methods=['GET'])
def movie():
    movie_id = request.args.get('id')
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'
    movie_details = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_credits = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '/credits?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_videos = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '/videos?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_response = {'details': movie_details, 'credits': movie_credits, 'videos': movie_videos}
    return json.dumps(movie_response)


@app.route('/compare', methods=['POST'])
def compare():
    compare_movies = request.json['movies']
    new_movie_id = request.args.get('movie_id')
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'

    movie_details = requests.get(
        'https://api.themoviedb.org/3/movie/' + new_movie_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    compare_movies.append(movie_details)

    high_revenue = compare_movies[0]['revenue']
    high_budget = compare_movies[0]['budget']
    high_rating = compare_movies[0]['vote_average']
    high_runtime = compare_movies[0]['runtime']
    high_count = compare_movies[0]['vote_count']

    for compare_movie in compare_movies:
        if compare_movie['revenue'] >= high_revenue:
            compare_movie['highest_revenue'] = True
            high_revenue = compare_movie['revenue']
        else:
            compare_movie['highest_revenue'] = False

        if compare_movie['budget'] >= high_budget:
            compare_movie['highest_budget'] = True
            high_budget = compare_movie['budget']
        else:
            compare_movie['highest_budget'] = False

        if compare_movie['vote_average'] >= high_rating:
            compare_movie['highest_rating'] = True
            high_rating = compare_movie['vote_average']
        else:
            compare_movie['highest_rating'] = False

        if compare_movie['runtime'] >= high_runtime:
            compare_movie['highest_runtime'] = True
            high_runtime = compare_movie['runtime']
        else:
            compare_movie['highest_runtime'] = False

        if compare_movie['vote_count'] >= high_count:
            compare_movie['highest_vote_count'] = True
            high_count = compare_movie['vote_count']
        else:
            compare_movie['highest_vote_count'] = False

    compare_movies_response = {'movies': compare_movies}
    return json.dumps(compare_movies_response)
