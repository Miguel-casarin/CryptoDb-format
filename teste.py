import requests
import csv
import datetime

# Função para buscar dados para um período específico
def fetch_data(start_timestamp, end_timestamp):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        "vs_currency": "usd",
        "from": start_timestamp,
        "to": end_timestamp
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro na requisição ({start_timestamp} - {end_timestamp}): {response.status_code}, {response.text}")
        return None

# Função para processar os dados e salvar no CSV
def process_and_save(data, filename, append=False):
    if not data or "prices" not in data or "market_caps" not in data or "total_volumes" not in data:
        print("⚠️ Dados inválidos recebidos da API. Pulando salvamento.")
        return
    
    mode = 'a' if append else 'w'
    hourly_data = []

    for i in range(len(data["prices"])):
        try:
            timestamp = data["prices"][i][0] // 1000
            date_time = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            price = data["prices"][i][1]
            market_cap = data["market_caps"][i][1]
            volume = data["total_volumes"][i][1]

            hourly_data.append([date_time, price, market_cap, volume])
        except IndexError:
            print(f"⚠️ Erro ao processar índice {i}. Pulando esse dado.")

    if not hourly_data:
        print("⚠️ Nenhum dado válido para salvar. Pulando escrita no CSV.")
        return

    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not append:
            writer.writerow(["Date", "Price", "Market Cap", "Volume"])  # Escreve cabeçalho se for a primeira vez
        writer.writerows(hourly_data)

    print(f"✅ Dados salvos com sucesso em {filename}")

# Definir datas para o mês de março de 2024
start_date = datetime.datetime(2024, 3, 1)
end_date = datetime.datetime(2024, 3, 31, 23, 59, 59)  # Fim do dia 31 de março de 2024

filename = "bitcoin_march_2024.csv"
first_run = True  

# Buscar dados para o mês de março de 2024
print(f"📡 Buscando dados de {start_date.strftime('%Y-%m-%d')} até {end_date.strftime('%Y-%m-%d')}")

start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

data = fetch_data(start_timestamp, end_timestamp)

process_and_save(data, filename, append=not first_run)

print("🚀 Coleta de dados finalizada!")
