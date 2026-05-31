import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adildiasismail777$",
    database="booharik"
)

cursor = db.cursor()

def add_user(telegram_id, username):

    cursor.execute(
        """
        INSERT IGNORE INTO users
        (telegram_id, username)
        VALUES (%s, %s)
        """,
        (telegram_id, username)
    )

    db.commit()

def get_users_count():

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    return cursor.fetchone()[0]

def sohranit_anketu(
    telegram_id,
    tekst,
    foto,
    strana,
    gorod,
    pol,
    vozrast
):

    cursor.execute(
        """
        INSERT INTO profiles
        (
            telegram_id,
            tekst,
            foto,
            strana,
            gorod,
            pol,
            vozrast
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)

        ON DUPLICATE KEY UPDATE
            tekst = VALUES(tekst),
            foto = VALUES(foto),
            strana = VALUES(strana),
            gorod = VALUES(gorod),
            pol = VALUES(pol),
            vozrast = VALUES(vozrast)
        """,
        (
            telegram_id,
            tekst,
            foto,
            strana,
            gorod,
            pol,
            vozrast
        )
    )

    db.commit()

def poluchit_anketu(telegram_id):

    cursor.execute(
        """
        SELECT
            telegram_id,
            tekst,
            foto,
            strana,
            gorod,
            pol,
            vozrast,
            prosmotry,
            laiki,
            status
        FROM profiles
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    return cursor.fetchone()

def poluchit_vse_ankety():

    cursor.execute(
        """
        SELECT
            telegram_id,
            tekst,
            foto,
            strana,
            gorod,
            pol,
            vozrast,
            prosmotry,
            laiki,
            status
        FROM profiles
        """
    )

    return cursor.fetchall()

def kolichestvo_anket():

    cursor.execute(
        "SELECT COUNT(*) FROM profiles"
    )

    return cursor.fetchone()[0]

def udalit_anketu(telegram_id):

    cursor.execute(
        """
        DELETE FROM profiles
        WHERE telegram_id=%s
        """,
        (telegram_id,)
    )

    db.commit()