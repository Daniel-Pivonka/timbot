def get_webopoly_standings(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT users.name, webopoly.wins FROM users, webopoly WHERE users.uid = webopoly.uid ORDER BY wins DESC')
    standings = cursor.fetchall()
    cursor.close()
    return standings


def increment_weboploy_wins(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE webopoly SET wins = wins + 1 WHERE webopoly.uid = (SELECT uid FROM users WHERE name = "{}")'.format(name))
        conn.commit()
        cursor.close()
        return 1
    except Exception as e:
        return e
