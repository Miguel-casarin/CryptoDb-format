import sqlite3
import csv

# Conectar ao banco de dados
conector = sqlite3.connect(r'C:\Users\migue\Documents\cryptodb2\banco\crypto.db')
cursor = conector.cursor()


cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_coin_date ON price (coin, date);")

caminho_arquivo = r'C:\Users\migue\Documents\cryptodb2\banco\coins.csv'

with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    leitor = csv.reader(arquivo)  # Criar o leitor CSV
    next(leitor)  # Pular cabeçalho
    
    for linha in leitor:
        if len(linha) < 5:  
            continue
        
        coin, date, price, market_cap, volume = linha

        
        cursor.execute("""
            INSERT OR IGNORE INTO price (coin, date, price, market_cap, volume)
            VALUES (?, ?, ?, ?, ?)
        """, (coin, date, float(price), float(market_cap), float(volume)))


conector.commit()
cursor.close()
conector.close()

print("Importação concluída com sucesso!")
