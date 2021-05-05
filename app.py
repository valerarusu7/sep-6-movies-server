from flask import Flask
import requests
import json
import time

app = Flask(__name__)


@app.route('/movies', methods=['GET'])
def movies():
    # tic = time.perf_counter()
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
            if "name" in movie:
                movie_obj = {"id": movie["id"], "title": movie["name"],
                             "poster_path": imageUrl + movie["poster_path"]}
            else:
                movie_obj = {"id": movie["id"], "title": movie["title"],
                             "poster_path": imageUrl + movie["poster_path"]}

            movies_result[obj["key"]].append(movie_obj)
    # toc = time.perf_counter()
    # print(f"netflix movies got in {toc - tic:0.4f} seconds")
    return json.dumps(movies_result)


if __name__ == '__main__':
    app.run()
