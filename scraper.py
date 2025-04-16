from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



def scrape_stock_data(symbol):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    
    driver = webdriver.Chrome(executable_path="./bin/chromedriver", options=options)
    url = f"https://ticker.finology.in/company/{symbol.upper()}"
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='mainContent_clsprice']"))
        )
        html = driver.page_source
    except Exception as e:
        driver.quit()
        return {"error": str(e)}
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    def get_metric(label_text):
        tag = soup.find(lambda tag: tag.name in ['small', 'span'] and label_text in tag.get_text(strip=True))
        if not tag:
            return None
        parent = tag.find_parent('div', class_='compess') or tag.find_parent('div', class_='d-flex')
        if not parent:
            return None
        number_tag = parent.find('span', class_='Number')
        if number_tag and number_tag.get('value'):
            return number_tag['value']
        elif number_tag:
            return number_tag.get_text(strip=True)
        p_tag = parent.find('p')
        return p_tag.get_text(strip=True) if p_tag else None

    metrics = {
        "Market Cap": get_metric("Market Cap"),
        "Enterprise Value": get_metric("Enterprise Value"),
        "No. of Shares": get_metric("No. of Shares"),
        "P/E": get_metric("P/E"),
        "P/B": get_metric("P/B"),
        "Face Value": get_metric("Face Value"),
        "Div. Yield": get_metric("Div. Yield"),
        "Book Value (TTM)": get_metric("Book Value (TTM)"),
        "CASH": get_metric("CASH"),
        "DEBT": get_metric("DEBT"),
    }

    today_high = soup.select_one("span#mainContent_ltrlTodayHigh")
    today_low = soup.select_one("span#mainContent_ltrlTodayLow")
    week52_high = soup.select_one("span#mainContent_ltrl52WH")
    week52_low = soup.select_one("span#mainContent_ltrl52WL")
    price_block = soup.find("div", id="mainContent_clsprice")
    current_price = None
    if price_block:
        price_span = price_block.find("span", class_="Number")
        if price_span:
            current_price = price_span.get("value") or price_span.text.strip()

    return {
        "Current Price": current_price,
        "Price Stats": {
            "Today High": today_high.text.strip() if today_high else "N/A",
            "Today Low": today_low.text.strip() if today_low else "N/A",
            "52 Week High": week52_high.text.strip() if week52_high else "N/A",
            "52 Week Low": week52_low.text.strip() if week52_low else "N/A",
        },
        "Metrics": metrics
    }
