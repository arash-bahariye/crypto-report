import json
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class createTotallMarketCapCSV:

    def __init__(self):
        self.getTotalMarketCap()

    def coin360(self, date):
        my_url = 'https://www.investing.com/crypto/charts'
        date1 = datetime.timestamp(date)
        option = Options()
        option.add_argument("--disable-notifications")
        option.headless = False
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=option)
        driver.get(my_url)
        driver.implicitly_wait(500)
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        driver.implicitly_wait(500)

        main_container = driver.find_element(By.CLASS_NAME, "wrapper")
        data = main_container.find_elements(By.XPATH, "./child::*")
        for i in data:
            if i.tag_name == "section":
                script = i.find_elements(By.TAG_NAME, "script")
                print(script[3].get_attribute('innerHTML'))
                js_elem = script[3].get_attribute('innerHTML')

        #js_elem = driver.find_element(By.XPATH, '/html/body/div[4]/section/script[1]')

        start = js_elem.find('{"1367107200"')
        end = js_elem.find('\' || \'{}')
        js_elem = json.loads(js_elem[start:end])
        value = None
        for i in range(48):
            try:
                value = js_elem[str(date1 + 3600 * i)[:-2]]
                break
            except:
                pass
        return str(int(value['market_cap_usd']))


    def getTotalMarketCap(self):

        while True:
            try:
                start_date = input(
                    'Date (typically the end of the last month) for total mkt. cap. (yyyy-mm-dd): ')
                valid_start_date6 = datetime.strptime(start_date + " 2:00:00", '%Y-%m-%d %H:%M:%S')
                break
            except ValueError:
                print('Invalid date! please try again')
                continue

        total_market_cap = self.coin360(valid_start_date6)
        valid_start_date6 = valid_start_date6.strftime('%Y-%m-%d')
        print("\n")
        print("capitalization in " + valid_start_date6 + " is: " + total_market_cap + " $")
        print("\n")


        while True:
            try:
                start_date = input(
                    'Date (typically the end of the second-last month) for δ of the total mkt. cap. (yyyy-mm-dd): ')
                valid_start_date7 = datetime.strptime(start_date + " 2:00:00", '%Y-%m-%d %H:%M:%S')
                break
            except ValueError:
                print('Invalid date! please try again')
                continue

        total_market_cap2 = self.coin360(valid_start_date7)
        valid_start_date7 = valid_start_date7.strftime('%Y-%m-%d')
        print("\n")
        print("capitalization in " + valid_start_date7 + " is: " + total_market_cap2 + " $")
        print("\n")

        total_capitalization = [["Description", valid_start_date6, valid_start_date7],
                                ["Total market capitalization in U.S $ ", total_market_cap, total_market_cap2]]

        with open('total_market_capitalization' + valid_start_date6 + ' VS ' + valid_start_date7 + '.csv', 'w',
                  newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(total_capitalization)
