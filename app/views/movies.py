from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie

movie = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = db.session.query(Movie).all()
        movies = movies_schema.dump(all_movies)

        # задаем количество элементов на странице
        LIMIT = 5

        # получаем значение из адресной строки по ключу "page"
        item = request.args.get("page")

        # делаем проверку на полученное значение из адресной страницы
        if item is None:
            page_n = request.args.get("page", 1)
        elif item.isdigit():
            page_n = int(item)
        else:
            page_n = request.args.get("page", 1)

        # выводим необходимое количество элементов в зависимости от страницы
        items_to_show = movies[(page_n - 1) * LIMIT:page_n * LIMIT]

        return items_to_show, 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "Movie add", 201


@movie.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == uid).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404

    def put(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        req_json = request.json

        movie.id = req_json.get('id')
        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()

        return "Move put", 204

    def patch(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        req_json = request.json

        if 'id' in req_json:
            movie.id = req_json.get('id')
        if 'title' in req_json:
            movie.title = req_json.get('title')
        if 'description' in req_json:
            movie.description = req_json.get('description')
        if 'trailer' in req_json:
            movie.trailer = req_json.get('trailer')
        if 'year' in req_json:
            movie.year = req_json.get('year')
        if 'rating' in req_json:
            movie.rating = req_json.get('rating')
        if 'genre_id' in req_json:
            movie.genre_id = req_json.get('genre_id')
        if 'director_id' in req_json:
            movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()

        return "Move patch", 204

    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "Move delete", 204


@movie.route('/director/<int:did>')
class MovieView(Resource):
    def get(self, did: int):
        try:
            movie = db.session.query(Movie).filter(Movie.director_id == did).all()
            return movies_schema.dump(movie), 200
        except Exception:
            return "", 404


@movie.route('/genre/<int:gid>')
class MovieView(Resource):
    def get(self, gid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.genre_id == gid).all()
            return movies_schema.dump(movie), 200
        except Exception:
            return "", 404


@movie.route('/director/<int:did>/genre/<int:gid>')
class MovieView(Resource):
    def get(self, did: int, gid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.director_id == did, Movie.genre_id == gid).all()
            return movies_schema.dump(movie), 200
        except Exception:
            return "", 404
