def register(username,password,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti_password u WHERE u.username=?", (username,))
    res = ver.fetchall()
    if res != []:
        s = "USERNAME GIA UTILIZZATO"
    else:
        c.execute("INSERT INTO utenti_password VALUES (?,?,?)",(username,password,1))
        s = "OK"
    db.commit()
    return s

def login(username,password,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti_password u WHERE u.username=? AND u.password=?", (username,password))
    res = ver.fetchall()
    if res == []:
        s = "LOGIN ERRATO"
    else:
        s = res[0][2]
    return s