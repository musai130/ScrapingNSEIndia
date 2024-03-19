import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)
actions = ActionChains(driver)
driver.get("https://www.nseindia.com/")
market_data = driver.find_element(By.ID, "link_2")
actions.move_to_element(market_data).perform()
actions.reset_actions()
preOpenMarket  = driver.find_element(By.LINK_TEXT, "Pre-Open Market").click()
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#livePreTable > tbody > tr:nth-child(1) > td:nth-child(2)')))
tablePrice = driver.find_element(By.CSS_SELECTOR, "#livePreTable > tbody").text.split("\n")[:-1]
finalPrices = []
for i in range(len(tablePrice)):
        tablePrice[i] = tablePrice[i].split(" ")
        if(len(tablePrice[i])>=3):
                finalPrices.append({'symbol': tablePrice[i][0], 'final': float(tablePrice[i][2].replace(",", ""))})
scrapedfinalPrise = pd.DataFrame(finalPrices)
scrapedfinalPrise.insert(0, 'id', range(0, 0 + len(scrapedfinalPrise)))
scrapedfinalPrise.to_csv('scrapedfinalPrise.csv', index=False)
print("Done")
driver.get("https://www.nseindia.com/")
niftyBank = driver.find_element(By.ID, "tabList_NIFTYBANK").click()
scrollTo = driver.find_element(By.CSS_SELECTOR, "body > div.main > div.mid_body.pt-1 > section.corporate_section.common-tabs.tabs-slider.slider-with-dots > div > div > div > nav > div > div")
viewAll = driver.find_element(By.CSS_SELECTOR, "#gainers_loosers > div.link-wrap > a")
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tab4_gainers_loosers > div.link-wrap > a')))
driver.execute_script("arguments[0].scrollIntoView(false);", scrollTo)
viewAll = list(filter(lambda x: x.is_displayed(), driver.find_elements(By.TAG_NAME, "a")))
(list( viewAll[i] for i in range(len(viewAll)) if viewAll[i].text == "View All"))[0].click()
niftyAlpha50 = WebDriverWait(driver, 20).until(EC.all_of(
    EC.element_to_be_clickable((By.ID, "equitieStockSelect")),
    EC.presence_of_element_located((By.CSS_SELECTOR, "#equityStockTable > tbody > tr.freezed-row")),
))
select = Select(niftyAlpha50[0])
select.select_by_visible_text("NIFTY ALPHA 50")
marketWatchEquityCmsNote = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#equityStockTable > tbody > tr:nth-child(51)")))
#marketWatchEquityCmsNote = driver.find_element(By.ID, "marketWatchEquityCmsNote")
driver.execute_script("arguments[0].scrollIntoView(false);", marketWatchEquityCmsNote)
time.sleep(10)
driver.quit()
