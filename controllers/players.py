from flask import render_template, request, redirect, url_for
from database.util import get_db
from config import RESULT_MESSAGES, ERR_CODE_MESSAGES
from util import has_control_character
import sqlite3

def index() -> str:
    con = get_db()
    cur = con.cursor()
    players = cur.execute('SELECT * FROM player_details').fetchall()
    return render_template('players.html', players=players)

def get(id: str) -> str:
    if request.args.get('code') is None:
        code = ""
    else:
        code = RESULT_MESSAGES[request.args.get('code')]
    con = get_db()
    cur = con.cursor()
    player = cur.execute('SELECT * FROM player_details WHERE id = ?', (id,)).fetchone()
    if player is None:
        return render_template('player-not-found.html')
    return render_template('player.html', player=player, code=code)

def edit(id):
    if request.args.get('err_code') is None:
        code = ""
    else:
        code = ERR_CODE_MESSAGES[request.args.get('err_code')]
    con = get_db()
    cur = con.cursor()
    player = cur.execute('SELECT * FROM player_details WHERE id = ?', (id,)).fetchone()
    if player is None:
        return render_template('player-not-found.html')
    universities = cur.execute('SELECT * FROM universities').fetchall()
    return render_template('edit_player.html', player=player, universities=universities, code=code)

def exec_update(id):
    name = request.form.get('name')
    grade = request.form.get('grade')
    university_id = request.form.get('univ_id')
    sex = request.form.get('sex')

    if name is None or has_control_character(name) or len(name) == 0:
        return redirect(url_for('edit_player', id=id, err_code='name-invalid'))

    try:
        grade = int(grade)
        university_id = int(university_id)
    except ValueError:
        return redirect(url_for('edit_player', id=id, err_code='params-must-be-integer'))

    if grade < 1 or grade > 4:
        return redirect(url_for('edit_player', id=id, err_code='grade-invalid'))

    if sex is None or not (sex == "男子" or sex == "女子"):
        return redirect(url_for('edit_player', id=id, err_code='sex-invalid'))

    con = get_db()
    cur = con.cursor()
    university = cur.execute('SELECT * FROM universities WHERE id = ?', (university_id,)).fetchone()
    if university is None:
        return redirect(url_for('edit_player', id=id, err_code='university-not-found'))

    try:
        cur.execute('''
            UPDATE players SET name = ?, grade = ?, sex = ?, university_id = ?
                WHERE id = ?
        ''', (name, grade, sex, university_id, id))
    except sqlite3.Error:
        return redirect(url_for('edit_player', id=id, err_code='database-error'))

    con.commit()

    return redirect(url_for('player', id=id , code="updated"))
