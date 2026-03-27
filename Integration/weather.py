# he thong 2: goi api thoi tiet tu openweathermap
import requests # requests de goi api qua http

def get_weather(city="Da Nang"):
    """
    Ham nay se:
    1. goi api cua OpenWeatherMap
    2. Nhan du lieu thoi tiet dang JSON
    3. Tra ve thong tin: nhiet do, do am, mo ta thoi tiet
    """

    # api key cua OpenWeatherMap (sinh vien phai dang ky mien phi)
    API_KEY = "76196b58ff1ba9c2eee0610046636146" # -> thay bang api key cua sinh vien

    # url goi api, don vi nhiet do (units=metric -> do c)
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Danang&appid=76196b58ff1ba9c2eee0610046636146&units=metric"
    #  gui get request den api
    response = requests.get(url)

    # parse json thanh dictionary python
    data = response.json()

    # kiem tra neu api tra ve loi
    if response.status_code != 200:
        return {
            "error": "Khong lay duoc du lieu thoi tiet",
            "status_code": response.status_code,
            "message": data.get("message", "Unknown error")
        }

    # kiem tra neu du lieu co cau truc dung
    if "main" not in data or "weather" not in data:
        return {
            "error": "Du lieu thoi tiet co cau truc khong ping",
            "response": data
        }

    # tra ve du lieu can thiet
    return {
        "city": city,
        "temp": data["main"]["temp"], # nhiet do
        "humidity": data["main"]["humidity"], # do am
        "description": data["weather"][0]["description"] # mo ta thoi tiet
    }