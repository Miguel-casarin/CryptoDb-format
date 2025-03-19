from datetime import datetime

day_coins = []

def ajustar_hora(data_str):
    dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    dt_ajustado = dt.replace(minute=0, second=0)
    return dt_ajustado.strftime("%Y-%m-%d %H:%M:%S")

def lista_calculos(coin, date):
    while coin == coin_selec and date == date_selec:
        day_coins.append(coin.price)
        #criar uma forma de apagar esses dados depois da lista ser usada

# tira a hora da string
def extrair_data(data_str):
    return data_str.split(" ")[0]

def max(day_coins):
    return max(day_coins)

def lower(day_coins):
    return lower(day_coins)

def open(day_coins, date,):
    return day_coins[0]

def closse(day_coins, date):
    return day_coins.pop()



