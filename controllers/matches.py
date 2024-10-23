from flask import render_template, request, redirect, url_for, jsonify
from database.util import get_db
from config import RESULT_MESSAGES, ERR_CODE_MESSAGES
import sqlite3

def index() -> str:
    con = get_db()
    cur = con.cursor()

    if request.args.get('player_id') is not None:
        if request.args.get('sex') is not None:
            if request.args.get('match_meta_id') is not None:
                matches = cur.execute( '''SELECT * FROM result_details WHERE (winner_id = ? OR loser_id = ?)
                        AND sex = ?
                        AND match_meta_id = ?
                    ''', (request.args.get('player_id'), request.args.get('player_id'), request.args.get('sex'), request.args.get('match_meta_id'))).fetchall()
            else:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE (winner_id = ? OR loser_id = ?) AND sex = ?
                    ''', (request.args.get('player_id'), request.args.get('player_id'), request.args.get('sex'))).fetchall()
        else:
            if request.args.get('match_meta_id') is not None:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE (winner_id = ? OR loser_id = ?)
                        AND match_meta_id = ?
                    ''', (request.args.get('player_id'), request.args.get('player_id'), request.args.get('match_meta_id'))).fetchall()
            else:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE winner_id = ? OR loser_id = ?
                    ''', (request.args.get('player_id'), request.args.get('player_id'))).fetchall()
    else:
        if request.args.get('sex') is not None:
            if request.args.get('match_meta_id') is not None:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE sex = ? AND match_meta_id = ?
                    ''', (request.args.get('sex'), request.args.get('match_meta_id'))).fetchall()
            else:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE sex = ?
                    ''', (request.args.get('sex'),)).fetchall()
        else:
            if request.args.get('match_meta_id') is not None:
                matches = cur.execute(
                    '''SELECT * FROM result_details
                        WHERE match_meta_id = ?
                    ''', (request.args.get('match_meta_id'),)).fetchall()
            else:
                matches = cur.execute('SELECT * FROM result_details').fetchall()

    if request.args.get('code') is None:
        code = ""
        if request.args.get('err_code') is None:
            err_code = ""
        else:
            err_code = ERR_CODE_MESSAGES[request.args.get('err_code')]
    else:
        code = RESULT_MESSAGES[request.args.get('code')]
        err_code = ""

    players = cur.execute('SELECT * FROM player_details').fetchall()
    match_metas = cur.execute('SELECT * FROM match_metas').fetchall()
    return render_template('matches.html', matches=matches, players=players, match_metas=match_metas,
                           player_id=int(request.args.get('player_id')) if request.args.get('player_id') is not None else 0,
                           match_meta_id=int(request.args.get('match_meta_id')) if request.args.get('match_meta_id') is not None else 0,
                           sex=request.args.get('sex') if request.args.get('sex') is not None else None,
                           code=code, err_code=err_code
    )

def filter() -> str:
    if request.form['player_id'] == '0':
        player_id = None
    else:
        player_id = request.form['player_id']

    if request.form['sex'] == '1':
        sex = "男子"
    elif request.form['sex'] == '2':
        sex = "女子"
    else:
        sex = None

    if request.form['match_meta_id'] == '0':
        match_meta_id = None
    else:
        match_meta_id = request.form['match_meta_id']

    return redirect(url_for('matches', player_id=player_id, sex=sex, match_meta_id=match_meta_id))

def create() -> str:
    if request.args.get('err_code') is None:
        code = ""
    else:
        code = ERR_CODE_MESSAGES[request.args.get('err_code')]

    con = get_db()
    cur = con.cursor()
    players = cur.execute('SELECT * FROM player_details').fetchall()
    match_metas = cur.execute('SELECT * FROM match_metas').fetchall()
    return render_template('add_match.html', players=[ dict(row) for row in players ], match_metas=[dict(row) for row in match_metas], code=code)

def exec_create():
    loser_game_count = request.form.get('loser_game_count')
    winner_game1_score = request.form.get('winner_game1_score')
    winner_game2_score = request.form.get('winner_game2_score')
    winner_game3_score = request.form.get('winner_game3_score')
    loser_game1_score = request.form.get('loser_game1_score')
    loser_game2_score = request.form.get('loser_game2_score')
    loser_game3_score = request.form.get('loser_game3_score')
    winner_id = request.form.get('winner_id')
    loser_id = request.form.get('loser_id')
    match_meta_id = request.form.get( 'match_meta_id' )

    try:
        loser_game_count = int(loser_game_count)
        winner_game1_score = int(winner_game1_score)
        winner_game2_score = int(winner_game2_score)
        loser_game1_score = int(loser_game1_score)
        loser_game2_score = int(loser_game2_score)
        winner_id = int(winner_id)
        loser_id = int(loser_id)
        match_meta_id = int(match_meta_id)
    except ValueError:
        return redirect(url_for('add_match', err_code='params-must-be-integer'))

    if not (loser_game_count == 0 or loser_game_count == 1):
        return redirect(url_for('add_match', err_code='loser-game-count-invalid'))

    game1_winner_score = max(winner_game1_score, loser_game1_score)
    game1_loser_score = min(winner_game1_score, loser_game1_score)
    game2_winner_score = max(winner_game2_score, loser_game2_score)
    game2_loser_score = min(winner_game2_score, loser_game2_score)

    if game1_winner_score - 2 < game1_loser_score or game2_winner_score - 2 < game2_loser_score:
        return redirect(url_for('add_match', err_code='score-invalid'))

    if game1_winner_score < 11 or game2_winner_score < 11 or game1_loser_score < 0 or game2_loser_score < 0:
        return redirect(url_for('add_match', err_code='score-invalid'))

    if game1_winner_score != 11 and game1_winner_score - game1_loser_score != 2:
        return redirect(url_for('add_match', err_code='score-invalid'))

    if game2_winner_score != 11 and game2_winner_score - game2_loser_score != 2:
        return redirect(url_for('add_match', err_code='score-invalid'))

    con = get_db()
    cur = con.cursor()

    if winner_id == loser_id:
        return redirect(url_for('add_match', err_code='player-is-same'))

    winner = cur.execute('SELECT * FROM players WHERE id = ?', (winner_id,)).fetchone()
    if winner is None:
        return redirect(url_for('add_match', err_code='player-not-found'))

    loser = cur.execute('SELECT * FROM players WHERE id = ?', (loser_id,)).fetchone()
    if loser is None:
        return redirect(url_for('add_match', err_code='player-not-found'))

    match_meta = cur.execute('SELECT * FROM match_metas WHERE id = ?', (match_meta_id,)).fetchone()
    if match_meta is None:
        return redirect(url_for('add_match', err_code='match-meta-not-found'))

    if loser_game_count == 1:
        try:
            winner_game3_score = int(winner_game3_score)
            loser_game3_score = int(loser_game3_score)
        except ValueError:
            return redirect(url_for('add_match', err_code='params-must-be-integer'))

        if winner_game3_score - 2 < loser_game3_score:
            return redirect(url_for('add_match', err_code='score-invalid'))

        if winner_game3_score != 11 and winner_game3_score - loser_game3_score != 2:
            return redirect(url_for('add_match', err_code='score-invalid'))
        try:
            cur.execute('''
                INSERT INTO match_results
                    (winner_game_count, loser_game_count,
                        winner_game1_score, winner_game2_score, winner_game3_score,
                        loser_game1_score, loser_game2_score, loser_game3_score,
                        winner_id, loser_id, match_meta_id
                    )
                VALUES (2, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                    loser_game_count,
                    winner_game1_score,
                    winner_game2_score,
                    winner_game3_score,
                    loser_game1_score,
                    loser_game2_score,
                    loser_game3_score,
                    winner_id,
                    loser_id,
                    match_meta_id,
                ))
        except sqlite3.Error:
            # データベースエラーが発生
            return redirect(url_for('add_match',err_code='database-error'))
    else:
        try:
            cur.execute('''
                INSERT INTO match_results
                    (winner_game_count, loser_game_count,
                        winner_game1_score, winner_game2_score,
                        loser_game1_score, loser_game2_score,
                        winner_id, loser_id, match_meta_id
                    )
                VALUES (2, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                    loser_game_count,
                    winner_game1_score,
                    winner_game2_score,
                    loser_game1_score,
                    loser_game2_score,
                    winner_id,
                    loser_id,
                    match_meta_id,
                ))
        except sqlite3.Error:
            # データベースエラーが発生
            return redirect(url_for('add_match',err_code='database-error'))

    con.commit()
    return redirect(url_for('matches'))

def exec_delete(id: str):
    con = get_db()
    cur = con.cursor()
    match = cur.execute('SELECT * FROM match_results WHERE id = ?', (id,)).fetchone()
    if match is None:
        return redirect(url_for('matches', err_code='match-not-found'))
    try:
        cur.execute('DELETE FROM match_results WHERE id = ?', (id,))
    except sqlite3.Error:
        return redirect(url_for('matches', err_code='database-error'))
    con.commit()
    return redirect(url_for('matches', code='deleted'))
