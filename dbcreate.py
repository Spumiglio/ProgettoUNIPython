import sqlite3
def create_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.executescript('''drop table if exists utenti;
                    create table utenti (
                    id text,
                    username text ,
                    password text ,
                    numerot text,
                    ruolo text                
                    );''')
    c.executescript('''drop table if exists ordini;
                        create table ordini (
                        id text ,
                        idprodotto text,
                        data date               
                        );''')
    c.executescript('''drop table if exists prodotti;
                        create table prodotti (
                        nome text ,
                        idprodotto text                   
                        );''')
    c.executescript('''drop table if exists indirizzi;
                        create table indirizzi (
                        id text,
                        via text,
                        CAP text,
                        citta text); ''')

    c.executescript('''drop table if exists tessere;
                        create table tessere (
                        id text,
                        data date,
                        punti text
                        );''')


    db.commit()
    db.close()


if __name__ == '__main__':
    create_db()

