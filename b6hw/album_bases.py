from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album


@route("/albums", method="POST")
def albums():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома: {}".format(request.forms.get("year")))

    try:
        new_album = album.save(year, artist, genre, name)
    except AssertionError as er:
        result = HTTPError(400, str(er))
    except album.AlreadyExists as er:
        result = HTTPError(409, str(er))
    else:
        result = "Альбом {} \"{}\" ({} год) сохранен".format(artist, name, year)

    return result


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_amount = len(albums_list)
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {} ({} шт): \n- ".format(artist, album_amount)
        result += "\n- ".join(album_names)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
