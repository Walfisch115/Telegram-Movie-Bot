import requests
import credentials


API_KEY = credentials.TMDB_TOKEN

base_url = f"https://api.themoviedb.org/3"
api_part = f"?api_key={API_KEY}"


def search_for_movies(query, language="de"):
    """Returns a List of Movies"""

    search_movie = "/search/movie"
    response = requests.get(f"{base_url}{search_movie}{api_part}&language={language}&query={query}")
    data = response.json()
    return data


def get_movie_by_id(movie_id, language="de"):
    """Returns Data about a Movie when given a Movie ID"""

    get_movie = f"/movie/{movie_id}"
    response = requests.get(f"{base_url}{get_movie}{api_part}&language={language}")
    data = response.json()
    return data


def get_movie_poster(movie_id, language="de", size="original"):
    """Returns first Image URL when given a Movie ID"""

    get_poster = f"/movie/{movie_id}/images"
    response = requests.get(f"{base_url}{get_poster}{api_part}&language={language}")
    data = response.json()
    poster_path = data["posters"][0]["file_path"]  # change number for other posters

    return f"https://image.tmdb.org/t/p/{size}{poster_path}"


# print(search_for_movies("john wick", "de"))
# print(get_movie_by_id(245891))
# print(get_movie_poster(120, "de"))
# movie = search_for_movies("john wick")
# print(movie["results"][0]["id"])