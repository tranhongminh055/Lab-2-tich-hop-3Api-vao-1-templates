# He thong 3: goi api tin tuc tu newsapi.org
import requests # dung de gui yeu cau den api newsapi

def get_news():
    """
    Ham nay se:
    1. goi api tin tuc
    2. lay danh sach bai bao
    3. tra ve 10 bai dau tien dang json
    """
    # api key newsapi ( sinh vien tu dang ky mien phi)
    API_KEY = "f9a733ebd0d14c26a7c73f18038fed2e"

    # goi tin tuc us (co the doi thanh 'vi' neu muon)
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=f9a733ebd0d14c26a7c73f18038fed2e"

    response = requests.get(url)
    data = response.json()

    articles = []

    # lay 10 bai bao dau tien
    for a in data["articles"][:10]:
        articles.append({
            "title": a["title"],
            "description": a["description"],
            "url": a["url"]
        })

    return articles
