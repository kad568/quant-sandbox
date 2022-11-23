import requests
from bs4 import BeautifulSoup as bs
import utils
import time
from tkinter import filedialog

class crypto_tickers:

    def crypto_by_rank(self, rank_range):

        session = requests.Session()

        if rank_range[1] <= 0:   
            response = session.get(utils.base_url, headers=utils.headers)
            soup = bs(response.content, 'lxml')  
            rank_range[1] += int(soup.find('span', attrs={'class': 'Mstart(15px) Fw(500) Fz(s)'}).text.split()[2])
            print(rank_range)

        offset = rank_range[0] - 1
        count = 250 # 250 is the most accepted by Yahoo finance

        sets_of_count = int((rank_range[1] - offset) / count)

        urls = []

        for set in range(0, sets_of_count):
            urls.append(f'https://finance.yahoo.com/crypto?offset={offset + set * count}&count={count}')
        
        urls.append(f'https://finance.yahoo.com/crypto?offset={offset + sets_of_count * count}&count={rank_range[1]-offset}')

        file_path = filedialog.askopenfilename()

        with open(file_path, 'r+') as file:
            file.truncate(0)
            for url in urls:
                response = session.get(url, headers=utils.headers)
                soup = bs(response.content, 'lxml')

                crypto_list = soup.find_all('tr')[1:]
                
                for crypto in crypto_list:                
                    ticker = crypto.find('td', attrs={'aria-label': 'Symbol'}).text
                    name = crypto.find('td', attrs={'aria-label': 'Name'}).text
                    mc = crypto.find('fin-streamer', attrs={'data-field': 'marketCap'})['value']

                    file.write(f'{name},{ticker},{mc}\n')

    def crypto_by_mc(self, mc_range):

        session = requests.Session()

        response = session.get(utils.base_url, headers=utils.headers)
        soup = bs(response.content, 'lxml')  
        rank_limit = int(soup.find('span', attrs={'class': 'Mstart(15px) Fw(500) Fz(s)'}).text.split()[2])

        offset = 0
        count = 250 # 250 is the most accepted by Yahoo finance

        sets_of_count = int((rank_limit - offset) / count)

        urls = []

        for set in range(0, sets_of_count):
            urls.append(f'https://finance.yahoo.com/crypto?offset={offset + set * count}&count={count}')
        
        urls.append(f'https://finance.yahoo.com/crypto?offset={offset + sets_of_count * count}&count={rank_limit-offset}')

        file_path = filedialog.askopenfilename()
        with open(file_path, 'r+') as file:
            file.truncate(0)
            for url in urls:
                response = session.get(url, headers=utils.headers)
                soup = bs(response.content, 'lxml')

                crypto_list = soup.find_all('tr')[1:]
                
                for crypto in crypto_list:                
                    ticker = crypto.find('td', attrs={'aria-label': 'Symbol'}).text
                    name = crypto.find('td', attrs={'aria-label': 'Name'}).text
                    mc = crypto.find('fin-streamer', attrs={'data-field': 'marketCap'})['value']

                    if mc_range[1] <= int(mc) <= mc_range[0]:
                        file.write(f'{name},{ticker},{mc}\n')
                if int(mc) <= mc_range[1]:
                    break

    def check_duplicate_tickers(self):
        duplicates = []
        with open('crypto_tickers.txt', 'r+') as file:
            seen = set()
            file = file.read().splitlines()
            with open('duplicate_tickers.txt', 'r+') as dup_f:
                dup_f.truncate(0)
                for line in file:
                    line_lower = line.lower()
                    if line_lower in seen:
                        duplicates.append(line)
                        dup_f.write(f'{line_lower.upper()}\n')
                    else:
                        seen.add(line_lower)
                
        return str(len(duplicates)*100/len(file))

crypto_tickers = crypto_tickers()

#################################################################################################

# crypto_tickers.crypto_by_rank(rank_range=[1, 0])

crypto_tickers.crypto_by_mc(mc_range=[100_000_000, 1_000_000])

print(str(crypto_tickers.check_duplicate_tickers()) + "%")