# import cac thu vien can thiet cho selenium

from selenium import webdriver
# -> webdriver: thu vien chinh de dieu khien trinh duyet

from selenium.webdriver.common.by import By
# -> By: Dung de chi cach tim phan tu

from selenium.webdriver.chrome.service import Service
# ->  service: cho phep selenium ket noi voi chromedriver

from selenium.webdriver.chrome.options import Options
# -> options: dung de cau hinh chrome, vi du chay an tat automatic agent

from webdriver_manager.chrome import ChromeDriverManager
# -> ChromeDriverManager: tu dong tai va quan ly chromedriver

import time
import signal
# -> time: dung de tam dung code sleep cho trang web tai xong

def timeout_handler(signum, frame):
    raise TimeoutError("Scraper timeout - took too long")

# ham chinh: lay du lieu san pham lazada

def get_lazada_products(keyword="dien thoai"):
    """
    - Input: keyword(tu khoa muon tim kiem tren lazada)
    - output: tra ve danh sach 10 san pham dau tien (o dang list cac dict)
    """
    driver = None
    try:
        # 1. cau hinh trinh duyet chrome
        options = Options()
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        # chay chrome o che do an khong mo cua so (phu hop khi lam server)

        options.add_argument("--disable-blink-features=AutomationControlled")
        # -> doi user-agent giong nhu nguoi dung that (ngan web chan bot)

        # 2. khoi tao chromedriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            # -> tu dong tai chromedriver phu hop

            options=options
            # -> ap dung cau hinh o tren 
        )
        
        # Set timeout 20 seconds
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)

        # 3. mo trang tim kiem lazada
        url = f"https://www.lazada.vn/catalog/?q={keyword}"
        # -> f-string: nhung keyword vao url tim kiem

        driver.get(url)
        # -> mo trang lazada theo tu khoa

        time.sleep(2)
        # -> cho javascript cua lazada tai xong(lazada load noi dung bang js)

        # 5. tim toan bo khoi san pham - thu cac selector khac neu chinh dung khong thanh cong
        products = driver.find_elements(By.CSS_SELECTOR, "[data-qa-type='product']")
        
        if not products:
            products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
        
        if not products:
            products = driver.find_elements(By.CSS_SELECTOR, "div[data-spm*='item']")

        data = [] # tao list rong de chua du lieu san pham

        # 6. duyet moi san pham (lay 10 san pham dau tien)
        for p in products[:10]: # [:10] nghia la lay 10 phan tu dau tien

            # lay ten san pham
            try: 
                title = p.find_element(By.CSS_SELECTOR, ".RfADt").text
            except:
                try:
                    title = p.find_element(By.CSS_SELECTOR, "[data-qa-type='title']").text
                except:
                    title = "Khong ro ten"

            # lay gia san pham
            try:
                price = p.find_element(By.CSS_SELECTOR, ".oo0xS").text
            except:
                try:
                    price = p.find_element(By.CSS_SELECTOR, "[data-qa-type='price']").text
                except:
                    price = "Khong ro gia"

            # lay anh san pham
            try:
                img_tag = p.find_element(By.TAG_NAME, "img")
                img = (
                    img_tag.get_attribute("data-src") or
                    img_tag.get_attribute("src") 
                )
            except:
                img = ""

            # lay link san pham
            try:
                link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "#"

            # them vao danh sach data
            data.append({
                "title": title,
                "price": price,
                "img": img,
                "link": link
            })

        # 7. dong trinh duyet va tra ket qua
        if driver:
            driver.quit()
        
        if not data:
            return [{"title": "Khong tim thay san pham", "price": "N/A", "img": "", "link": "#"}]
        
        return data
        
    except Exception as e:
        print(f"Loi trong scraper: {e}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        # Return sample data on error instead of crashing
        return [
            
        ]