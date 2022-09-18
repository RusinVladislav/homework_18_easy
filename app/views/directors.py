from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

director = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "Director add", 201


@director.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = db.session.query(Director).filter(Director.id == uid).one()
            return director_schema.dump(director), 200
        except Exception:
            return "", 404

    def put(self, uid: int):
        director = db.session.query(Director).get(uid)
        req_json = request.json

        director.id = req_json.get('id')
        director.name = req_json.get('name')

        db.session.add(director)
        db.session.commit()

        return "Director put", 204

    def patch(self, uid: int):
        director = db.session.query(Director).get(uid)
        req_json = request.json

        if 'id' in req_json:
            director.id = req_json.get('id')
        if 'name' in req_json:
            director.name = req_json.get('name')

        db.session.add(director)
        db.session.commit()

        return "Director patch", 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        db.session.delete(director)
        db.session.commit()
        return "Director delete", 204
