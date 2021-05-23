from flask import Flask, request
import requests
import json
from flask_cors import CORS
from bs4 import BeautifulSoup as BS

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
    similar_movies = requests.get(
        'https://api.themoviedb.org/3/movie/' + movie_id + '/similar?api_key=' + TMDB_API_KEY + '&language=en-US').json()
    movie_response = {'details': movie_details, 'credits': movie_credits, 'videos': movie_videos,
                      'similar_movies': similar_movies['results']}
    return json.dumps(movie_response)


@app.route('/compare', methods=['POST'])
def compare():
    compare_movies = request.json['movies']
    new_movie_id = request.args.get('movie_id')
    TMDB_API_KEY = 'e453502d7e2f31ded447961d9d1f121c'

    if new_movie_id != '0':
        movie_details = requests.get(
            'https://api.themoviedb.org/3/movie/' + new_movie_id + '?api_key=' + TMDB_API_KEY + '&language=en-US').json()
        compare_movies.append(movie_details)

    high_revenue = 0
    high_budget = 0
    high_rating = 0
    high_runtime = 0
    high_count = 0
    high_revenue_id = 0
    high_budget_id = 0
    high_rating_id = 0
    high_runtime_id = 0
    high_count_id = 0
    highest_revenue = 0

    for compare_movie in compare_movies:
        if compare_movie['revenue'] >= high_revenue:
            high_revenue_id = compare_movie['id']
            high_revenue = compare_movie['revenue']

        if compare_movie['budget'] >= high_budget:
            high_budget_id = compare_movie['id']
            high_budget = compare_movie['budget']

        if compare_movie['vote_average'] >= high_rating:
            high_rating_id = compare_movie['id']
            high_rating = compare_movie['vote_average']

        if compare_movie['runtime'] >= high_runtime:
            high_runtime_id = compare_movie['id']
            high_runtime = compare_movie['runtime']

        if compare_movie['vote_count'] >= high_count:
            high_count_id = compare_movie['id']
            high_count = compare_movie['vote_count']

    for m in compare_movies:
        if m['id'] == high_revenue_id:
            m['highest_revenue_color'] = 'green'
            highest_revenue = m['revenue']
        else:
            m['highest_revenue_color'] = 'red'
        m['highest_budget_color'] = 'green' if m['id'] == high_budget_id else 'red'
        m['highest_runtime_color'] = 'green' if m['id'] == high_runtime_id else 'red'
        m['highest_rating_color'] = 'green' if m['id'] == high_rating_id else 'red'
        m['highest_vote_count_color'] = 'green' if m['id'] == high_count_id else 'red'

    for m in compare_movies:
        if m['id'] != high_revenue_id:
            movie_revenue = m['revenue']
            m['percentage_change'] = round(((highest_revenue - movie_revenue) / movie_revenue) * 100.0, 2)

    compare_movies_response = {'movies': compare_movies}
    return json.dumps(compare_movies_response)


@app.route('/box-offices', methods=['GET'])
def box_office():
    year = request.args.get('year')
    page = requests.get(
        'https://www.boxofficemojo.com/year/' + year + '/?grossesOption=totalGrosses&sort=rank&sortDir=asc')
    soup = BS(page.content, 'html.parser')

    titles_data = []
    titles = soup.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
    gross = soup.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
    theaters = soup.find_all('td', class_='a-text-right mojo-field-type-positive_integer')

    for i in range(0, 29):
        gross_movie = {'rank': i + 1, 'name': titles[i].select('a')[0].string,
                       'gross': gross[i].string.replace(',', '').replace('$', ''),
                       'theaters': theaters[i].string.replace(',', '')}
        titles_data.append(gross_movie)

    box_office_response = {'box_office_movies': titles_data}
    return json.dumps(box_office_response)
