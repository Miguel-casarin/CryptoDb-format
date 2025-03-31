import sqlite3

conector = sqlite3.connect(r'C:\Users\migue\Documents\cryptodb2\format\crypto3.db')
cursor = conector.cursor()



cursor.execute("""
    CREATE TABLE ds_coin (
    coin_id INTEGER PRIMARY KEY,  
    coin_name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE tickey (
    coin_id INTEGER NOT NULL,      
    date_hour TEXT NOT NULL,       
    price INTEGER NOT NULL,        
    volume INTEGER NOT NULL,       
    market_camp INTEGER NOT NULL,  
    PRIMARY KEY (coin_id, date_hour),  
    FOREIGN KEY (coin_id) REFERENCES ds_coin(coin_id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE viewer (
    date TEXT NOT NULL,            
    coin_id INTEGER NOT NULL,       
    open INTEGER NOT NULL,          
    close INTEGER NOT NULL,        
    max INTEGER NOT NULL,           
    lower FLOAT NOT NULL,           
    PRIMARY KEY (date, coin_id),  
    FOREIGN KEY (coin_id) REFERENCES ds_coin(coin_id) ON DELETE CASCADE
    );
""")

conector.commit()
cursor.close()
conector.close()