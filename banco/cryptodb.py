import sqlite3

# Conectar ao banco de dados
conector = sqlite3.connect(r'C:\Users\migue\Documents\cryptodb2\banco\crypto.db')
cursor = conector.cursor()



cursor.execute("""
     CREATE TABLE IF NOT EXISTS price (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT,
        date TEXT,
        price float,
        market_cap float,
        volume float
    )
""")

conector.commit()
cursor.close()
conector.close()