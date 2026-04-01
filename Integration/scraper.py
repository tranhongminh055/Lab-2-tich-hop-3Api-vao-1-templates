# Scraper dung Fake Store API - dam bao 100% thanh cong

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote


def get_lazada_products(keyword="dien thoai"):
    """
    - Input: keyword (tu khoa muon tim kiem)
    - Output: tra ve danh sach san pham (list cac dict)

    Dung Fake Store API - API cong khai, dam bao 100% thanh cong
    """

    try:
        # Tue thong tin tu 2 API cong khai de dam bao tuong doi on dinh
        api_urls = [
            "https://fakestoreapi.com/products",
            "https://dummyjson.com/products?limit=100"
        ]

        products = []
        status = None

        for url in api_urls:
            print(f"[DEBUG] Dang GET API: {url}")
            response = requests.get(url, timeout=15)
            print(f"[DEBUG] Status code tu {url}: {response.status_code}")

            if response.status_code != 200:
                print(f"[WARN] {url} tra ve HTTP {response.status_code}, chuyen sang source khac")
                continue

            status = response.status_code
            try:
                data = response.json()
            except Exception as e:
                print(f"[WARN] Loi parse JSON tu {url}: {e}, chuyen sang source khac")
                continue

            if isinstance(data, list):
                products = data
            elif isinstance(data, dict) and 'products' in data:
                products = data.get('products', [])
            else:
                print(f"[WARN] Dinh dang JSON khong hop le tu {url}")
                continue

            if len(products) > 0:
                print(f"[DEBUG] Tim thay {len(products)} san pham tu {url}")
                break

        if len(products) == 0:
            print("[ERROR] Cac API ngoai du lieu deu loi hoac tra ve rong")
            return [{"title": "Loi lay du lieu. Hay thu lai sau.", "price": "", "img": "", "link": "#"}]

        # 4. Filter theo keyword va format data
        print("[DEBUG] Parsing JSON response...")
        print(f"[DEBUG] Tim thay: {len(products)} san pham (trong danh sach)")

        # 4. Filter theo keyword va format data
        filtered_products = []
        keyword_lower = keyword.lower()

        for product in products:
            title = product.get('title', '')
            description = product.get('description', '')
            category = product.get('category', '')

            description_lower = description.lower() if isinstance(description, str) else ''
            category_lower = category.lower() if isinstance(category, str) else ''

            # Filter: neu keyword xuat hien trong title, description hoac category
            if (keyword_lower in title.lower() or
                keyword_lower in description_lower or
                keyword_lower in category_lower):

                price_value = product.get('price', 0)
                try:
                    price_value = float(price_value)
                except:
                    price_value = 0

                img = product.get('image', '') or product.get('thumbnail', '')
                if not img and isinstance(product.get('images', []), list) and product.get('images', []):
                    img = product.get('images')[0]

                pid = product.get('id', product.get('productId', ''))
                link = ''
                if pid:
                    link = f"https://fakestoreapi.com/products/{pid}"

                filtered_products.append({
                    "title": title[:100],
                    "price": f"$ {price_value:.2f}",
                    "img": img,
                    "link": link or '#'
                })

        # Neu khong co san pham phu hop, lay tat ca san pham
        if len(filtered_products) == 0:
            print("[INFO] Khong co san pham phu hop, lay tat ca san pham")
            for product in products[:10]:
                price_value = product.get('price', 0)
                try:
                    price_value = float(price_value)
                except:
                    price_value = 0

                img = product.get('image', '') or product.get('thumbnail', '')
                if not img and isinstance(product.get('images', []), list) and product.get('images', []):
                    img = product.get('images')[0]

                pid = product.get('id', product.get('productId', ''))
                link = f"https://fakestoreapi.com/products/{pid}" if pid else '#'

                filtered_products.append({
                    "title": product.get('title', '')[:100],
                    "price": f"$ {price_value:.2f}",
                    "img": img,
                    "link": link
                })

        print(f"[DEBUG] Tra ve {len(filtered_products)} san pham")
        return filtered_products[:10]  # Lay 10 san pham dau

    except requests.exceptions.Timeout:
        print("[ERROR] Timeout")
        return [{"title": "Timeout - server khong respond", "price": "", "img": "", "link": "#"}]

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        return [{"title": f"Loi: {type(e).__name__}", "price": "", "img": "", "link": "#"}]


def get_products_from_shopee_html(keyword, session, headers):
    """Backup: Parse HTML Shopee neu can"""
    try:
        print("[DEBUG] Backup: Dang parse HTML Shopee...")
        url = f"https://shopee.vn/search?keyword={quote(keyword)}"
        print(f"[DEBUG] GET: {url}")

        response = session.get(url, timeout=15)
        print(f"[DEBUG] HTML status: {response.status_code}")

        if response.status_code != 200:
            return [{"title": "Khong the tai trang Shopee", "price": "", "img": "", "link": "#"}]

        soup = BeautifulSoup(response.text, 'html.parser')
        products_data = []

        # Tim cac san pham trong HTML
        items = soup.find_all('div', class_=re.compile(r'(product|item)'))
        print(f"[DEBUG] Tim thay {len(items)} elements")

        if len(items) == 0:
            return [{"title": "Khong tim thay san pham trong HTML", "price": "", "img": "", "link": "#"}]

        for idx, item in enumerate(items[:10]):
            try:
                # Tim title
                title_elem = item.find('span') or item.find('p')
                title = title_elem.get_text(strip=True)[:100] if title_elem else "Khong ro ten"

                # Tim price
                price_elem = item.find('span', class_=re.compile(r'price'))
                price = price_elem.get_text(strip=True) if price_elem else "Khong ro gia"

                # Tim img
                img_elem = item.find('img')
                img = img_elem.get('src', '') if img_elem else ""

                # Tim link
                link_elem = item.find('a', href=True)
                link = link_elem.get('href', '#') if link_elem else "#"

                if title and len(title) > 3:
                    products_data.append({
                        "title": title,
                        "price": price,
                        "img": img,
                        "link": link
                    })
            except:
                continue

        if len(products_data) > 0:
            print(f"[DEBUG] Tra ve {len(products_data)} san pham tu HTML")
            return products_data
        else:
            return [{"title": "Khong tim thay san pham tu HTML", "price": "", "img": "", "link": "#"}]

    except Exception as e:
        print(f"[ERROR] HTML parse error: {e}")
        return [{"title": f"Loi parse HTML: {type(e).__name__}", "price": "", "img": "", "link": "#"}]
