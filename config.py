from typing import Final

RESULT_MESSAGES: Final[dict[str, str]] = {
    'added': '結果を追加しました',
    'deleted': '削除しました',
    'updated': '更新しました'
}

ERR_CODE_MESSAGES: Final[dict[str, str]] = {
    'params-must-be-integer': 'パラメータ存在してないか整数であるべきパラメータが整数ではないです',
    'loser-game-count-invalid': '敗者のゲーム数が不正です',
    'score-invalid': 'スコアが不正です',
    'player-not-found': 'プレイヤーが見つかりません',
    'match-meta-not-found': '試合メタが見つかりません',
    'database-error': 'データベースエラー',
    'player-is-same': '勝者と敗者が同じです',
    'match-not-found': '試合が見つかりません',
    'name-invalid': '名前が不正です',
    'grade-invalid': '学年が不正です',
    'sex-invalid': '性別が不正です',
    'university-not-found': '大学が見つかりません'
}
