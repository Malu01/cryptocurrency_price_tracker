import pandas as pd  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
import time 
from datetime import datetime 

# 1. Setup Chrome Options (Headless mode optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")

# 2. Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_crypto_data():
    try:
        # CoinMarketCap website used to navigate
        url = "https://coinmarketcap.com/" 
        driver.get(url)    
        time.sleep(5)  

        #  scrape Top 10 coins data to create the list
        crypto_data = []
        
    
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")[0:10] 

        for row in rows:
            # Data extraction logic [cite: 2]
            name = row.find_element(By.XPATH, ".//td[3]//p[1]").text
            price = row.find_element(By.XPATH, ".//td[4]").text
            change_24h = row.find_element(By.XPATH, ".//td[5]").text
            market_cap = row.find_element(By.XPATH, ".//td[8]").text
            
            crypto_data.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Price": price,
                "24h Change": change_24h,
                "Market Cap": market_cap
            })

        # 3.Converts our list of dictionaries into a clean table
        df = pd.DataFrame(crypto_data)
        
        df.to_csv("crypto_prices.csv", mode='a', index=False, header=not pd.io.common.file_exists("crypto_prices.csv"))
        
        print("Data successfully saved to crypto_prices.csv!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit() 

if __name__ == "__main__": 
    scrape_crypto_data() 
    