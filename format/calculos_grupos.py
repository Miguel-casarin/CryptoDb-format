import numpy
import pandas as pd
import sqlite3 as sq

intervalos_med_des = [3, 5, 7, 9, 21]
intervalos_ifr = [5, 7, 14, 21]

conector = sq.connect(r'C:\Users\migue\Documents\cryptodb2\format\crypto4.db')
cursor = conector.cursor()

def media_total():
    lista_moedas = list(range(1, 80))  # lista de 1 a 79
    medias = {}

    for moeda in lista_moedas:
        cursor.execute("SELECT price FROM price WHERE coin_id = ?;", (moeda,))
        valores = [linha[0] for linha in cursor.fetchall()]
        
        medias[moeda] = numpy.mean(valores) 

    return medias

#res_media_total = media_total()
#print(res_media_total)

def media_intervalada(intervalo):
    lista_moedas = list(range(1, 80))  
    desvios_intervalados = {}

    for moeda in lista_moedas:
        cursor.execute("SELECT price FROM price WHERE coin_id = ? ORDER BY date_hour;", (moeda,))
        valores = [linha[0] for linha in cursor.fetchall()]
        desvios_por_moeda = []

        for i in range(0, len(valores), intervalo):
            grupo = valores[i:i+intervalo]
            desvios_por_moeda.append(numpy.mean(grupo))
        
        desvios_intervalados[moeda] = desvios_por_moeda
    
    return desvios_intervalados

#res_media_intervalada = media_intervalada(3)
#print(res_media_intervalada)

def desvio_padrao_total():
    lista_moedas = list(range(1, 80))  # lista de 1 a 79
    desvios = {}

    for moeda in lista_moedas:
        cursor.execute("SELECT price FROM price WHERE coin_id = ?;", (moeda,))
        valores = [linha[0] for linha in cursor.fetchall()]
        
        desvios[moeda] = numpy.std(valores) if valores else None

    return desvios

     
#desvio_padrao_total_res = desvio_padrao_total()
#print(desvio_padrao_total_res)

def desvio_padrao_inter(intervalo):
    lista_moedas = list(range(1, 80))  
    desvios_intervalados = {}

    for moeda in lista_moedas:
        cursor.execute("SELECT price FROM price WHERE coin_id = ? ORDER BY date_hour;", (moeda,))
        valores = [linha[0] for linha in cursor.fetchall()]
        desvios_por_moeda = []

        for i in range(0, len(valores), intervalo):
            grupo = valores[i:i+intervalo]
            desvios_por_moeda.append(numpy.std(grupo))
        
        desvios_intervalados[moeda] = desvios_por_moeda
    
    return desvios_intervalados

def desvio_padrao_total(intervalo):
      cursor.execute("SELECT price FROM price;")
      valores = [linha[0] for linha in cursor.fetchall()]
      desvios = []

      for i in range(0, len(valores), intervalo):
            grupo = valores[i:i+intervalo]  
            desvios.append(numpy.std(grupo))
    
      return desvios

#res_desvios = desvio_padrao_inter(3)
#print(res_desvios)

def ifr_total(intervalo):
    lista_moedas = list(range(1,80))
    rsis = {}

    for moeda in lista_moedas:
        cursor.execute("SELECT date, close FROM movement_diary WHERE coin_id = ? ORDER BY date;", (moeda,))
        dados = cursor.fetchall()

        df = pd.DataFrame(dados, columns=['date', 'close'])
        df['close'] = df['close'].astype(float)

        df['delta'] = df['close'].diff()
        df['gain'] = df['delta'].clip(lower=0)
        df['loss'] = -df['delta'].clip(upper=0)

        df['avg_gain'] = df['gain'].ewm(alpha=1/intervalo, min_periods=intervalo).mean()
        df['avg_loss'] = df['loss'].ewm(alpha=1/intervalo, min_periods=intervalo).mean()

        df['rs'] = df['avg_gain'] / df['avg_loss']
        df['rsi'] = 100 - (100 / (1 + df['rs']))

        rsis[moeda] = df['rsi'].iloc[-1] if not df['rsi'].empty else None

    return rsis
def ifr(intervalo):
    lista_moedas = list(range(1, 80))
    rsis = {}

    for moeda in lista_moedas:
        cursor.execute("""
            SELECT date, close FROM movement_diary 
            WHERE coin_id = ? 
            ORDER BY date
        """, (moeda,))
        dados = cursor.fetchall()

        if not dados:
            continue

        df = pd.DataFrame(dados, columns=['date', 'close'])
        df['close'] = df['close'].astype(float)

        df['delta'] = df['close'].diff()
        df['gain'] = df['delta'].clip(lower=0)
        df['loss'] = -df['delta'].clip(upper=0)

        df['avg_gain'] = df['gain'].ewm(alpha=1/intervalo, min_periods=intervalo).mean()
        df['avg_loss'] = df['loss'].ewm(alpha=1/intervalo, min_periods=intervalo).mean()

        df['rs'] = df['avg_gain'] / df['avg_loss']
        df['rsi'] = 100 - (100 / (1 + df['rs']))

        # Cria dicionário {data: rsi} para essa moeda
        rsis[moeda] = df[['date', 'rsi']].dropna().set_index('date')['rsi'].to_dict()

    return rsis

#resultado_ifr = ifr(14) 
#print(resultado_ifr)

def insert_media():
    for intervalo in intervalos_med_des:
        medias = media_intervalada(intervalo)

        for coin_id, lista_medias in medias.items():
            for idx, media_valor in enumerate(lista_medias):
                cursor.execute("""
                    SELECT date_hour FROM price 
                    WHERE coin_id = ? 
                    ORDER BY date_hour 
                    LIMIT 1 OFFSET ?
                """, (coin_id, idx * intervalo))
                resultado = cursor.fetchone()
                if resultado is None:
                    continue
                data = resultado[0][:10]  

                col_nome = f"med_{intervalo}d"
                cursor.execute(f"""
                    INSERT OR REPLACE INTO indicator (date, coin_id, {col_nome})
                    VALUES (?, ?, ?)
                    ON CONFLICT(date, coin_id) DO UPDATE SET {col_nome} = excluded.{col_nome}
                """, (data, coin_id, media_valor))

    conector.commit()

def insert_desvio():
    for intervalo in intervalos_med_des:
        desvios = desvio_padrao_inter(intervalo)

        for coin_id, lista_desvios in desvios.items():
            for idx, desvio_valor in enumerate(lista_desvios):
                cursor.execute("""
                    SELECT date_hour FROM price 
                    WHERE coin_id = ? 
                    ORDER BY date_hour 
                    LIMIT 1 OFFSET ?
                """, (coin_id, idx * intervalo))
                resultado = cursor.fetchone()
                if resultado is None:
                    continue
                data = resultado[0][:10]

                col_nome = f"std_{intervalo}d"
                cursor.execute(f"""
                    INSERT OR REPLACE INTO indicator (date, coin_id, {col_nome})
                    VALUES (?, ?, ?)
                    ON CONFLICT(date, coin_id) DO UPDATE SET {col_nome} = excluded.{col_nome}
                """, (data, coin_id, desvio_valor))

    conector.commit()

def insert_ifr():
    for intervalo in intervalos_ifr:
        ifrs = ifr(intervalo) 
        for coin_id, valores_diarios in ifrs.items():
            for data, rsi_valor in valores_diarios.items():
                col_nome = f"ifr_{intervalo}d"

                cursor.execute(f"""
                    INSERT OR REPLACE INTO indicator (date, coin_id, {col_nome})
                    VALUES (?, ?, ?)
                    ON CONFLICT(date, coin_id) DO UPDATE SET {col_nome} = excluded.{col_nome}
                """, (data, coin_id, rsi_valor))

    conector.commit()


insert_media()
insert_desvio()
insert_ifr()

conector.close()