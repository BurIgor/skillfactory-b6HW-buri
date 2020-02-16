import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


class Error(Exception):
    pass


class AlreadyExists(Error):
    pass


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def save(year, artist, genre, name):
    # Проверка корректности ввода
    assert isinstance(year, int), "Некорректный год"
    assert isinstance(artist, str), "Некорректный исполнитель"
    assert isinstance(genre, str), "Некорректный жанр"
    assert isinstance(name, str), "Некорректный альбом"

    session = connect_db()  # Подключение к базе данных
    existed_album = session.query(Album).filter(Album.album == name, Album.artist == artist).first()
    if existed_album is not None:
        raise AlreadyExists("Альбом уже был записан ранее.")

    new_album = Album(year=year, artist=artist, genre=genre, album=name)

    session.add(new_album)
    session.commit()

    return new_album
