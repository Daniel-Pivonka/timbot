def getWebopolyStandings(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT users.name, webopoly.wins FROM users, webopoly WHERE users.uid = webopoly.uid ORDER BY wins DESC")
    standings = cursor.fetchall()
    cursor.close()
    return standings
