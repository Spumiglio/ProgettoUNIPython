import sqlite3
def create_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.executescript('''drop table if exists utenti;
                      CREATE TABLE "utenti"
                    (
                        id text,
                        nome text,
                        cognome text,
                        telefono text,
                        pagamento text,
                        datip text,
                        email text,
                        password text,
                        matricola text,
                        idtessera text
                    );''')
    c.executescript('''drop table if exists ordini;
                        create table ordini (
                        id text ,
                        idprodotto text,
                        data text,
                        quantita text,
                        idOrdine text,
                        dataConsegna text,
                        pagamento text,
                        datipagamento text
                        );''')
    c.executescript('''drop table if exists prodotti;
                        create table prodotti (
                        idprodotto text,
                        nome text ,
                        marca text,
                        quantita text,
                        prezzo text,
                        immagine blob,
                        tag text,
                        categoria text
                        );''')
    c.executescript('''drop table if exists indirizzi;
                        create table indirizzi (
                        id text,
                        via text,
                        CAP text,
                        localita text,
                        provincia text,
                        paese text
                        ); ''')

    c.executescript('''drop table if exists tessere;
                        create table tessere (
                        idtessera text,
                        data text,
                        punti text
                        );''')


    db.commit()
    db.close()


if __name__ == '__main__':
    create_db()

