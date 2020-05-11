import sqlite3
def create_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.executescript('''drop table if exists utenti_password;
                    create table utenti_password (
                    username text ,
                    password text ,
                    id integer                  
                    );''')
    c.executescript('''drop table if exists ordini;
                        create table ordini (
                        id integer ,
                        idprodotto integer               
                        );''')
    c.executescript('''drop table if exists prodotti;
                        create table prodotti (
                        nome text ,
                        idprodotto integer                   
                        );''')
    db.commit()
    db.close()


if __name__ == '__main__':
    create_db()

