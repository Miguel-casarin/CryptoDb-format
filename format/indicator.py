import sqlite3

conector = sqlite3.connect(r'C:\Users\migue\Documents\cryptodb2\format\crypto4.db')
cursor = conector.cursor()

cursor.execute("""
    CREATE TABLE indicator (
        date TEXT NOT NULL,
        coin_id INTEGER NOT NULL,
        med_3d FLOAT,
        med_5d FLOAT,
        med_7d FLOAT,
        med_9d FLOAT,
        med_21d FLOAT,
        std_3d FLOAT,
        std_5d FLOAT,
        std_7d FLOAT,
        std_9d FLOAT,
        std_21d FLOAT,
        ifr_5d FLOAT,
        ifr_7d FLOAT,
        ifr_14d FLOAT,
        ifr_21d FLOAT,
        PRIMARY KEY (date, coin_id),
        FOREIGN KEY (coin_id) REFERENCES coin(coin_id) ON DELETE CASCADE
    )
""")

conector.commit()
cursor.close()
conector.close()
