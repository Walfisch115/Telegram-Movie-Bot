import requests
import credentials
from datetime import datetime
import time
import tmdb_functions as tmdb


TOKEN = credentials.TELEGRAM_TOKEN
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    """Sends a Message when given a Chat ID and a Text."""

    response = {"chat_id": chat_id, "text": f"{text}"}
    message = requests.post(f"{BASE_URL}/sendMessage", response)
    return message


def send_photo(chat_id, caption, image_url):
    """Sends a Photo when given a Chat ID, a Caption and an Image URL."""

    response = {"chat_id": chat_id, "text": f"{image_url}"}
    image = requests.post(f"{BASE_URL}/sendPhoto?chat_id={chat_id}&photo={image_url}&caption={caption}", response)
    return image


def convert_release_date(release_date):
    """Converts the Release Date of a Movie to another Time Format."""

    date_object = datetime.strptime(release_date, '%Y-%m-%d')
    date_object = date_object.strftime('%d.%m.%Y')

    return str(date_object)


if __name__ == '__main__':

    update_id = 0

    while True:
        try:
            reply_without_offset = requests.get(f"{BASE_URL}/getupdates")

            update_id = reply_without_offset.json()["result"][0]["update_id"]

        except IndexError:
            print("Keine neuen Nachrichten")
            time.sleep(5.0)

        else:
            while True:

                # pull updates with offset
                reply = requests.get(f"{BASE_URL}/getupdates?offset={update_id}")

                # message handling
                for data in reply.json().get("result"):

                    if data["update_id"] == update_id:

                        try:
                            # get message text, first name and chat id
                            message = str(data["message"]["text"])
                            first_name = data["message"]["from"]["first_name"]
                            chat_id = data["message"]["chat"]["id"]

                            response = {"chat_id": chat_id, }

                            # Reagiere auf die Eingabe
                            # Fallunterscheidung
                            if message.startswith("/start"):

                                print("starts with /start")
                                send_message(chat_id, f"Hello {first_name}, I'm the Movie Bot."
                                                      f"\n"
                                                      f"\nYou can use the following commands:"
                                                      f"\n/movie moviename"
                                                      f"\n/poster moviename"
                                                      f"\n/description moviename")

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
                                release = convert_release_date(movie["release_date"])
                                runtime = movie["runtime"]
                                rating = round(movie["vote_average"], 1)

                                print("/movie request")

                                send_message(chat_id, f"{title}"
                                                      f"\nGenre: {genre}"
                                                      f"\nLaufzeit: {runtime} Minuten"
                                                      f"\nBewertung: {rating}/10"
                                                      f"\nKinostart: {release}")

                            elif message.startswith("/poster"):

                                query = message[8:]
                                movie_search = tmdb.search_for_movies(query)
                                movie_id = movie_search["results"][0]["id"]

                                movie = tmdb.get_movie_by_id(movie_id)
                                title = movie["title"]
                                poster_url = tmdb.get_movie_poster(movie_id)

                                print("/poster request")

                                send_photo(chat_id, title, poster_url)

                            elif message.startswith("/description"):

                                query = message[13:]
                                movie_search = tmdb.search_for_movies(query)
                                movie_id = movie_search["results"][0]["id"]

                                movie = tmdb.get_movie_by_id(movie_id)
                                description = movie["overview"]

                                print("/description request")

                                send_message(chat_id, f"{description}")

                            else:
                                send_message(chat_id, f"Please /start, {first_name}".encode("utf8"))

                        except Exception as e:
                            print(e)

                    # increase offset
                    update_id = data["update_id"] + 1

                # Pull Intervall
                time.sleep(5.0)
