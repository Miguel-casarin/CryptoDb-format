import numpy
import sqlite3 as sq

conector = sq.connect(r'C:\Users\migue\Documents\cryptodb2\format\crypto4.db')
cursor = conector.cursor()

def media_total():
    cursor.execute("SELECT price FROM price;")
    valores = [linha[0] for linha in cursor.fetchall()]

    return numpy.mean(valores) if valores else None

#resultados_total = media_total()
#print("media: ", resultados_total)

def media_intervalada(intervalo):
    cursor.execute("SELECT price FROM price;")
    valores = [linha[0] for linha in cursor.fetchall()]
    desvios = []

    for i in range(0, len(valores), intervalo):
            grupo = valores[i:i+intervalo]  
            desvios.append(numpy.mean(grupo))
    
    return desvios


#resultados_intervalo = media_intervalada(3)
#print("Médias dos preços (de 3 em 3):", resultados_intervalo)

def desvio_padrao_total():
     cursor.execute("SELECT price FROM price;")
     valores = [linha[0] for linha in cursor.fetchall()]

     return numpy.std(valores) if valores else None
     
#desvio_padrao_total_res = desvio_padrao_total()
#print(desvio_padrao_total_res)

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