#!/usr/keio/Anaconda3-2023.09-0/bin/python

from typing import Optional

from flask import Flask

import controllers.index as index_controller
import controllers.players as players_controller
import controllers.matches as matches_controller

from database.util import close_db_connection

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception: Optional[BaseException]) -> None:
    close_db_connection()

@app.route('/')
def index() -> str:
    return index_controller.index()

@app.route('/players')
def players() -> str:
    return players_controller.index()

@app.route('/players/<id>')
def player(id: str) -> str:
    return players_controller.get(id)

@app.route('/players/<id>/edit')
def edit_player(id):
    return players_controller.edit(id)

@app.route('/players/<id>', methods=['POST'])
def edit_player_execute(id):
    return players_controller.exec_update(id)

@app.route('/matches')
def matches() -> str:
    return matches_controller.index()

@app.route('/matches/filter', methods=['POST'])
def filter_matches() -> str:
    return matches_controller.filter()

@app.route('/matches/create')
def add_match() -> str:
    return matches_controller.create()

@app.route('/matches', methods=['POST'])
def add_match_execute():
    return matches_controller.exec_create()

@app.route('/matches/<id>', methods=['POST'])
def delete_match_execute(id: str):
    return matches_controller.exec_delete(id)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
