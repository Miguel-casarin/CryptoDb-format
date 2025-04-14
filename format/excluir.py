import sqlite3

conector = sqlite3.connect(r'C:\Users\migue\Documents\cryptodb2\format\crypto4.db')
cursor = conector.cursor()
cursor.execute("DROP TABLE IF EXISTS indicator;")
conector.commit()