import requests
import csv
import datetime


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
    "tezos", "flow", "helium", "eos", "aave", "kusama", 
    "quant", "iota", "gala", "the-graph", "bittorrent", 
    "radix", "neo", "kava", "waves", "zcash", "maker", 
    "loopring", "amp-token", "dash", "chiliz", "celo", 
    "nem", "curve-dao-token", "mina-protocol", 
    "basic-attention-token", "stacks", "harmony", "arweave", "1inch", 
    "okb", "qtum", "decred", "icon", "revain", "audius", 
    "kadena", "siacoin", "0x", "ontology", "bancor", 
    "ankr", "livepeer", "nexo", "uma", "skale", "wax", 
    "digibyte", "golem", "serum", "velas", "celer-network", "fetch-ai"
]


def fetch_data(crypto, start_timestamp, end_timestamp):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart/range"
    params = {
        "vs_currency": "usd",
        "from": start_timestamp,
        "to": end_timestamp
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição para {crypto} ({start_timestamp} - {end_timestamp}): {response.status_code}, {response.text}")
        return None


def process_and_save(crypto, data, filename, append=False):
    if not data or "prices" not in data or "market_caps" not in data or "total_volumes" not in data:
        print(f"Dados inválidos para {crypto}. Pulando salvamento.")
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
            print(f"Erro ao processar índice {i} para {crypto}. Pulando esse dado.")

    if not hourly_data:
        print(f"Nenhum dado válido para {crypto}. Pulando escrita no CSV.")
        return

    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not append:
            writer.writerow(["Date", "Price", "Market Cap", "Volume"])
        writer.writerows(hourly_data)

    print(f"Dados de {crypto} salvos em {filename}")


def run_data_collection():
    for crypto in list_coins:
        for month, (start_day, end_day) in months.items():
            start_date = datetime.datetime(2024, month, start_day)
            end_date = datetime.datetime(2024, month, end_day, 23, 59, 59)
            
            csv_filename = f"{crypto}_{start_date.strftime('%B_%Y')}.csv"
            
            print(f"Buscando dados de {crypto} para {start_date.strftime('%B %Y')}...")
            
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())
            
            data = fetch_data(crypto, start_timestamp, end_timestamp)
            
            process_and_save(crypto, data, csv_filename, append=False)

    print("Coleta de dados finalizada!")


run_data_collection()
