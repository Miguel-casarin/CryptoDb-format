import requests
import csv
import datetime
import time


csv_filename = "coinsfavornaoderproblema.csv"

months = {
    3: (1, 31), 4: (1, 30), 5: (1, 31), 6: (1, 30),
    7: (1, 31), 8: (1, 31), 9: (1, 30), 10: (1, 31),
    11: (1, 30), 12: (1, 31)
}


list_coins = [
    "bitcoin", "ethereum", "ripple", "tether", "binancecoin", 
    "solana", "dogecoin", "cardano", "tron", "chainlink", 
    "stellar", "polkadot", "shiba-inu", "wrapped-bitcoin", "litecoin",
    "ftx-token", "near", "monero", "algorand", "bitcoin-cash", 
    "ethereum-classic", "cosmos", "filecoin", "internet-computer",
    "vechain", "axie-infinity", "the-sandbox", "decentraland",
    "flow", "helium", "eos", "aave", "kusama", 
    "iota", "gala", "the-graph", "bittorrent", 
    "radix", "neo", "kava", "waves", "zcash", "maker", 
    "loopring", "amp-token", "dash", "chiliz", "celo", 
    "nem", "curve-dao-token", "mina-protocol", 
    "basic-attention-token", "stacks", "harmony", "arweave", "1inch", 
    "okb", "qtum", "decred", "icon", "revain", "audius", 
    "kadena", "siacoin", "0x", "ontology", "bancor", 
    "ankr", "livepeer", "nexo", "uma", "skale", "wax", 
    "digibyte", "golem", "serum", "velas", "celer-network", "fetch-ai"
]
# Função para buscar dados de um período específico
def fetch_data(coin, start_timestamp, end_timestamp):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range"
    params = {
        "vs_currency": "usd",
        "from": start_timestamp,
        "to": end_timestamp
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f" Erro na requisição para {coin} ({start_timestamp} - {end_timestamp}): {response.status_code}, {response.text}")
        return None


def process_and_save(coin, data, filename, append=True):
    if not data or "prices" not in data or "market_caps" not in data or "total_volumes" not in data:
        print(f" Dados inválidos recebidos da API para {coin}. Pulando salvamento.")
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

            hourly_data.append([coin, date_time, price, market_cap, volume])
        except IndexError:
            print(f" Erro ao processar índice {i} para {coin}. Pulando esse dado.")

    if not hourly_data:
        print(f" Nenhum dado valido para salvar para {coin}. Pulando escrita no CSV.")
        return

    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not append:
            writer.writerow(["Coin", "Date", "Price", "Market Cap", "Volume"])  # Escreve cabeçalho se for a primeira vez
        writer.writerows(hourly_data)

    print(f" Dados de {coin} salvos com sucesso em {filename}")

# Iterar pelos meses e buscar os dados
for month, (start_day, end_day) in months.items():
    start_date = datetime.datetime(2024, month, start_day)
    end_date = datetime.datetime(2024, month, end_day, 23, 59, 59)
    
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    for coin in list_coins:
        print(f"Buscando dados de {coin} para {start_date.strftime('%Y-%m-%d')} até {end_date.strftime('%Y-%m-%d')}")
        
        data = fetch_data(coin, start_timestamp, end_timestamp)
        process_and_save(coin, data, csv_filename, append=True)
        
        print("Aguardando 2 minutos antes da próxima requisição...")
        time.sleep(120)  # Aguarda 2 minutos

print("Coleta de dados finalizada!")
