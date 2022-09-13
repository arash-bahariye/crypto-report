from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import csv
import requests
from datetime import datetime
from selenium.webdriver.chrome.options import Options

class createTop20CoinsMarketCapCSV:

    def __init__(self):
        self.get_coins_cap()


    def get_coin_list(self):

        coin_market_cap_URL = input("Please enter the web archive/coin market cap URL for calculating coins capitalization: ")
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.get(coin_market_cap_URL)
        x = 0
        y = 900
        for count in range(0, 10):
            driver.execute_script(f"window.scrollTo({x}, {y})")
            count += 1
            y += 900
            time.sleep(2)
        coins = driver.find_elements(By.CLASS_NAME, "iworPT")
        coins_list = []
        for coin in coins:
            coins_list.append(coin.text)

        coins_list = [*{*coins_list}]
        print("\n")
        print(coins_list)
        print("\n")
        print("Total coins:")
        print(len(coins_list))
        print("\n")
        return coins_list

    def get_coins_cap(self):

        coins_list = self.get_coin_list()
        coins_dic = {}

        response = requests.get("https://api.coingecko.com/api/v3/coins/")
        while response.status_code != 200:
            print("API is unavailable, program is waiting 10 seconds to make the request again")
            time.sleep(10)
            response = requests.get("https://api.coingecko.com/api/v3/coins/")
        coins_full_list = json.loads(response.content)

        for coin in coins_full_list:
            for coin_name in coins_list:
                if coin["name"] == coin_name:
                    coins_dic[coin["id"]] = coin["name"]
        print("\n")
        print(coins_dic)
        print("\n")
        while True:
            try:
                start_date = input(
                    'Date (typically the end of the last month) for top 20 coins by mkt. cap. (yyyy-mm-dd): ')
                valid_start_date6 = datetime.strptime(start_date + " 2:00:00", '%Y-%m-%d %H:%M:%S')
                break
            except ValueError:
                print('Invalid date! please try again')
                continue

        lastDay = valid_start_date6.strftime("%d-%m-%Y")

        coin_cap = {}
        for item in coins_dic:
            response = requests.get(
                "https://api.coingecko.com/api/v3/coins/" + item + "/history?date=" + lastDay)
            print("https://api.coingecko.com/api/v3/coins/" + item + "/history?date=" + lastDay)
            time.sleep(2)
            while response.status_code != 200:
                print("API is unavailable, program is waiting 60 seconds to make the request again")
                time.sleep(60)
                response = requests.get(
                    "https://api.coingecko.com/api/v3/coins/" + item + "/history?date=" + lastDay)
            if response.status_code == 200:
                coin_capital = json.loads(response.content)
                if coin_capital:
                    try:
                        coin_cap[coins_dic[item]] = int(coin_capital['market_data']['market_cap']['usd'])
                    except:
                        print("couldnt find any information about market capitalization for " + item)
                        coin_cap[coins_dic[item]] = 0
                else:
                    coin_cap[coins_dic[item]] = 0

        new_coin_cap = dict(sorted(coin_cap.items(), reverse=True, key=lambda items: items[1]))
        new_coin_cap = {kv[0]: kv[1] for i, kv in enumerate(new_coin_cap.items()) if i <= 19}

        print("\n")
        print("top 20 coins market capitalization's in " + lastDay + " are: ")
        print("\n")
        print(new_coin_cap)
        print("\n")


        unsorted_array = [['CRYPTO_COIN', 'Top 20 Coins Capitalization at ' + lastDay + ' in U.S $']]
        for cap1 in new_coin_cap:
            unsorted_array.append([cap1, int(new_coin_cap[cap1])])

        print('experiment:')
        print(unsorted_array)
        print("\n")

        with open('top_20_market_cap_' + lastDay + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
            writer.writerows(unsorted_array)






