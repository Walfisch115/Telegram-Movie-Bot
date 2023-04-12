import requests
import credentials
from datetime import datetime
import tmdb_functions as tmdb


TOKEN = credentials.TELEGRAM_TOKEN
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

reply = requests.get(f"{BASE_URL}/getupdates")  # /getupdates?offset=update_id


def send_message(chat_id, text):
    """Sends a Message when given a Chat ID and a Text"""

    response = {"chat_id": chat_id, "text": f"{text}"}
    message = requests.post(f"{BASE_URL}/sendMessage", response)
    return message


def send_photo(chat_id, caption, image_url):
    """Sends a Photo when given a Chat ID, a Caption and an Image URL"""

    response = {"chat_id": chat_id, "text": f"{image_url}"}
    image = requests.post(f"{BASE_URL}/sendPhoto?chat_id={chat_id}&photo={image_url}&caption={caption}", response)
    return image


def convert_release_date(release_date):

    date_object = datetime.strptime(release_date, '%Y-%m-%d')
    date_object = date_object.strftime('%d.%m.%Y')

    return str(date_object)


for data in reply.json().get("result"):

    try:
        # Hole den Nachrichtentext, den Vornamen und die ChatID
        message = str(data["message"]["text"])
        first_name = data["message"]["from"]["first_name"]
        chat_id = data["message"]["chat"]["id"]

        response = {"chat_id": chat_id, }

        # Reagiere auf die Eingabe
        # Fallunterscheidung
        if message.startswith("/start"):

            send_message(chat_id, f"Hello {first_name}, I'm the Movie Bot.\n\nYou can use the following commands:\n/movie moviename\n/poster moviename\n/description moviename")

        # elif message.startswith("/help"):
        #     pass

        elif message.startswith("/movie"):

            query = message[7:]
            movie_search = tmdb.search_for_movies(query)
            movie_id = movie_search["results"][0]["id"]

            movie = tmdb.get_movie_by_id(movie_id)
            title = movie["title"]
            genre_list = []
            for x in movie["genres"]:
                genre_list.append(x["name"])
            genre = ", ".join(genre_list)
            print(genre)
            release = convert_release_date(movie["release_date"])
            runtime = movie["runtime"]
            rating = round(movie["vote_average"], 1)

            send_message(chat_id, f"{title}\nGenre: {genre}\nLaufzeit: {runtime} Minuten\nBewertung: {rating}/10\nKinostart: {release}")

        elif message.startswith("/poster"):

            query = message[8:]
            movie_search = tmdb.search_for_movies(query)
            movie_id = movie_search["results"][0]["id"]

            movie = tmdb.get_movie_by_id(movie_id)
            title = movie["title"]
            poster_url = tmdb.get_movie_poster(movie_id)

            send_photo(chat_id, title, poster_url)

        elif message.startswith("/description"):

            query = message[13:]
            movie_search = tmdb.search_for_movies(query)
            movie_id = movie_search["results"][0]["id"]

            movie = tmdb.get_movie_by_id(movie_id)
            description = movie["overview"]

            send_message(chat_id, f"{description}")

        # else:
        #     send_message(chat_id, f"Please /start, {first_name}".encode("utf8"))

    except Exception as e:
        print(e)
