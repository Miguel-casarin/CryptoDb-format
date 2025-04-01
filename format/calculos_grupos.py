import numpy
import sqlite3 as sq

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

def desvio_padrao_inter(intervalo):
      cursor.execute("SELECT price FROM price;")
      valores = [linha[0] for linha in cursor.fetchall()]
      desvios = []

      for i in range(0, len(valores), intervalo):
            grupo = valores[i:i+intervalo]  
            desvios.append(numpy.std(grupo))
    
      return desvios

res_desvios = desvio_padrao_inter(3)
print(res_desvios)

conector.close()