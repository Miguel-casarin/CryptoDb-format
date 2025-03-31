import csv
import sqlite3
from datetime import datetime

# Caminhos dos arquivos
csv_file = r'C:\Users\migue\Documents\cryptodb2\coinsfavornaoderproblema.csv'
db_file = r'C:\Users\migue\Documents\cryptodb2\format\crypto3.db'

# Funções para manipulação de dados
def ajustar_hora(data_str):
    dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    dt_ajustado = dt.replace(minute=0, second=0)
    return dt_ajustado.strftime("%Y-%m-%d %H:%M:%S")

def extrair_data(data_str):
    return data_str.split(" ")[0]

def processar_csv_e_inserir():
    conector = sqlite3.connect(db_file)
    cursor = conector.cursor()
    
    # Dicionário para armazenar os preços por moeda e data
    day_coins = {}
    
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            coin = row['coin']
            date_hour = ajustar_hora(row['Date'])
            date_only = extrair_data(row['Date'])
            price = float(row['Price'])
            market_cap = float(row['Market Cap'])
            volume = float(row['Volume'])
            
            # Inserir na tabela Ds_coin
            cursor.execute("INSERT OR IGNORE INTO Ds_coin (coin_name) VALUES (?)", (coin,))
            cursor.execute("SELECT coin_id FROM Ds_coin WHERE coin_name = ?", (coin,))
            coin_id = cursor.fetchone()[0]
            
            # Inserir na tabela tickey
            cursor.execute("""
                INSERT OR REPLACE INTO tickey (coin_id, date_hour, price, volume, market_camp)
                VALUES (?, ?, ?, ?, ?)
            """, (coin_id, date_hour, price, volume, market_cap))
            
            # Armazenar preços para cálculo posterior
            if (coin_id, date_only) not in day_coins:
                day_coins[(coin_id, date_only)] = []
            day_coins[(coin_id, date_only)].append(price)
    
    # Processar e inserir na tabela viewer
    for (coin_id, date), prices in day_coins.items():
        open_price = prices[0]
        close_price = prices[-1]
        max_price = max(prices)
        min_price = min(prices)
        
        cursor.execute("""
            INSERT OR REPLACE INTO viewer (date, coin_id, open, closse, max, lower)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, coin_id, open_price, close_price, max_price, min_price))
    
    conector.commit()
    cursor.close()
    conector.close()

if __name__ == "__main__":
    processar_csv_e_inserir()
