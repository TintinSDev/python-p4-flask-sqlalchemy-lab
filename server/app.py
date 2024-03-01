#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
     animal = Animal.query.get_or_404(id)
     response_data = f"<ul>ID: {animal.id}</li><li>Name: {animal.name}</li><li>Species:{animal.species}</li><li>Zookeper: {animal.zookeeper.name}</li><li>Enclosure: {animal.enclosure.environment}</li></ul>"
     return make_response(response_data, 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    animals_list = '<li>' + '</li><li>'.join([animal.name for animal in zookeeper.animals]) + '</li>'
    response_data = f"<ul><li>Name: {zookeeper.name}</li><li>Birthday: {str(zookeeper.birthday)}</li><li>{len(zookeeper.animals)} Animal:<ul>{animals_list}</ul></li></ul>"
    return make_response(response_data, 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    animals_list = '<li>' + '</li><li>'.join([animal.name for animal in enclosure.animals]) + '</li>'
    response_data = f"<ul><li>Environment: {enclosure.environment} Open to Visitors: {'open to visitors' if enclosure.open_to_visitors else 'not open to visitors'}</li><li>{len(enclosure.animals)} Animals:<ul>{animals_list}</ul></li></ul>"
    return make_response(response_data, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
