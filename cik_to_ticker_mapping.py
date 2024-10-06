import json

def load_cik_to_ticker_mapping(tickers_json, tickers_exchange_json, cik_to_tickers_json, sec_cik_tiker):
    cik_to_ticker = {}

    # From: https://www.sec.gov/files/company_tickers.json
    for tickers_json_file in tickers_json:
        try:
            with open(tickers_json_file, 'r') as f:
                tickers_data = json.load(f)
                for company in tickers_data.values():
                    cik_str = str(company['cik_str']).strip() if isinstance(company['cik_str'], str) else str(company['cik_str'])
                    cik_to_ticker[str(int(cik_str))] = company['ticker']
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {tickers_json_file}: {e}")

    # From: https://www.kaggle.com/datasets/svendaj/sec-edgar-cik-ticker-exchange
    try:
        with open(tickers_exchange_json, 'r') as f:
            tickers_exchange_data = json.load(f)
            for company in tickers_exchange_data['data']:
                cik_str = str(company[0]).strip()  # 0: cik
                cik_to_ticker[str(int(cik_str))] = company[2]  # 2: ticker
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {tickers_exchange_json}: {e}")

    # From: pip install -U sec-cik-mapper, 2024
    try:
        with open(cik_to_tickers_json, 'r') as f:
            tickers_data = json.load(f)
            for key in tickers_data.keys():
                cik = str(int(key.strip()))
                ticker = tickers_data[key][0]
                cik_to_ticker[cik] = ticker
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {cik_to_tickers_json}: {e}")

    # From: https://dan.vonkohorn.com/2016/07/03/cik-ticker-mappings/, gist.github.com/x011/b6d22c462a2e4ab8d6c1f1eab42a0a83
    try:
        with open(sec_cik_tiker, 'r') as f:
            for line in f:
                cik, ticker = line.strip().split('|')
                cik_to_ticker[str(int(cik))] = ticker
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading {sec_cik_tiker}: {e}")

    # save to file
    with open(r'mapped\cik_to_ticker_mapping.json', 'w') as f:
        json.dump(cik_to_ticker, f)
        print(f"Saved {len(cik_to_ticker)} CIK-ticker map.")
    return cik_to_ticker

def main():
    tickers_json = []
    tickers_json.append(r'multisource\company_tickers_2017.json')
    tickers_json.append(r'multisource\company_tickers_2018.json')
    tickers_json.append(r'multisource\company_tickers_2019.json')
    tickers_json.append(r'multisource\company_tickers_2020.json')
    tickers_json.append(r'multisource\company_tickers_2021.json')
    tickers_json.append(r'multisource\company_tickers_2022.json')
    tickers_json.append(r'multisource\company_tickers_2023.json')
    tickers_json.append(r'multisource\company_tickers_2024.json')

    tickers_exchange_json = r'multisource\company_tickers_exchange.json'
    cik_to_tickers_json = r'multisource\cik_to_tickers.json'
    cik_to_ticker = r'multisource\SEC_CIK_TICKER'

    cik_to_ticker = load_cik_to_ticker_mapping(tickers_json, tickers_exchange_json, cik_to_tickers_json, cik_to_ticker)

if __name__ == "__main__":
    main()
