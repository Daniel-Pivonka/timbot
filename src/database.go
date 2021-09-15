def get_webopoly_standings(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT users.name, webopoly.wins FROM users, webopoly WHERE users.uid = webopoly.uid ORDER BY wins DESC')
    standings = cursor.fetchall()
    cursor.close()
    return standings


def increment_webopoly_wins(conn, name):
    cursor = conn.cursor()
    uid = int(cursor.execute('SELECT uid FROM users WHERE name = "{}"'.format(name)))
    wins = int(cursor.execute('SELECT wins FROM webopoly WHERE uid = {}'.format(uid)))
    cursor.execute('UPDATE webopoly SET wins = {} WHERE uid = {}'.format(wins + 1, uid))
    conn.commit()
    cursor.close()
    return None
