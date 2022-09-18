from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genre = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "Genre add", 201


@genre.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == uid).one()
            return genre_schema.dump(genre), 200
        except Exception:
            return "", 404

    def put(self, uid: int):
        genre = db.session.query(Genre).get(uid)
        req_json = request.json

        genre.id = req_json.get('id')
        genre.name = req_json.get('name')

        db.session.add(genre)
        db.session.commit()

        return "Genre put", 204

    def patch(self, uid: int):
        genre = db.session.query(Genre).get(uid)
        req_json = request.json

        if 'id' in req_json:
            genre.id = req_json.get('id')
        if 'name' in req_json:
            genre.name = req_json.get('name')

        db.session.add(genre)
        db.session.commit()

        return "Genre patch", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "Genre delete", 204
