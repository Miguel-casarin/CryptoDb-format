import sqlite3

# Caminho do banco de dados
db_file = r'C:\Users\migue\Documents\cryptodb2\format\crypto3.db'

def query_inner_join():
    conector = sqlite3.connect(db_file)
    cursor = conector.cursor()
    
    query = """
        SELECT 
            t.date_hour, 
            d.coin_name, 
            v.open, 
            v.closse
        FROM tickey t
        INNER JOIN Ds_coin d ON t.coin_id = d.coin_id
        INNER JOIN viewer v ON t.coin_id = v.coin_id AND DATE(t.date_hour) = v.date
        ORDER BY t.date_hour;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    for row in results:
        print(row)  # Printando os resultados no terminal
    
    cursor.close()
    conector.close()

# Executa a função para exibir os dados no terminal
query_inner_join()
